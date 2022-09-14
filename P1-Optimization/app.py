from kubernetes import client, config
import os, time
import subprocess
from subprocess import DEVNULL
import shlex

AWS_REGION = os.environ.get('AWS_REGION', 'us-gov-west-1')
APP_KUBECONFIG = os.environ.get('APP_KUBECONFIG')
MGMT_KUBECONFIG = os.environ.get('MGMT_KUBECONFIG')

UMBRELLA_APP = os.environ.get('UMBRELLA_APP')
APPLICATION_APP = os.environ.get('APPLICATION_APP')

KUBECTL_PATH = os.environ.get('KUBECTL_PATH', '/usr/local/bin/kubectl')

SKIP_MONGO_STATEFULSET = True if os.environ.get('SKIP_MONGO_STATEFULSET', 'true') == 'true' else False

core = client.CoreV1Api()
apps = client.AppsV1Api()
custom = client.CustomObjectsApi()


def _load_kubeconfig(config_file):
    global core
    global apps
    global custom

    config.load_kube_config(config_file=config_file)
    core = client.CoreV1Api()
    apps = client.AppsV1Api()
    custom = client.CustomObjectsApi()


def _disable_argo_autosync():
    _load_kubeconfig(MGMT_KUBECONFIG)

    argo_patch_command = '%s patch application -n argocd %s -p=\'[{"op": "remove", "path": "/spec/syncPolicy"}]\' --type=json' % (KUBECTL_PATH, UMBRELLA_APP)
    subprocess.Popen(shlex.split(argo_patch_command), env={'KUBECONFIG': MGMT_KUBECONFIG}, stdout=DEVNULL, stderr=DEVNULL).wait()

    subapp_resp = custom.list_cluster_custom_object(group="argoproj.io", version="v1alpha1", plural="applications", label_selector='app.kubernetes.io/instance={}'.format(UMBRELLA_APP))

    for subapp in subapp_resp['items']:
        argo_patch_command = '%s patch application -n argocd %s -p=\'[{"op": "remove", "path": "/spec/syncPolicy"}]\' --type=json' % (KUBECTL_PATH, subapp['metadata']['name'])
        subprocess.Popen(shlex.split(argo_patch_command), env={'KUBECONFIG': MGMT_KUBECONFIG}, stdout=DEVNULL, stderr=DEVNULL).wait()


def _enable_argo_autosync():
    _load_kubeconfig(MGMT_KUBECONFIG)

    argo_patch_command = '%s patch application -n argocd %s -p=\'[{"op": "add", "path": "/spec/syncPolicy", "value": {"automated": {"prune": true, "selfHeal": true}}}]\' --type=json' % (KUBECTL_PATH, UMBRELLA_APP)
    subprocess.Popen(shlex.split(argo_patch_command), env={'KUBECONFIG': MGMT_KUBECONFIG}, stdout=DEVNULL).wait()

    sub_applications = custom.list_cluster_custom_object(group="argoproj.io", version="v1alpha1", plural="applications", label_selector='app.kubernetes.io/instance={}'.format(UMBRELLA_APP))

    for subapp in sub_applications['items']:
        argo_patch_command = '%s patch application -n argocd %s -p=\'[{"op": "add", "path": "/spec/syncPolicy", "value": {"automated": {"prune": true, "selfHeal": true}}}]\' --type=json' % (KUBECTL_PATH, subapp['metadata']['name'])
        subprocess.Popen(shlex.split(argo_patch_command), env={'KUBECONFIG': MGMT_KUBECONFIG}, stdout=DEVNULL).wait()


def _get_istio_injected_namespaces():
    _load_kubeconfig(APP_KUBECONFIG)

    namespaces = []

    namespaces_resp = core.list_namespace(label_selector='istio-injection=enabled')
    for ns_obj in namespaces_resp.items:
        namespaces.append(ns_obj.metadata.name)

    return namespaces


def _get_daemonsets(namespaces):
    _load_kubeconfig(APP_KUBECONFIG)

    daemonsets = []

    ds_resp = apps.list_daemon_set_for_all_namespaces()

    for ds_obj in ds_resp.items:
        if ds_obj.metadata.namespace in namespaces:
            daemonset = {'namespace': ds_obj.metadata.namespace, 'name': ds_obj.metadata.name}

            is_istio_enabled = True

            if ds_obj.spec.template.metadata.annotations is not None and 'sidecar.istio.io/inject' in ds_obj.spec.template.metadata.annotations and ds_obj.spec.template.metadata.annotations['sidecar.istio.io/inject'] == 'false':
                is_istio_enabled = False

            if is_istio_enabled:
                daemonsets.append(daemonset)

    return daemonsets


def _get_statefulsets(namespaces):
    _load_kubeconfig(APP_KUBECONFIG)

    statefulsets = []

    ss_resp = apps.list_stateful_set_for_all_namespaces()

    for ss_obj in ss_resp.items:
        if ss_obj.metadata.namespace in namespaces:
            statefulset = {'namespace': ss_obj.metadata.namespace, 'name': ss_obj.metadata.name}

            is_istio_enabled = True

            if ss_obj.spec.template.metadata.annotations is not None and 'sidecar.istio.io/inject' in ss_obj.spec.template.metadata.annotations and ss_obj.spec.template.metadata.annotations['sidecar.istio.io/inject'] == 'false':
                is_istio_enabled = False

            if is_istio_enabled:
                statefulsets.append(statefulset)

    return statefulsets


def _get_deployments(namespaces):
    _load_kubeconfig(APP_KUBECONFIG)

    deployments = []

    deployment_resp = apps.list_deployment_for_all_namespaces()

    for deploy_obj in deployment_resp.items:
        if deploy_obj.metadata.namespace in namespaces:
            deployment = {'namespace': deploy_obj.metadata.namespace, 'name': deploy_obj.metadata.name, 'has_pvc': False}

            is_istio_enabled = True

            if deploy_obj.spec.template.metadata.annotations is not None and 'sidecar.istio.io/inject' in deploy_obj.spec.template.metadata.annotations and deploy_obj.spec.template.metadata.annotations['sidecar.istio.io/inject'] == 'false':
                is_istio_enabled = False

            if is_istio_enabled:
                if deploy_obj.spec.template.spec.volumes is not None:
                    for vol in deploy_obj.spec.template.spec.volumes:
                        if vol.persistent_volume_claim is not None:
                            deployment['has_pvc'] = True
                            break

                deployments.append(deployment)

    return deployments


def _get_deployment_pods(namespace, deployment):
    _load_kubeconfig(APP_KUBECONFIG)

    pods = []

    deployment_resp = apps.read_namespaced_deployment(namespace=namespace, name=deployment)
    deployment_revision = deployment_resp.metadata.annotations['deployment.kubernetes.io/revision']

    replicaset_resp = apps.list_namespaced_replica_set(namespace=namespace)

    replicaset_name = ''
    for replicaset in replicaset_resp.items:
        if replicaset.metadata.owner_references[0].name == deployment and replicaset.metadata.annotations['deployment.kubernetes.io/revision'] == deployment_revision:
            replicaset_name = replicaset.metadata.name

    pod_resp = core.list_namespaced_pod(namespace=namespace)

    for pod_obj in pod_resp.items:
        if pod_obj.metadata.owner_references is not None and pod_obj.metadata.owner_references[0].name == replicaset_name:
            pod = {
                'name': pod_obj.metadata.name,
                'object': pod_obj
            }
            pods.append(pod)
    return pods


def _scale_deployment(namespace, deployment):
    _load_kubeconfig(APP_KUBECONFIG)

    print('[SCALING] {}/{}'.format(namespace, deployment))

    deployment_resp = apps.read_namespaced_deployment(namespace=namespace, name=deployment)
    current_replicas = deployment_resp.spec.replicas

    apps.patch_namespaced_deployment(namespace=namespace, name=deployment, body={'spec': {'replicas': 0}})
    while len(_get_deployment_pods(namespace=namespace, deployment=deployment)) != 0:
        time.sleep(3)

    apps.patch_namespaced_deployment(namespace=namespace, name=deployment, body={'spec': {'replicas': current_replicas}})
    while len(_get_deployment_pods(namespace=namespace, deployment=deployment)) != current_replicas:
        time.sleep(3)



def _roll_deployment(namespace, deployment):
    print('[ROLLING] {}/{}'.format(namespace, deployment))

    roll_command = '%s rollout restart -n %s deploy/%s' % (KUBECTL_PATH, namespace, deployment)
    subprocess.call(shlex.split(roll_command), env={'KUBECONFIG': APP_KUBECONFIG}, stdout=DEVNULL, stderr=DEVNULL)


def _roll_statefulset(namespace, statefulset):
    print('[ROLLING] {}/{}'.format(namespace, statefulset))

    roll_command = '%s rollout restart -n %s statefulset/%s' % (KUBECTL_PATH, namespace, statefulset)
    subprocess.call(shlex.split(roll_command), env={'KUBECONFIG': APP_KUBECONFIG}, stdout=DEVNULL, stderr=DEVNULL)


def _roll_daemonset(namespace, daemonset):
    print('[ROLLING] {}/{}'.format(namespace, daemonset))

    roll_command = '%s rollout restart -n %s daemonset/%s' % (KUBECTL_PATH, namespace, daemonset)
    subprocess.call(shlex.split(roll_command), env={'KUBECONFIG': APP_KUBECONFIG}, stdout=DEVNULL, stderr=DEVNULL)


if __name__ == '__main__':
    print("Disabling ArgoCD autosync for umbrella '{}' and all sub-applications (might take a bit).. ".format(UMBRELLA_APP), end='', flush=True)
    _disable_argo_autosync()
    print('Done')

    print('Gathering istio-injected namespaces.. ', end='', flush=True)
    namespaces = _get_istio_injected_namespaces()
    print('Done')

    print('\n-----------\nDEPLOYMENTS\n-----------\n')

    print('Gathering deployments in istio-injected namespaces.. ', end='', flush=True)
    deployments = _get_deployments(namespaces=namespaces)
    print('Done\n')

    for deploy in deployments:
        if deploy['namespace'] == 'cso-wp-site' and deploy['name'] == 'cso-wp-site':
            _roll_deployment(namespace=deploy['namespace'], deployment=deploy['name'])

        elif deploy['has_pvc'] and deploy['namespace'] != 'cso-wp-site':
            _scale_deployment(namespace=deploy['namespace'], deployment=deploy['name'])

        else:
            _roll_deployment(namespace=deploy['namespace'], deployment=deploy['name'])

    print('\n------------\nSTATEFULSETS\n------------\n')

    print('Gathering statefulsets in istio-injected namespaces.. ', end='', flush=True)
    statefulsets = _get_statefulsets(namespaces=namespaces)
    print('Done\n')

    for ss in statefulsets:
        if SKIP_MONGO_STATEFULSET and 'mongodb-sharded' in ss['name']:
            print('[SKIPPING] {0}/{1} (kubectl rollout restart -n {0} statefulset/{1})'.format(ss['namespace'], ss['name']))
        else:
            _roll_statefulset(namespace=ss['namespace'], statefulset=ss['name'])

    print('\n----------\nDAEMONSETS\n----------\n')

    print('Gathering daemonsets in istio-injected namespaces.. ', end='', flush=True)
    daemonsets = _get_daemonsets(namespaces=namespaces)
    print('Done\n')

    for ds in daemonsets:
        _roll_daemonset(namespace=ds['namespace'], daemonset=ds['name'])

    print("\nEnabling ArgoCD autosync for umbrella '{}' and all sub-applications (might take a bit).. ".format(UMBRELLA_APP), end='', flush=True)
    _enable_argo_autosync()
    print('Done')



# Continuous Delivery 
 
## We use GitOps as the Delivery mechanism for Platform One. 
 
 
There are two core technologies we use for GitOps: 
1. Flux CD for platform developer GitOps 
2. Argo CD for application developer GitOps 
 
We initially started with Argo CD for both personas.  
 
_Italic The disadvantage of using Argo for Platform Layer GitOps was it ran into race conditions when multiple pipeline tools were needed and did not have native support to manage secrets using SOPS and Helm Secrets_
 
We then switched to Flux CD which addressed the secrets management and lock conditions better than Argo. But Flux CD does not have a UI (User Interface) which developers need to visualize their application deployment.  
 
Therefore, we split the GitOps into two paths to take advantage of specific capabilities each tool brings. 
___ 
 
Sample ARGO UI 
 
![image](https://user-images.githubusercontent.com/52505604/158284789-0f4deb52-2fa0-4f80-aff2-e08af2089c6a.png) 
 
 

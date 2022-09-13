# Gatus Config

Gatus config.yaml is presently generated with cue-lang.

[Installation](https://cuelang.org/docs/install/)

## Running

```
cue export --out yaml config.cue > config.yaml

# In dev, include the cluster name to generate utility belt URLs with the clustername suffix
cue export --out yaml config.cue -t cluster_name=$CLUSTER_NAME > config.yaml
```

Long-term, we could build the execution into terraform, but that would then make cue a hard dependency
for execution.  This seems excessive for the time being, so we're committing both the .yaml and the .cue

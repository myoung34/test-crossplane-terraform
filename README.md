Testing Crossplane
==================


```shell
$ k create ns crossplane-system
$ AWS_PROFILE=default && echo -e "[default]\naws_access_key_id = redact\naws_secret_access_key = redact" > creds.conf
$ kubectl create secret generic aws-creds -n crossplane-system --from-file=creds=./creds.conf
$ kubectl create secret generic git-credentials -n crossplane-system --from-literal=creds=https://myoung34:redact@github.com
$ kustomize build --enable-helm | k apply -f -
```


To uninstall: https://docs.crossplane.io/v1.9/reference/uninstall/

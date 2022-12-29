Testing Crossplane
==================

This is my own test for crossplane with AWS and terraform (AWS)

1) Create a user with a key (obv in prod this would be IRSA or similar)
2) Create opaque secrets for git and the aws user
3) Set up crossplane, use bare aws provider to create a state bucket for terraform
4) Set up the terraform provider to use `terraform/*.tf` in a repo with previous bucket for state
5) Issue a PR with TF to `terraform/` or a change to any manifest (including inline TF via crossplane) and see checks happen

# Pre-reqs

Create an IAM user with these permissions:

```terraform
data "aws_iam_policy_document" "crossplane_s3" {
  statement {
    sid = "1"
    effect = "Allow"

    actions = [
      "s3:*"
    ]

    resources = [
      "arn:aws:s3:::us-marcyoung-crossplane",
      "arn:aws:s3:::us-marcyoung-crossplane/*",
      "arn:aws:s3:::us-marcyoung-sometest",
      "arn:aws:s3:::us-marcyoung-sometest/*",
    ]

  }
  statement {
    sid = "2"
    effect = "Allow"

    actions = [
      "s3:CreateBucket",
      "s3:ListAllMyBuckets",
      "s3:GetBucketLocation",
    ]

    resources = [
      "arn:aws:s3:::*",
    ]

  }
}

resource "aws_iam_group_policy" "crossplane" {
  name   = "crossplane-s3-access"
  group  = "crossplane"
  policy = data.aws_iam_policy_document.crossplane_s3.json
}
```

Generate an IAM access key and secret key, set aside for the `creds.conf` file

Create the namespace and base secrets:

```shell
$ k create ns crossplane-system
$ AWS_PROFILE=default && echo -e "[default]\naws_access_key_id = redact\naws_secret_access_key = redact" > creds.conf
$ kubectl create secret generic aws-creds -n crossplane-system --from-file=creds=./creds.conf
$ kubectl create secret generic git-credentials -n crossplane-system --from-literal=creds=https://myoung34:redact@github.com
$ kustomize build --enable-helm | k apply -f -
```


# Uninstall

To uninstall: https://docs.crossplane.io/v1.9/reference/uninstall/

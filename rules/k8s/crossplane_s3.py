from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.common.util.data_structures_utils import find_in_dict
from checkov.kubernetes.checks.resource.base_spec_check import BaseK8Check


class CrossplaneS3(BaseK8Check):
    def __init__(self):
        name = "Ensure Stuff"
        id = "CUSTOM_CROSSPLANE_K8S_1"

        # apiVersion: s3.aws.crossplane.io/v1beta1 kind: Bucket
        # Location: spec.forProvider.serverSideEncryptionConfiguration.rules[].applyServerSideEncryptionByDefault.kmsMasterKeyId
        # Location: spec.forProvider.serverSideEncryptionConfiguration.rules[].applyServerSideEncryptionByDefault.sseAlgorithm
        supported_kind = ['Bucket']
        categories = [CheckCategories.KUBERNETES]
        super().__init__(
            name=name,
            id=id,
            categories=categories,
            supported_entities=supported_kind
        )

    def scan_spec_conf(self, conf):
        if not find_in_dict(conf, "spec/forProvider").get("serverSideEncryptionConfiguration"):
            return CheckResult.FAILED
        return CheckResult.PASSED


check = CrossplaneS3()

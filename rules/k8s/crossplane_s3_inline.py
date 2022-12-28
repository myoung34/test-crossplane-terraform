from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.common.util.data_structures_utils import find_in_dict
from checkov.kubernetes.checks.resource.base_spec_check import BaseK8Check
from checkov.terraform.runner import Runner as tf_graph_runner
from checkov.common.util.banner import banner as checkov_banner
from checkov.runner_filter import RunnerFilter
from checkov.common.runners.runner_registry import RunnerRegistry
from checkov.common.typing import _SkippedCheck
from typing import Any, TYPE_CHECKING
from pprint import pprint
import tempfile
import shutil
import os

DEFAULT_RUNNERS = (
    tf_graph_runner(),
)


class WorkspaceInline(BaseK8Check):
    def __init__(self):
        name = "Ensure Stuff"
        id = "CUSTOM_CROSSPLANE_K8S_2"

        supported_kind = ['Workspace']
        categories = [CheckCategories.KUBERNETES]
        super().__init__(
            name=name,
            id=id,
            categories=categories,
            supported_entities=supported_kind
        )

    #def run(
    #    scanned_file,
    #    entity_configuration,
    #    entity_name,
    #    entity_type,
    #    skip_info
    #):
    #    raise("fuck")


    def scan_spec_conf(self, conf):
        reports = []
        if find_in_dict(conf, "spec/forProvider").get("source") == 'Inline':
            temp_dirpath = tempfile.mkdtemp()
            temp_file = f'{tempfile.NamedTemporaryFile(dir=temp_dirpath).name}.tf'
            try:
                with open(temp_file, "w") as tf_file:
                    tf_file.writelines(find_in_dict(conf, "spec/forProvider").get("module"))
                with open(temp_file, "r") as tf_file:
                    runner_filter = RunnerFilter(framework='terraform', checks=None, skip_checks='CKV*')
                    runner_registry = RunnerRegistry('', runner_filter, *DEFAULT_RUNNERS)
                    reports = runner_registry.run(
                        root_folder=None,
                        external_checks_dir=['rules/tf/'],
                        files=[temp_file],
                    )
            finally:
                shutil.rmtree(temp_dirpath)

        if len(reports) > 0 and len(reports[0].failed_checks) > 0:
            print()
            [print(fc) for fc in reports[0].failed_checks]
            print()
            return CheckResult.FAILED

        return CheckResult.PASSED


check = WorkspaceInline()

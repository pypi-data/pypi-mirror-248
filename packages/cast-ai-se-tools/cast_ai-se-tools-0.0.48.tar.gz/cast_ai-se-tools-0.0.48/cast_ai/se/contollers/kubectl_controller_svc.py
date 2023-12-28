import logging
import subprocess
import time
from typing import Optional

from cast_ai.se.constants import CAST_NS, EVERY_MINUTE_SCHEDULE
from cast_ai.se.misc_utils import get_get_deployments_command, validate_required_tools_exist
from cast_ai.se.models.execution_status import ExecutionStatus


class KubectlController:
    def __init__(self, context: str):
        self._logger = logging.getLogger(__name__)
        validate_required_tools_exist()
        self._cmd_prefix = f"kubectl --context {context}"
        self._context = context

    def trigger_cronjob(self, cronjob_name: str, namespace: str = CAST_NS,
                        exec_wait: bool = False) -> ExecutionStatus:
        self._logger.info(f"{'-' * 70} Triggering {cronjob_name} cronjob")
        try:
            wait_time = 60
            exec_timeout = 300
            exec_msg = ""
            # Step 1: Get the original schedule
            origin_schedule = self.get_original_schedule(cronjob_name)
            # Step 2: Modify CronJob schedule (so it runs every minute...so it starts right away (NOW))
            self.patch_cronjob(cronjob_name, EVERY_MINUTE_SCHEDULE)
            # Step 3: Wait for execution
            for _ in range(wait_time):
                if self.is_cronjob_active(cronjob_name, namespace):
                    self._logger.debug(f"Cronjob {cronjob_name} found ACTIVE")
                    # Step 4: Restore original schedule
                    self.patch_cronjob(cronjob_name, origin_schedule)
                    if exec_wait:
                        self._logger.debug(f"Waiting for Cronjob {cronjob_name} to finish")
                        for _ in range(exec_timeout):
                            if not self.is_cronjob_active(cronjob_name, namespace):
                                break
                            time.sleep(1)
                        else:
                            exec_msg = "Cronjob still active..."
                            self._logger.warning(exec_msg)
                    break
                time.sleep(1)

            return ExecutionStatus(exec_msg)
        except subprocess.CalledProcessError as e:
            self._logger.exception(f"Error executing kubectl: {str(e)}")
            raise RuntimeError(f"Error executing kubectl: {str(e)}")
        except Exception as e:
            self._logger.exception(f"An error occurred: {str(e)}")
            raise RuntimeError(f"An error occurred: {str(e)}")

    def patch_cronjob(self, cronjob_name: str, schedule: str) -> None:
        self._logger.info(f"Modifying schedule for CronJob '{cronjob_name}' in namespace '{CAST_NS}' to {schedule}")
        kubectl_cmd = ["kubectl", "--context", self._context, "patch", "cronjob", cronjob_name, "-n", CAST_NS,
                       "--type=json", "-p", f'[{{"op": "replace", "path": "/spec/schedule", "value": "{schedule}"}}]']

        result = subprocess.check_output(kubectl_cmd, text=True, shell=True)
        self._logger.debug(f"Command=[{' '.join(kubectl_cmd)} | Output=[{result.rstrip()}]")

    # def set_context(self, context_name: str) -> ExecutionStatus:
    #     try:
    #         kubectl_cmd = "kubectl config current-context"
    #         current_context_result = subprocess.check_output(kubectl_cmd, text=True, shell=True)
    #         self._logger.info(f"Current context = {current_context_result} ")
    #         if current_context_result == context_name:
    #             return ExecutionStatus()
    #         self._logger.info(f"Modifying context to = {context_name} ")
    #         kubectl_cmd = f"kubectl config use-context {context_name}"
    #         result = subprocess.check_output(kubectl_cmd, text=True, shell=True)
    #         self._logger.debug(f"Command=[{' '.join(kubectl_cmd)} | Output=[{result.rstrip()}]")
    #     except Exception as e:
    #         self._logger.exception(f"An error occurred while trying to modify context: {str(e)}")
    #         raise RuntimeError(f"An error occurred while trying to modify context: {str(e)}")

    def get_original_schedule(self, cronjob_name) -> str:
        # json_path = "jsonpath='{.spec.schedule}'"
        # get_schedule_cmd = f"kubectl get cronjob {cronjob_name} -n {CAST_NS} -o {json_path}"
        get_schedule_cmd = (f"{self._cmd_prefix} get cronjob {cronjob_name} -n {CAST_NS} "
                            f"-o jsonpath='{{.spec.schedule}}'")

        origin_schedule = subprocess.check_output(get_schedule_cmd, text=True, shell=True).strip("'")
        self._logger.info(f"Original schedule of {cronjob_name} = {origin_schedule}")
        return origin_schedule

    def scale_deployments(self, replica_count: int) -> ExecutionStatus:
        self._logger.info(f"{'-' * 70}[ Scaling Deployments to {replica_count} ]")
        try:
            # Get the list of deployments across all namespaces with namespace and name
            get_deployments_command = f"{self._cmd_prefix} {get_get_deployments_command(bool(not replica_count))}"
            result = subprocess.check_output(get_deployments_command, text=True, shell=True)
            deployments = result.split()
            self._logger.debug(f'Command=[{str(get_deployments_command)}] | Output=[{" ".join(deployments)}]')

            # Iterate over pairs of namespace and deployment name
            for i in range(0, len(deployments), 1):
                deployment_name = deployments[i]

                kubectl_cmd = (f"{self._cmd_prefix} scale --replicas={replica_count} deployment/{deployment_name} "
                               f"--namespace=default")
                result = subprocess.check_output(kubectl_cmd, text=True, shell=True)
                self._logger.debug(f'Command=[{" ".join(kubectl_cmd)}] | Output=[{result.rstrip()}]')
                self._logger.info(f"Deployment {deployment_name}[default] scaled to {replica_count} replicas.")
            return ExecutionStatus()
        except subprocess.CalledProcessError as e:
            self._logger.exception(f"Error executing kubectl command related to deployments scaling: {str(e)}")
            raise RuntimeError(f"Error executing kubectl command related to deployments scaling: {str(e)}")

    def is_cronjob_active(self, cronjob_name: str, namespace: str) -> Optional[bool]:
        command = f'{self._cmd_prefix} get cronjobs.batch -n {namespace} {cronjob_name}'
        try:
            result = subprocess.check_output(command, shell=True, text=True)
            # Split the output by lines
            lines = result.split("\n")

            result = result.rstrip().replace("\n", " -<!n>- ")
            result = ' '.join(result.split())
            self._logger.debug(f"Command=[{command}] | Output=[{result}]")

            if lines[1].split()[-3] == "1":
                return True
            return False

        except subprocess.CalledProcessError as e:
            self._logger.exception(f"Error executing/parsing kubectl command:{command} -=> {str(e)}")
            return None

    def get_context_cloud_type(self) -> str:
        command = f"{self._cmd_prefix} cluster-info"
        try:
            result = subprocess.check_output(command, shell=True, text=True)
            if "eks.amazonaws.com" in result:
                self._logger.info("k8s cluster reflects it`s an EKS cluster")
                return "eks"
            elif "azmk8s.io" in result:
                self._logger.info("k8s cluster reflects it`s an AKS cluster")
                return "aks"
            self._logger.debug(f"k8s cluster reflects an unknown cluster type {result}")
            return ""
        except subprocess.CalledProcessError as e:
            self._logger.exception(f"Error executing/parsing kubectl command:{command} -=> {str(e)}")
            return ""

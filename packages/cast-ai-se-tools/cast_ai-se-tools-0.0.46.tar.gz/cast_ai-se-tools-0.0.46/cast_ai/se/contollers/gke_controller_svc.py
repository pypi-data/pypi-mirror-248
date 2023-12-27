import logging

from cast_ai.se.contollers.cloud_controller_svc import CloudController
from cast_ai.se.models.cloud_confs import GkeConfig
from cast_ai.se.models.execution_status import ExecutionStatus

from google.cloud import container_v1
from google.oauth2 import service_account


class GKEController(CloudController):
    def __init__(self, gke_conf: GkeConfig):
        try:
            self.conf = gke_conf
            self._logger = logging.getLogger(__name__)
            credentials = service_account.Credentials.from_service_account_file(
                self.conf.path,
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )
            self._client = container_v1.ClusterManagerClient(credentials=credentials)
        except Exception as e:
            self._logger.critical(f"An error occurred during GKEController initialization: {str(e)}")
            raise RuntimeError(f"An error occurred during GKEController initialization: {str(e)}")

    def disable_autoscaler(self) -> ExecutionStatus:
        # TODO: ...implement this method
        return ExecutionStatus()

    def get_node_count(self) -> int:
        node_pool = self._get_node_pool()
        return node_pool.initial_node_count

    def _get_node_pool(self):
        node_pool_path = self._get_node_pool_path()
        node_pool = self._client.get_node_pool(name=node_pool_path)
        return node_pool

    def _get_node_pool_path(self):
        cluster_path = f"projects/{self.conf.project_id}/locations/{self.conf.zone}/clusters/{self.conf.cluster_name}"
        node_pool_path = f"{cluster_path}/nodePools/{self.conf.ng}"
        return node_pool_path

    def scale(self, node_count: int) -> ExecutionStatus:
        try:
            node_pool = self._get_node_pool()
            node_pool_path = self._get_node_pool_path()
            update_request = container_v1.SetNodePoolSizeRequest(
                name=node_pool_path, node_count=node_count
            )
            response = self._client.set_node_pool_size(request=update_request)
            return ExecutionStatus()
        except Exception as e:
            self._logger.critical(f"An error occurred during GKEController initialization: {str(e)}")
            raise RuntimeError(f"An error occurred during GKEController initialization: {str(e)}")

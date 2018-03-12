########
# Copyright (c) 2018 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

import requests
from urlparse import urljoin

from cloudify_common import constants

from .utils import get_rest_client, get_auth_headers

# TODO: Add support for clusters


class CommonContext(object):
    def __init__(self, rest_host, username, password, tenant,
                 blueprint_id, deployment_id,
                 ssl_cert=None, rest_port=constants.DEFAULT_PORT,
                 rest_protocol=constants.DEFAULT_PROTOCOL,
                 trust_all=False):
        self._rest_host = rest_host,
        self._rest_port = rest_port,
        self._username = username,
        self._password = password,
        self._tenant = tenant,
        self._rest_protocol = rest_protocol,
        self._ssl_cert = ssl_cert,
        self._trust_all = trust_all
        
        self._headers = get_auth_headers(username, password, tenant)

        self._client = get_rest_client(
            rest_host=rest_host,
            rest_port=rest_port,
            headers=self._headers,
            rest_protocol=rest_protocol,
            ssl_cert=ssl_cert,
            trust_all=trust_all
        )
        self._blueprint_id = blueprint_id
        self._deployment_id = deployment_id

        self._blueprint = None
        self._deployment = None

    @property
    def _manager_file_server_url(self):
        return '{protocol}://{rest_host}:{rest_port}/resources'.format(
            protocol=self._rest_protocol,
            rest_host=self._rest_host,
            rest_port=self._rest_port
        )

    @property
    def blueprint(self):
        if not self._blueprint:
            self._blueprint = self._client.blueprints.get(self._blueprint_id)
        return self._blueprint

    @property
    def deployment(self):
        if not self._deployment:
            self._deployment = self._client.deployments.get(
                self._deployment_id
            )
        return self._deployment

    def download_resource_from_manager(self, resource_path):
        full_path = urljoin(self._manager_file_server_url, resource_path)
        response = requests.get(
            full_path, 
            headers=self._headers, 
            verify=self._ssl_cert
        )
        return response.ok


class OperationContext(CommonContext):
    def __init__(self, instance_id, *args, **kwargs):
        super(OperationContext, self).__init__(*args, **kwargs)
        self._instance_id = instance_id

        self._node = None
        self._instance = None

    @property
    def instance(self):
        if not self._instance:
            self._instance = self._client.node_instances.get(
                self._instance_id, evaluate_functions=True
            )
        return self._instance

    @property
    def node(self):
        if not self._node:
            self._node = self._client.nodes.get(
                self._deployment_id, self.instance.node_id
            )
        return self._node


class RelationshipContext(CommonContext):
    def __init__(self, source_instance_id, target_instance_id,
                 *args, **kwargs):
        super(RelationshipContext, self).__init__(*args, **kwargs)
        self._source_instance_id = source_instance_id
        self._target_instance_id = target_instance_id

        self._source_node = None
        self._source_instance = None
        self._target_node = None
        self._target_instance = None

    @property
    def source_instance(self):
        if not self._source_instance:
            self._source_instance = self._client.node_instances.get(
                self._source_instance_id, evaluate_functions=True
            )
        return self._source_instance

    @property
    def source_node(self):
        if not self._source_node:
            self._source_node = self._client.nodes.get(
                self._deployment_id, self.source_instance.node_id
            )
        return self._source_node

    @property
    def target_instance(self):
        if not self._target_instance:
            self._target_instance = self._client.node_instances.get(
                self._target_instance_id, evaluate_functions=True
            )
        return self._target_instance

    @property
    def target_node(self):
        if not self._target_node:
            self._target_node = self._client.nodes.get(
                self._deployment_id, self.target_instance.node_id
            )
        return self._target_node


class WorkflowContext(CommonContext):
    def __init__(self, workflow_id, *args, **kwargs):
        super(WorkflowContext, self).__init__(*args, **kwargs)
        self._workflow_id = workflow_id

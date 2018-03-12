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

from cloudify_common import constants
from cloudify_common.utils import get_auth_header
from cloudify_rest_client.client import CloudifyClient


def get_auth_headers(username, password, tenant=None):
    headers = get_auth_header(username, password)
    if tenant:
        headers[constants.CLOUDIFY_TENANT_HEADER] = tenant
    return headers


def get_rest_client(rest_host, headers,
                    ssl_cert=None, rest_port=constants.DEFAULT_PORT,
                    rest_protocol=constants.DEFAULT_PROTOCOL,
                    trust_all=False):
    return CloudifyClient(
        host=rest_host,
        port=rest_port,
        protocol=rest_protocol,
        headers=headers,
        cert=ssl_cert,
        trust_all=trust_all
    )

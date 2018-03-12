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

import os
import json
from proxy_tools import proxy
from threading import local as ThreadLocal

from cloudify_common.exceptions import NoContextSet
from cloudify_common.constants import CONTEXT_ENV_VAR

from . import context


class CurrentCtx(ThreadLocal):
    def __init__(self):
        if CONTEXT_ENV_VAR not in os.environ:
            raise NoContextSet('No context set')

        context_path = os.environ[CONTEXT_ENV_VAR]
        with open(context_path, 'r') as f:
            context_dict = json.load(f)

        if context_dict.get('is_operation'):
            _ctx = context.OperationContext(**context_dict)
        elif context_dict.get('is_relationship_operation'):
            _ctx = context.RelationshipContext(**context_dict)
        else:
            _ctx = context.WorkflowContext(**context_dict)

        self.ctx = _ctx


@proxy
def ctx():
    return CurrentCtx().ctx

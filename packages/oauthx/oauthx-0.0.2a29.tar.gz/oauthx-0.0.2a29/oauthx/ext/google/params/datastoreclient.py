# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
from typing import Annotated
from typing import TypeAlias

import fastapi
import google.auth.credentials
from aiopki.ext.google.client import get_credential
from google.cloud import datastore


__all__: list[str] = ['DatastoreClient']




async def get() -> datastore.Client:
    return datastore.Client(
        credentials=await get_credential(),
        project=os.environ['GOOGLE_DATASTORE_PROJECT'],
        namespace=os.environ['GOOGLE_DATASTORE_NAMESPACE']
    )


DatastoreClient: TypeAlias = Annotated[datastore.Client, fastapi.Depends(get)]
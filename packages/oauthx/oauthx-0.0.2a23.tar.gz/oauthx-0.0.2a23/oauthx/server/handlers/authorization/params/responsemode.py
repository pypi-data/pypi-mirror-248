# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Annotated
from typing import TypeAlias

import fastapi
import pydantic

from oauthx.server.request import Request
from oauthx.server.params import IssuerIdentifier
from oauthx.server.params import ObjectFactory
from oauthx.server.types import InvalidAuthorizationRequest
from oauthx.server.types import IResponseMode
from .client import Client
from .query import RESPONSE_MODE
from .redirecturi import RedirectURI
from .responsetype import ResponseType
from .state import State


__all__: list[str] = [
    'ResponseMode'
]


async def get(
    request: Request,
    iss: IssuerIdentifier,
    client: Client,
    response_type: ResponseType,
    redirect_uri: RedirectURI,
    state: State,
    factory: ObjectFactory,
    response_mode: str | None = RESPONSE_MODE,
) -> IResponseMode:
    try:
        obj = await factory.response_mode(
            iss=iss,
            client=client,
            response_type=response_type,
            response_mode=response_mode,
            redirect_uri=redirect_uri,
            state=state
        )
        request.response_mode = obj
        return obj
    except pydantic.ValidationError:
        raise InvalidAuthorizationRequest(
            error='invalid_request',
            allow_redirect=True,
            redirect_uri=redirect_uri,
            context={'client_name': client.get_display_name()}
        )


ResponseMode: TypeAlias = Annotated[
    IResponseMode,
    fastapi.Depends(get)
]
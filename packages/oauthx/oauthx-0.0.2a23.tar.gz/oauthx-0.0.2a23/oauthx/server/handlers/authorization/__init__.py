# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import fastapi

from oauthx.lib.exceptions import InvalidRequest
from oauthx.server.params import ContentEncryptionKey
from oauthx.server.params import CurrentSubject
from oauthx.server.params import ObjectFactory
from oauthx.server.params import PluginRunner
from oauthx.server.params import RequestSession
from oauthx.server.params import TokenIssuer
from oauthx.server.params import TokenSigner
from oauthx.server.request import Request
from oauthx.server.types import LoginRequired
from oauthx.server.types import InvalidResponseType
from oauthx.server.types import UnauthorizedAccount
from oauthx.server.types import UnauthorizedClient
from ..baserequesthandler import BaseRequestHandler
from .params import Client
from .params import AuthorizationRequest
from .params import RedirectURI
from .params import ResponseMode
from .params import ResponseType
from .params import ResourceOwner
from .params import Scope
from .params import State
from .params import TargetResources


class AuthorizationRequestHandler(BaseRequestHandler):
    """Provides an interface for the resource owner to authorize a certain
    scope for a client, and redirect back to the clients' redirection
    endpoint.
    """
    __module__: str = 'oauthx.server.handlers'
    client: Client
    name: str = 'oauth2.authorize'
    path: str = '/authorize'
    redirect_uri: RedirectURI
    responses: dict[int | str, Any] = {
        400: {
            'description': (
                "Unrecoverable error that is not allowed to redirect"
            )
        }
    }
    response_class: type[fastapi.Response] = fastapi.responses.RedirectResponse
    response_description: str = "Redirect to the clients' redirection endpoint."
    response_type: ResponseType
    scope: Scope
    status_code: int = 302
    subject: CurrentSubject | None
    summary: str = "Authorization Endpoint"

    def setup(
        self,
        *,
        issuer: TokenIssuer,
        client: Client,
        response_mode: ResponseMode,
        key: ContentEncryptionKey,
        redirect_uri: RedirectURI,
        subject: CurrentSubject,
        params: AuthorizationRequest,
        plugins: PluginRunner,
        owner: ResourceOwner,
        resources: TargetResources,
        response_type: ResponseType,
        scope: Scope,
        session: RequestSession,
        signer: TokenSigner,
        state: State,
        factory: ObjectFactory,
        **_: Any
    ):
        self.client = client
        self.factory = factory
        self.issuer = issuer
        self.key = key
        self.owner = owner
        self.params = params
        self.plugins = plugins
        self.redirect_uri = redirect_uri
        self.resources = resources
        self.response_mode = response_mode
        self.response_type = response_type
        self.scope = scope
        self.session = session
        self.signer = signer
        self.state = state
        self.subject = subject

    async def handle(self, request: Request) -> fastapi.Response:
        if not self.client.allows_response_type(self.response_type):
            raise InvalidResponseType

        if not self.client.can_grant(self.response_mode.grants()):
            self.logger.debug(
                "Client does not allow the requested grant (client: %s)",
                self.client.id
            )
            raise UnauthorizedClient

        if not self.state and self.client.requires_state():
            self.logger.debug(
                "Client requires the state parameter (client: %s)",
                self.client.id
            )
            raise InvalidRequest(
                "The client requires the use of the state "
                "parameter."
            )

        # If the authorization request was not pushed, persist
        # the parameters.
        if self.params is None:
            self.params = await self.factory.request(
                client=self.client, # type: ignore
                request=self.request,
                redirect_uri=self.redirect_uri,
                resources=self.resources
            )
            self.logger.debug(
                "Persisted authorization request parameters (client: %s, urn: %s)",
                self.client.id, self.params.request_uri
            )
        await self.storage.persist(self.params)
        if self.subject is None:
            self.logger.debug(
                "Request is not authenticated (client: %s, request: %s)",
                self.client.id, self.params.request_uri
            )
            raise LoginRequired(
                client=self.client,
                next_url=self.params.get_authorize_url(request),
                deny_url=await self.response_mode.deny(),
                a=self.params.id
            )
        if self.owner is None:
            raise NotImplementedError

        await self.subject.decrypt_keys(self.key)
        userinfo = await self.factory.userinfo(
            subject=self.subject,
            contributors=[self.session, self.client]
        )
        if not self.client.allows_delegation_to(userinfo):
            raise UnauthorizedAccount({
                'deny_url': await self.response_mode.deny()
            })

        response = await self.plugins.validate_scope(
            client=self.client,
            request=self.params,
            scope=self.params.scope
        )
        if response is not None:
            return response

        assert self.params.id
        authorization = await self.factory.authorization(
            request=self.params,
            client_id=self.client.id,
            lifecycle='GRANTED',
            scope=self.scope,
            sub=self.subject.get_primary_key(), # type: ignore
            token_types=self.response_mode.get_token_types()
        )
        authorization.contribute(self.params)
        authorization.contribute(self.session)
        await self.storage.persist(authorization)
        await self.storage.delete(self.params)
        
        code = await self.issuer.authorization_code(
            signer=self.signer,
            client=self.client,
            owner=self.owner,
            authorization_id=authorization.id,
            sub=self.subject.get_primary_key(), # type: ignore
            redirect_uri=self.params.redirect_uri
        )
        return await self.response_mode.redirect(
            signer=self.signer,
            code=code
        )
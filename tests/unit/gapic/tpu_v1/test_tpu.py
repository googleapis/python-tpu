# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule


from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.tpu_v1.services.tpu import TpuAsyncClient
from google.cloud.tpu_v1.services.tpu import TpuClient
from google.cloud.tpu_v1.services.tpu import pagers
from google.cloud.tpu_v1.services.tpu import transports
from google.cloud.tpu_v1.types import cloud_tpu
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import timestamp_pb2  # type: ignore
import google.auth


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert TpuClient._get_default_mtls_endpoint(None) is None
    assert TpuClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert TpuClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    assert (
        TpuClient._get_default_mtls_endpoint(sandbox_endpoint) == sandbox_mtls_endpoint
    )
    assert (
        TpuClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert TpuClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class", [TpuClient, TpuAsyncClient,])
def test_tpu_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "tpu.googleapis.com:443"


@pytest.mark.parametrize(
    "transport_class,transport_name",
    [
        (transports.TpuGrpcTransport, "grpc"),
        (transports.TpuGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_tpu_client_service_account_always_use_jwt(transport_class, transport_name):
    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(
        service_account.Credentials, "with_always_use_jwt_access", create=True
    ) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize("client_class", [TpuClient, TpuAsyncClient,])
def test_tpu_client_from_service_account_file(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "tpu.googleapis.com:443"


def test_tpu_client_get_transport_class():
    transport = TpuClient.get_transport_class()
    available_transports = [
        transports.TpuGrpcTransport,
    ]
    assert transport in available_transports

    transport = TpuClient.get_transport_class("grpc")
    assert transport == transports.TpuGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (TpuClient, transports.TpuGrpcTransport, "grpc"),
        (TpuAsyncClient, transports.TpuGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
@mock.patch.object(TpuClient, "DEFAULT_ENDPOINT", modify_default_endpoint(TpuClient))
@mock.patch.object(
    TpuAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(TpuAsyncClient)
)
def test_tpu_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(TpuClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(TpuClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (TpuClient, transports.TpuGrpcTransport, "grpc", "true"),
        (TpuAsyncClient, transports.TpuGrpcAsyncIOTransport, "grpc_asyncio", "true"),
        (TpuClient, transports.TpuGrpcTransport, "grpc", "false"),
        (TpuAsyncClient, transports.TpuGrpcAsyncIOTransport, "grpc_asyncio", "false"),
    ],
)
@mock.patch.object(TpuClient, "DEFAULT_ENDPOINT", modify_default_endpoint(TpuClient))
@mock.patch.object(
    TpuAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(TpuAsyncClient)
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_tpu_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                )


@pytest.mark.parametrize("client_class", [TpuClient, TpuAsyncClient])
@mock.patch.object(TpuClient, "DEFAULT_ENDPOINT", modify_default_endpoint(TpuClient))
@mock.patch.object(
    TpuAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(TpuAsyncClient)
)
def test_tpu_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(
            client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint
        )
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(
            options
        )
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            with mock.patch(
                "google.auth.transport.mtls.default_client_cert_source",
                return_value=mock_client_cert_source,
            ):
                (
                    api_endpoint,
                    cert_source,
                ) = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (TpuClient, transports.TpuGrpcTransport, "grpc"),
        (TpuAsyncClient, transports.TpuGrpcAsyncIOTransport, "grpc_asyncio"),
    ],
)
def test_tpu_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (TpuClient, transports.TpuGrpcTransport, "grpc", grpc_helpers),
        (
            TpuAsyncClient,
            transports.TpuGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_tpu_client_client_options_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


def test_tpu_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.tpu_v1.services.tpu.transports.TpuGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = TpuClient(client_options={"api_endpoint": "squid.clam.whelk"})
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,grpc_helpers",
    [
        (TpuClient, transports.TpuGrpcTransport, "grpc", grpc_helpers),
        (
            TpuAsyncClient,
            transports.TpuGrpcAsyncIOTransport,
            "grpc_asyncio",
            grpc_helpers_async,
        ),
    ],
)
def test_tpu_client_create_channel_credentials_file(
    client_class, transport_class, transport_name, grpc_helpers
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")

    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "tpu.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=None,
            default_host="tpu.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize("request_type", [cloud_tpu.ListNodesRequest, dict,])
def test_list_nodes(request_type, transport: str = "grpc"):
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_nodes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tpu.ListNodesResponse(
            next_page_token="next_page_token_value", unreachable=["unreachable_value"],
        )
        response = client.list_nodes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.ListNodesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNodesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_nodes_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_nodes), "__call__") as call:
        client.list_nodes()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.ListNodesRequest()


@pytest.mark.asyncio
async def test_list_nodes_async(
    transport: str = "grpc_asyncio", request_type=cloud_tpu.ListNodesRequest
):
    client = TpuAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_nodes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_tpu.ListNodesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_nodes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.ListNodesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNodesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_nodes_async_from_dict():
    await test_list_nodes_async(request_type=dict)


def test_list_nodes_field_headers():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.ListNodesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_nodes), "__call__") as call:
        call.return_value = cloud_tpu.ListNodesResponse()
        client.list_nodes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_nodes_field_headers_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.ListNodesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_nodes), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_tpu.ListNodesResponse()
        )
        await client.list_nodes(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_nodes_flattened():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_nodes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tpu.ListNodesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_nodes(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_nodes_flattened_error():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_nodes(
            cloud_tpu.ListNodesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_nodes_flattened_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_nodes), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tpu.ListNodesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_tpu.ListNodesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_nodes(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_nodes_flattened_error_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_nodes(
            cloud_tpu.ListNodesRequest(), parent="parent_value",
        )


def test_list_nodes_pager(transport_name: str = "grpc"):
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_nodes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_tpu.ListNodesResponse(
                nodes=[cloud_tpu.Node(), cloud_tpu.Node(), cloud_tpu.Node(),],
                next_page_token="abc",
            ),
            cloud_tpu.ListNodesResponse(nodes=[], next_page_token="def",),
            cloud_tpu.ListNodesResponse(
                nodes=[cloud_tpu.Node(),], next_page_token="ghi",
            ),
            cloud_tpu.ListNodesResponse(nodes=[cloud_tpu.Node(), cloud_tpu.Node(),],),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_nodes(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, cloud_tpu.Node) for i in results)


def test_list_nodes_pages(transport_name: str = "grpc"):
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_nodes), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_tpu.ListNodesResponse(
                nodes=[cloud_tpu.Node(), cloud_tpu.Node(), cloud_tpu.Node(),],
                next_page_token="abc",
            ),
            cloud_tpu.ListNodesResponse(nodes=[], next_page_token="def",),
            cloud_tpu.ListNodesResponse(
                nodes=[cloud_tpu.Node(),], next_page_token="ghi",
            ),
            cloud_tpu.ListNodesResponse(nodes=[cloud_tpu.Node(), cloud_tpu.Node(),],),
            RuntimeError,
        )
        pages = list(client.list_nodes(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_nodes_async_pager():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_nodes), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_tpu.ListNodesResponse(
                nodes=[cloud_tpu.Node(), cloud_tpu.Node(), cloud_tpu.Node(),],
                next_page_token="abc",
            ),
            cloud_tpu.ListNodesResponse(nodes=[], next_page_token="def",),
            cloud_tpu.ListNodesResponse(
                nodes=[cloud_tpu.Node(),], next_page_token="ghi",
            ),
            cloud_tpu.ListNodesResponse(nodes=[cloud_tpu.Node(), cloud_tpu.Node(),],),
            RuntimeError,
        )
        async_pager = await client.list_nodes(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloud_tpu.Node) for i in responses)


@pytest.mark.asyncio
async def test_list_nodes_async_pages():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_nodes), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_tpu.ListNodesResponse(
                nodes=[cloud_tpu.Node(), cloud_tpu.Node(), cloud_tpu.Node(),],
                next_page_token="abc",
            ),
            cloud_tpu.ListNodesResponse(nodes=[], next_page_token="def",),
            cloud_tpu.ListNodesResponse(
                nodes=[cloud_tpu.Node(),], next_page_token="ghi",
            ),
            cloud_tpu.ListNodesResponse(nodes=[cloud_tpu.Node(), cloud_tpu.Node(),],),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_nodes(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [cloud_tpu.GetNodeRequest, dict,])
def test_get_node(request_type, transport: str = "grpc"):
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tpu.Node(
            name="name_value",
            description="description_value",
            accelerator_type="accelerator_type_value",
            ip_address="ip_address_value",
            port="port_value",
            state=cloud_tpu.Node.State.CREATING,
            health_description="health_description_value",
            tensorflow_version="tensorflow_version_value",
            network="network_value",
            cidr_block="cidr_block_value",
            service_account="service_account_value",
            health=cloud_tpu.Node.Health.HEALTHY,
            use_service_networking=True,
            api_version=cloud_tpu.Node.ApiVersion.V1_ALPHA1,
        )
        response = client.get_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.GetNodeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_tpu.Node)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.accelerator_type == "accelerator_type_value"
    assert response.ip_address == "ip_address_value"
    assert response.port == "port_value"
    assert response.state == cloud_tpu.Node.State.CREATING
    assert response.health_description == "health_description_value"
    assert response.tensorflow_version == "tensorflow_version_value"
    assert response.network == "network_value"
    assert response.cidr_block == "cidr_block_value"
    assert response.service_account == "service_account_value"
    assert response.health == cloud_tpu.Node.Health.HEALTHY
    assert response.use_service_networking is True
    assert response.api_version == cloud_tpu.Node.ApiVersion.V1_ALPHA1


def test_get_node_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node), "__call__") as call:
        client.get_node()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.GetNodeRequest()


@pytest.mark.asyncio
async def test_get_node_async(
    transport: str = "grpc_asyncio", request_type=cloud_tpu.GetNodeRequest
):
    client = TpuAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_tpu.Node(
                name="name_value",
                description="description_value",
                accelerator_type="accelerator_type_value",
                ip_address="ip_address_value",
                port="port_value",
                state=cloud_tpu.Node.State.CREATING,
                health_description="health_description_value",
                tensorflow_version="tensorflow_version_value",
                network="network_value",
                cidr_block="cidr_block_value",
                service_account="service_account_value",
                health=cloud_tpu.Node.Health.HEALTHY,
                use_service_networking=True,
                api_version=cloud_tpu.Node.ApiVersion.V1_ALPHA1,
            )
        )
        response = await client.get_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.GetNodeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_tpu.Node)
    assert response.name == "name_value"
    assert response.description == "description_value"
    assert response.accelerator_type == "accelerator_type_value"
    assert response.ip_address == "ip_address_value"
    assert response.port == "port_value"
    assert response.state == cloud_tpu.Node.State.CREATING
    assert response.health_description == "health_description_value"
    assert response.tensorflow_version == "tensorflow_version_value"
    assert response.network == "network_value"
    assert response.cidr_block == "cidr_block_value"
    assert response.service_account == "service_account_value"
    assert response.health == cloud_tpu.Node.Health.HEALTHY
    assert response.use_service_networking is True
    assert response.api_version == cloud_tpu.Node.ApiVersion.V1_ALPHA1


@pytest.mark.asyncio
async def test_get_node_async_from_dict():
    await test_get_node_async(request_type=dict)


def test_get_node_field_headers():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.GetNodeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node), "__call__") as call:
        call.return_value = cloud_tpu.Node()
        client.get_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_node_field_headers_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.GetNodeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cloud_tpu.Node())
        await client.get_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_node_flattened():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tpu.Node()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_node(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_node_flattened_error():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_node(
            cloud_tpu.GetNodeRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_node_flattened_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_node), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tpu.Node()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(cloud_tpu.Node())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_node(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_node_flattened_error_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_node(
            cloud_tpu.GetNodeRequest(), name="name_value",
        )


@pytest.mark.parametrize("request_type", [cloud_tpu.CreateNodeRequest, dict,])
def test_create_node(request_type, transport: str = "grpc"):
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.create_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.CreateNodeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_node_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node), "__call__") as call:
        client.create_node()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.CreateNodeRequest()


@pytest.mark.asyncio
async def test_create_node_async(
    transport: str = "grpc_asyncio", request_type=cloud_tpu.CreateNodeRequest
):
    client = TpuAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.create_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.CreateNodeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_node_async_from_dict():
    await test_create_node_async(request_type=dict)


def test_create_node_field_headers():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.CreateNodeRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.create_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_node_field_headers_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.CreateNodeRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.create_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_node_flattened():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_node(
            parent="parent_value",
            node=cloud_tpu.Node(name="name_value"),
            node_id="node_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].node
        mock_val = cloud_tpu.Node(name="name_value")
        assert arg == mock_val
        arg = args[0].node_id
        mock_val = "node_id_value"
        assert arg == mock_val


def test_create_node_flattened_error():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_node(
            cloud_tpu.CreateNodeRequest(),
            parent="parent_value",
            node=cloud_tpu.Node(name="name_value"),
            node_id="node_id_value",
        )


@pytest.mark.asyncio
async def test_create_node_flattened_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_node), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_node(
            parent="parent_value",
            node=cloud_tpu.Node(name="name_value"),
            node_id="node_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val
        arg = args[0].node
        mock_val = cloud_tpu.Node(name="name_value")
        assert arg == mock_val
        arg = args[0].node_id
        mock_val = "node_id_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_create_node_flattened_error_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_node(
            cloud_tpu.CreateNodeRequest(),
            parent="parent_value",
            node=cloud_tpu.Node(name="name_value"),
            node_id="node_id_value",
        )


@pytest.mark.parametrize("request_type", [cloud_tpu.DeleteNodeRequest, dict,])
def test_delete_node(request_type, transport: str = "grpc"):
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.delete_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.DeleteNodeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_node_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node), "__call__") as call:
        client.delete_node()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.DeleteNodeRequest()


@pytest.mark.asyncio
async def test_delete_node_async(
    transport: str = "grpc_asyncio", request_type=cloud_tpu.DeleteNodeRequest
):
    client = TpuAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.delete_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.DeleteNodeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_node_async_from_dict():
    await test_delete_node_async(request_type=dict)


def test_delete_node_field_headers():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.DeleteNodeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.delete_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_node_field_headers_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.DeleteNodeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.delete_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_node_flattened():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_node(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_delete_node_flattened_error():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_node(
            cloud_tpu.DeleteNodeRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_node_flattened_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_node), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/op")

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_node(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_delete_node_flattened_error_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_node(
            cloud_tpu.DeleteNodeRequest(), name="name_value",
        )


@pytest.mark.parametrize("request_type", [cloud_tpu.ReimageNodeRequest, dict,])
def test_reimage_node(request_type, transport: str = "grpc"):
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reimage_node), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.reimage_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.ReimageNodeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_reimage_node_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reimage_node), "__call__") as call:
        client.reimage_node()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.ReimageNodeRequest()


@pytest.mark.asyncio
async def test_reimage_node_async(
    transport: str = "grpc_asyncio", request_type=cloud_tpu.ReimageNodeRequest
):
    client = TpuAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reimage_node), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.reimage_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.ReimageNodeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_reimage_node_async_from_dict():
    await test_reimage_node_async(request_type=dict)


def test_reimage_node_field_headers():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.ReimageNodeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reimage_node), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.reimage_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_reimage_node_field_headers_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.ReimageNodeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.reimage_node), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.reimage_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.parametrize("request_type", [cloud_tpu.StopNodeRequest, dict,])
def test_stop_node(request_type, transport: str = "grpc"):
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.stop_node), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.stop_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.StopNodeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_stop_node_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.stop_node), "__call__") as call:
        client.stop_node()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.StopNodeRequest()


@pytest.mark.asyncio
async def test_stop_node_async(
    transport: str = "grpc_asyncio", request_type=cloud_tpu.StopNodeRequest
):
    client = TpuAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.stop_node), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.stop_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.StopNodeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_stop_node_async_from_dict():
    await test_stop_node_async(request_type=dict)


def test_stop_node_field_headers():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.StopNodeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.stop_node), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.stop_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_stop_node_field_headers_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.StopNodeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.stop_node), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.stop_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.parametrize("request_type", [cloud_tpu.StartNodeRequest, dict,])
def test_start_node(request_type, transport: str = "grpc"):
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_node), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name="operations/spam")
        response = client.start_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.StartNodeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_start_node_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_node), "__call__") as call:
        client.start_node()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.StartNodeRequest()


@pytest.mark.asyncio
async def test_start_node_async(
    transport: str = "grpc_asyncio", request_type=cloud_tpu.StartNodeRequest
):
    client = TpuAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_node), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/spam")
        )
        response = await client.start_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.StartNodeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_start_node_async_from_dict():
    await test_start_node_async(request_type=dict)


def test_start_node_field_headers():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.StartNodeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_node), "__call__") as call:
        call.return_value = operations_pb2.Operation(name="operations/op")
        client.start_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_start_node_field_headers_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.StartNodeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.start_node), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name="operations/op")
        )
        await client.start_node(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.parametrize(
    "request_type", [cloud_tpu.ListTensorFlowVersionsRequest, dict,]
)
def test_list_tensor_flow_versions(request_type, transport: str = "grpc"):
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensor_flow_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tpu.ListTensorFlowVersionsResponse(
            next_page_token="next_page_token_value", unreachable=["unreachable_value"],
        )
        response = client.list_tensor_flow_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.ListTensorFlowVersionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTensorFlowVersionsPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_tensor_flow_versions_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensor_flow_versions), "__call__"
    ) as call:
        client.list_tensor_flow_versions()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.ListTensorFlowVersionsRequest()


@pytest.mark.asyncio
async def test_list_tensor_flow_versions_async(
    transport: str = "grpc_asyncio",
    request_type=cloud_tpu.ListTensorFlowVersionsRequest,
):
    client = TpuAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensor_flow_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_tpu.ListTensorFlowVersionsResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_tensor_flow_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.ListTensorFlowVersionsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListTensorFlowVersionsAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_tensor_flow_versions_async_from_dict():
    await test_list_tensor_flow_versions_async(request_type=dict)


def test_list_tensor_flow_versions_field_headers():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.ListTensorFlowVersionsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensor_flow_versions), "__call__"
    ) as call:
        call.return_value = cloud_tpu.ListTensorFlowVersionsResponse()
        client.list_tensor_flow_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_tensor_flow_versions_field_headers_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.ListTensorFlowVersionsRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensor_flow_versions), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_tpu.ListTensorFlowVersionsResponse()
        )
        await client.list_tensor_flow_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_tensor_flow_versions_flattened():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensor_flow_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tpu.ListTensorFlowVersionsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_tensor_flow_versions(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_tensor_flow_versions_flattened_error():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_tensor_flow_versions(
            cloud_tpu.ListTensorFlowVersionsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_tensor_flow_versions_flattened_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensor_flow_versions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tpu.ListTensorFlowVersionsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_tpu.ListTensorFlowVersionsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_tensor_flow_versions(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_tensor_flow_versions_flattened_error_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_tensor_flow_versions(
            cloud_tpu.ListTensorFlowVersionsRequest(), parent="parent_value",
        )


def test_list_tensor_flow_versions_pager(transport_name: str = "grpc"):
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensor_flow_versions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_tpu.ListTensorFlowVersionsResponse(
                tensorflow_versions=[
                    cloud_tpu.TensorFlowVersion(),
                    cloud_tpu.TensorFlowVersion(),
                    cloud_tpu.TensorFlowVersion(),
                ],
                next_page_token="abc",
            ),
            cloud_tpu.ListTensorFlowVersionsResponse(
                tensorflow_versions=[], next_page_token="def",
            ),
            cloud_tpu.ListTensorFlowVersionsResponse(
                tensorflow_versions=[cloud_tpu.TensorFlowVersion(),],
                next_page_token="ghi",
            ),
            cloud_tpu.ListTensorFlowVersionsResponse(
                tensorflow_versions=[
                    cloud_tpu.TensorFlowVersion(),
                    cloud_tpu.TensorFlowVersion(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_tensor_flow_versions(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, cloud_tpu.TensorFlowVersion) for i in results)


def test_list_tensor_flow_versions_pages(transport_name: str = "grpc"):
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensor_flow_versions), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_tpu.ListTensorFlowVersionsResponse(
                tensorflow_versions=[
                    cloud_tpu.TensorFlowVersion(),
                    cloud_tpu.TensorFlowVersion(),
                    cloud_tpu.TensorFlowVersion(),
                ],
                next_page_token="abc",
            ),
            cloud_tpu.ListTensorFlowVersionsResponse(
                tensorflow_versions=[], next_page_token="def",
            ),
            cloud_tpu.ListTensorFlowVersionsResponse(
                tensorflow_versions=[cloud_tpu.TensorFlowVersion(),],
                next_page_token="ghi",
            ),
            cloud_tpu.ListTensorFlowVersionsResponse(
                tensorflow_versions=[
                    cloud_tpu.TensorFlowVersion(),
                    cloud_tpu.TensorFlowVersion(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_tensor_flow_versions(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_tensor_flow_versions_async_pager():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensor_flow_versions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_tpu.ListTensorFlowVersionsResponse(
                tensorflow_versions=[
                    cloud_tpu.TensorFlowVersion(),
                    cloud_tpu.TensorFlowVersion(),
                    cloud_tpu.TensorFlowVersion(),
                ],
                next_page_token="abc",
            ),
            cloud_tpu.ListTensorFlowVersionsResponse(
                tensorflow_versions=[], next_page_token="def",
            ),
            cloud_tpu.ListTensorFlowVersionsResponse(
                tensorflow_versions=[cloud_tpu.TensorFlowVersion(),],
                next_page_token="ghi",
            ),
            cloud_tpu.ListTensorFlowVersionsResponse(
                tensorflow_versions=[
                    cloud_tpu.TensorFlowVersion(),
                    cloud_tpu.TensorFlowVersion(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_tensor_flow_versions(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloud_tpu.TensorFlowVersion) for i in responses)


@pytest.mark.asyncio
async def test_list_tensor_flow_versions_async_pages():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_tensor_flow_versions),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_tpu.ListTensorFlowVersionsResponse(
                tensorflow_versions=[
                    cloud_tpu.TensorFlowVersion(),
                    cloud_tpu.TensorFlowVersion(),
                    cloud_tpu.TensorFlowVersion(),
                ],
                next_page_token="abc",
            ),
            cloud_tpu.ListTensorFlowVersionsResponse(
                tensorflow_versions=[], next_page_token="def",
            ),
            cloud_tpu.ListTensorFlowVersionsResponse(
                tensorflow_versions=[cloud_tpu.TensorFlowVersion(),],
                next_page_token="ghi",
            ),
            cloud_tpu.ListTensorFlowVersionsResponse(
                tensorflow_versions=[
                    cloud_tpu.TensorFlowVersion(),
                    cloud_tpu.TensorFlowVersion(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_tensor_flow_versions(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [cloud_tpu.GetTensorFlowVersionRequest, dict,])
def test_get_tensor_flow_version(request_type, transport: str = "grpc"):
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensor_flow_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tpu.TensorFlowVersion(
            name="name_value", version="version_value",
        )
        response = client.get_tensor_flow_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.GetTensorFlowVersionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_tpu.TensorFlowVersion)
    assert response.name == "name_value"
    assert response.version == "version_value"


def test_get_tensor_flow_version_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensor_flow_version), "__call__"
    ) as call:
        client.get_tensor_flow_version()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.GetTensorFlowVersionRequest()


@pytest.mark.asyncio
async def test_get_tensor_flow_version_async(
    transport: str = "grpc_asyncio", request_type=cloud_tpu.GetTensorFlowVersionRequest
):
    client = TpuAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensor_flow_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_tpu.TensorFlowVersion(name="name_value", version="version_value",)
        )
        response = await client.get_tensor_flow_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.GetTensorFlowVersionRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_tpu.TensorFlowVersion)
    assert response.name == "name_value"
    assert response.version == "version_value"


@pytest.mark.asyncio
async def test_get_tensor_flow_version_async_from_dict():
    await test_get_tensor_flow_version_async(request_type=dict)


def test_get_tensor_flow_version_field_headers():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.GetTensorFlowVersionRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensor_flow_version), "__call__"
    ) as call:
        call.return_value = cloud_tpu.TensorFlowVersion()
        client.get_tensor_flow_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_tensor_flow_version_field_headers_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.GetTensorFlowVersionRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensor_flow_version), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_tpu.TensorFlowVersion()
        )
        await client.get_tensor_flow_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_tensor_flow_version_flattened():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensor_flow_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tpu.TensorFlowVersion()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_tensor_flow_version(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_tensor_flow_version_flattened_error():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_tensor_flow_version(
            cloud_tpu.GetTensorFlowVersionRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_tensor_flow_version_flattened_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_tensor_flow_version), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tpu.TensorFlowVersion()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_tpu.TensorFlowVersion()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_tensor_flow_version(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_tensor_flow_version_flattened_error_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_tensor_flow_version(
            cloud_tpu.GetTensorFlowVersionRequest(), name="name_value",
        )


@pytest.mark.parametrize("request_type", [cloud_tpu.ListAcceleratorTypesRequest, dict,])
def test_list_accelerator_types(request_type, transport: str = "grpc"):
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_accelerator_types), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tpu.ListAcceleratorTypesResponse(
            next_page_token="next_page_token_value", unreachable=["unreachable_value"],
        )
        response = client.list_accelerator_types(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.ListAcceleratorTypesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAcceleratorTypesPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


def test_list_accelerator_types_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_accelerator_types), "__call__"
    ) as call:
        client.list_accelerator_types()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.ListAcceleratorTypesRequest()


@pytest.mark.asyncio
async def test_list_accelerator_types_async(
    transport: str = "grpc_asyncio", request_type=cloud_tpu.ListAcceleratorTypesRequest
):
    client = TpuAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_accelerator_types), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_tpu.ListAcceleratorTypesResponse(
                next_page_token="next_page_token_value",
                unreachable=["unreachable_value"],
            )
        )
        response = await client.list_accelerator_types(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.ListAcceleratorTypesRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListAcceleratorTypesAsyncPager)
    assert response.next_page_token == "next_page_token_value"
    assert response.unreachable == ["unreachable_value"]


@pytest.mark.asyncio
async def test_list_accelerator_types_async_from_dict():
    await test_list_accelerator_types_async(request_type=dict)


def test_list_accelerator_types_field_headers():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.ListAcceleratorTypesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_accelerator_types), "__call__"
    ) as call:
        call.return_value = cloud_tpu.ListAcceleratorTypesResponse()
        client.list_accelerator_types(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_accelerator_types_field_headers_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.ListAcceleratorTypesRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_accelerator_types), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_tpu.ListAcceleratorTypesResponse()
        )
        await client.list_accelerator_types(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_accelerator_types_flattened():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_accelerator_types), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tpu.ListAcceleratorTypesResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_accelerator_types(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


def test_list_accelerator_types_flattened_error():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_accelerator_types(
            cloud_tpu.ListAcceleratorTypesRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_accelerator_types_flattened_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_accelerator_types), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tpu.ListAcceleratorTypesResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_tpu.ListAcceleratorTypesResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_accelerator_types(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = "parent_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_list_accelerator_types_flattened_error_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_accelerator_types(
            cloud_tpu.ListAcceleratorTypesRequest(), parent="parent_value",
        )


def test_list_accelerator_types_pager(transport_name: str = "grpc"):
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_accelerator_types), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_tpu.ListAcceleratorTypesResponse(
                accelerator_types=[
                    cloud_tpu.AcceleratorType(),
                    cloud_tpu.AcceleratorType(),
                    cloud_tpu.AcceleratorType(),
                ],
                next_page_token="abc",
            ),
            cloud_tpu.ListAcceleratorTypesResponse(
                accelerator_types=[], next_page_token="def",
            ),
            cloud_tpu.ListAcceleratorTypesResponse(
                accelerator_types=[cloud_tpu.AcceleratorType(),], next_page_token="ghi",
            ),
            cloud_tpu.ListAcceleratorTypesResponse(
                accelerator_types=[
                    cloud_tpu.AcceleratorType(),
                    cloud_tpu.AcceleratorType(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_accelerator_types(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, cloud_tpu.AcceleratorType) for i in results)


def test_list_accelerator_types_pages(transport_name: str = "grpc"):
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials, transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_accelerator_types), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_tpu.ListAcceleratorTypesResponse(
                accelerator_types=[
                    cloud_tpu.AcceleratorType(),
                    cloud_tpu.AcceleratorType(),
                    cloud_tpu.AcceleratorType(),
                ],
                next_page_token="abc",
            ),
            cloud_tpu.ListAcceleratorTypesResponse(
                accelerator_types=[], next_page_token="def",
            ),
            cloud_tpu.ListAcceleratorTypesResponse(
                accelerator_types=[cloud_tpu.AcceleratorType(),], next_page_token="ghi",
            ),
            cloud_tpu.ListAcceleratorTypesResponse(
                accelerator_types=[
                    cloud_tpu.AcceleratorType(),
                    cloud_tpu.AcceleratorType(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_accelerator_types(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_accelerator_types_async_pager():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_accelerator_types),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_tpu.ListAcceleratorTypesResponse(
                accelerator_types=[
                    cloud_tpu.AcceleratorType(),
                    cloud_tpu.AcceleratorType(),
                    cloud_tpu.AcceleratorType(),
                ],
                next_page_token="abc",
            ),
            cloud_tpu.ListAcceleratorTypesResponse(
                accelerator_types=[], next_page_token="def",
            ),
            cloud_tpu.ListAcceleratorTypesResponse(
                accelerator_types=[cloud_tpu.AcceleratorType(),], next_page_token="ghi",
            ),
            cloud_tpu.ListAcceleratorTypesResponse(
                accelerator_types=[
                    cloud_tpu.AcceleratorType(),
                    cloud_tpu.AcceleratorType(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_accelerator_types(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, cloud_tpu.AcceleratorType) for i in responses)


@pytest.mark.asyncio
async def test_list_accelerator_types_async_pages():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_accelerator_types),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloud_tpu.ListAcceleratorTypesResponse(
                accelerator_types=[
                    cloud_tpu.AcceleratorType(),
                    cloud_tpu.AcceleratorType(),
                    cloud_tpu.AcceleratorType(),
                ],
                next_page_token="abc",
            ),
            cloud_tpu.ListAcceleratorTypesResponse(
                accelerator_types=[], next_page_token="def",
            ),
            cloud_tpu.ListAcceleratorTypesResponse(
                accelerator_types=[cloud_tpu.AcceleratorType(),], next_page_token="ghi",
            ),
            cloud_tpu.ListAcceleratorTypesResponse(
                accelerator_types=[
                    cloud_tpu.AcceleratorType(),
                    cloud_tpu.AcceleratorType(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_accelerator_types(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [cloud_tpu.GetAcceleratorTypeRequest, dict,])
def test_get_accelerator_type(request_type, transport: str = "grpc"):
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_accelerator_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tpu.AcceleratorType(
            name="name_value", type_="type__value",
        )
        response = client.get_accelerator_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.GetAcceleratorTypeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_tpu.AcceleratorType)
    assert response.name == "name_value"
    assert response.type_ == "type__value"


def test_get_accelerator_type_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_accelerator_type), "__call__"
    ) as call:
        client.get_accelerator_type()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.GetAcceleratorTypeRequest()


@pytest.mark.asyncio
async def test_get_accelerator_type_async(
    transport: str = "grpc_asyncio", request_type=cloud_tpu.GetAcceleratorTypeRequest
):
    client = TpuAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_accelerator_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_tpu.AcceleratorType(name="name_value", type_="type__value",)
        )
        response = await client.get_accelerator_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == cloud_tpu.GetAcceleratorTypeRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, cloud_tpu.AcceleratorType)
    assert response.name == "name_value"
    assert response.type_ == "type__value"


@pytest.mark.asyncio
async def test_get_accelerator_type_async_from_dict():
    await test_get_accelerator_type_async(request_type=dict)


def test_get_accelerator_type_field_headers():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.GetAcceleratorTypeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_accelerator_type), "__call__"
    ) as call:
        call.return_value = cloud_tpu.AcceleratorType()
        client.get_accelerator_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_accelerator_type_field_headers_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloud_tpu.GetAcceleratorTypeRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_accelerator_type), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_tpu.AcceleratorType()
        )
        await client.get_accelerator_type(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_accelerator_type_flattened():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_accelerator_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tpu.AcceleratorType()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_accelerator_type(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


def test_get_accelerator_type_flattened_error():
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_accelerator_type(
            cloud_tpu.GetAcceleratorTypeRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_accelerator_type_flattened_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_accelerator_type), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloud_tpu.AcceleratorType()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloud_tpu.AcceleratorType()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_accelerator_type(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = "name_value"
        assert arg == mock_val


@pytest.mark.asyncio
async def test_get_accelerator_type_flattened_error_async():
    client = TpuAsyncClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_accelerator_type(
            cloud_tpu.GetAcceleratorTypeRequest(), name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.TpuGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = TpuClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.TpuGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = TpuClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.TpuGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = TpuClient(client_options=options, transport=transport,)

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = TpuClient(
            client_options=options, credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.TpuGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = TpuClient(client_options={"scopes": ["1", "2"]}, transport=transport,)


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.TpuGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = TpuClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.TpuGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.TpuGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [transports.TpuGrpcTransport, transports.TpuGrpcAsyncIOTransport,],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = TpuClient(credentials=ga_credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.TpuGrpcTransport,)


def test_tpu_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.TpuTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_tpu_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.tpu_v1.services.tpu.transports.TpuTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.TpuTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_nodes",
        "get_node",
        "create_node",
        "delete_node",
        "reimage_node",
        "stop_node",
        "start_node",
        "list_tensor_flow_versions",
        "get_tensor_flow_version",
        "list_accelerator_types",
        "get_accelerator_type",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


def test_tpu_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.tpu_v1.services.tpu.transports.TpuTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.TpuTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_tpu_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.tpu_v1.services.tpu.transports.TpuTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.TpuTransport()
        adc.assert_called_once()


def test_tpu_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        TpuClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [transports.TpuGrpcTransport, transports.TpuGrpcAsyncIOTransport,],
)
def test_tpu_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.TpuGrpcTransport, grpc_helpers),
        (transports.TpuGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
def test_tpu_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "tpu.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=("https://www.googleapis.com/auth/cloud-platform",),
            scopes=["1", "2"],
            default_host="tpu.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class", [transports.TpuGrpcTransport, transports.TpuGrpcAsyncIOTransport]
)
def test_tpu_grpc_transport_client_cert_source_for_mtls(transport_class):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


def test_tpu_host_no_port():
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint="tpu.googleapis.com"),
    )
    assert client.transport._host == "tpu.googleapis.com:443"


def test_tpu_host_with_port():
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="tpu.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "tpu.googleapis.com:8000"


def test_tpu_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.TpuGrpcTransport(host="squid.clam.whelk", channel=channel,)
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_tpu_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.TpuGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class", [transports.TpuGrpcTransport, transports.TpuGrpcAsyncIOTransport]
)
def test_tpu_transport_channel_mtls_with_client_cert_source(transport_class):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class", [transports.TpuGrpcTransport, transports.TpuGrpcAsyncIOTransport]
)
def test_tpu_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_tpu_grpc_lro_client():
    client = TpuClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_tpu_grpc_lro_async_client():
    client = TpuAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(transport.operations_client, operations_v1.OperationsAsyncClient,)

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_accelerator_type_path():
    project = "squid"
    location = "clam"
    accelerator_type = "whelk"
    expected = "projects/{project}/locations/{location}/acceleratorTypes/{accelerator_type}".format(
        project=project, location=location, accelerator_type=accelerator_type,
    )
    actual = TpuClient.accelerator_type_path(project, location, accelerator_type)
    assert expected == actual


def test_parse_accelerator_type_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "accelerator_type": "nudibranch",
    }
    path = TpuClient.accelerator_type_path(**expected)

    # Check that the path construction is reversible.
    actual = TpuClient.parse_accelerator_type_path(path)
    assert expected == actual


def test_node_path():
    project = "cuttlefish"
    location = "mussel"
    node = "winkle"
    expected = "projects/{project}/locations/{location}/nodes/{node}".format(
        project=project, location=location, node=node,
    )
    actual = TpuClient.node_path(project, location, node)
    assert expected == actual


def test_parse_node_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "node": "abalone",
    }
    path = TpuClient.node_path(**expected)

    # Check that the path construction is reversible.
    actual = TpuClient.parse_node_path(path)
    assert expected == actual


def test_tensor_flow_version_path():
    project = "squid"
    location = "clam"
    tensor_flow_version = "whelk"
    expected = "projects/{project}/locations/{location}/tensorFlowVersions/{tensor_flow_version}".format(
        project=project, location=location, tensor_flow_version=tensor_flow_version,
    )
    actual = TpuClient.tensor_flow_version_path(project, location, tensor_flow_version)
    assert expected == actual


def test_parse_tensor_flow_version_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "tensor_flow_version": "nudibranch",
    }
    path = TpuClient.tensor_flow_version_path(**expected)

    # Check that the path construction is reversible.
    actual = TpuClient.parse_tensor_flow_version_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "cuttlefish"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = TpuClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "mussel",
    }
    path = TpuClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = TpuClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "winkle"
    expected = "folders/{folder}".format(folder=folder,)
    actual = TpuClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nautilus",
    }
    path = TpuClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = TpuClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "scallop"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = TpuClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "abalone",
    }
    path = TpuClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = TpuClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "squid"
    expected = "projects/{project}".format(project=project,)
    actual = TpuClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "clam",
    }
    path = TpuClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = TpuClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "whelk"
    location = "octopus"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = TpuClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
    }
    path = TpuClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = TpuClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(transports.TpuTransport, "_prep_wrapped_messages") as prep:
        client = TpuClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(transports.TpuTransport, "_prep_wrapped_messages") as prep:
        transport_class = TpuClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)


@pytest.mark.asyncio
async def test_transport_close_async():
    client = TpuAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc_asyncio",
    )
    with mock.patch.object(
        type(getattr(client.transport, "grpc_channel")), "close"
    ) as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = TpuClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        with mock.patch.object(
            type(getattr(client.transport, close_name)), "close"
        ) as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()


def test_client_ctx():
    transports = [
        "grpc",
    ]
    for transport in transports:
        client = TpuClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()


@pytest.mark.parametrize(
    "client_class,transport_class",
    [
        (TpuClient, transports.TpuGrpcTransport),
        (TpuAsyncClient, transports.TpuGrpcAsyncIOTransport),
    ],
)
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
            )

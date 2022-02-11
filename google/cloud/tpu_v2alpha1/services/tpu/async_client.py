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
from collections import OrderedDict
import functools
import re
from typing import Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core.client_options import ClientOptions
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.tpu_v2alpha1.services.tpu import pagers
from google.cloud.tpu_v2alpha1.types import cloud_tpu
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import TpuTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import TpuGrpcAsyncIOTransport
from .client import TpuClient


class TpuAsyncClient:
    """Manages TPU nodes and other resources
    TPU API v2alpha1
    """

    _client: TpuClient

    DEFAULT_ENDPOINT = TpuClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = TpuClient.DEFAULT_MTLS_ENDPOINT

    accelerator_type_path = staticmethod(TpuClient.accelerator_type_path)
    parse_accelerator_type_path = staticmethod(TpuClient.parse_accelerator_type_path)
    node_path = staticmethod(TpuClient.node_path)
    parse_node_path = staticmethod(TpuClient.parse_node_path)
    runtime_version_path = staticmethod(TpuClient.runtime_version_path)
    parse_runtime_version_path = staticmethod(TpuClient.parse_runtime_version_path)
    common_billing_account_path = staticmethod(TpuClient.common_billing_account_path)
    parse_common_billing_account_path = staticmethod(
        TpuClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(TpuClient.common_folder_path)
    parse_common_folder_path = staticmethod(TpuClient.parse_common_folder_path)
    common_organization_path = staticmethod(TpuClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        TpuClient.parse_common_organization_path
    )
    common_project_path = staticmethod(TpuClient.common_project_path)
    parse_common_project_path = staticmethod(TpuClient.parse_common_project_path)
    common_location_path = staticmethod(TpuClient.common_location_path)
    parse_common_location_path = staticmethod(TpuClient.parse_common_location_path)

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            TpuAsyncClient: The constructed client.
        """
        return TpuClient.from_service_account_info.__func__(TpuAsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            TpuAsyncClient: The constructed client.
        """
        return TpuClient.from_service_account_file.__func__(TpuAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variabel is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        return TpuClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> TpuTransport:
        """Returns the transport used by the client instance.

        Returns:
            TpuTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(TpuClient).get_transport_class, type(TpuClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, TpuTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the tpu client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.TpuTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = TpuClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_nodes(
        self,
        request: Union[cloud_tpu.ListNodesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListNodesAsyncPager:
        r"""Lists nodes.

        .. code-block::

            from google.cloud import tpu_v2alpha1

            def sample_list_nodes():
                # Create a client
                client = tpu_v2alpha1.TpuClient()

                # Initialize request argument(s)
                request = tpu_v2alpha1.ListNodesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_nodes(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.tpu_v2alpha1.types.ListNodesRequest, dict]):
                The request object. Request for
                [ListNodes][google.cloud.tpu.v2alpha1.Tpu.ListNodes].
            parent (:class:`str`):
                Required. The parent resource name.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tpu_v2alpha1.services.tpu.pagers.ListNodesAsyncPager:
                Response for
                [ListNodes][google.cloud.tpu.v2alpha1.Tpu.ListNodes].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_tpu.ListNodesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_nodes,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListNodesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_node(
        self,
        request: Union[cloud_tpu.GetNodeRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_tpu.Node:
        r"""Gets the details of a node.

        .. code-block::

            from google.cloud import tpu_v2alpha1

            def sample_get_node():
                # Create a client
                client = tpu_v2alpha1.TpuClient()

                # Initialize request argument(s)
                request = tpu_v2alpha1.GetNodeRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_node(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.tpu_v2alpha1.types.GetNodeRequest, dict]):
                The request object. Request for
                [GetNode][google.cloud.tpu.v2alpha1.Tpu.GetNode].
            name (:class:`str`):
                Required. The resource name.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tpu_v2alpha1.types.Node:
                A TPU instance.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_tpu.GetNodeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_node,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_node(
        self,
        request: Union[cloud_tpu.CreateNodeRequest, dict] = None,
        *,
        parent: str = None,
        node: cloud_tpu.Node = None,
        node_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a node.

        .. code-block::

            from google.cloud import tpu_v2alpha1

            def sample_create_node():
                # Create a client
                client = tpu_v2alpha1.TpuClient()

                # Initialize request argument(s)
                node = tpu_v2alpha1.Node()
                node.accelerator_type = "accelerator_type_value"
                node.runtime_version = "runtime_version_value"

                request = tpu_v2alpha1.CreateNodeRequest(
                    parent="parent_value",
                    node=node,
                )

                # Make the request
                operation = client.create_node(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.tpu_v2alpha1.types.CreateNodeRequest, dict]):
                The request object. Request for
                [CreateNode][google.cloud.tpu.v2alpha1.Tpu.CreateNode].
            parent (:class:`str`):
                Required. The parent resource name.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            node (:class:`google.cloud.tpu_v2alpha1.types.Node`):
                Required. The node.
                This corresponds to the ``node`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            node_id (:class:`str`):
                The unqualified resource name.
                This corresponds to the ``node_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.tpu_v2alpha1.types.Node` A TPU
                instance.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, node, node_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_tpu.CreateNodeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if node is not None:
            request.node = node
        if node_id is not None:
            request.node_id = node_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_node,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloud_tpu.Node,
            metadata_type=cloud_tpu.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_node(
        self,
        request: Union[cloud_tpu.DeleteNodeRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a node.

        .. code-block::

            from google.cloud import tpu_v2alpha1

            def sample_delete_node():
                # Create a client
                client = tpu_v2alpha1.TpuClient()

                # Initialize request argument(s)
                request = tpu_v2alpha1.DeleteNodeRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_node(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.tpu_v2alpha1.types.DeleteNodeRequest, dict]):
                The request object. Request for
                [DeleteNode][google.cloud.tpu.v2alpha1.Tpu.DeleteNode].
            name (:class:`str`):
                Required. The resource name.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.tpu_v2alpha1.types.Node` A TPU
                instance.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_tpu.DeleteNodeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_node,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloud_tpu.Node,
            metadata_type=cloud_tpu.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def stop_node(
        self,
        request: Union[cloud_tpu.StopNodeRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Stops a node. This operation is only available with
        single TPU nodes.


        .. code-block::

            from google.cloud import tpu_v2alpha1

            def sample_stop_node():
                # Create a client
                client = tpu_v2alpha1.TpuClient()

                # Initialize request argument(s)
                request = tpu_v2alpha1.StopNodeRequest(
                )

                # Make the request
                operation = client.stop_node(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.tpu_v2alpha1.types.StopNodeRequest, dict]):
                The request object. Request for
                [StopNode][google.cloud.tpu.v2alpha1.Tpu.StopNode].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.tpu_v2alpha1.types.Node` A TPU
                instance.

        """
        # Create or coerce a protobuf request object.
        request = cloud_tpu.StopNodeRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.stop_node,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloud_tpu.Node,
            metadata_type=cloud_tpu.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def start_node(
        self,
        request: Union[cloud_tpu.StartNodeRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Starts a node.

        .. code-block::

            from google.cloud import tpu_v2alpha1

            def sample_start_node():
                # Create a client
                client = tpu_v2alpha1.TpuClient()

                # Initialize request argument(s)
                request = tpu_v2alpha1.StartNodeRequest(
                )

                # Make the request
                operation = client.start_node(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.tpu_v2alpha1.types.StartNodeRequest, dict]):
                The request object. Request for
                [StartNode][google.cloud.tpu.v2alpha1.Tpu.StartNode].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.tpu_v2alpha1.types.Node` A TPU
                instance.

        """
        # Create or coerce a protobuf request object.
        request = cloud_tpu.StartNodeRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.start_node,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloud_tpu.Node,
            metadata_type=cloud_tpu.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_node(
        self,
        request: Union[cloud_tpu.UpdateNodeRequest, dict] = None,
        *,
        node: cloud_tpu.Node = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the configurations of a node.

        .. code-block::

            from google.cloud import tpu_v2alpha1

            def sample_update_node():
                # Create a client
                client = tpu_v2alpha1.TpuClient()

                # Initialize request argument(s)
                node = tpu_v2alpha1.Node()
                node.accelerator_type = "accelerator_type_value"
                node.runtime_version = "runtime_version_value"

                request = tpu_v2alpha1.UpdateNodeRequest(
                    node=node,
                )

                # Make the request
                operation = client.update_node(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.tpu_v2alpha1.types.UpdateNodeRequest, dict]):
                The request object. Request for
                [UpdateNode][google.cloud.tpu.v2alpha1.Tpu.UpdateNode].
            node (:class:`google.cloud.tpu_v2alpha1.types.Node`):
                Required. The node. Only fields specified in update_mask
                are updated.

                This corresponds to the ``node`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. Mask of fields from [Node][Tpu.Node] to
                update. Supported fields: None.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.tpu_v2alpha1.types.Node` A TPU
                instance.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([node, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_tpu.UpdateNodeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if node is not None:
            request.node = node
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_node,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("node.name", request.node.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloud_tpu.Node,
            metadata_type=cloud_tpu.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def generate_service_identity(
        self,
        request: Union[cloud_tpu.GenerateServiceIdentityRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_tpu.GenerateServiceIdentityResponse:
        r"""Generates the Cloud TPU service identity for the
        project.


        .. code-block::

            from google.cloud import tpu_v2alpha1

            def sample_generate_service_identity():
                # Create a client
                client = tpu_v2alpha1.TpuClient()

                # Initialize request argument(s)
                request = tpu_v2alpha1.GenerateServiceIdentityRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.generate_service_identity(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.tpu_v2alpha1.types.GenerateServiceIdentityRequest, dict]):
                The request object. Request for
                [GenerateServiceIdentity][google.cloud.tpu.v2alpha1.Tpu.GenerateServiceIdentity].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tpu_v2alpha1.types.GenerateServiceIdentityResponse:
                Response for
                   [GenerateServiceIdentity][google.cloud.tpu.v2alpha1.Tpu.GenerateServiceIdentity].

        """
        # Create or coerce a protobuf request object.
        request = cloud_tpu.GenerateServiceIdentityRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.generate_service_identity,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_accelerator_types(
        self,
        request: Union[cloud_tpu.ListAcceleratorTypesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAcceleratorTypesAsyncPager:
        r"""Lists accelerator types supported by this API.

        .. code-block::

            from google.cloud import tpu_v2alpha1

            def sample_list_accelerator_types():
                # Create a client
                client = tpu_v2alpha1.TpuClient()

                # Initialize request argument(s)
                request = tpu_v2alpha1.ListAcceleratorTypesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_accelerator_types(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.tpu_v2alpha1.types.ListAcceleratorTypesRequest, dict]):
                The request object. Request for
                [ListAcceleratorTypes][google.cloud.tpu.v2alpha1.Tpu.ListAcceleratorTypes].
            parent (:class:`str`):
                Required. The parent resource name.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tpu_v2alpha1.services.tpu.pagers.ListAcceleratorTypesAsyncPager:
                Response for
                   [ListAcceleratorTypes][google.cloud.tpu.v2alpha1.Tpu.ListAcceleratorTypes].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_tpu.ListAcceleratorTypesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_accelerator_types,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListAcceleratorTypesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_accelerator_type(
        self,
        request: Union[cloud_tpu.GetAcceleratorTypeRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_tpu.AcceleratorType:
        r"""Gets AcceleratorType.

        .. code-block::

            from google.cloud import tpu_v2alpha1

            def sample_get_accelerator_type():
                # Create a client
                client = tpu_v2alpha1.TpuClient()

                # Initialize request argument(s)
                request = tpu_v2alpha1.GetAcceleratorTypeRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_accelerator_type(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.tpu_v2alpha1.types.GetAcceleratorTypeRequest, dict]):
                The request object. Request for
                [GetAcceleratorType][google.cloud.tpu.v2alpha1.Tpu.GetAcceleratorType].
            name (:class:`str`):
                Required. The resource name.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tpu_v2alpha1.types.AcceleratorType:
                A accelerator type that a Node can be
                configured with.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_tpu.GetAcceleratorTypeRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_accelerator_type,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_runtime_versions(
        self,
        request: Union[cloud_tpu.ListRuntimeVersionsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRuntimeVersionsAsyncPager:
        r"""Lists runtime versions supported by this API.

        .. code-block::

            from google.cloud import tpu_v2alpha1

            def sample_list_runtime_versions():
                # Create a client
                client = tpu_v2alpha1.TpuClient()

                # Initialize request argument(s)
                request = tpu_v2alpha1.ListRuntimeVersionsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_runtime_versions(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.tpu_v2alpha1.types.ListRuntimeVersionsRequest, dict]):
                The request object. Request for
                [ListRuntimeVersions][google.cloud.tpu.v2alpha1.Tpu.ListRuntimeVersions].
            parent (:class:`str`):
                Required. The parent resource name.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tpu_v2alpha1.services.tpu.pagers.ListRuntimeVersionsAsyncPager:
                Response for
                   [ListRuntimeVersions][google.cloud.tpu.v2alpha1.Tpu.ListRuntimeVersions].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_tpu.ListRuntimeVersionsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_runtime_versions,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListRuntimeVersionsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_runtime_version(
        self,
        request: Union[cloud_tpu.GetRuntimeVersionRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_tpu.RuntimeVersion:
        r"""Gets a runtime version.

        .. code-block::

            from google.cloud import tpu_v2alpha1

            def sample_get_runtime_version():
                # Create a client
                client = tpu_v2alpha1.TpuClient()

                # Initialize request argument(s)
                request = tpu_v2alpha1.GetRuntimeVersionRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_runtime_version(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.tpu_v2alpha1.types.GetRuntimeVersionRequest, dict]):
                The request object. Request for
                [GetRuntimeVersion][google.cloud.tpu.v2alpha1.Tpu.GetRuntimeVersion].
            name (:class:`str`):
                Required. The resource name.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tpu_v2alpha1.types.RuntimeVersion:
                A runtime version that a Node can be
                configured with.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_tpu.GetRuntimeVersionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_runtime_version,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def get_guest_attributes(
        self,
        request: Union[cloud_tpu.GetGuestAttributesRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_tpu.GetGuestAttributesResponse:
        r"""Retrieves the guest attributes for the node.

        .. code-block::

            from google.cloud import tpu_v2alpha1

            def sample_get_guest_attributes():
                # Create a client
                client = tpu_v2alpha1.TpuClient()

                # Initialize request argument(s)
                request = tpu_v2alpha1.GetGuestAttributesRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_guest_attributes(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.tpu_v2alpha1.types.GetGuestAttributesRequest, dict]):
                The request object. Request for
                [GetGuestAttributes][google.cloud.tpu.v2alpha1.Tpu.GetGuestAttributes].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.tpu_v2alpha1.types.GetGuestAttributesResponse:
                Response for
                   [GetGuestAttributes][google.cloud.tpu.v2alpha1.Tpu.GetGuestAttributes].

        """
        # Create or coerce a protobuf request object.
        request = cloud_tpu.GetGuestAttributesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_guest_attributes,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-tpu",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("TpuAsyncClient",)

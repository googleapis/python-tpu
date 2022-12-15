# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from typing import MutableMapping, MutableSequence

from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from google.type import interval_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.tpu.v2alpha1",
    manifest={
        "GuestAttributes",
        "GuestAttributesValue",
        "GuestAttributesEntry",
        "AttachedDisk",
        "SchedulingConfig",
        "NetworkEndpoint",
        "AccessConfig",
        "NetworkConfig",
        "ServiceAccount",
        "Node",
        "QueuedResource",
        "QueuedResourceState",
        "ListNodesRequest",
        "ListNodesResponse",
        "GetNodeRequest",
        "CreateNodeRequest",
        "DeleteNodeRequest",
        "StopNodeRequest",
        "StartNodeRequest",
        "UpdateNodeRequest",
        "ListQueuedResourcesRequest",
        "ListQueuedResourcesResponse",
        "GetQueuedResourceRequest",
        "CreateQueuedResourceRequest",
        "DeleteQueuedResourceRequest",
        "ServiceIdentity",
        "GenerateServiceIdentityRequest",
        "GenerateServiceIdentityResponse",
        "AcceleratorType",
        "GetAcceleratorTypeRequest",
        "ListAcceleratorTypesRequest",
        "ListAcceleratorTypesResponse",
        "RuntimeVersion",
        "GetRuntimeVersionRequest",
        "ListRuntimeVersionsRequest",
        "ListRuntimeVersionsResponse",
        "OperationMetadata",
        "Symptom",
        "GetGuestAttributesRequest",
        "GetGuestAttributesResponse",
        "SimulateMaintenanceEventRequest",
        "ShieldedInstanceConfig",
    },
)


class GuestAttributes(proto.Message):
    r"""A guest attributes.

    Attributes:
        query_path (str):
            The path to be queried. This can be the
            default namespace ('/') or a nested namespace
            ('/\<namespace\>/') or a specified key
            ('/\<namespace\>/\<key\>')
        query_value (google.cloud.tpu_v2alpha1.types.GuestAttributesValue):
            The value of the requested queried path.
    """

    query_path: str = proto.Field(
        proto.STRING,
        number=1,
    )
    query_value: "GuestAttributesValue" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="GuestAttributesValue",
    )


class GuestAttributesValue(proto.Message):
    r"""Array of guest attribute namespace/key/value tuples.

    Attributes:
        items (MutableSequence[google.cloud.tpu_v2alpha1.types.GuestAttributesEntry]):
            The list of guest attributes entries.
    """

    items: MutableSequence["GuestAttributesEntry"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="GuestAttributesEntry",
    )


class GuestAttributesEntry(proto.Message):
    r"""A guest attributes namespace/key/value entry.

    Attributes:
        namespace (str):
            Namespace for the guest attribute entry.
        key (str):
            Key for the guest attribute entry.
        value (str):
            Value for the guest attribute entry.
    """

    namespace: str = proto.Field(
        proto.STRING,
        number=1,
    )
    key: str = proto.Field(
        proto.STRING,
        number=2,
    )
    value: str = proto.Field(
        proto.STRING,
        number=3,
    )


class AttachedDisk(proto.Message):
    r"""A node-attached disk resource.
    Next ID: 8;

    Attributes:
        source_disk (str):
            Specifies the full path to an existing disk.
            For example:
            "projects/my-project/zones/us-central1-c/disks/my-disk".
        mode (google.cloud.tpu_v2alpha1.types.AttachedDisk.DiskMode):
            The mode in which to attach this disk. If not specified, the
            default is READ_WRITE mode. Only applicable to data_disks.
    """

    class DiskMode(proto.Enum):
        r"""The different mode of the attached disk."""
        DISK_MODE_UNSPECIFIED = 0
        READ_WRITE = 1
        READ_ONLY = 2

    source_disk: str = proto.Field(
        proto.STRING,
        number=3,
    )
    mode: DiskMode = proto.Field(
        proto.ENUM,
        number=4,
        enum=DiskMode,
    )


class SchedulingConfig(proto.Message):
    r"""Sets the scheduling options for this node.

    Attributes:
        preemptible (bool):
            Defines whether the node is preemptible.
        reserved (bool):
            Whether the node is created under a
            reservation.
    """

    preemptible: bool = proto.Field(
        proto.BOOL,
        number=1,
    )
    reserved: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class NetworkEndpoint(proto.Message):
    r"""A network endpoint over which a TPU worker can be reached.

    Attributes:
        ip_address (str):
            The internal IP address of this network
            endpoint.
        port (int):
            The port of this network endpoint.
        access_config (google.cloud.tpu_v2alpha1.types.AccessConfig):
            The access config for the TPU worker.
    """

    ip_address: str = proto.Field(
        proto.STRING,
        number=1,
    )
    port: int = proto.Field(
        proto.INT32,
        number=2,
    )
    access_config: "AccessConfig" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="AccessConfig",
    )


class AccessConfig(proto.Message):
    r"""An access config attached to the TPU worker.

    Attributes:
        external_ip (str):
            Output only. An external IP address
            associated with the TPU worker.
    """

    external_ip: str = proto.Field(
        proto.STRING,
        number=1,
    )


class NetworkConfig(proto.Message):
    r"""Network related configurations.

    Attributes:
        network (str):
            The name of the network for the TPU node. It
            must be a preexisting Google Compute Engine
            network. If none is provided, "default" will be
            used.
        subnetwork (str):
            The name of the subnetwork for the TPU node.
            It must be a preexisting Google Compute Engine
            subnetwork. If none is provided, "default" will
            be used.
        enable_external_ips (bool):
            Indicates that external IP addresses would be
            associated with the TPU workers. If set to
            false, the specified subnetwork or network
            should have Private Google Access enabled.
        can_ip_forward (bool):
            Allows the TPU node to send and receive
            packets with non-matching destination or source
            IPs. This is required if you plan to use the TPU
            workers to forward routes.
    """

    network: str = proto.Field(
        proto.STRING,
        number=1,
    )
    subnetwork: str = proto.Field(
        proto.STRING,
        number=2,
    )
    enable_external_ips: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    can_ip_forward: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class ServiceAccount(proto.Message):
    r"""A service account.

    Attributes:
        email (str):
            Email address of the service account. If
            empty, default Compute service account will be
            used.
        scope (MutableSequence[str]):
            The list of scopes to be made available for
            this service account. If empty, access to all
            Cloud APIs will be allowed.
    """

    email: str = proto.Field(
        proto.STRING,
        number=1,
    )
    scope: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class Node(proto.Message):
    r"""A TPU instance.

    Attributes:
        name (str):
            Output only. Immutable. The name of the TPU.
        description (str):
            The user-supplied description of the TPU.
            Maximum of 512 characters.
        accelerator_type (str):
            The type of hardware accelerators associated
            with this node.
        state (google.cloud.tpu_v2alpha1.types.Node.State):
            Output only. The current state for the TPU
            Node.
        health_description (str):
            Output only. If this field is populated, it
            contains a description of why the TPU Node is
            unhealthy.
        runtime_version (str):
            Required. The runtime version running in the
            Node.
        network_config (google.cloud.tpu_v2alpha1.types.NetworkConfig):
            Network configurations for the TPU node.
        cidr_block (str):
            The CIDR block that the TPU node will use
            when selecting an IP address. This CIDR block
            must be a /29 block; the Compute Engine networks
            API forbids a smaller block, and using a larger
            block would be wasteful (a node can only consume
            one IP address). Errors will occur if the CIDR
            block has already been used for a currently
            existing TPU node, the CIDR block conflicts with
            any subnetworks in the user's provided network,
            or the provided network is peered with another
            network that is using that CIDR block.
        service_account (google.cloud.tpu_v2alpha1.types.ServiceAccount):
            The Google Cloud Platform Service Account to
            be used by the TPU node VMs. If None is
            specified, the default compute service account
            will be used.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the node was
            created.
        scheduling_config (google.cloud.tpu_v2alpha1.types.SchedulingConfig):
            The scheduling options for this node.
        network_endpoints (MutableSequence[google.cloud.tpu_v2alpha1.types.NetworkEndpoint]):
            Output only. The network endpoints where TPU
            workers can be accessed and sent work. It is
            recommended that runtime clients of the node
            reach out to the 0th entry in this map first.
        health (google.cloud.tpu_v2alpha1.types.Node.Health):
            The health status of the TPU node.
        labels (MutableMapping[str, str]):
            Resource labels to represent user-provided
            metadata.
        metadata (MutableMapping[str, str]):
            Custom metadata to apply to the TPU Node.
            Can set startup-script and shutdown-script
        tags (MutableSequence[str]):
            Tags to apply to the TPU Node. Tags are used
            to identify valid sources or targets for network
            firewalls.
        id (int):
            Output only. The unique identifier for the
            TPU Node.
        data_disks (MutableSequence[google.cloud.tpu_v2alpha1.types.AttachedDisk]):
            The additional data disks for the Node.
        api_version (google.cloud.tpu_v2alpha1.types.Node.ApiVersion):
            Output only. The API version that created
            this Node.
        symptoms (MutableSequence[google.cloud.tpu_v2alpha1.types.Symptom]):
            Output only. The Symptoms that have occurred
            to the TPU Node.
        queued_resource (str):
            Output only. The qualified name of the
            QueuedResource that requested this Node.
        shielded_instance_config (google.cloud.tpu_v2alpha1.types.ShieldedInstanceConfig):
            Shielded Instance options.
    """

    class State(proto.Enum):
        r"""Represents the different states of a TPU node during its
        lifecycle.
        """
        STATE_UNSPECIFIED = 0
        CREATING = 1
        READY = 2
        RESTARTING = 3
        REIMAGING = 4
        DELETING = 5
        REPAIRING = 6
        STOPPED = 8
        STOPPING = 9
        STARTING = 10
        PREEMPTED = 11
        TERMINATED = 12
        HIDING = 13
        HIDDEN = 14
        UNHIDING = 15

    class Health(proto.Enum):
        r"""Health defines the status of a TPU node as reported by
        Health Monitor.
        """
        HEALTH_UNSPECIFIED = 0
        HEALTHY = 1
        TIMEOUT = 3
        UNHEALTHY_TENSORFLOW = 4
        UNHEALTHY_MAINTENANCE = 5

    class ApiVersion(proto.Enum):
        r"""TPU API Version."""
        API_VERSION_UNSPECIFIED = 0
        V1_ALPHA1 = 1
        V1 = 2
        V2_ALPHA1 = 3

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )
    accelerator_type: str = proto.Field(
        proto.STRING,
        number=5,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=9,
        enum=State,
    )
    health_description: str = proto.Field(
        proto.STRING,
        number=10,
    )
    runtime_version: str = proto.Field(
        proto.STRING,
        number=11,
    )
    network_config: "NetworkConfig" = proto.Field(
        proto.MESSAGE,
        number=36,
        message="NetworkConfig",
    )
    cidr_block: str = proto.Field(
        proto.STRING,
        number=13,
    )
    service_account: "ServiceAccount" = proto.Field(
        proto.MESSAGE,
        number=37,
        message="ServiceAccount",
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=16,
        message=timestamp_pb2.Timestamp,
    )
    scheduling_config: "SchedulingConfig" = proto.Field(
        proto.MESSAGE,
        number=17,
        message="SchedulingConfig",
    )
    network_endpoints: MutableSequence["NetworkEndpoint"] = proto.RepeatedField(
        proto.MESSAGE,
        number=21,
        message="NetworkEndpoint",
    )
    health: Health = proto.Field(
        proto.ENUM,
        number=22,
        enum=Health,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=24,
    )
    metadata: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=34,
    )
    tags: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=40,
    )
    id: int = proto.Field(
        proto.INT64,
        number=33,
    )
    data_disks: MutableSequence["AttachedDisk"] = proto.RepeatedField(
        proto.MESSAGE,
        number=41,
        message="AttachedDisk",
    )
    api_version: ApiVersion = proto.Field(
        proto.ENUM,
        number=38,
        enum=ApiVersion,
    )
    symptoms: MutableSequence["Symptom"] = proto.RepeatedField(
        proto.MESSAGE,
        number=39,
        message="Symptom",
    )
    queued_resource: str = proto.Field(
        proto.STRING,
        number=43,
    )
    shielded_instance_config: "ShieldedInstanceConfig" = proto.Field(
        proto.MESSAGE,
        number=45,
        message="ShieldedInstanceConfig",
    )


class QueuedResource(proto.Message):
    r"""A QueuedResource represents a request for resources that will
    be placed in a queue and fulfilled when the necessary resources
    are available.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Output only. Immutable. The name of the
            QueuedResource.
        tpu (google.cloud.tpu_v2alpha1.types.QueuedResource.Tpu):
            Defines a TPU resource.

            This field is a member of `oneof`_ ``resource``.
        best_effort (google.cloud.tpu_v2alpha1.types.QueuedResource.BestEffort):
            The BestEffort tier.

            This field is a member of `oneof`_ ``tier``.
        guaranteed (google.cloud.tpu_v2alpha1.types.QueuedResource.Guaranteed):
            The Guaranteed tier

            This field is a member of `oneof`_ ``tier``.
        queueing_policy (google.cloud.tpu_v2alpha1.types.QueuedResource.QueueingPolicy):
            The queueing policy of the QueuedRequest.
        state (google.cloud.tpu_v2alpha1.types.QueuedResourceState):
            Output only. State of the QueuedResource
            request
    """

    class Tpu(proto.Message):
        r"""Details of the TPU resource(s) being requested.

        Attributes:
            node_spec (MutableSequence[google.cloud.tpu_v2alpha1.types.QueuedResource.Tpu.NodeSpec]):
                The TPU node(s) being requested.
        """

        class NodeSpec(proto.Message):
            r"""Details of the TPU node(s) being requested. Users can request
            either a single node or multiple nodes.
            NodeSpec provides the specification for node(s) to be created.

            Attributes:
                parent (str):
                    Required. The parent resource name.
                node_id (str):
                    The unqualified resource name. Should follow the
                    ``^[A-Za-z0-9_.~+%-]+$`` regex format. This is only
                    specified when requesting a single node. In case of
                    multi-node requests, multi_node_params must be populated
                    instead. It's an error to specify both node_id and
                    multi_node_params.
                node (google.cloud.tpu_v2alpha1.types.Node):
                    Required. The node.
            """

            parent: str = proto.Field(
                proto.STRING,
                number=1,
            )
            node_id: str = proto.Field(
                proto.STRING,
                number=2,
            )
            node: "Node" = proto.Field(
                proto.MESSAGE,
                number=3,
                message="Node",
            )

        node_spec: MutableSequence["QueuedResource.Tpu.NodeSpec"] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="QueuedResource.Tpu.NodeSpec",
        )

    class BestEffort(proto.Message):
        r"""BestEffort tier definition."""

    class Guaranteed(proto.Message):
        r"""Guaranteed tier definition.

        Attributes:
            min_duration (google.protobuf.duration_pb2.Duration):
                Optional. Defines the minimum duration of the
                guarantee. If specified, the requested resources
                will only be provisioned if they can be
                allocated for at least the given duration.
            reserved (bool):
                Optional. Specifies the request should be
                scheduled on reserved capacity.
        """

        min_duration: duration_pb2.Duration = proto.Field(
            proto.MESSAGE,
            number=1,
            message=duration_pb2.Duration,
        )
        reserved: bool = proto.Field(
            proto.BOOL,
            number=2,
        )

    class QueueingPolicy(proto.Message):
        r"""Defines the policy of the QueuedRequest.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            valid_until_duration (google.protobuf.duration_pb2.Duration):
                A relative time after which resources should
                not be created. If the request cannot be
                fulfilled by this time the request will be
                failed.

                This field is a member of `oneof`_ ``start_timing_constraints``.
            valid_until_time (google.protobuf.timestamp_pb2.Timestamp):
                An absolute time after which resources should
                not be created. If the request cannot be
                fulfilled by this time the request will be
                failed.

                This field is a member of `oneof`_ ``start_timing_constraints``.
            valid_after_duration (google.protobuf.duration_pb2.Duration):
                A relative time after which resources may be
                created.

                This field is a member of `oneof`_ ``start_timing_constraints``.
            valid_after_time (google.protobuf.timestamp_pb2.Timestamp):
                An absolute time at which resources may be
                created.

                This field is a member of `oneof`_ ``start_timing_constraints``.
            valid_interval (google.type.interval_pb2.Interval):
                An absolute time interval within which
                resources may be created.

                This field is a member of `oneof`_ ``start_timing_constraints``.
        """

        valid_until_duration: duration_pb2.Duration = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="start_timing_constraints",
            message=duration_pb2.Duration,
        )
        valid_until_time: timestamp_pb2.Timestamp = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="start_timing_constraints",
            message=timestamp_pb2.Timestamp,
        )
        valid_after_duration: duration_pb2.Duration = proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="start_timing_constraints",
            message=duration_pb2.Duration,
        )
        valid_after_time: timestamp_pb2.Timestamp = proto.Field(
            proto.MESSAGE,
            number=4,
            oneof="start_timing_constraints",
            message=timestamp_pb2.Timestamp,
        )
        valid_interval: interval_pb2.Interval = proto.Field(
            proto.MESSAGE,
            number=5,
            oneof="start_timing_constraints",
            message=interval_pb2.Interval,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    tpu: Tpu = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="resource",
        message=Tpu,
    )
    best_effort: BestEffort = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="tier",
        message=BestEffort,
    )
    guaranteed: Guaranteed = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="tier",
        message=Guaranteed,
    )
    queueing_policy: QueueingPolicy = proto.Field(
        proto.MESSAGE,
        number=5,
        message=QueueingPolicy,
    )
    state: "QueuedResourceState" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="QueuedResourceState",
    )


class QueuedResourceState(proto.Message):
    r"""QueuedResourceState defines the details of the QueuedResource
    request.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        state (google.cloud.tpu_v2alpha1.types.QueuedResourceState.State):
            State of the QueuedResource request.
        creating_data (google.cloud.tpu_v2alpha1.types.QueuedResourceState.CreatingData):
            Further data for the creating state.

            This field is a member of `oneof`_ ``state_data``.
        accepted_data (google.cloud.tpu_v2alpha1.types.QueuedResourceState.AcceptedData):
            Further data for the accepted state.

            This field is a member of `oneof`_ ``state_data``.
        provisioning_data (google.cloud.tpu_v2alpha1.types.QueuedResourceState.ProvisioningData):
            Further data for the provisioning state.

            This field is a member of `oneof`_ ``state_data``.
        failed_data (google.cloud.tpu_v2alpha1.types.QueuedResourceState.FailedData):
            Further data for the failed state.

            This field is a member of `oneof`_ ``state_data``.
        deleting_data (google.cloud.tpu_v2alpha1.types.QueuedResourceState.DeletingData):
            Further data for the deleting state.

            This field is a member of `oneof`_ ``state_data``.
        active_data (google.cloud.tpu_v2alpha1.types.QueuedResourceState.ActiveData):
            Further data for the active state.

            This field is a member of `oneof`_ ``state_data``.
        suspending_data (google.cloud.tpu_v2alpha1.types.QueuedResourceState.SuspendingData):
            Further data for the suspending state.

            This field is a member of `oneof`_ ``state_data``.
        suspended_data (google.cloud.tpu_v2alpha1.types.QueuedResourceState.SuspendedData):
            Further data for the suspended state.

            This field is a member of `oneof`_ ``state_data``.
    """

    class State(proto.Enum):
        r"""Output only state of the request"""
        STATE_UNSPECIFIED = 0
        CREATING = 1
        ACCEPTED = 2
        PROVISIONING = 3
        FAILED = 4
        DELETING = 5
        ACTIVE = 6
        SUSPENDING = 7
        SUSPENDED = 8

    class CreatingData(proto.Message):
        r"""Further data for the creating state."""

    class AcceptedData(proto.Message):
        r"""Further data for the accepted state."""

    class ProvisioningData(proto.Message):
        r"""Further data for the provisioning state."""

    class FailedData(proto.Message):
        r"""Further data for the failed state.

        Attributes:
            error (google.rpc.status_pb2.Status):
                The error that caused the queued resource to
                enter the FAILED state.
        """

        error: status_pb2.Status = proto.Field(
            proto.MESSAGE,
            number=1,
            message=status_pb2.Status,
        )

    class DeletingData(proto.Message):
        r"""Further data for the deleting state."""

    class ActiveData(proto.Message):
        r"""Further data for the active state."""

    class SuspendingData(proto.Message):
        r"""Further data for the suspending state."""

    class SuspendedData(proto.Message):
        r"""Further data for the suspended state."""

    state: State = proto.Field(
        proto.ENUM,
        number=1,
        enum=State,
    )
    creating_data: CreatingData = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="state_data",
        message=CreatingData,
    )
    accepted_data: AcceptedData = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="state_data",
        message=AcceptedData,
    )
    provisioning_data: ProvisioningData = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="state_data",
        message=ProvisioningData,
    )
    failed_data: FailedData = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="state_data",
        message=FailedData,
    )
    deleting_data: DeletingData = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="state_data",
        message=DeletingData,
    )
    active_data: ActiveData = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="state_data",
        message=ActiveData,
    )
    suspending_data: SuspendingData = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="state_data",
        message=SuspendingData,
    )
    suspended_data: SuspendedData = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="state_data",
        message=SuspendedData,
    )


class ListNodesRequest(proto.Message):
    r"""Request for [ListNodes][google.cloud.tpu.v2alpha1.Tpu.ListNodes].

    Attributes:
        parent (str):
            Required. The parent resource name.
        page_size (int):
            The maximum number of items to return.
        page_token (str):
            The next_page_token value returned from a previous List
            request, if any.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListNodesResponse(proto.Message):
    r"""Response for [ListNodes][google.cloud.tpu.v2alpha1.Tpu.ListNodes].

    Attributes:
        nodes (MutableSequence[google.cloud.tpu_v2alpha1.types.Node]):
            The listed nodes.
        next_page_token (str):
            The next page token or empty if none.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    nodes: MutableSequence["Node"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Node",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetNodeRequest(proto.Message):
    r"""Request for [GetNode][google.cloud.tpu.v2alpha1.Tpu.GetNode].

    Attributes:
        name (str):
            Required. The resource name.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateNodeRequest(proto.Message):
    r"""Request for [CreateNode][google.cloud.tpu.v2alpha1.Tpu.CreateNode].

    Attributes:
        parent (str):
            Required. The parent resource name.
        node_id (str):
            The unqualified resource name.
        node (google.cloud.tpu_v2alpha1.types.Node):
            Required. The node.
        request_id (str):
            Idempotent request UUID.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    node_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    node: "Node" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Node",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=6,
    )


class DeleteNodeRequest(proto.Message):
    r"""Request for [DeleteNode][google.cloud.tpu.v2alpha1.Tpu.DeleteNode].

    Attributes:
        name (str):
            Required. The resource name.
        request_id (str):
            Idempotent request UUID.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class StopNodeRequest(proto.Message):
    r"""Request for [StopNode][google.cloud.tpu.v2alpha1.Tpu.StopNode].

    Attributes:
        name (str):
            Required. The resource name.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class StartNodeRequest(proto.Message):
    r"""Request for [StartNode][google.cloud.tpu.v2alpha1.Tpu.StartNode].

    Attributes:
        name (str):
            Required. The resource name.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateNodeRequest(proto.Message):
    r"""Request for [UpdateNode][google.cloud.tpu.v2alpha1.Tpu.UpdateNode].

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. Mask of fields from [Node][Tpu.Node] to update.
            Supported fields: [description, tags, labels, metadata,
            network_config.enable_external_ips].
        node (google.cloud.tpu_v2alpha1.types.Node):
            Required. The node. Only fields specified in update_mask are
            updated.
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=1,
        message=field_mask_pb2.FieldMask,
    )
    node: "Node" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Node",
    )


class ListQueuedResourcesRequest(proto.Message):
    r"""Request for
    [ListQueuedResources][google.cloud.tpu.v2alpha1.Tpu.ListQueuedResources].

    Attributes:
        parent (str):
            Required. The parent resource name.
        page_size (int):
            The maximum number of items to return.
        page_token (str):
            The next_page_token value returned from a previous List
            request, if any.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListQueuedResourcesResponse(proto.Message):
    r"""Response for
    [ListQueuedResources][google.cloud.tpu.v2alpha1.Tpu.ListQueuedResources].

    Attributes:
        queued_resources (MutableSequence[google.cloud.tpu_v2alpha1.types.QueuedResource]):
            The listed queued resources.
        next_page_token (str):
            The next page token or empty if none.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    queued_resources: MutableSequence["QueuedResource"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="QueuedResource",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetQueuedResourceRequest(proto.Message):
    r"""Request for
    [GetQueuedResource][google.cloud.tpu.v2alpha1.Tpu.GetQueuedResource]

    Attributes:
        name (str):
            Required. The resource name.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateQueuedResourceRequest(proto.Message):
    r"""Request for
    [CreateQueuedResource][google.cloud.tpu.v2alpha1.Tpu.CreateQueuedResource].

    Attributes:
        parent (str):
            Required. The parent resource name.
        queued_resource_id (str):
            The unqualified resource name. Should follow the
            ``^[A-Za-z0-9_.~+%-]+$`` regex format.
        queued_resource (google.cloud.tpu_v2alpha1.types.QueuedResource):
            Required. The queued resource.
        request_id (str):
            Idempotent request UUID.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    queued_resource_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    queued_resource: "QueuedResource" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="QueuedResource",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class DeleteQueuedResourceRequest(proto.Message):
    r"""Request for
    [DeleteQueuedResource][google.cloud.tpu.v2alpha1.Tpu.DeleteQueuedResource].

    Attributes:
        name (str):
            Required. The resource name.
        request_id (str):
            Idempotent request UUID.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ServiceIdentity(proto.Message):
    r"""The per-product per-project service identity for Cloud TPU
    service.

    Attributes:
        email (str):
            The email address of the service identity.
    """

    email: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GenerateServiceIdentityRequest(proto.Message):
    r"""Request for
    [GenerateServiceIdentity][google.cloud.tpu.v2alpha1.Tpu.GenerateServiceIdentity].

    Attributes:
        parent (str):
            Required. The parent resource name.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GenerateServiceIdentityResponse(proto.Message):
    r"""Response for
    [GenerateServiceIdentity][google.cloud.tpu.v2alpha1.Tpu.GenerateServiceIdentity].

    Attributes:
        identity (google.cloud.tpu_v2alpha1.types.ServiceIdentity):
            ServiceIdentity that was created or
            retrieved.
    """

    identity: "ServiceIdentity" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="ServiceIdentity",
    )


class AcceleratorType(proto.Message):
    r"""A accelerator type that a Node can be configured with.

    Attributes:
        name (str):
            The resource name.
        type_ (str):
            The accelerator type.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    type_: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetAcceleratorTypeRequest(proto.Message):
    r"""Request for
    [GetAcceleratorType][google.cloud.tpu.v2alpha1.Tpu.GetAcceleratorType].

    Attributes:
        name (str):
            Required. The resource name.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListAcceleratorTypesRequest(proto.Message):
    r"""Request for
    [ListAcceleratorTypes][google.cloud.tpu.v2alpha1.Tpu.ListAcceleratorTypes].

    Attributes:
        parent (str):
            Required. The parent resource name.
        page_size (int):
            The maximum number of items to return.
        page_token (str):
            The next_page_token value returned from a previous List
            request, if any.
        filter (str):
            List filter.
        order_by (str):
            Sort results.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=5,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=6,
    )


class ListAcceleratorTypesResponse(proto.Message):
    r"""Response for
    [ListAcceleratorTypes][google.cloud.tpu.v2alpha1.Tpu.ListAcceleratorTypes].

    Attributes:
        accelerator_types (MutableSequence[google.cloud.tpu_v2alpha1.types.AcceleratorType]):
            The listed nodes.
        next_page_token (str):
            The next page token or empty if none.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    accelerator_types: MutableSequence["AcceleratorType"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="AcceleratorType",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class RuntimeVersion(proto.Message):
    r"""A runtime version that a Node can be configured with.

    Attributes:
        name (str):
            The resource name.
        version (str):
            The runtime version.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    version: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetRuntimeVersionRequest(proto.Message):
    r"""Request for
    [GetRuntimeVersion][google.cloud.tpu.v2alpha1.Tpu.GetRuntimeVersion].

    Attributes:
        name (str):
            Required. The resource name.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListRuntimeVersionsRequest(proto.Message):
    r"""Request for
    [ListRuntimeVersions][google.cloud.tpu.v2alpha1.Tpu.ListRuntimeVersions].

    Attributes:
        parent (str):
            Required. The parent resource name.
        page_size (int):
            The maximum number of items to return.
        page_token (str):
            The next_page_token value returned from a previous List
            request, if any.
        filter (str):
            List filter.
        order_by (str):
            Sort results.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=5,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=6,
    )


class ListRuntimeVersionsResponse(proto.Message):
    r"""Response for
    [ListRuntimeVersions][google.cloud.tpu.v2alpha1.Tpu.ListRuntimeVersions].

    Attributes:
        runtime_versions (MutableSequence[google.cloud.tpu_v2alpha1.types.RuntimeVersion]):
            The listed nodes.
        next_page_token (str):
            The next page token or empty if none.
        unreachable (MutableSequence[str]):
            Locations that could not be reached.
    """

    @property
    def raw_page(self):
        return self

    runtime_versions: MutableSequence["RuntimeVersion"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="RuntimeVersion",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class OperationMetadata(proto.Message):
    r"""Metadata describing an [Operation][google.longrunning.Operation]

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the operation was created.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            The time the operation finished running.
        target (str):
            Target of the operation - for example
            projects/project-1/connectivityTests/test-1
        verb (str):
            Name of the verb executed by the operation.
        status_detail (str):
            Human-readable status of the operation, if
            any.
        cancel_requested (bool):
            Specifies if cancellation was requested for
            the operation.
        api_version (str):
            API version.
    """

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    target: str = proto.Field(
        proto.STRING,
        number=3,
    )
    verb: str = proto.Field(
        proto.STRING,
        number=4,
    )
    status_detail: str = proto.Field(
        proto.STRING,
        number=5,
    )
    cancel_requested: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    api_version: str = proto.Field(
        proto.STRING,
        number=7,
    )


class Symptom(proto.Message):
    r"""A Symptom instance.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Timestamp when the Symptom is created.
        symptom_type (google.cloud.tpu_v2alpha1.types.Symptom.SymptomType):
            Type of the Symptom.
        details (str):
            Detailed information of the current Symptom.
        worker_id (str):
            A string used to uniquely distinguish a
            worker within a TPU node.
    """

    class SymptomType(proto.Enum):
        r"""SymptomType represents the different types of Symptoms that a
        TPU can be at.
        """
        SYMPTOM_TYPE_UNSPECIFIED = 0
        LOW_MEMORY = 1
        OUT_OF_MEMORY = 2
        EXECUTE_TIMED_OUT = 3
        MESH_BUILD_FAIL = 4
        HBM_OUT_OF_MEMORY = 5
        PROJECT_ABUSE = 6

    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    symptom_type: SymptomType = proto.Field(
        proto.ENUM,
        number=2,
        enum=SymptomType,
    )
    details: str = proto.Field(
        proto.STRING,
        number=3,
    )
    worker_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class GetGuestAttributesRequest(proto.Message):
    r"""Request for
    [GetGuestAttributes][google.cloud.tpu.v2alpha1.Tpu.GetGuestAttributes].

    Attributes:
        name (str):
            Required. The resource name.
        query_path (str):
            The guest attributes path to be queried.
        worker_ids (MutableSequence[str]):
            The 0-based worker ID. If it is empty, all
            workers' GuestAttributes will be returned.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    query_path: str = proto.Field(
        proto.STRING,
        number=2,
    )
    worker_ids: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class GetGuestAttributesResponse(proto.Message):
    r"""Response for
    [GetGuestAttributes][google.cloud.tpu.v2alpha1.Tpu.GetGuestAttributes].

    Attributes:
        guest_attributes (MutableSequence[google.cloud.tpu_v2alpha1.types.GuestAttributes]):
            The guest attributes for the TPU workers.
    """

    guest_attributes: MutableSequence["GuestAttributes"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="GuestAttributes",
    )


class SimulateMaintenanceEventRequest(proto.Message):
    r"""Request for
    [SimulateMaintenanceEvent][google.cloud.tpu.v2alpha1.Tpu.SimulateMaintenanceEvent].

    Attributes:
        name (str):
            Required. The resource name.
        worker_ids (MutableSequence[str]):
            The 0-based worker ID. If it is empty, worker
            ID 0 will be selected for maintenance event
            simulation. A maintenance event will only be
            fired on the first specified worker ID. Future
            implementations may support firing on multiple
            workers.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    worker_ids: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class ShieldedInstanceConfig(proto.Message):
    r"""A set of Shielded Instance options.

    Attributes:
        enable_secure_boot (bool):
            Defines whether the instance has Secure Boot
            enabled.
    """

    enable_secure_boot: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))

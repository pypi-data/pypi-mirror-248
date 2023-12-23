# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.config.v1 import user_config_pb2 as spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2


class UserConfigStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.create = channel.unary_unary(
                '/spaceone.api.config.v1.UserConfig/create',
                request_serializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.SetUserConfigRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigInfo.FromString,
                )
        self.update = channel.unary_unary(
                '/spaceone.api.config.v1.UserConfig/update',
                request_serializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.SetUserConfigRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigInfo.FromString,
                )
        self.set = channel.unary_unary(
                '/spaceone.api.config.v1.UserConfig/set',
                request_serializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.SetUserConfigRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigInfo.FromString,
                )
        self.delete = channel.unary_unary(
                '/spaceone.api.config.v1.UserConfig/delete',
                request_serializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.get = channel.unary_unary(
                '/spaceone.api.config.v1.UserConfig/get',
                request_serializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigInfo.FromString,
                )
        self.list = channel.unary_unary(
                '/spaceone.api.config.v1.UserConfig/list',
                request_serializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigsInfo.FromString,
                )
        self.stat = channel.unary_unary(
                '/spaceone.api.config.v1.UserConfig/stat',
                request_serializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigStatQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                )


class UserConfigServicer(object):
    """Missing associated documentation comment in .proto file."""

    def create(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def set(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UserConfigServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'create': grpc.unary_unary_rpc_method_handler(
                    servicer.create,
                    request_deserializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.SetUserConfigRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigInfo.SerializeToString,
            ),
            'update': grpc.unary_unary_rpc_method_handler(
                    servicer.update,
                    request_deserializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.SetUserConfigRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigInfo.SerializeToString,
            ),
            'set': grpc.unary_unary_rpc_method_handler(
                    servicer.set,
                    request_deserializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.SetUserConfigRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigInfo.SerializeToString,
            ),
            'delete': grpc.unary_unary_rpc_method_handler(
                    servicer.delete,
                    request_deserializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigInfo.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigsInfo.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigStatQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.config.v1.UserConfig', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class UserConfig(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.config.v1.UserConfig/create',
            spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.SetUserConfigRequest.SerializeToString,
            spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def update(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.config.v1.UserConfig/update',
            spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.SetUserConfigRequest.SerializeToString,
            spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def set(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.config.v1.UserConfig/set',
            spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.SetUserConfigRequest.SerializeToString,
            spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.config.v1.UserConfig/delete',
            spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.config.v1.UserConfig/get',
            spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigRequest.SerializeToString,
            spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def list(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.config.v1.UserConfig/list',
            spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigQuery.SerializeToString,
            spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigsInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def stat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.config.v1.UserConfig/stat',
            spaceone_dot_api_dot_config_dot_v1_dot_user__config__pb2.UserConfigStatQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

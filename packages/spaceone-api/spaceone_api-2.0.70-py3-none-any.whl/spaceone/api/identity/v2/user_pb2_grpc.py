# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.identity.v2 import user_pb2 as spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2


class UserStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.create = channel.unary_unary(
                '/spaceone.api.identity.v2.User/create',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.CreateUserRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
                )
        self.update = channel.unary_unary(
                '/spaceone.api.identity.v2.User/update',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UpdateUserRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
                )
        self.verify_email = channel.unary_unary(
                '/spaceone.api.identity.v2.User/verify_email',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.VerifyUserEmailRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.disable_mfa = channel.unary_unary(
                '/spaceone.api.identity.v2.User/disable_mfa',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.DisableUserMFARequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
                )
        self.set_required_actions = channel.unary_unary(
                '/spaceone.api.identity.v2.User/set_required_actions',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.SetRequiredActionsRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
                )
        self.enable = channel.unary_unary(
                '/spaceone.api.identity.v2.User/enable',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
                )
        self.disable = channel.unary_unary(
                '/spaceone.api.identity.v2.User/disable',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
                )
        self.delete = channel.unary_unary(
                '/spaceone.api.identity.v2.User/delete',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.get = channel.unary_unary(
                '/spaceone.api.identity.v2.User/get',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
                )
        self.list = channel.unary_unary(
                '/spaceone.api.identity.v2.User/list',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserSearchQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UsersInfo.FromString,
                )
        self.stat = channel.unary_unary(
                '/spaceone.api.identity.v2.User/stat',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserStatQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                )


class UserServicer(object):
    """Missing associated documentation comment in .proto file."""

    def create(self, request, context):
        """You can create user. after create user you have to binding role to user.
        See role-binding create api.
        External type user do not need password.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update(self, request, context):
        """Update user info by given user_id
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def verify_email(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def disable_mfa(self, request, context):
        """Disable MFA for user. If this api is called, send email to user.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def set_required_actions(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def enable(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def disable(self, request, context):
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


def add_UserServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'create': grpc.unary_unary_rpc_method_handler(
                    servicer.create,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.CreateUserRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.SerializeToString,
            ),
            'update': grpc.unary_unary_rpc_method_handler(
                    servicer.update,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UpdateUserRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.SerializeToString,
            ),
            'verify_email': grpc.unary_unary_rpc_method_handler(
                    servicer.verify_email,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.VerifyUserEmailRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'disable_mfa': grpc.unary_unary_rpc_method_handler(
                    servicer.disable_mfa,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.DisableUserMFARequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.SerializeToString,
            ),
            'set_required_actions': grpc.unary_unary_rpc_method_handler(
                    servicer.set_required_actions,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.SetRequiredActionsRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.SerializeToString,
            ),
            'enable': grpc.unary_unary_rpc_method_handler(
                    servicer.enable,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.SerializeToString,
            ),
            'disable': grpc.unary_unary_rpc_method_handler(
                    servicer.disable,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.SerializeToString,
            ),
            'delete': grpc.unary_unary_rpc_method_handler(
                    servicer.delete,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserSearchQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UsersInfo.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserStatQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.identity.v2.User', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class User(object):
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.User/create',
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.CreateUserRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.User/update',
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UpdateUserRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def verify_email(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.User/verify_email',
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.VerifyUserEmailRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def disable_mfa(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.User/disable_mfa',
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.DisableUserMFARequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def set_required_actions(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.User/set_required_actions',
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.SetRequiredActionsRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def enable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.User/enable',
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def disable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.User/disable',
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.User/delete',
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserRequest.SerializeToString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.User/get',
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.User/list',
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserSearchQuery.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UsersInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.User/stat',
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserStatQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

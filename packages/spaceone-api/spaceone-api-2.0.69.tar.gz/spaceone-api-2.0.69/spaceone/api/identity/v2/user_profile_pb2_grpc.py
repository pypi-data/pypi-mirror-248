# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from spaceone.api.identity.v2 import user_pb2 as spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2
from spaceone.api.identity.v2 import user_profile_pb2 as spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2
from spaceone.api.identity.v2 import workspace_pb2 as spaceone_dot_api_dot_identity_dot_v2_dot_workspace__pb2


class UserProfileStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.update = channel.unary_unary(
                '/spaceone.api.identity.v2.UserProfile/update',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.UpdateUserProfileRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
                )
        self.verify_email = channel.unary_unary(
                '/spaceone.api.identity.v2.UserProfile/verify_email',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.VerifyEmailRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.confirm_email = channel.unary_unary(
                '/spaceone.api.identity.v2.UserProfile/confirm_email',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.ConfirmEmailRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
                )
        self.reset_password = channel.unary_unary(
                '/spaceone.api.identity.v2.UserProfile/reset_password',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.UserProfileRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.enable_mfa = channel.unary_unary(
                '/spaceone.api.identity.v2.UserProfile/enable_mfa',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.EnableMFARequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
                )
        self.disable_mfa = channel.unary_unary(
                '/spaceone.api.identity.v2.UserProfile/disable_mfa',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.DisableMFARequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
                )
        self.confirm_mfa = channel.unary_unary(
                '/spaceone.api.identity.v2.UserProfile/confirm_mfa',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.ConfirmMFARequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
                )
        self.get = channel.unary_unary(
                '/spaceone.api.identity.v2.UserProfile/get',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.UserProfileRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
                )
        self.get_workspaces = channel.unary_unary(
                '/spaceone.api.identity.v2.UserProfile/get_workspaces',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.UserProfileRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__pb2.WorkspacesInfo.FromString,
                )


class UserProfileServicer(object):
    """Missing associated documentation comment in .proto file."""

    def update(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def verify_email(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def confirm_email(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def reset_password(self, request, context):
        """+noauth
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def enable_mfa(self, request, context):
        """Enable MFA for user. If this api is called, send email to user.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def disable_mfa(self, request, context):
        """Disable MFA for user. If this api is called, send email to user.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def confirm_mfa(self, request, context):
        """Confirm MFA for user by given verify_code which is sent by your authentication method.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_workspaces(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UserProfileServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'update': grpc.unary_unary_rpc_method_handler(
                    servicer.update,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.UpdateUserProfileRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.SerializeToString,
            ),
            'verify_email': grpc.unary_unary_rpc_method_handler(
                    servicer.verify_email,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.VerifyEmailRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'confirm_email': grpc.unary_unary_rpc_method_handler(
                    servicer.confirm_email,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.ConfirmEmailRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.SerializeToString,
            ),
            'reset_password': grpc.unary_unary_rpc_method_handler(
                    servicer.reset_password,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.UserProfileRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'enable_mfa': grpc.unary_unary_rpc_method_handler(
                    servicer.enable_mfa,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.EnableMFARequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.SerializeToString,
            ),
            'disable_mfa': grpc.unary_unary_rpc_method_handler(
                    servicer.disable_mfa,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.DisableMFARequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.SerializeToString,
            ),
            'confirm_mfa': grpc.unary_unary_rpc_method_handler(
                    servicer.confirm_mfa,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.ConfirmMFARequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.UserProfileRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.SerializeToString,
            ),
            'get_workspaces': grpc.unary_unary_rpc_method_handler(
                    servicer.get_workspaces,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.UserProfileRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_workspace__pb2.WorkspacesInfo.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.identity.v2.UserProfile', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class UserProfile(object):
    """Missing associated documentation comment in .proto file."""

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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.UserProfile/update',
            spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.UpdateUserProfileRequest.SerializeToString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.UserProfile/verify_email',
            spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.VerifyEmailRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def confirm_email(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.UserProfile/confirm_email',
            spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.ConfirmEmailRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def reset_password(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.UserProfile/reset_password',
            spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.UserProfileRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def enable_mfa(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.UserProfile/enable_mfa',
            spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.EnableMFARequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.UserProfile/disable_mfa',
            spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.DisableMFARequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def confirm_mfa(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.UserProfile/confirm_mfa',
            spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.ConfirmMFARequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.UserProfile/get',
            spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.UserProfileRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_user__pb2.UserInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_workspaces(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.identity.v2.UserProfile/get_workspaces',
            spaceone_dot_api_dot_identity_dot_v2_dot_user__profile__pb2.UserProfileRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_workspace__pb2.WorkspacesInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

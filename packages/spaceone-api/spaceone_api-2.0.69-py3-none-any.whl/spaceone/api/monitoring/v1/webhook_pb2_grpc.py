# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.monitoring.v1 import webhook_pb2 as spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2


class WebhookStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.create = channel.unary_unary(
                '/spaceone.api.monitoring.v1.Webhook/create',
                request_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.CreateWebhookRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookInfo.FromString,
                )
        self.update = channel.unary_unary(
                '/spaceone.api.monitoring.v1.Webhook/update',
                request_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.UpdateWebhookRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookInfo.FromString,
                )
        self.update_plugin = channel.unary_unary(
                '/spaceone.api.monitoring.v1.Webhook/update_plugin',
                request_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.UpdateWebhookPluginRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookInfo.FromString,
                )
        self.verify_plugin = channel.unary_unary(
                '/spaceone.api.monitoring.v1.Webhook/verify_plugin',
                request_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.enable = channel.unary_unary(
                '/spaceone.api.monitoring.v1.Webhook/enable',
                request_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookInfo.FromString,
                )
        self.disable = channel.unary_unary(
                '/spaceone.api.monitoring.v1.Webhook/disable',
                request_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookInfo.FromString,
                )
        self.delete = channel.unary_unary(
                '/spaceone.api.monitoring.v1.Webhook/delete',
                request_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.get = channel.unary_unary(
                '/spaceone.api.monitoring.v1.Webhook/get',
                request_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookInfo.FromString,
                )
        self.list = channel.unary_unary(
                '/spaceone.api.monitoring.v1.Webhook/list',
                request_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhooksInfo.FromString,
                )
        self.stat = channel.unary_unary(
                '/spaceone.api.monitoring.v1.Webhook/stat',
                request_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookStatQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                )


class WebhookServicer(object):
    """Missing associated documentation comment in .proto file."""

    def create(self, request, context):
        """Creates a new Webhook. A Webhook collects data from an external monitoring system with a webhook URL generated by the resource.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update(self, request, context):
        """Updates a specific Webhook. You can make changes in Webhook settings, including the name and tags.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update_plugin(self, request, context):
        """Updates the plugin of a specific DataSource. You can change the `version` of the plugin and select the `upgrade_mode` among `AUTO`, `MANUAL`, and `NONE`.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def verify_plugin(self, request, context):
        """Verifies a specific plugin for a Webhook.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def enable(self, request, context):
        """Enables a specific Webhook. By enabling a Webhook, you can communicate with an external application.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def disable(self, request, context):
        """Disables a specific Webhook. By disabling a Webhook, you cannot communicate with an external application, as the webhook URL from the Webhook becomes invalid.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete(self, request, context):
        """Deletes a specific Webhook. By deleting a Webhook, you cannot collect data from an external monitoring system, as the `REST URL` is also deleted.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Gets a specific Webhook. Prints detailed information about the Webhook, including the name, the version, and the created datetime.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list(self, request, context):
        """Gets a list of all Webhooks. You can use a query to get a filtered list of Webhooks.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WebhookServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'create': grpc.unary_unary_rpc_method_handler(
                    servicer.create,
                    request_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.CreateWebhookRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookInfo.SerializeToString,
            ),
            'update': grpc.unary_unary_rpc_method_handler(
                    servicer.update,
                    request_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.UpdateWebhookRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookInfo.SerializeToString,
            ),
            'update_plugin': grpc.unary_unary_rpc_method_handler(
                    servicer.update_plugin,
                    request_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.UpdateWebhookPluginRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookInfo.SerializeToString,
            ),
            'verify_plugin': grpc.unary_unary_rpc_method_handler(
                    servicer.verify_plugin,
                    request_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'enable': grpc.unary_unary_rpc_method_handler(
                    servicer.enable,
                    request_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookInfo.SerializeToString,
            ),
            'disable': grpc.unary_unary_rpc_method_handler(
                    servicer.disable,
                    request_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookInfo.SerializeToString,
            ),
            'delete': grpc.unary_unary_rpc_method_handler(
                    servicer.delete,
                    request_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookInfo.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhooksInfo.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookStatQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.monitoring.v1.Webhook', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Webhook(object):
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.monitoring.v1.Webhook/create',
            spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.CreateWebhookRequest.SerializeToString,
            spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.monitoring.v1.Webhook/update',
            spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.UpdateWebhookRequest.SerializeToString,
            spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def update_plugin(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.monitoring.v1.Webhook/update_plugin',
            spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.UpdateWebhookPluginRequest.SerializeToString,
            spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def verify_plugin(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.monitoring.v1.Webhook/verify_plugin',
            spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.monitoring.v1.Webhook/enable',
            spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookRequest.SerializeToString,
            spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.monitoring.v1.Webhook/disable',
            spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookRequest.SerializeToString,
            spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.monitoring.v1.Webhook/delete',
            spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookRequest.SerializeToString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.monitoring.v1.Webhook/get',
            spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookRequest.SerializeToString,
            spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.monitoring.v1.Webhook/list',
            spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookQuery.SerializeToString,
            spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhooksInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.monitoring.v1.Webhook/stat',
            spaceone_dot_api_dot_monitoring_dot_v1_dot_webhook__pb2.WebhookStatQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

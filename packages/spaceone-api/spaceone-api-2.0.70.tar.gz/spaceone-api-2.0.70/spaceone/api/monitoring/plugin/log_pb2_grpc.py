# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from spaceone.api.monitoring.plugin import log_pb2 as spaceone_dot_api_dot_monitoring_dot_plugin_dot_log__pb2


class LogStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.list = channel.unary_stream(
                '/spaceone.api.monitoring.plugin.Log/list',
                request_serializer=spaceone_dot_api_dot_monitoring_dot_plugin_dot_log__pb2.LogRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_monitoring_dot_plugin_dot_log__pb2.LogsDataInfo.FromString,
                )


class LogServicer(object):
    """Missing associated documentation comment in .proto file."""

    def list(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LogServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'list': grpc.unary_stream_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_monitoring_dot_plugin_dot_log__pb2.LogRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_monitoring_dot_plugin_dot_log__pb2.LogsDataInfo.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.monitoring.plugin.Log', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Log(object):
    """Missing associated documentation comment in .proto file."""

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
        return grpc.experimental.unary_stream(request, target, '/spaceone.api.monitoring.plugin.Log/list',
            spaceone_dot_api_dot_monitoring_dot_plugin_dot_log__pb2.LogRequest.SerializeToString,
            spaceone_dot_api_dot_monitoring_dot_plugin_dot_log__pb2.LogsDataInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/monitoring/plugin/data_source.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n0spaceone/api/monitoring/plugin/data_source.proto\x12\x1espaceone.api.monitoring.plugin\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\"7\n\x0bInitRequest\x12(\n\x07options\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\"}\n\x13PluginVerifyRequest\x12(\n\x07options\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\x12,\n\x0bsecret_data\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x0e\n\x06schema\x18\x03 \x01(\t\"7\n\nPluginInfo\x12)\n\x08metadata\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct2\xc8\x01\n\nDataSource\x12\x61\n\x04init\x12+.spaceone.api.monitoring.plugin.InitRequest\x1a*.spaceone.api.monitoring.plugin.PluginInfo\"\x00\x12W\n\x06verify\x12\x33.spaceone.api.monitoring.plugin.PluginVerifyRequest\x1a\x16.google.protobuf.Empty\"\x00\x42\x45ZCgithub.com/cloudforet-io/api/dist/go/spaceone/api/monitoring/pluginb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.monitoring.plugin.data_source_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'ZCgithub.com/cloudforet-io/api/dist/go/spaceone/api/monitoring/plugin'
  _globals['_INITREQUEST']._serialized_start=143
  _globals['_INITREQUEST']._serialized_end=198
  _globals['_PLUGINVERIFYREQUEST']._serialized_start=200
  _globals['_PLUGINVERIFYREQUEST']._serialized_end=325
  _globals['_PLUGININFO']._serialized_start=327
  _globals['_PLUGININFO']._serialized_end=382
  _globals['_DATASOURCE']._serialized_start=385
  _globals['_DATASOURCE']._serialized_end=585
# @@protoc_insertion_point(module_scope)

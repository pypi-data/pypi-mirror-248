# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/statistics/v1/resource.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from spaceone.api.core.v1 import query_pb2 as spaceone_dot_api_dot_core_dot_v1_dot_query__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)spaceone/api/statistics/v1/resource.proto\x12\x1aspaceone.api.statistics.v1\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\"\x8f\x01\n\x12StatAggregateQuery\x12\x15\n\rresource_type\x18\x01 \x01(\t\x12\x34\n\x05query\x18\x02 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12,\n\x0b\x65xtend_data\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\"\x99\x02\n\x11StatAggregateJoin\x12\x15\n\rresource_type\x18\x01 \x01(\t\x12\x34\n\x05query\x18\x02 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12,\n\x0b\x65xtend_data\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x44\n\x04type\x18\x04 \x01(\x0e\x32\x36.spaceone.api.statistics.v1.StatAggregateJoin.JoinType\x12\x0c\n\x04keys\x18\x05 \x03(\t\"5\n\x08JoinType\x12\x08\n\x04LEFT\x10\x00\x12\t\n\x05RIGHT\x10\x01\x12\t\n\x05OUTER\x10\x02\x12\t\n\x05INNER\x10\x03\"\x90\x01\n\x13StatAggregateConcat\x12\x15\n\rresource_type\x18\x01 \x01(\t\x12\x34\n\x05query\x18\x02 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12,\n\x0b\x65xtend_data\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\"!\n\x04Sort\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x65sc\x18\x02 \x01(\x08\"H\n\x14StatAggregateFormula\x12\x0e\n\x04\x65val\x18\x01 \x01(\tH\x00\x12\x0f\n\x05query\x18\x02 \x01(\tH\x00\x42\x0f\n\rformula_alias\"<\n\x13StatAggregateFillNA\x12%\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\"\x9a\x03\n\rStatAggregate\x12?\n\x05query\x18\x01 \x01(\x0b\x32..spaceone.api.statistics.v1.StatAggregateQueryH\x00\x12=\n\x04join\x18\x02 \x01(\x0b\x32-.spaceone.api.statistics.v1.StatAggregateJoinH\x00\x12\x41\n\x06\x63oncat\x18\x03 \x01(\x0b\x32/.spaceone.api.statistics.v1.StatAggregateConcatH\x00\x12*\n\x04sort\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.ListValueH\x00\x12\x43\n\x07\x66ormula\x18\x05 \x01(\x0b\x32\x30.spaceone.api.statistics.v1.StatAggregateFormulaH\x00\x12\x42\n\x07\x66ill_na\x18\x06 \x01(\x0b\x32/.spaceone.api.statistics.v1.StatAggregateFillNAH\x00\x42\x11\n\x0f\x61ggregate_alias\"(\n\x08StatPage\x12\r\n\x05start\x18\x01 \x01(\r\x12\r\n\x05limit\x18\x02 \x01(\r\"\x87\x01\n\x13ResourceStatRequest\x12<\n\taggregate\x18\x01 \x03(\x0b\x32).spaceone.api.statistics.v1.StatAggregate\x12\x32\n\x04page\x18\x02 \x01(\x0b\x32$.spaceone.api.statistics.v1.StatPage2\x85\x01\n\x08Resource\x12y\n\x04stat\x12/.spaceone.api.statistics.v1.ResourceStatRequest\x1a\x17.google.protobuf.Struct\"\'\x82\xd3\xe4\x93\x02!\"\x1c/statistics/v1/resource/stat:\x01*BAZ?github.com/cloudforet-io/api/dist/go/spaceone/api/statistics/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.statistics.v1.resource_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z?github.com/cloudforet-io/api/dist/go/spaceone/api/statistics/v1'
  _globals['_RESOURCE'].methods_by_name['stat']._options = None
  _globals['_RESOURCE'].methods_by_name['stat']._serialized_options = b'\202\323\344\223\002!\"\034/statistics/v1/resource/stat:\001*'
  _globals['_STATAGGREGATEQUERY']._serialized_start=168
  _globals['_STATAGGREGATEQUERY']._serialized_end=311
  _globals['_STATAGGREGATEJOIN']._serialized_start=314
  _globals['_STATAGGREGATEJOIN']._serialized_end=595
  _globals['_STATAGGREGATEJOIN_JOINTYPE']._serialized_start=542
  _globals['_STATAGGREGATEJOIN_JOINTYPE']._serialized_end=595
  _globals['_STATAGGREGATECONCAT']._serialized_start=598
  _globals['_STATAGGREGATECONCAT']._serialized_end=742
  _globals['_SORT']._serialized_start=744
  _globals['_SORT']._serialized_end=777
  _globals['_STATAGGREGATEFORMULA']._serialized_start=779
  _globals['_STATAGGREGATEFORMULA']._serialized_end=851
  _globals['_STATAGGREGATEFILLNA']._serialized_start=853
  _globals['_STATAGGREGATEFILLNA']._serialized_end=913
  _globals['_STATAGGREGATE']._serialized_start=916
  _globals['_STATAGGREGATE']._serialized_end=1326
  _globals['_STATPAGE']._serialized_start=1328
  _globals['_STATPAGE']._serialized_end=1368
  _globals['_RESOURCESTATREQUEST']._serialized_start=1371
  _globals['_RESOURCESTATREQUEST']._serialized_end=1506
  _globals['_RESOURCE']._serialized_start=1509
  _globals['_RESOURCE']._serialized_end=1642
# @@protoc_insertion_point(module_scope)

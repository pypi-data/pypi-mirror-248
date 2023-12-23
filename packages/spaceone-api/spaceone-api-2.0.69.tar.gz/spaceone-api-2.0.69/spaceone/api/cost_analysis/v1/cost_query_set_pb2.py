# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/cost_analysis/v1/cost_query_set.proto
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
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from spaceone.api.core.v1 import query_pb2 as spaceone_dot_api_dot_core_dot_v1_dot_query__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n2spaceone/api/cost_analysis/v1/cost_query_set.proto\x12\x1dspaceone.api.cost_analysis.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\"\x92\x01\n\x19\x43reateCostQuerySetRequest\x12\x16\n\x0e\x64\x61ta_source_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12(\n\x07options\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12%\n\x04tags\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\"\x95\x01\n\x19UpdateCostQuerySetRequest\x12\x19\n\x11\x63ost_query_set_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12(\n\x07options\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12%\n\x04tags\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\"0\n\x13\x43ostQuerySetRequest\x12\x19\n\x11\x63ost_query_set_id\x18\x01 \x01(\t\"e\n\x11\x43ostQuerySetQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x16\n\x0e\x64\x61ta_source_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\"\xf0\x01\n\x10\x43ostQuerySetInfo\x12\x19\n\x11\x63ost_query_set_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12(\n\x07options\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12%\n\x04tags\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x15 \x01(\t\x12\x0f\n\x07user_id\x18\x16 \x01(\t\x12\x16\n\x0e\x64\x61ta_source_id\x18\x17 \x01(\t\x12\x12\n\ncreated_at\x18\x1f \x01(\t\x12\x12\n\nupdated_at\x18  \x01(\t\"j\n\x11\x43ostQuerySetsInfo\x12@\n\x07results\x18\x01 \x03(\x0b\x32/.spaceone.api.cost_analysis.v1.CostQuerySetInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"e\n\x15\x43ostQuerySetStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12\x16\n\x0e\x64\x61ta_source_id\x18\x02 \x01(\t2\xb4\x07\n\x0c\x43ostQuerySet\x12\xa7\x01\n\x06\x63reate\x12\x38.spaceone.api.cost_analysis.v1.CreateCostQuerySetRequest\x1a/.spaceone.api.cost_analysis.v1.CostQuerySetInfo\"2\x82\xd3\xe4\x93\x02,\"\'/cost-analysis/v1/cost-query-set/create:\x01*\x12\xa7\x01\n\x06update\x12\x38.spaceone.api.cost_analysis.v1.UpdateCostQuerySetRequest\x1a/.spaceone.api.cost_analysis.v1.CostQuerySetInfo\"2\x82\xd3\xe4\x93\x02,\"\'/cost-analysis/v1/cost-query-set/update:\x01*\x12\x88\x01\n\x06\x64\x65lete\x12\x32.spaceone.api.cost_analysis.v1.CostQuerySetRequest\x1a\x16.google.protobuf.Empty\"2\x82\xd3\xe4\x93\x02,\"\'/cost-analysis/v1/cost-query-set/delete:\x01*\x12\x9b\x01\n\x03get\x12\x32.spaceone.api.cost_analysis.v1.CostQuerySetRequest\x1a/.spaceone.api.cost_analysis.v1.CostQuerySetInfo\"/\x82\xd3\xe4\x93\x02)\"$/cost-analysis/v1/cost-query-set/get:\x01*\x12\x9c\x01\n\x04list\x12\x30.spaceone.api.cost_analysis.v1.CostQuerySetQuery\x1a\x30.spaceone.api.cost_analysis.v1.CostQuerySetsInfo\"0\x82\xd3\xe4\x93\x02*\"%/cost-analysis/v1/cost-query-set/list:\x01*\x12\x87\x01\n\x04stat\x12\x34.spaceone.api.cost_analysis.v1.CostQuerySetStatQuery\x1a\x17.google.protobuf.Struct\"0\x82\xd3\xe4\x93\x02*\"%/cost-analysis/v1/cost-query-set/stat:\x01*BDZBgithub.com/cloudforet-io/api/dist/go/spaceone/api/cost_analysis/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.cost_analysis.v1.cost_query_set_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'ZBgithub.com/cloudforet-io/api/dist/go/spaceone/api/cost_analysis/v1'
  _globals['_COSTQUERYSET'].methods_by_name['create']._options = None
  _globals['_COSTQUERYSET'].methods_by_name['create']._serialized_options = b'\202\323\344\223\002,\"\'/cost-analysis/v1/cost-query-set/create:\001*'
  _globals['_COSTQUERYSET'].methods_by_name['update']._options = None
  _globals['_COSTQUERYSET'].methods_by_name['update']._serialized_options = b'\202\323\344\223\002,\"\'/cost-analysis/v1/cost-query-set/update:\001*'
  _globals['_COSTQUERYSET'].methods_by_name['delete']._options = None
  _globals['_COSTQUERYSET'].methods_by_name['delete']._serialized_options = b'\202\323\344\223\002,\"\'/cost-analysis/v1/cost-query-set/delete:\001*'
  _globals['_COSTQUERYSET'].methods_by_name['get']._options = None
  _globals['_COSTQUERYSET'].methods_by_name['get']._serialized_options = b'\202\323\344\223\002)\"$/cost-analysis/v1/cost-query-set/get:\001*'
  _globals['_COSTQUERYSET'].methods_by_name['list']._options = None
  _globals['_COSTQUERYSET'].methods_by_name['list']._serialized_options = b'\202\323\344\223\002*\"%/cost-analysis/v1/cost-query-set/list:\001*'
  _globals['_COSTQUERYSET'].methods_by_name['stat']._options = None
  _globals['_COSTQUERYSET'].methods_by_name['stat']._serialized_options = b'\202\323\344\223\002*\"%/cost-analysis/v1/cost-query-set/stat:\001*'
  _globals['_CREATECOSTQUERYSETREQUEST']._serialized_start=209
  _globals['_CREATECOSTQUERYSETREQUEST']._serialized_end=355
  _globals['_UPDATECOSTQUERYSETREQUEST']._serialized_start=358
  _globals['_UPDATECOSTQUERYSETREQUEST']._serialized_end=507
  _globals['_COSTQUERYSETREQUEST']._serialized_start=509
  _globals['_COSTQUERYSETREQUEST']._serialized_end=557
  _globals['_COSTQUERYSETQUERY']._serialized_start=559
  _globals['_COSTQUERYSETQUERY']._serialized_end=660
  _globals['_COSTQUERYSETINFO']._serialized_start=663
  _globals['_COSTQUERYSETINFO']._serialized_end=903
  _globals['_COSTQUERYSETSINFO']._serialized_start=905
  _globals['_COSTQUERYSETSINFO']._serialized_end=1011
  _globals['_COSTQUERYSETSTATQUERY']._serialized_start=1013
  _globals['_COSTQUERYSETSTATQUERY']._serialized_end=1114
  _globals['_COSTQUERYSET']._serialized_start=1117
  _globals['_COSTQUERYSET']._serialized_end=2065
# @@protoc_insertion_point(module_scope)

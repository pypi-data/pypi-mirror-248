# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/identity/v1/api_key.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&spaceone/api/identity/v1/api_key.proto\x12\x18spaceone.api.identity.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\"9\n\x13\x43reateAPIKeyRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"6\n\rAPIKeyRequest\x12\x12\n\napi_key_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"G\n\x10GetAPIKeyRequest\x12\x12\n\napi_key_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\x12\x0c\n\x04only\x18\x03 \x03(\t\"\xf2\x01\n\nAPIKeyInfo\x12\x12\n\napi_key_id\x18\x01 \x01(\t\x12\x0f\n\x07\x61pi_key\x18\x02 \x01(\t\x12\x39\n\x05state\x18\x03 \x01(\x0e\x32*.spaceone.api.identity.v1.APIKeyInfo.State\x12\x0f\n\x07user_id\x18\x04 \x01(\t\x12\x11\n\tdomain_id\x18\x05 \x01(\t\x12\x18\n\x10last_accessed_at\x18\n \x01(\t\x12\x12\n\ncreated_at\x18\x0b \x01(\t\"2\n\x05State\x12\x0e\n\nNONE_STATE\x10\x00\x12\x0b\n\x07\x45NABLED\x10\x01\x12\x0c\n\x08\x44ISABLED\x10\x02\"\xe1\x01\n\x0b\x41PIKeyQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x12\n\napi_key_id\x18\x02 \x01(\t\x12:\n\x05state\x18\x03 \x01(\x0e\x32+.spaceone.api.identity.v1.APIKeyQuery.State\x12\x0f\n\x07user_id\x18\x04 \x01(\t\x12\x11\n\tdomain_id\x18\x05 \x01(\t\"2\n\x05State\x12\x0e\n\nNONE_STATE\x10\x00\x12\x0b\n\x07\x45NABLED\x10\x01\x12\x0c\n\x08\x44ISABLED\x10\x02\"Y\n\x0b\x41PIKeysInfo\x12\x35\n\x07results\x18\x01 \x03(\x0b\x32$.spaceone.api.identity.v1.APIKeyInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"Z\n\x0f\x41PIKeyStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t2\xf4\x06\n\x06\x41PIKey\x12\x85\x01\n\x06\x63reate\x12-.spaceone.api.identity.v1.CreateAPIKeyRequest\x1a$.spaceone.api.identity.v1.APIKeyInfo\"&\x82\xd3\xe4\x93\x02 \"\x1b/identity/v1/api-key/create:\x01*\x12\x7f\n\x06\x65nable\x12\'.spaceone.api.identity.v1.APIKeyRequest\x1a$.spaceone.api.identity.v1.APIKeyInfo\"&\x82\xd3\xe4\x93\x02 \"\x1b/identity/v1/api-key/enable:\x01*\x12\x81\x01\n\x07\x64isable\x12\'.spaceone.api.identity.v1.APIKeyRequest\x1a$.spaceone.api.identity.v1.APIKeyInfo\"\'\x82\xd3\xe4\x93\x02!\"\x1c/identity/v1/api-key/disable:\x01*\x12q\n\x06\x64\x65lete\x12\'.spaceone.api.identity.v1.APIKeyRequest\x1a\x16.google.protobuf.Empty\"&\x82\xd3\xe4\x93\x02 \"\x1b/identity/v1/api-key/delete:\x01*\x12|\n\x03get\x12*.spaceone.api.identity.v1.GetAPIKeyRequest\x1a$.spaceone.api.identity.v1.APIKeyInfo\"#\x82\xd3\xe4\x93\x02\x1d\"\x18/identity/v1/api-key/get:\x01*\x12z\n\x04list\x12%.spaceone.api.identity.v1.APIKeyQuery\x1a%.spaceone.api.identity.v1.APIKeysInfo\"$\x82\xd3\xe4\x93\x02\x1e\"\x19/identity/v1/api-key/list:\x01*\x12p\n\x04stat\x12).spaceone.api.identity.v1.APIKeyStatQuery\x1a\x17.google.protobuf.Struct\"$\x82\xd3\xe4\x93\x02\x1e\"\x19/identity/v1/api-key/stat:\x01*B?Z=github.com/cloudforet-io/api/dist/go/spaceone/api/identity/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.identity.v1.api_key_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z=github.com/cloudforet-io/api/dist/go/spaceone/api/identity/v1'
  _globals['_APIKEY'].methods_by_name['create']._options = None
  _globals['_APIKEY'].methods_by_name['create']._serialized_options = b'\202\323\344\223\002 \"\033/identity/v1/api-key/create:\001*'
  _globals['_APIKEY'].methods_by_name['enable']._options = None
  _globals['_APIKEY'].methods_by_name['enable']._serialized_options = b'\202\323\344\223\002 \"\033/identity/v1/api-key/enable:\001*'
  _globals['_APIKEY'].methods_by_name['disable']._options = None
  _globals['_APIKEY'].methods_by_name['disable']._serialized_options = b'\202\323\344\223\002!\"\034/identity/v1/api-key/disable:\001*'
  _globals['_APIKEY'].methods_by_name['delete']._options = None
  _globals['_APIKEY'].methods_by_name['delete']._serialized_options = b'\202\323\344\223\002 \"\033/identity/v1/api-key/delete:\001*'
  _globals['_APIKEY'].methods_by_name['get']._options = None
  _globals['_APIKEY'].methods_by_name['get']._serialized_options = b'\202\323\344\223\002\035\"\030/identity/v1/api-key/get:\001*'
  _globals['_APIKEY'].methods_by_name['list']._options = None
  _globals['_APIKEY'].methods_by_name['list']._serialized_options = b'\202\323\344\223\002\036\"\031/identity/v1/api-key/list:\001*'
  _globals['_APIKEY'].methods_by_name['stat']._options = None
  _globals['_APIKEY'].methods_by_name['stat']._serialized_options = b'\202\323\344\223\002\036\"\031/identity/v1/api-key/stat:\001*'
  _globals['_CREATEAPIKEYREQUEST']._serialized_start=191
  _globals['_CREATEAPIKEYREQUEST']._serialized_end=248
  _globals['_APIKEYREQUEST']._serialized_start=250
  _globals['_APIKEYREQUEST']._serialized_end=304
  _globals['_GETAPIKEYREQUEST']._serialized_start=306
  _globals['_GETAPIKEYREQUEST']._serialized_end=377
  _globals['_APIKEYINFO']._serialized_start=380
  _globals['_APIKEYINFO']._serialized_end=622
  _globals['_APIKEYINFO_STATE']._serialized_start=572
  _globals['_APIKEYINFO_STATE']._serialized_end=622
  _globals['_APIKEYQUERY']._serialized_start=625
  _globals['_APIKEYQUERY']._serialized_end=850
  _globals['_APIKEYQUERY_STATE']._serialized_start=572
  _globals['_APIKEYQUERY_STATE']._serialized_end=622
  _globals['_APIKEYSINFO']._serialized_start=852
  _globals['_APIKEYSINFO']._serialized_end=941
  _globals['_APIKEYSTATQUERY']._serialized_start=943
  _globals['_APIKEYSTATQUERY']._serialized_end=1033
  _globals['_APIKEY']._serialized_start=1036
  _globals['_APIKEY']._serialized_end=1920
# @@protoc_insertion_point(module_scope)

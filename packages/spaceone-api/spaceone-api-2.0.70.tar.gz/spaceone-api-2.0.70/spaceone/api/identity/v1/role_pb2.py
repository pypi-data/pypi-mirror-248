# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/identity/v1/role.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#spaceone/api/identity/v1/role.proto\x12\x18spaceone.api.identity.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\"\x96\x01\n\nRolePolicy\x12\x44\n\x0bpolicy_type\x18\x01 \x01(\x0e\x32/.spaceone.api.identity.v1.RolePolicy.PolicyType\x12\x11\n\tpolicy_id\x18\x02 \x01(\t\"/\n\nPolicyType\x12\x08\n\x04NONE\x10\x00\x12\x0b\n\x07MANAGED\x10\x01\x12\n\n\x06\x43USTOM\x10\x02\"\x95\x01\n\x0ePagePermission\x12\x0c\n\x04page\x18\x01 \x01(\t\x12G\n\npermission\x18\x02 \x01(\x0e\x32\x33.spaceone.api.identity.v1.PagePermission.Permission\",\n\nPermission\x12\x08\n\x04NONE\x10\x00\x12\x08\n\x04VIEW\x10\x01\x12\n\n\x06MANAGE\x10\x02\"\x8e\x02\n\x11\x43reateRoleRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x35\n\trole_type\x18\x02 \x01(\x0e\x32\".spaceone.api.identity.v1.RoleType\x12\x36\n\x08policies\x18\x03 \x03(\x0b\x32$.spaceone.api.identity.v1.RolePolicy\x12\x42\n\x10page_permissions\x18\x04 \x03(\x0b\x32(.spaceone.api.identity.v1.PagePermission\x12%\n\x04tags\x18\x05 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x06 \x01(\t\"\x8a\x02\n\x11UpdateRoleRequest\x12\x0f\n\x07role_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x36\n\x08policies\x18\x03 \x03(\x0b\x32$.spaceone.api.identity.v1.RolePolicy\x12\x42\n\x10page_permissions\x18\x04 \x03(\x0b\x32(.spaceone.api.identity.v1.PagePermission\x12%\n\x04tags\x18\x05 \x01(\x0b\x32\x17.google.protobuf.Struct\x12 \n\x18release_page_permissions\x18\x06 \x01(\x08\x12\x11\n\tdomain_id\x18\x07 \x01(\t\"1\n\x0bRoleRequest\x12\x0f\n\x07role_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"B\n\x0eGetRoleRequest\x12\x0f\n\x07role_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\x12\x0c\n\x04only\x18\x03 \x03(\t\"\xbe\x02\n\x08RoleInfo\x12\x0f\n\x07role_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x35\n\trole_type\x18\x03 \x01(\x0e\x32\".spaceone.api.identity.v1.RoleType\x12\x36\n\x08policies\x18\x04 \x03(\x0b\x32$.spaceone.api.identity.v1.RolePolicy\x12\x42\n\x10page_permissions\x18\x05 \x03(\x0b\x32(.spaceone.api.identity.v1.PagePermission\x12%\n\x04tags\x18\x06 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x0b \x01(\t\x12\x12\n\ncreated_at\x18\x15 \x01(\t\x12\x12\n\ndeleted_at\x18\x16 \x01(\t\"\xb3\x01\n\tRoleQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x0f\n\x07role_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x35\n\trole_type\x18\x05 \x01(\x0e\x32\".spaceone.api.identity.v1.RoleType\x12\x11\n\tpolicy_id\x18\x06 \x01(\t\x12\x11\n\tdomain_id\x18\x07 \x01(\t\"U\n\tRolesInfo\x12\x33\n\x07results\x18\x01 \x03(\x0b\x32\".spaceone.api.identity.v1.RoleInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"X\n\rRoleStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t*9\n\x08RoleType\x12\x08\n\x04NONE\x10\x00\x12\n\n\x06SYSTEM\x10\x01\x12\n\n\x06\x44OMAIN\x10\x02\x12\x0b\n\x07PROJECT\x10\x03\x32\xcd\x05\n\x04Role\x12~\n\x06\x63reate\x12+.spaceone.api.identity.v1.CreateRoleRequest\x1a\".spaceone.api.identity.v1.RoleInfo\"#\x82\xd3\xe4\x93\x02\x1d\"\x18/identity/v1/role/create:\x01*\x12~\n\x06update\x12+.spaceone.api.identity.v1.UpdateRoleRequest\x1a\".spaceone.api.identity.v1.RoleInfo\"#\x82\xd3\xe4\x93\x02\x1d\"\x18/identity/v1/role/update:\x01*\x12l\n\x06\x64\x65lete\x12%.spaceone.api.identity.v1.RoleRequest\x1a\x16.google.protobuf.Empty\"#\x82\xd3\xe4\x93\x02\x1d\"\x18/identity/v1/role/delete:\x01*\x12u\n\x03get\x12(.spaceone.api.identity.v1.GetRoleRequest\x1a\".spaceone.api.identity.v1.RoleInfo\" \x82\xd3\xe4\x93\x02\x1a\"\x15/identity/v1/role/get:\x01*\x12s\n\x04list\x12#.spaceone.api.identity.v1.RoleQuery\x1a#.spaceone.api.identity.v1.RolesInfo\"!\x82\xd3\xe4\x93\x02\x1b\"\x16/identity/v1/role/list:\x01*\x12k\n\x04stat\x12\'.spaceone.api.identity.v1.RoleStatQuery\x1a\x17.google.protobuf.Struct\"!\x82\xd3\xe4\x93\x02\x1b\"\x16/identity/v1/role/stat:\x01*B?Z=github.com/cloudforet-io/api/dist/go/spaceone/api/identity/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.identity.v1.role_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z=github.com/cloudforet-io/api/dist/go/spaceone/api/identity/v1'
  _globals['_ROLE'].methods_by_name['create']._options = None
  _globals['_ROLE'].methods_by_name['create']._serialized_options = b'\202\323\344\223\002\035\"\030/identity/v1/role/create:\001*'
  _globals['_ROLE'].methods_by_name['update']._options = None
  _globals['_ROLE'].methods_by_name['update']._serialized_options = b'\202\323\344\223\002\035\"\030/identity/v1/role/update:\001*'
  _globals['_ROLE'].methods_by_name['delete']._options = None
  _globals['_ROLE'].methods_by_name['delete']._serialized_options = b'\202\323\344\223\002\035\"\030/identity/v1/role/delete:\001*'
  _globals['_ROLE'].methods_by_name['get']._options = None
  _globals['_ROLE'].methods_by_name['get']._serialized_options = b'\202\323\344\223\002\032\"\025/identity/v1/role/get:\001*'
  _globals['_ROLE'].methods_by_name['list']._options = None
  _globals['_ROLE'].methods_by_name['list']._serialized_options = b'\202\323\344\223\002\033\"\026/identity/v1/role/list:\001*'
  _globals['_ROLE'].methods_by_name['stat']._options = None
  _globals['_ROLE'].methods_by_name['stat']._serialized_options = b'\202\323\344\223\002\033\"\026/identity/v1/role/stat:\001*'
  _globals['_ROLETYPE']._serialized_start=1834
  _globals['_ROLETYPE']._serialized_end=1891
  _globals['_ROLEPOLICY']._serialized_start=189
  _globals['_ROLEPOLICY']._serialized_end=339
  _globals['_ROLEPOLICY_POLICYTYPE']._serialized_start=292
  _globals['_ROLEPOLICY_POLICYTYPE']._serialized_end=339
  _globals['_PAGEPERMISSION']._serialized_start=342
  _globals['_PAGEPERMISSION']._serialized_end=491
  _globals['_PAGEPERMISSION_PERMISSION']._serialized_start=447
  _globals['_PAGEPERMISSION_PERMISSION']._serialized_end=491
  _globals['_CREATEROLEREQUEST']._serialized_start=494
  _globals['_CREATEROLEREQUEST']._serialized_end=764
  _globals['_UPDATEROLEREQUEST']._serialized_start=767
  _globals['_UPDATEROLEREQUEST']._serialized_end=1033
  _globals['_ROLEREQUEST']._serialized_start=1035
  _globals['_ROLEREQUEST']._serialized_end=1084
  _globals['_GETROLEREQUEST']._serialized_start=1086
  _globals['_GETROLEREQUEST']._serialized_end=1152
  _globals['_ROLEINFO']._serialized_start=1155
  _globals['_ROLEINFO']._serialized_end=1473
  _globals['_ROLEQUERY']._serialized_start=1476
  _globals['_ROLEQUERY']._serialized_end=1655
  _globals['_ROLESINFO']._serialized_start=1657
  _globals['_ROLESINFO']._serialized_end=1742
  _globals['_ROLESTATQUERY']._serialized_start=1744
  _globals['_ROLESTATQUERY']._serialized_end=1832
  _globals['_ROLE']._serialized_start=1894
  _globals['_ROLE']._serialized_end=2611
# @@protoc_insertion_point(module_scope)

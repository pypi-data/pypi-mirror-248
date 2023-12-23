# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/identity/v1/project_group.proto
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
from spaceone.api.identity.v1 import role_pb2 as spaceone_dot_api_dot_identity_dot_v1_dot_role__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,spaceone/api/identity/v1/project_group.proto\x12\x18spaceone.api.identity.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\x1a#spaceone/api/identity/v1/role.proto\"\x84\x01\n\x19\x43reateProjectGroupRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x1f\n\x17parent_project_group_id\x18\x02 \x01(\t\x12%\n\x04tags\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x04 \x01(\t\"\xc4\x01\n\x19UpdateProjectGroupRequest\x12\x18\n\x10project_group_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x1f\n\x17parent_project_group_id\x18\x03 \x01(\t\x12$\n\x1crelease_parent_project_group\x18\x04 \x01(\x08\x12%\n\x04tags\x18\x05 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x06 \x01(\t\"B\n\x13ProjectGroupRequest\x12\x18\n\x10project_group_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"S\n\x16GetProjectGroupRequest\x12\x18\n\x10project_group_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\x12\x0c\n\x04only\x18\x03 \x03(\t\"\xb2\x01\n\x11ProjectGroupQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x18\n\x10project_group_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x1f\n\x17parent_project_group_id\x18\x04 \x01(\t\x12\x15\n\rauthor_within\x18\x05 \x01(\x08\x12\x11\n\tdomain_id\x18\x06 \x01(\t\"\xeb\x01\n\x10ProjectGroupInfo\x12\x18\n\x10project_group_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12%\n\x04tags\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12M\n\x19parent_project_group_info\x18\x04 \x01(\x0b\x32*.spaceone.api.identity.v1.ProjectGroupInfo\x12\x11\n\tdomain_id\x18\x0b \x01(\t\x12\x12\n\ncreated_by\x18\x15 \x01(\t\x12\x12\n\ncreated_at\x18\x16 \x01(\t\"e\n\x11ProjectGroupsInfo\x12;\n\x07results\x18\x01 \x03(\x0b\x32*.spaceone.api.identity.v1.ProjectGroupInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"\xda\x01\n\x1c\x41\x64\x64ProjectGroupMemberRequest\x12\x18\n\x10project_group_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\x0f\n\x07role_id\x18\x03 \x01(\t\x12*\n\x06labels\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12%\n\x04tags\x18\x05 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x06 \x01(\t\x12\x18\n\x10is_external_user\x18\x07 \x01(\x08\"\xb2\x01\n\x1fModifyProjectGroupMemberRequest\x12\x18\n\x10project_group_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12*\n\x06labels\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12%\n\x04tags\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x05 \x01(\t\"_\n\x1fRemoveProjectGroupMemberRequest\x12\x18\n\x10project_group_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\x11\n\tdomain_id\x18\x03 \x01(\t\"\xb3\x01\n\x17ProjectGroupMemberQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x18\n\x10project_group_id\x18\x02 \x01(\t\x12\x0f\n\x07user_id\x18\x03 \x01(\t\x12\x0f\n\x07role_id\x18\x04 \x01(\t\x12\x1d\n\x15include_parent_member\x18\x05 \x01(\x08\x12\x11\n\tdomain_id\x18\x06 \x01(\t\"\xdb\x02\n\x1bProjectGroupRoleBindingInfo\x12\x17\n\x0frole_binding_id\x18\x01 \x01(\t\x12\x15\n\rresource_type\x18\x02 \x01(\t\x12\x13\n\x0bresource_id\x18\x03 \x01(\t\x12\x35\n\trole_info\x18\x04 \x01(\x0b\x32\".spaceone.api.identity.v1.RoleInfo\x12\x46\n\x12project_group_info\x18\x05 \x01(\x0b\x32*.spaceone.api.identity.v1.ProjectGroupInfo\x12*\n\x06labels\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.ListValue\x12%\n\x04tags\x18\x08 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x0b \x01(\t\x12\x12\n\ncreated_at\x18\x15 \x01(\t\"{\n\x1cProjectGroupRoleBindingsInfo\x12\x46\n\x07results\x18\x01 \x03(\x0b\x32\x35.spaceone.api.identity.v1.ProjectGroupRoleBindingInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"\x86\x01\n\x18ProjectGroupProjectQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x18\n\x10project_group_id\x18\x02 \x01(\t\x12\x11\n\trecursive\x18\x03 \x01(\x08\x12\x11\n\tdomain_id\x18\x04 \x01(\t\"\xe5\x01\n\x17ProjectGroupProjectInfo\x12\x12\n\nproject_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12%\n\x04tags\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x46\n\x12project_group_info\x18\x04 \x01(\x0b\x32*.spaceone.api.identity.v1.ProjectGroupInfo\x12\x11\n\tdomain_id\x18\x0b \x01(\t\x12\x12\n\ncreated_by\x18\x15 \x01(\t\x12\x12\n\ncreated_at\x18\x16 \x01(\t\"s\n\x18ProjectGroupProjectsInfo\x12\x42\n\x07results\x18\x01 \x03(\x0b\x32\x31.spaceone.api.identity.v1.ProjectGroupProjectInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"`\n\x15ProjectGroupStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t2\xc1\r\n\x0cProjectGroup\x12\x97\x01\n\x06\x63reate\x12\x33.spaceone.api.identity.v1.CreateProjectGroupRequest\x1a*.spaceone.api.identity.v1.ProjectGroupInfo\",\x82\xd3\xe4\x93\x02&\"!/identity/v1/project-group/create:\x01*\x12\x97\x01\n\x06update\x12\x33.spaceone.api.identity.v1.UpdateProjectGroupRequest\x1a*.spaceone.api.identity.v1.ProjectGroupInfo\",\x82\xd3\xe4\x93\x02&\"!/identity/v1/project-group/update:\x01*\x12}\n\x06\x64\x65lete\x12-.spaceone.api.identity.v1.ProjectGroupRequest\x1a\x16.google.protobuf.Empty\",\x82\xd3\xe4\x93\x02&\"!/identity/v1/project-group/delete:\x01*\x12\x8e\x01\n\x03get\x12\x30.spaceone.api.identity.v1.GetProjectGroupRequest\x1a*.spaceone.api.identity.v1.ProjectGroupInfo\")\x82\xd3\xe4\x93\x02#\"\x1e/identity/v1/project-group/get:\x01*\x12\x8c\x01\n\x04list\x12+.spaceone.api.identity.v1.ProjectGroupQuery\x1a+.spaceone.api.identity.v1.ProjectGroupsInfo\"*\x82\xd3\xe4\x93\x02$\"\x1f/identity/v1/project-group/list:\x01*\x12|\n\x04stat\x12/.spaceone.api.identity.v1.ProjectGroupStatQuery\x1a\x17.google.protobuf.Struct\"*\x82\xd3\xe4\x93\x02$\"\x1f/identity/v1/project-group/stat:\x01*\x12\xad\x01\n\nadd_member\x12\x36.spaceone.api.identity.v1.AddProjectGroupMemberRequest\x1a\x35.spaceone.api.identity.v1.ProjectGroupRoleBindingInfo\"0\x82\xd3\xe4\x93\x02*\"%/identity/v1/project-group/add-member:\x01*\x12\xb6\x01\n\rmodify_member\x12\x39.spaceone.api.identity.v1.ModifyProjectGroupMemberRequest\x1a\x35.spaceone.api.identity.v1.ProjectGroupRoleBindingInfo\"3\x82\xd3\xe4\x93\x02-\"(/identity/v1/project-group/modify-member:\x01*\x12\x97\x01\n\rremove_member\x12\x39.spaceone.api.identity.v1.RemoveProjectGroupMemberRequest\x1a\x16.google.protobuf.Empty\"3\x82\xd3\xe4\x93\x02-\"(/identity/v1/project-group/remove-member:\x01*\x12\xad\x01\n\x0clist_members\x12\x31.spaceone.api.identity.v1.ProjectGroupMemberQuery\x1a\x36.spaceone.api.identity.v1.ProjectGroupRoleBindingsInfo\"2\x82\xd3\xe4\x93\x02,\"\'/identity/v1/project-group/list-members:\x01*\x12\xac\x01\n\rlist_projects\x12\x32.spaceone.api.identity.v1.ProjectGroupProjectQuery\x1a\x32.spaceone.api.identity.v1.ProjectGroupProjectsInfo\"3\x82\xd3\xe4\x93\x02-\"(/identity/v1/project-group/list-projects:\x01*B?Z=github.com/cloudforet-io/api/dist/go/spaceone/api/identity/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spaceone.api.identity.v1.project_group_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z=github.com/cloudforet-io/api/dist/go/spaceone/api/identity/v1'
  _globals['_PROJECTGROUP'].methods_by_name['create']._options = None
  _globals['_PROJECTGROUP'].methods_by_name['create']._serialized_options = b'\202\323\344\223\002&\"!/identity/v1/project-group/create:\001*'
  _globals['_PROJECTGROUP'].methods_by_name['update']._options = None
  _globals['_PROJECTGROUP'].methods_by_name['update']._serialized_options = b'\202\323\344\223\002&\"!/identity/v1/project-group/update:\001*'
  _globals['_PROJECTGROUP'].methods_by_name['delete']._options = None
  _globals['_PROJECTGROUP'].methods_by_name['delete']._serialized_options = b'\202\323\344\223\002&\"!/identity/v1/project-group/delete:\001*'
  _globals['_PROJECTGROUP'].methods_by_name['get']._options = None
  _globals['_PROJECTGROUP'].methods_by_name['get']._serialized_options = b'\202\323\344\223\002#\"\036/identity/v1/project-group/get:\001*'
  _globals['_PROJECTGROUP'].methods_by_name['list']._options = None
  _globals['_PROJECTGROUP'].methods_by_name['list']._serialized_options = b'\202\323\344\223\002$\"\037/identity/v1/project-group/list:\001*'
  _globals['_PROJECTGROUP'].methods_by_name['stat']._options = None
  _globals['_PROJECTGROUP'].methods_by_name['stat']._serialized_options = b'\202\323\344\223\002$\"\037/identity/v1/project-group/stat:\001*'
  _globals['_PROJECTGROUP'].methods_by_name['add_member']._options = None
  _globals['_PROJECTGROUP'].methods_by_name['add_member']._serialized_options = b'\202\323\344\223\002*\"%/identity/v1/project-group/add-member:\001*'
  _globals['_PROJECTGROUP'].methods_by_name['modify_member']._options = None
  _globals['_PROJECTGROUP'].methods_by_name['modify_member']._serialized_options = b'\202\323\344\223\002-\"(/identity/v1/project-group/modify-member:\001*'
  _globals['_PROJECTGROUP'].methods_by_name['remove_member']._options = None
  _globals['_PROJECTGROUP'].methods_by_name['remove_member']._serialized_options = b'\202\323\344\223\002-\"(/identity/v1/project-group/remove-member:\001*'
  _globals['_PROJECTGROUP'].methods_by_name['list_members']._options = None
  _globals['_PROJECTGROUP'].methods_by_name['list_members']._serialized_options = b'\202\323\344\223\002,\"\'/identity/v1/project-group/list-members:\001*'
  _globals['_PROJECTGROUP'].methods_by_name['list_projects']._options = None
  _globals['_PROJECTGROUP'].methods_by_name['list_projects']._serialized_options = b'\202\323\344\223\002-\"(/identity/v1/project-group/list-projects:\001*'
  _globals['_CREATEPROJECTGROUPREQUEST']._serialized_start=235
  _globals['_CREATEPROJECTGROUPREQUEST']._serialized_end=367
  _globals['_UPDATEPROJECTGROUPREQUEST']._serialized_start=370
  _globals['_UPDATEPROJECTGROUPREQUEST']._serialized_end=566
  _globals['_PROJECTGROUPREQUEST']._serialized_start=568
  _globals['_PROJECTGROUPREQUEST']._serialized_end=634
  _globals['_GETPROJECTGROUPREQUEST']._serialized_start=636
  _globals['_GETPROJECTGROUPREQUEST']._serialized_end=719
  _globals['_PROJECTGROUPQUERY']._serialized_start=722
  _globals['_PROJECTGROUPQUERY']._serialized_end=900
  _globals['_PROJECTGROUPINFO']._serialized_start=903
  _globals['_PROJECTGROUPINFO']._serialized_end=1138
  _globals['_PROJECTGROUPSINFO']._serialized_start=1140
  _globals['_PROJECTGROUPSINFO']._serialized_end=1241
  _globals['_ADDPROJECTGROUPMEMBERREQUEST']._serialized_start=1244
  _globals['_ADDPROJECTGROUPMEMBERREQUEST']._serialized_end=1462
  _globals['_MODIFYPROJECTGROUPMEMBERREQUEST']._serialized_start=1465
  _globals['_MODIFYPROJECTGROUPMEMBERREQUEST']._serialized_end=1643
  _globals['_REMOVEPROJECTGROUPMEMBERREQUEST']._serialized_start=1645
  _globals['_REMOVEPROJECTGROUPMEMBERREQUEST']._serialized_end=1740
  _globals['_PROJECTGROUPMEMBERQUERY']._serialized_start=1743
  _globals['_PROJECTGROUPMEMBERQUERY']._serialized_end=1922
  _globals['_PROJECTGROUPROLEBINDINGINFO']._serialized_start=1925
  _globals['_PROJECTGROUPROLEBINDINGINFO']._serialized_end=2272
  _globals['_PROJECTGROUPROLEBINDINGSINFO']._serialized_start=2274
  _globals['_PROJECTGROUPROLEBINDINGSINFO']._serialized_end=2397
  _globals['_PROJECTGROUPPROJECTQUERY']._serialized_start=2400
  _globals['_PROJECTGROUPPROJECTQUERY']._serialized_end=2534
  _globals['_PROJECTGROUPPROJECTINFO']._serialized_start=2537
  _globals['_PROJECTGROUPPROJECTINFO']._serialized_end=2766
  _globals['_PROJECTGROUPPROJECTSINFO']._serialized_start=2768
  _globals['_PROJECTGROUPPROJECTSINFO']._serialized_end=2883
  _globals['_PROJECTGROUPSTATQUERY']._serialized_start=2885
  _globals['_PROJECTGROUPSTATQUERY']._serialized_end=2981
  _globals['_PROJECTGROUP']._serialized_start=2984
  _globals['_PROJECTGROUP']._serialized_end=4713
# @@protoc_insertion_point(module_scope)

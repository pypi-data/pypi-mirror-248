import sys
import typing
import bpy_types

GenericType = typing.TypeVar("GenericType")


class NODE_OT_collapse_hide_unused_toggle(bpy_types.Operator):
    bl_idname: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def as_keywords(self, ignore):
        ''' 

        '''
        ...

    def as_pointer(self):
        ''' 

        '''
        ...

    def bl_rna_get_subclass(self):
        ''' 

        '''
        ...

    def bl_rna_get_subclass_py(self):
        ''' 

        '''
        ...

    def driver_add(self):
        ''' 

        '''
        ...

    def driver_remove(self):
        ''' 

        '''
        ...

    def execute(self, context):
        ''' 

        '''
        ...

    def get(self):
        ''' 

        '''
        ...

    def id_properties_clear(self):
        ''' 

        '''
        ...

    def id_properties_ensure(self):
        ''' 

        '''
        ...

    def id_properties_ui(self):
        ''' 

        '''
        ...

    def is_property_hidden(self):
        ''' 

        '''
        ...

    def is_property_overridable_library(self):
        ''' 

        '''
        ...

    def is_property_readonly(self):
        ''' 

        '''
        ...

    def is_property_set(self):
        ''' 

        '''
        ...

    def items(self):
        ''' 

        '''
        ...

    def keyframe_delete(self):
        ''' 

        '''
        ...

    def keyframe_insert(self):
        ''' 

        '''
        ...

    def keys(self):
        ''' 

        '''
        ...

    def path_from_id(self):
        ''' 

        '''
        ...

    def path_resolve(self):
        ''' 

        '''
        ...

    def poll(self, context):
        ''' 

        '''
        ...

    def poll_message_set(self):
        ''' 

        '''
        ...

    def pop(self):
        ''' 

        '''
        ...

    def property_overridable_library_set(self):
        ''' 

        '''
        ...

    def property_unset(self):
        ''' 

        '''
        ...

    def type_recast(self):
        ''' 

        '''
        ...

    def values(self):
        ''' 

        '''
        ...


class NODE_OT_tree_path_parent(bpy_types.Operator):
    bl_idname: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def as_keywords(self, ignore):
        ''' 

        '''
        ...

    def as_pointer(self):
        ''' 

        '''
        ...

    def bl_rna_get_subclass(self):
        ''' 

        '''
        ...

    def bl_rna_get_subclass_py(self):
        ''' 

        '''
        ...

    def driver_add(self):
        ''' 

        '''
        ...

    def driver_remove(self):
        ''' 

        '''
        ...

    def execute(self, context):
        ''' 

        '''
        ...

    def get(self):
        ''' 

        '''
        ...

    def id_properties_clear(self):
        ''' 

        '''
        ...

    def id_properties_ensure(self):
        ''' 

        '''
        ...

    def id_properties_ui(self):
        ''' 

        '''
        ...

    def is_property_hidden(self):
        ''' 

        '''
        ...

    def is_property_overridable_library(self):
        ''' 

        '''
        ...

    def is_property_readonly(self):
        ''' 

        '''
        ...

    def is_property_set(self):
        ''' 

        '''
        ...

    def items(self):
        ''' 

        '''
        ...

    def keyframe_delete(self):
        ''' 

        '''
        ...

    def keyframe_insert(self):
        ''' 

        '''
        ...

    def keys(self):
        ''' 

        '''
        ...

    def path_from_id(self):
        ''' 

        '''
        ...

    def path_resolve(self):
        ''' 

        '''
        ...

    def poll(self, context):
        ''' 

        '''
        ...

    def poll_message_set(self):
        ''' 

        '''
        ...

    def pop(self):
        ''' 

        '''
        ...

    def property_overridable_library_set(self):
        ''' 

        '''
        ...

    def property_unset(self):
        ''' 

        '''
        ...

    def type_recast(self):
        ''' 

        '''
        ...

    def values(self):
        ''' 

        '''
        ...


class NodeAddOperator:
    def create_node(self, context, node_type):
        ''' 

        '''
        ...

    def deselect_nodes(self, context):
        ''' 

        '''
        ...

    def invoke(self, context, event):
        ''' 

        '''
        ...

    def poll(self, context):
        ''' 

        '''
        ...

    def store_mouse_cursor(self, context, event):
        ''' 

        '''
        ...


class NodeInterfaceOperator:
    def poll(self, context):
        ''' 

        '''
        ...


class NodeSetting(bpy_types.PropertyGroup):
    bl_rna: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def as_pointer(self):
        ''' 

        '''
        ...

    def bl_rna_get_subclass(self):
        ''' 

        '''
        ...

    def bl_rna_get_subclass_py(self):
        ''' 

        '''
        ...

    def driver_add(self):
        ''' 

        '''
        ...

    def driver_remove(self):
        ''' 

        '''
        ...

    def get(self):
        ''' 

        '''
        ...

    def id_properties_clear(self):
        ''' 

        '''
        ...

    def id_properties_ensure(self):
        ''' 

        '''
        ...

    def id_properties_ui(self):
        ''' 

        '''
        ...

    def is_property_hidden(self):
        ''' 

        '''
        ...

    def is_property_overridable_library(self):
        ''' 

        '''
        ...

    def is_property_readonly(self):
        ''' 

        '''
        ...

    def is_property_set(self):
        ''' 

        '''
        ...

    def items(self):
        ''' 

        '''
        ...

    def keyframe_delete(self):
        ''' 

        '''
        ...

    def keyframe_insert(self):
        ''' 

        '''
        ...

    def keys(self):
        ''' 

        '''
        ...

    def path_from_id(self):
        ''' 

        '''
        ...

    def path_resolve(self):
        ''' 

        '''
        ...

    def pop(self):
        ''' 

        '''
        ...

    def property_overridable_library_set(self):
        ''' 

        '''
        ...

    def property_unset(self):
        ''' 

        '''
        ...

    def type_recast(self):
        ''' 

        '''
        ...

    def values(self):
        ''' 

        '''
        ...


class NODE_OT_add_node(NodeAddOperator, bpy_types.Operator):
    bl_idname: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def as_keywords(self, ignore):
        ''' 

        '''
        ...

    def as_pointer(self):
        ''' 

        '''
        ...

    def bl_rna_get_subclass(self):
        ''' 

        '''
        ...

    def bl_rna_get_subclass_py(self):
        ''' 

        '''
        ...

    def create_node(self, context, node_type):
        ''' 

        '''
        ...

    def description(self, _context, properties):
        ''' 

        '''
        ...

    def deselect_nodes(self, context):
        ''' 

        '''
        ...

    def driver_add(self):
        ''' 

        '''
        ...

    def driver_remove(self):
        ''' 

        '''
        ...

    def execute(self, context):
        ''' 

        '''
        ...

    def get(self):
        ''' 

        '''
        ...

    def id_properties_clear(self):
        ''' 

        '''
        ...

    def id_properties_ensure(self):
        ''' 

        '''
        ...

    def id_properties_ui(self):
        ''' 

        '''
        ...

    def invoke(self, context, event):
        ''' 

        '''
        ...

    def is_property_hidden(self):
        ''' 

        '''
        ...

    def is_property_overridable_library(self):
        ''' 

        '''
        ...

    def is_property_readonly(self):
        ''' 

        '''
        ...

    def is_property_set(self):
        ''' 

        '''
        ...

    def items(self):
        ''' 

        '''
        ...

    def keyframe_delete(self):
        ''' 

        '''
        ...

    def keyframe_insert(self):
        ''' 

        '''
        ...

    def keys(self):
        ''' 

        '''
        ...

    def path_from_id(self):
        ''' 

        '''
        ...

    def path_resolve(self):
        ''' 

        '''
        ...

    def poll(self, context):
        ''' 

        '''
        ...

    def poll_message_set(self):
        ''' 

        '''
        ...

    def pop(self):
        ''' 

        '''
        ...

    def property_overridable_library_set(self):
        ''' 

        '''
        ...

    def property_unset(self):
        ''' 

        '''
        ...

    def store_mouse_cursor(self, context, event):
        ''' 

        '''
        ...

    def type_recast(self):
        ''' 

        '''
        ...

    def values(self):
        ''' 

        '''
        ...


class NodeAddZoneOperator(NodeAddOperator):
    def create_node(self, context, node_type):
        ''' 

        '''
        ...

    def deselect_nodes(self, context):
        ''' 

        '''
        ...

    def execute(self, context):
        ''' 

        '''
        ...

    def invoke(self, context, event):
        ''' 

        '''
        ...

    def poll(self, context):
        ''' 

        '''
        ...

    def store_mouse_cursor(self, context, event):
        ''' 

        '''
        ...


class NODE_OT_interface_item_duplicate(NodeInterfaceOperator,
                                       bpy_types.Operator):
    bl_idname: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def as_keywords(self, ignore):
        ''' 

        '''
        ...

    def as_pointer(self):
        ''' 

        '''
        ...

    def bl_rna_get_subclass(self):
        ''' 

        '''
        ...

    def bl_rna_get_subclass_py(self):
        ''' 

        '''
        ...

    def driver_add(self):
        ''' 

        '''
        ...

    def driver_remove(self):
        ''' 

        '''
        ...

    def execute(self, context):
        ''' 

        '''
        ...

    def get(self):
        ''' 

        '''
        ...

    def id_properties_clear(self):
        ''' 

        '''
        ...

    def id_properties_ensure(self):
        ''' 

        '''
        ...

    def id_properties_ui(self):
        ''' 

        '''
        ...

    def is_property_hidden(self):
        ''' 

        '''
        ...

    def is_property_overridable_library(self):
        ''' 

        '''
        ...

    def is_property_readonly(self):
        ''' 

        '''
        ...

    def is_property_set(self):
        ''' 

        '''
        ...

    def items(self):
        ''' 

        '''
        ...

    def keyframe_delete(self):
        ''' 

        '''
        ...

    def keyframe_insert(self):
        ''' 

        '''
        ...

    def keys(self):
        ''' 

        '''
        ...

    def path_from_id(self):
        ''' 

        '''
        ...

    def path_resolve(self):
        ''' 

        '''
        ...

    def poll(self, context):
        ''' 

        '''
        ...

    def poll_message_set(self):
        ''' 

        '''
        ...

    def pop(self):
        ''' 

        '''
        ...

    def property_overridable_library_set(self):
        ''' 

        '''
        ...

    def property_unset(self):
        ''' 

        '''
        ...

    def type_recast(self):
        ''' 

        '''
        ...

    def values(self):
        ''' 

        '''
        ...


class NODE_OT_interface_item_new(NodeInterfaceOperator, bpy_types.Operator):
    bl_idname: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def as_keywords(self, ignore):
        ''' 

        '''
        ...

    def as_pointer(self):
        ''' 

        '''
        ...

    def bl_rna_get_subclass(self):
        ''' 

        '''
        ...

    def bl_rna_get_subclass_py(self):
        ''' 

        '''
        ...

    def driver_add(self):
        ''' 

        '''
        ...

    def driver_remove(self):
        ''' 

        '''
        ...

    def execute(self, context):
        ''' 

        '''
        ...

    def find_valid_socket_type(self, tree):
        ''' 

        '''
        ...

    def get(self):
        ''' 

        '''
        ...

    def id_properties_clear(self):
        ''' 

        '''
        ...

    def id_properties_ensure(self):
        ''' 

        '''
        ...

    def id_properties_ui(self):
        ''' 

        '''
        ...

    def is_property_hidden(self):
        ''' 

        '''
        ...

    def is_property_overridable_library(self):
        ''' 

        '''
        ...

    def is_property_readonly(self):
        ''' 

        '''
        ...

    def is_property_set(self):
        ''' 

        '''
        ...

    def items(self):
        ''' 

        '''
        ...

    def keyframe_delete(self):
        ''' 

        '''
        ...

    def keyframe_insert(self):
        ''' 

        '''
        ...

    def keys(self):
        ''' 

        '''
        ...

    def path_from_id(self):
        ''' 

        '''
        ...

    def path_resolve(self):
        ''' 

        '''
        ...

    def poll(self, context):
        ''' 

        '''
        ...

    def poll_message_set(self):
        ''' 

        '''
        ...

    def pop(self):
        ''' 

        '''
        ...

    def property_overridable_library_set(self):
        ''' 

        '''
        ...

    def property_unset(self):
        ''' 

        '''
        ...

    def type_recast(self):
        ''' 

        '''
        ...

    def values(self):
        ''' 

        '''
        ...


class NODE_OT_interface_item_remove(NodeInterfaceOperator, bpy_types.Operator):
    bl_idname: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def as_keywords(self, ignore):
        ''' 

        '''
        ...

    def as_pointer(self):
        ''' 

        '''
        ...

    def bl_rna_get_subclass(self):
        ''' 

        '''
        ...

    def bl_rna_get_subclass_py(self):
        ''' 

        '''
        ...

    def driver_add(self):
        ''' 

        '''
        ...

    def driver_remove(self):
        ''' 

        '''
        ...

    def execute(self, context):
        ''' 

        '''
        ...

    def get(self):
        ''' 

        '''
        ...

    def id_properties_clear(self):
        ''' 

        '''
        ...

    def id_properties_ensure(self):
        ''' 

        '''
        ...

    def id_properties_ui(self):
        ''' 

        '''
        ...

    def is_property_hidden(self):
        ''' 

        '''
        ...

    def is_property_overridable_library(self):
        ''' 

        '''
        ...

    def is_property_readonly(self):
        ''' 

        '''
        ...

    def is_property_set(self):
        ''' 

        '''
        ...

    def items(self):
        ''' 

        '''
        ...

    def keyframe_delete(self):
        ''' 

        '''
        ...

    def keyframe_insert(self):
        ''' 

        '''
        ...

    def keys(self):
        ''' 

        '''
        ...

    def path_from_id(self):
        ''' 

        '''
        ...

    def path_resolve(self):
        ''' 

        '''
        ...

    def poll(self, context):
        ''' 

        '''
        ...

    def poll_message_set(self):
        ''' 

        '''
        ...

    def pop(self):
        ''' 

        '''
        ...

    def property_overridable_library_set(self):
        ''' 

        '''
        ...

    def property_unset(self):
        ''' 

        '''
        ...

    def type_recast(self):
        ''' 

        '''
        ...

    def values(self):
        ''' 

        '''
        ...


class NODE_OT_add_repeat_zone(NodeAddZoneOperator, NodeAddOperator,
                              bpy_types.Operator):
    bl_idname: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    input_node_type: typing.Any
    ''' '''

    output_node_type: typing.Any
    ''' '''

    def as_keywords(self, ignore):
        ''' 

        '''
        ...

    def as_pointer(self):
        ''' 

        '''
        ...

    def bl_rna_get_subclass(self):
        ''' 

        '''
        ...

    def bl_rna_get_subclass_py(self):
        ''' 

        '''
        ...

    def create_node(self, context, node_type):
        ''' 

        '''
        ...

    def deselect_nodes(self, context):
        ''' 

        '''
        ...

    def driver_add(self):
        ''' 

        '''
        ...

    def driver_remove(self):
        ''' 

        '''
        ...

    def execute(self, context):
        ''' 

        '''
        ...

    def get(self):
        ''' 

        '''
        ...

    def id_properties_clear(self):
        ''' 

        '''
        ...

    def id_properties_ensure(self):
        ''' 

        '''
        ...

    def id_properties_ui(self):
        ''' 

        '''
        ...

    def invoke(self, context, event):
        ''' 

        '''
        ...

    def is_property_hidden(self):
        ''' 

        '''
        ...

    def is_property_overridable_library(self):
        ''' 

        '''
        ...

    def is_property_readonly(self):
        ''' 

        '''
        ...

    def is_property_set(self):
        ''' 

        '''
        ...

    def items(self):
        ''' 

        '''
        ...

    def keyframe_delete(self):
        ''' 

        '''
        ...

    def keyframe_insert(self):
        ''' 

        '''
        ...

    def keys(self):
        ''' 

        '''
        ...

    def path_from_id(self):
        ''' 

        '''
        ...

    def path_resolve(self):
        ''' 

        '''
        ...

    def poll(self, context):
        ''' 

        '''
        ...

    def poll_message_set(self):
        ''' 

        '''
        ...

    def pop(self):
        ''' 

        '''
        ...

    def property_overridable_library_set(self):
        ''' 

        '''
        ...

    def property_unset(self):
        ''' 

        '''
        ...

    def store_mouse_cursor(self, context, event):
        ''' 

        '''
        ...

    def type_recast(self):
        ''' 

        '''
        ...

    def values(self):
        ''' 

        '''
        ...


class NODE_OT_add_simulation_zone(NodeAddZoneOperator, NodeAddOperator,
                                  bpy_types.Operator):
    bl_idname: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    input_node_type: typing.Any
    ''' '''

    output_node_type: typing.Any
    ''' '''

    def as_keywords(self, ignore):
        ''' 

        '''
        ...

    def as_pointer(self):
        ''' 

        '''
        ...

    def bl_rna_get_subclass(self):
        ''' 

        '''
        ...

    def bl_rna_get_subclass_py(self):
        ''' 

        '''
        ...

    def create_node(self, context, node_type):
        ''' 

        '''
        ...

    def deselect_nodes(self, context):
        ''' 

        '''
        ...

    def driver_add(self):
        ''' 

        '''
        ...

    def driver_remove(self):
        ''' 

        '''
        ...

    def execute(self, context):
        ''' 

        '''
        ...

    def get(self):
        ''' 

        '''
        ...

    def id_properties_clear(self):
        ''' 

        '''
        ...

    def id_properties_ensure(self):
        ''' 

        '''
        ...

    def id_properties_ui(self):
        ''' 

        '''
        ...

    def invoke(self, context, event):
        ''' 

        '''
        ...

    def is_property_hidden(self):
        ''' 

        '''
        ...

    def is_property_overridable_library(self):
        ''' 

        '''
        ...

    def is_property_readonly(self):
        ''' 

        '''
        ...

    def is_property_set(self):
        ''' 

        '''
        ...

    def items(self):
        ''' 

        '''
        ...

    def keyframe_delete(self):
        ''' 

        '''
        ...

    def keyframe_insert(self):
        ''' 

        '''
        ...

    def keys(self):
        ''' 

        '''
        ...

    def path_from_id(self):
        ''' 

        '''
        ...

    def path_resolve(self):
        ''' 

        '''
        ...

    def poll(self, context):
        ''' 

        '''
        ...

    def poll_message_set(self):
        ''' 

        '''
        ...

    def pop(self):
        ''' 

        '''
        ...

    def property_overridable_library_set(self):
        ''' 

        '''
        ...

    def property_unset(self):
        ''' 

        '''
        ...

    def store_mouse_cursor(self, context, event):
        ''' 

        '''
        ...

    def type_recast(self):
        ''' 

        '''
        ...

    def values(self):
        ''' 

        '''
        ...

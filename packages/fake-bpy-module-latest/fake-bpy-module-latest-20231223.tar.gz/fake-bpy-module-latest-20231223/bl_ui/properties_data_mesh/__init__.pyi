import sys
import typing
import bpy_types
import rna_prop_ui

GenericType = typing.TypeVar("GenericType")


class ColorAttributesListBase:
    display_domain_names: typing.Any
    ''' '''

    def filter_items(self, _context, data, property):
        ''' 

        '''
        ...


class MESH_MT_attribute_context_menu(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def append(self, draw_func):
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

    def draw(self, _context):
        ''' 

        '''
        ...

    def draw_collapsible(self, context, layout):
        ''' 

        '''
        ...

    def draw_preset(self, _context):
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

    def is_extended(self):
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

    def path_menu(self, searchpaths, operator, props_default, prop_filepath,
                  filter_ext, filter_path, display_name, add_operator):
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

    def prepend(self, draw_func):
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

    def remove(self, draw_func):
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


class MESH_MT_color_attribute_context_menu(bpy_types.Menu,
                                           bpy_types._GenericUI):
    bl_label: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def append(self, draw_func):
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

    def draw(self, _context):
        ''' 

        '''
        ...

    def draw_collapsible(self, context, layout):
        ''' 

        '''
        ...

    def draw_preset(self, _context):
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

    def is_extended(self):
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

    def path_menu(self, searchpaths, operator, props_default, prop_filepath,
                  filter_ext, filter_path, display_name, add_operator):
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

    def prepend(self, draw_func):
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

    def remove(self, draw_func):
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


class MESH_MT_shape_key_context_menu(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def append(self, draw_func):
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

    def draw(self, _context):
        ''' 

        '''
        ...

    def draw_collapsible(self, context, layout):
        ''' 

        '''
        ...

    def draw_preset(self, _context):
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

    def is_extended(self):
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

    def path_menu(self, searchpaths, operator, props_default, prop_filepath,
                  filter_ext, filter_path, display_name, add_operator):
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

    def prepend(self, draw_func):
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

    def remove(self, draw_func):
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


class MESH_MT_vertex_group_context_menu(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def append(self, draw_func):
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

    def draw(self, _context):
        ''' 

        '''
        ...

    def draw_collapsible(self, context, layout):
        ''' 

        '''
        ...

    def draw_preset(self, _context):
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

    def is_extended(self):
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

    def path_menu(self, searchpaths, operator, props_default, prop_filepath,
                  filter_ext, filter_path, display_name, add_operator):
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

    def prepend(self, draw_func):
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

    def remove(self, draw_func):
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


class MESH_UL_attributes(bpy_types.UIList, bpy_types._GenericUI):
    bl_rna: typing.Any
    ''' '''

    display_domain_names: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def append(self, draw_func):
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

    def draw_item(self, _context, layout, _data, attribute, _icon,
                  _active_data, _active_propname, _index):
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

    def filter_items(self, _context, data, property):
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

    def is_extended(self):
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

    def prepend(self, draw_func):
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

    def remove(self, draw_func):
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


class MESH_UL_shape_keys(bpy_types.UIList, bpy_types._GenericUI):
    bl_rna: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def append(self, draw_func):
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

    def draw_item(self, _context, layout, _data, item, icon, active_data,
                  _active_propname, index):
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

    def is_extended(self):
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

    def prepend(self, draw_func):
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

    def remove(self, draw_func):
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


class MESH_UL_uvmaps(bpy_types.UIList, bpy_types._GenericUI):
    bl_rna: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def append(self, draw_func):
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

    def draw_item(self, _context, layout, _data, item, icon, _active_data,
                  _active_propname, _index):
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

    def is_extended(self):
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

    def prepend(self, draw_func):
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

    def remove(self, draw_func):
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


class MESH_UL_vgroups(bpy_types.UIList, bpy_types._GenericUI):
    bl_rna: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def append(self, draw_func):
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

    def draw_item(self, _context, layout, _data, item, icon, _active_data_,
                  _active_propname, _index):
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

    def is_extended(self):
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

    def prepend(self, draw_func):
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

    def remove(self, draw_func):
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


class MeshButtonsPanel:
    bl_context: typing.Any
    ''' '''

    bl_region_type: typing.Any
    ''' '''

    bl_space_type: typing.Any
    ''' '''

    def poll(self, context):
        ''' 

        '''
        ...


class MESH_UL_color_attributes(bpy_types.UIList, bpy_types._GenericUI,
                               ColorAttributesListBase):
    bl_rna: typing.Any
    ''' '''

    display_domain_names: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def append(self, draw_func):
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

    def draw_item(self, _context, layout, data, attribute, _icon, _active_data,
                  _active_propname, _index):
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

    def filter_items(self, _context, data, property):
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

    def is_extended(self):
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

    def prepend(self, draw_func):
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

    def remove(self, draw_func):
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


class MESH_UL_color_attributes_selector(bpy_types.UIList, bpy_types._GenericUI,
                                        ColorAttributesListBase):
    bl_rna: typing.Any
    ''' '''

    display_domain_names: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def append(self, draw_func):
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

    def draw_item(self, _context, layout, _data, attribute, _icon,
                  _active_data, _active_propname, _index):
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

    def filter_items(self, _context, data, property):
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

    def is_extended(self):
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

    def prepend(self, draw_func):
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

    def remove(self, draw_func):
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


class DATA_PT_context_mesh(MeshButtonsPanel, bpy_types.Panel,
                           bpy_types._GenericUI):
    COMPAT_ENGINES: typing.Any
    ''' '''

    bl_context: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_region_type: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    bl_space_type: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def append(self, draw_func):
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

    def draw(self, context):
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

    def is_extended(self):
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

    def pop(self):
        ''' 

        '''
        ...

    def prepend(self, draw_func):
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

    def remove(self, draw_func):
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


class DATA_PT_custom_props_mesh(MeshButtonsPanel, rna_prop_ui.PropertyPanel,
                                bpy_types.Panel, bpy_types._GenericUI):
    COMPAT_ENGINES: typing.Any
    ''' '''

    bl_context: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_order: typing.Any
    ''' '''

    bl_region_type: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    bl_space_type: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def append(self, draw_func):
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

    def draw(self, context):
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

    def is_extended(self):
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

    def pop(self):
        ''' 

        '''
        ...

    def prepend(self, draw_func):
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

    def remove(self, draw_func):
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


class DATA_PT_customdata(MeshButtonsPanel, bpy_types.Panel,
                         bpy_types._GenericUI):
    COMPAT_ENGINES: typing.Any
    ''' '''

    bl_context: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_region_type: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    bl_space_type: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def append(self, draw_func):
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

    def draw(self, context):
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

    def is_extended(self):
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

    def pop(self):
        ''' 

        '''
        ...

    def prepend(self, draw_func):
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

    def remove(self, draw_func):
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


class DATA_PT_mesh_attributes(MeshButtonsPanel, bpy_types.Panel,
                              bpy_types._GenericUI):
    COMPAT_ENGINES: typing.Any
    ''' '''

    bl_context: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_region_type: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    bl_space_type: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def append(self, draw_func):
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

    def draw(self, context):
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

    def is_extended(self):
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

    def pop(self):
        ''' 

        '''
        ...

    def prepend(self, draw_func):
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

    def remove(self, draw_func):
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


class DATA_PT_remesh(MeshButtonsPanel, bpy_types.Panel, bpy_types._GenericUI):
    COMPAT_ENGINES: typing.Any
    ''' '''

    bl_context: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_region_type: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    bl_space_type: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def append(self, draw_func):
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

    def draw(self, context):
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

    def is_extended(self):
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

    def pop(self):
        ''' 

        '''
        ...

    def prepend(self, draw_func):
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

    def remove(self, draw_func):
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


class DATA_PT_shape_keys(MeshButtonsPanel, bpy_types.Panel,
                         bpy_types._GenericUI):
    COMPAT_ENGINES: typing.Any
    ''' '''

    bl_context: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_region_type: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    bl_space_type: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def append(self, draw_func):
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

    def draw(self, context):
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

    def is_extended(self):
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

    def pop(self):
        ''' 

        '''
        ...

    def prepend(self, draw_func):
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

    def remove(self, draw_func):
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


class DATA_PT_texture_space(MeshButtonsPanel, bpy_types.Panel,
                            bpy_types._GenericUI):
    COMPAT_ENGINES: typing.Any
    ''' '''

    bl_context: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_region_type: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    bl_space_type: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def append(self, draw_func):
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

    def draw(self, context):
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

    def is_extended(self):
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

    def pop(self):
        ''' 

        '''
        ...

    def prepend(self, draw_func):
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

    def remove(self, draw_func):
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


class DATA_PT_uv_texture(MeshButtonsPanel, bpy_types.Panel,
                         bpy_types._GenericUI):
    COMPAT_ENGINES: typing.Any
    ''' '''

    bl_context: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_region_type: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    bl_space_type: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def append(self, draw_func):
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

    def draw(self, context):
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

    def is_extended(self):
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

    def pop(self):
        ''' 

        '''
        ...

    def prepend(self, draw_func):
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

    def remove(self, draw_func):
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


class DATA_PT_vertex_groups(MeshButtonsPanel, bpy_types.Panel,
                            bpy_types._GenericUI):
    COMPAT_ENGINES: typing.Any
    ''' '''

    bl_context: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_region_type: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    bl_space_type: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def append(self, draw_func):
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

    def draw(self, context):
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

    def is_extended(self):
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

    def pop(self):
        ''' 

        '''
        ...

    def prepend(self, draw_func):
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

    def remove(self, draw_func):
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


class DATA_PT_vertex_colors(DATA_PT_mesh_attributes, MeshButtonsPanel,
                            bpy_types.Panel, bpy_types._GenericUI):
    COMPAT_ENGINES: typing.Any
    ''' '''

    bl_context: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_region_type: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    bl_space_type: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    def append(self, draw_func):
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

    def draw(self, context):
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

    def is_extended(self):
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

    def pop(self):
        ''' 

        '''
        ...

    def prepend(self, draw_func):
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

    def remove(self, draw_func):
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


def draw_attribute_warnings(context, layout):
    ''' 

    '''

    ...

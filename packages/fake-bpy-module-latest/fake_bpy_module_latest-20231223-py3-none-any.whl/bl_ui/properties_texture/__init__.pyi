import sys
import typing
import bpy_types
import rna_prop_ui

GenericType = typing.TypeVar("GenericType")


class TEXTURE_MT_context_menu(bpy_types.Menu, bpy_types._GenericUI):
    COMPAT_ENGINES: typing.Any
    ''' '''

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


class TEXTURE_UL_texslots(bpy_types.UIList, bpy_types._GenericUI):
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


class TextureButtonsPanel:
    bl_context: typing.Any
    ''' '''

    bl_region_type: typing.Any
    ''' '''

    bl_space_type: typing.Any
    ''' '''


class TextureColorsPoll:
    def poll(self, context):
        ''' 

        '''
        ...


class TEXTURE_PT_context(TextureButtonsPanel, bpy_types.Panel,
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


class TEXTURE_PT_custom_props(TextureButtonsPanel, rna_prop_ui.PropertyPanel,
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


class TEXTURE_PT_node(TextureButtonsPanel, bpy_types.Panel,
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


class TEXTURE_PT_preview(TextureButtonsPanel, bpy_types.Panel,
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


class TextureSlotPanel(TextureButtonsPanel):
    COMPAT_ENGINES: typing.Any
    ''' '''

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


class TextureTypePanel(TextureButtonsPanel):
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


class TEXTURE_PT_colors(TextureColorsPoll, TextureButtonsPanel,
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


class TEXTURE_PT_colors_ramp(TextureColorsPoll, TextureButtonsPanel,
                             bpy_types.Panel, bpy_types._GenericUI):
    COMPAT_ENGINES: typing.Any
    ''' '''

    bl_context: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_parent_id: typing.Any
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

    def draw_header(self, context):
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


class TEXTURE_PT_influence(TextureSlotPanel, TextureButtonsPanel,
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


class TEXTURE_PT_mapping(TextureSlotPanel, TextureButtonsPanel,
                         bpy_types.Panel, bpy_types._GenericUI):
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


class TEXTURE_PT_blend(TextureTypePanel, TextureButtonsPanel, bpy_types.Panel,
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

    tex_type: typing.Any
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


class TEXTURE_PT_clouds(TextureTypePanel, TextureButtonsPanel, bpy_types.Panel,
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

    tex_type: typing.Any
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


class TEXTURE_PT_distortednoise(TextureTypePanel, TextureButtonsPanel,
                                bpy_types.Panel, bpy_types._GenericUI):
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

    tex_type: typing.Any
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


class TEXTURE_PT_image(TextureTypePanel, TextureButtonsPanel, bpy_types.Panel,
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

    tex_type: typing.Any
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


class TEXTURE_PT_image_alpha(TextureTypePanel, TextureButtonsPanel,
                             bpy_types.Panel, bpy_types._GenericUI):
    COMPAT_ENGINES: typing.Any
    ''' '''

    bl_context: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_parent_id: typing.Any
    ''' '''

    bl_region_type: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    bl_space_type: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    tex_type: typing.Any
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

    def draw_header(self, context):
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


class TEXTURE_PT_image_mapping(TextureTypePanel, TextureButtonsPanel,
                               bpy_types.Panel, bpy_types._GenericUI):
    COMPAT_ENGINES: typing.Any
    ''' '''

    bl_context: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_parent_id: typing.Any
    ''' '''

    bl_region_type: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    bl_space_type: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    tex_type: typing.Any
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


class TEXTURE_PT_image_mapping_crop(TextureTypePanel, TextureButtonsPanel,
                                    bpy_types.Panel, bpy_types._GenericUI):
    COMPAT_ENGINES: typing.Any
    ''' '''

    bl_context: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_parent_id: typing.Any
    ''' '''

    bl_region_type: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    bl_space_type: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    tex_type: typing.Any
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


class TEXTURE_PT_image_sampling(TextureTypePanel, TextureButtonsPanel,
                                bpy_types.Panel, bpy_types._GenericUI):
    COMPAT_ENGINES: typing.Any
    ''' '''

    bl_context: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_parent_id: typing.Any
    ''' '''

    bl_region_type: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    bl_space_type: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    tex_type: typing.Any
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


class TEXTURE_PT_image_settings(TextureTypePanel, TextureButtonsPanel,
                                bpy_types.Panel, bpy_types._GenericUI):
    COMPAT_ENGINES: typing.Any
    ''' '''

    bl_context: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_parent_id: typing.Any
    ''' '''

    bl_region_type: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    bl_space_type: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    tex_type: typing.Any
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


class TEXTURE_PT_magic(TextureTypePanel, TextureButtonsPanel, bpy_types.Panel,
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

    tex_type: typing.Any
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


class TEXTURE_PT_marble(TextureTypePanel, TextureButtonsPanel, bpy_types.Panel,
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

    tex_type: typing.Any
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


class TEXTURE_PT_musgrave(TextureTypePanel, TextureButtonsPanel,
                          bpy_types.Panel, bpy_types._GenericUI):
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

    tex_type: typing.Any
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


class TEXTURE_PT_stucci(TextureTypePanel, TextureButtonsPanel, bpy_types.Panel,
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

    tex_type: typing.Any
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


class TEXTURE_PT_voronoi(TextureTypePanel, TextureButtonsPanel,
                         bpy_types.Panel, bpy_types._GenericUI):
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

    tex_type: typing.Any
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


class TEXTURE_PT_voronoi_feature_weights(TextureTypePanel, TextureButtonsPanel,
                                         bpy_types.Panel,
                                         bpy_types._GenericUI):
    COMPAT_ENGINES: typing.Any
    ''' '''

    bl_context: typing.Any
    ''' '''

    bl_label: typing.Any
    ''' '''

    bl_parent_id: typing.Any
    ''' '''

    bl_region_type: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    bl_space_type: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    tex_type: typing.Any
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


class TEXTURE_PT_wood(TextureTypePanel, TextureButtonsPanel, bpy_types.Panel,
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

    tex_type: typing.Any
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


def context_tex_datablock(context):
    ''' 

    '''

    ...


def texture_filter_common(tex, layout):
    ''' 

    '''

    ...

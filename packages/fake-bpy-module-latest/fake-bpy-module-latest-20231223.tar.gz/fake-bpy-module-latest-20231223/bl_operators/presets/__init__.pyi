import sys
import typing
import bpy_types

GenericType = typing.TypeVar("GenericType")


class AddPresetBase:
    bl_options: typing.Any
    ''' '''

    def as_filename(self, name):
        ''' 

        '''
        ...

    def check(self, _context):
        ''' 

        '''
        ...

    def execute(self, context):
        ''' 

        '''
        ...

    def invoke(self, context, _event):
        ''' 

        '''
        ...


class ExecutePreset(bpy_types.Operator):
    bl_idname: typing.Any
    ''' '''

    bl_label: typing.Any
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


class WM_MT_operator_presets(bpy_types.Menu, bpy_types._GenericUI):
    bl_label: typing.Any
    ''' '''

    bl_rna: typing.Any
    ''' '''

    id_data: typing.Any
    ''' '''

    preset_operator: typing.Any
    ''' '''

    preset_subdir: typing.Any
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


class AddPresetCamera(AddPresetBase, bpy_types.Operator):
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

    preset_defines: typing.Any
    ''' '''

    preset_menu: typing.Any
    ''' '''

    preset_subdir: typing.Any
    ''' '''

    preset_values: typing.Any
    ''' '''

    def as_filename(self, name):
        ''' 

        '''
        ...

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

    def check(self, _context):
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

    def invoke(self, context, _event):
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


class AddPresetCameraSafeAreas(AddPresetBase, bpy_types.Operator):
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

    preset_defines: typing.Any
    ''' '''

    preset_menu: typing.Any
    ''' '''

    preset_subdir: typing.Any
    ''' '''

    preset_values: typing.Any
    ''' '''

    def as_filename(self, name):
        ''' 

        '''
        ...

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

    def check(self, _context):
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

    def invoke(self, context, _event):
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


class AddPresetCloth(AddPresetBase, bpy_types.Operator):
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

    preset_defines: typing.Any
    ''' '''

    preset_menu: typing.Any
    ''' '''

    preset_subdir: typing.Any
    ''' '''

    preset_values: typing.Any
    ''' '''

    def as_filename(self, name):
        ''' 

        '''
        ...

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

    def check(self, _context):
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

    def invoke(self, context, _event):
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


class AddPresetFluid(AddPresetBase, bpy_types.Operator):
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

    preset_defines: typing.Any
    ''' '''

    preset_menu: typing.Any
    ''' '''

    preset_subdir: typing.Any
    ''' '''

    preset_values: typing.Any
    ''' '''

    def as_filename(self, name):
        ''' 

        '''
        ...

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

    def check(self, _context):
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

    def invoke(self, context, _event):
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


class AddPresetGpencilBrush(AddPresetBase, bpy_types.Operator):
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

    preset_defines: typing.Any
    ''' '''

    preset_menu: typing.Any
    ''' '''

    preset_subdir: typing.Any
    ''' '''

    preset_values: typing.Any
    ''' '''

    def as_filename(self, name):
        ''' 

        '''
        ...

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

    def check(self, _context):
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

    def invoke(self, context, _event):
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


class AddPresetGpencilMaterial(AddPresetBase, bpy_types.Operator):
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

    preset_defines: typing.Any
    ''' '''

    preset_menu: typing.Any
    ''' '''

    preset_subdir: typing.Any
    ''' '''

    preset_values: typing.Any
    ''' '''

    def as_filename(self, name):
        ''' 

        '''
        ...

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

    def check(self, _context):
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

    def invoke(self, context, _event):
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


class AddPresetHairDynamics(AddPresetBase, bpy_types.Operator):
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

    preset_defines: typing.Any
    ''' '''

    preset_menu: typing.Any
    ''' '''

    preset_subdir: typing.Any
    ''' '''

    preset_values: typing.Any
    ''' '''

    def as_filename(self, name):
        ''' 

        '''
        ...

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

    def check(self, _context):
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

    def invoke(self, context, _event):
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


class AddPresetInterfaceTheme(AddPresetBase, bpy_types.Operator):
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

    preset_menu: typing.Any
    ''' '''

    preset_subdir: typing.Any
    ''' '''

    def as_filename(self, name):
        ''' 

        '''
        ...

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

    def check(self, _context):
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

    def invoke(self, context, _event):
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


class AddPresetKeyconfig(AddPresetBase, bpy_types.Operator):
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

    preset_menu: typing.Any
    ''' '''

    preset_subdir: typing.Any
    ''' '''

    def add(self, _context, filepath):
        ''' 

        '''
        ...

    def as_filename(self, name):
        ''' 

        '''
        ...

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

    def check(self, _context):
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

    def invoke(self, context, _event):
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

    def poll_message_set(self):
        ''' 

        '''
        ...

    def pop(self):
        ''' 

        '''
        ...

    def post_cb(self, context):
        ''' 

        '''
        ...

    def pre_cb(self, context):
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


class AddPresetNodeColor(AddPresetBase, bpy_types.Operator):
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

    preset_defines: typing.Any
    ''' '''

    preset_menu: typing.Any
    ''' '''

    preset_subdir: typing.Any
    ''' '''

    preset_values: typing.Any
    ''' '''

    def as_filename(self, name):
        ''' 

        '''
        ...

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

    def check(self, _context):
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

    def invoke(self, context, _event):
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


class AddPresetOperator(AddPresetBase, bpy_types.Operator):
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

    preset_defines: typing.Any
    ''' '''

    preset_menu: typing.Any
    ''' '''

    preset_subdir: typing.Any
    ''' '''

    preset_values: typing.Any
    ''' '''

    def as_filename(self, name):
        ''' 

        '''
        ...

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

    def check(self, _context):
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

    def invoke(self, context, _event):
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

    def operator_path(self, operator):
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


class AddPresetRender(AddPresetBase, bpy_types.Operator):
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

    preset_defines: typing.Any
    ''' '''

    preset_menu: typing.Any
    ''' '''

    preset_subdir: typing.Any
    ''' '''

    preset_values: typing.Any
    ''' '''

    def as_filename(self, name):
        ''' 

        '''
        ...

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

    def check(self, _context):
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

    def invoke(self, context, _event):
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


class AddPresetTextEditor(AddPresetBase, bpy_types.Operator):
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

    preset_defines: typing.Any
    ''' '''

    preset_menu: typing.Any
    ''' '''

    preset_subdir: typing.Any
    ''' '''

    preset_values: typing.Any
    ''' '''

    def as_filename(self, name):
        ''' 

        '''
        ...

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

    def check(self, _context):
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

    def invoke(self, context, _event):
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


class AddPresetTrackingCamera(AddPresetBase, bpy_types.Operator):
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

    preset_defines: typing.Any
    ''' '''

    preset_menu: typing.Any
    ''' '''

    preset_subdir: typing.Any
    ''' '''

    preset_values: typing.Any
    ''' '''

    def as_filename(self, name):
        ''' 

        '''
        ...

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

    def check(self, _context):
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

    def invoke(self, context, _event):
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


class AddPresetTrackingSettings(AddPresetBase, bpy_types.Operator):
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

    preset_defines: typing.Any
    ''' '''

    preset_menu: typing.Any
    ''' '''

    preset_subdir: typing.Any
    ''' '''

    preset_values: typing.Any
    ''' '''

    def as_filename(self, name):
        ''' 

        '''
        ...

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

    def check(self, _context):
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

    def invoke(self, context, _event):
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


class AddPresetTrackingTrackColor(AddPresetBase, bpy_types.Operator):
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

    preset_defines: typing.Any
    ''' '''

    preset_menu: typing.Any
    ''' '''

    preset_subdir: typing.Any
    ''' '''

    preset_values: typing.Any
    ''' '''

    def as_filename(self, name):
        ''' 

        '''
        ...

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

    def check(self, _context):
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

    def invoke(self, context, _event):
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

import sys
import typing
import bpy_types

GenericType = typing.TypeVar("GenericType")


class ToolActivePanelHelper:
    bl_label: typing.Any
    ''' '''

    def draw(self, context):
        ''' 

        '''
        ...


class ToolDef:
    cursor: typing.Any
    ''' '''

    data_block: typing.Any
    ''' '''

    description: typing.Any
    ''' '''

    draw_cursor: typing.Any
    ''' '''

    draw_settings: typing.Any
    ''' '''

    icon: typing.Any
    ''' '''

    idname: typing.Any
    ''' '''

    keymap: typing.Any
    ''' '''

    label: typing.Any
    ''' '''

    operator: typing.Any
    ''' '''

    options: typing.Any
    ''' '''

    widget: typing.Any
    ''' '''

    widget_properties: typing.Any
    ''' '''

    def count(self, value):
        ''' 

        '''
        ...

    def from_dict(self, kw_args):
        ''' 

        '''
        ...

    def from_fn(self, fn):
        ''' 

        '''
        ...

    def index(self, value, start, stop):
        ''' 

        '''
        ...


class ToolSelectPanelHelper:
    def draw(self, context):
        ''' 

        '''
        ...

    def draw_active_tool_fallback(self, context, layout, tool,
                                  is_horizontal_layout):
        ''' 

        '''
        ...

    def draw_active_tool_header(self, context, layout, show_tool_icon_always,
                                tool_key):
        ''' 

        '''
        ...

    def draw_cls(self, layout, context, detect_layout, scale_y):
        ''' 

        '''
        ...

    def draw_fallback_tool_items(self, layout, context):
        ''' 

        '''
        ...

    def draw_fallback_tool_items_for_pie_menu(self, layout, context):
        ''' 

        '''
        ...

    def keymap_ui_hierarchy(self, context_mode):
        ''' 

        '''
        ...

    def register(self):
        ''' 

        '''
        ...

    def register_ensure(self):
        ''' 

        '''
        ...

    def tool_active_from_context(self, context):
        ''' 

        '''
        ...

    def tools_all(self):
        ''' 

        '''
        ...

    def tools_from_context(self, context, mode):
        ''' 

        '''
        ...


class WM_MT_toolsystem_submenu(bpy_types.Menu, bpy_types._GenericUI):
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


def activate_by_id(context, space_type, idname, as_fallback):
    ''' 

    '''

    ...


def activate_by_id_or_cycle(context, space_type, idname, offset, as_fallback):
    ''' 

    '''

    ...


def description_from_id(context, space_type, idname, use_operator):
    ''' 

    '''

    ...


def item_from_flat_index(context, space_type, index):
    ''' 

    '''

    ...


def item_from_id(context, space_type, idname):
    ''' 

    '''

    ...


def item_from_id_active(context, space_type, idname):
    ''' 

    '''

    ...


def item_from_id_active_with_group(context, space_type, idname):
    ''' 

    '''

    ...


def item_from_index_active(context, space_type, index):
    ''' 

    '''

    ...


def item_group_from_id(context, space_type, idname, coerce):
    ''' 

    '''

    ...


def keymap_from_id(context, space_type, idname):
    ''' 

    '''

    ...

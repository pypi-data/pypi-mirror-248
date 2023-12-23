import sys
import typing
import bpy_types

GenericType = typing.TypeVar("GenericType")


class UnifiedPaintPanel:
    def get_brush_mode(self, context):
        ''' 

        '''
        ...

    def paint_settings(self, context):
        ''' 

        '''
        ...

    def prop_unified(self, layout, context, brush, prop_name, unified_name,
                     pressure_name, icon, text, slider, header):
        ''' 

        '''
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        ''' 

        '''
        ...

    def prop_unified_color_picker(self, parent, context, brush, prop_name,
                                  value_slider):
        ''' 

        '''
        ...


class VIEW3D_MT_tools_projectpaint_clone(bpy_types.Menu, bpy_types._GenericUI):
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


class BrushPanel(UnifiedPaintPanel):
    def get_brush_mode(self, context):
        ''' 

        '''
        ...

    def paint_settings(self, context):
        ''' 

        '''
        ...

    def poll(self, context):
        ''' 

        '''
        ...

    def prop_unified(self, layout, context, brush, prop_name, unified_name,
                     pressure_name, icon, text, slider, header):
        ''' 

        '''
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        ''' 

        '''
        ...

    def prop_unified_color_picker(self, parent, context, brush, prop_name,
                                  value_slider):
        ''' 

        '''
        ...


class BrushSelectPanel(BrushPanel, UnifiedPaintPanel):
    bl_label: typing.Any
    ''' '''

    def draw(self, context):
        ''' 

        '''
        ...

    def get_brush_mode(self, context):
        ''' 

        '''
        ...

    def paint_settings(self, context):
        ''' 

        '''
        ...

    def poll(self, context):
        ''' 

        '''
        ...

    def prop_unified(self, layout, context, brush, prop_name, unified_name,
                     pressure_name, icon, text, slider, header):
        ''' 

        '''
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        ''' 

        '''
        ...

    def prop_unified_color_picker(self, parent, context, brush, prop_name,
                                  value_slider):
        ''' 

        '''
        ...


class ClonePanel(BrushPanel, UnifiedPaintPanel):
    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    def draw(self, context):
        ''' 

        '''
        ...

    def draw_header(self, context):
        ''' 

        '''
        ...

    def get_brush_mode(self, context):
        ''' 

        '''
        ...

    def paint_settings(self, context):
        ''' 

        '''
        ...

    def poll(self, context):
        ''' 

        '''
        ...

    def prop_unified(self, layout, context, brush, prop_name, unified_name,
                     pressure_name, icon, text, slider, header):
        ''' 

        '''
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        ''' 

        '''
        ...

    def prop_unified_color_picker(self, parent, context, brush, prop_name,
                                  value_slider):
        ''' 

        '''
        ...


class ColorPalettePanel(BrushPanel, UnifiedPaintPanel):
    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    def draw(self, context):
        ''' 

        '''
        ...

    def get_brush_mode(self, context):
        ''' 

        '''
        ...

    def paint_settings(self, context):
        ''' 

        '''
        ...

    def poll(self, context):
        ''' 

        '''
        ...

    def prop_unified(self, layout, context, brush, prop_name, unified_name,
                     pressure_name, icon, text, slider, header):
        ''' 

        '''
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        ''' 

        '''
        ...

    def prop_unified_color_picker(self, parent, context, brush, prop_name,
                                  value_slider):
        ''' 

        '''
        ...


class DisplayPanel(BrushPanel, UnifiedPaintPanel):
    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    def draw(self, context):
        ''' 

        '''
        ...

    def draw_header(self, context):
        ''' 

        '''
        ...

    def get_brush_mode(self, context):
        ''' 

        '''
        ...

    def paint_settings(self, context):
        ''' 

        '''
        ...

    def poll(self, context):
        ''' 

        '''
        ...

    def prop_unified(self, layout, context, brush, prop_name, unified_name,
                     pressure_name, icon, text, slider, header):
        ''' 

        '''
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        ''' 

        '''
        ...

    def prop_unified_color_picker(self, parent, context, brush, prop_name,
                                  value_slider):
        ''' 

        '''
        ...


class FalloffPanel(BrushPanel, UnifiedPaintPanel):
    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    def draw(self, context):
        ''' 

        '''
        ...

    def get_brush_mode(self, context):
        ''' 

        '''
        ...

    def paint_settings(self, context):
        ''' 

        '''
        ...

    def poll(self, context):
        ''' 

        '''
        ...

    def prop_unified(self, layout, context, brush, prop_name, unified_name,
                     pressure_name, icon, text, slider, header):
        ''' 

        '''
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        ''' 

        '''
        ...

    def prop_unified_color_picker(self, parent, context, brush, prop_name,
                                  value_slider):
        ''' 

        '''
        ...


class SmoothStrokePanel(BrushPanel, UnifiedPaintPanel):
    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    def draw(self, context):
        ''' 

        '''
        ...

    def draw_header(self, context):
        ''' 

        '''
        ...

    def get_brush_mode(self, context):
        ''' 

        '''
        ...

    def paint_settings(self, context):
        ''' 

        '''
        ...

    def poll(self, context):
        ''' 

        '''
        ...

    def prop_unified(self, layout, context, brush, prop_name, unified_name,
                     pressure_name, icon, text, slider, header):
        ''' 

        '''
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        ''' 

        '''
        ...

    def prop_unified_color_picker(self, parent, context, brush, prop_name,
                                  value_slider):
        ''' 

        '''
        ...


class StrokePanel(BrushPanel, UnifiedPaintPanel):
    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    bl_ui_units_x: typing.Any
    ''' '''

    def draw(self, context):
        ''' 

        '''
        ...

    def get_brush_mode(self, context):
        ''' 

        '''
        ...

    def paint_settings(self, context):
        ''' 

        '''
        ...

    def poll(self, context):
        ''' 

        '''
        ...

    def prop_unified(self, layout, context, brush, prop_name, unified_name,
                     pressure_name, icon, text, slider, header):
        ''' 

        '''
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        ''' 

        '''
        ...

    def prop_unified_color_picker(self, parent, context, brush, prop_name,
                                  value_slider):
        ''' 

        '''
        ...


class TextureMaskPanel(BrushPanel, UnifiedPaintPanel):
    bl_label: typing.Any
    ''' '''

    bl_options: typing.Any
    ''' '''

    def draw(self, context):
        ''' 

        '''
        ...

    def get_brush_mode(self, context):
        ''' 

        '''
        ...

    def paint_settings(self, context):
        ''' 

        '''
        ...

    def poll(self, context):
        ''' 

        '''
        ...

    def prop_unified(self, layout, context, brush, prop_name, unified_name,
                     pressure_name, icon, text, slider, header):
        ''' 

        '''
        ...

    def prop_unified_color(self, parent, context, brush, prop_name, text):
        ''' 

        '''
        ...

    def prop_unified_color_picker(self, parent, context, brush, prop_name,
                                  value_slider):
        ''' 

        '''
        ...


def brush_basic__draw_color_selector(context, layout, brush, gp_settings,
                                     props):
    ''' 

    '''

    ...


def brush_basic_gpencil_paint_settings(layout, context, brush, compact):
    ''' 

    '''

    ...


def brush_basic_gpencil_sculpt_settings(layout, _context, brush, compact):
    ''' 

    '''

    ...


def brush_basic_gpencil_vertex_settings(layout, _context, brush, compact):
    ''' 

    '''

    ...


def brush_basic_gpencil_weight_settings(layout, _context, brush, compact):
    ''' 

    '''

    ...


def brush_basic_texpaint_settings(layout, context, brush, compact):
    ''' 

    '''

    ...


def brush_mask_texture_settings(layout, brush):
    ''' 

    '''

    ...


def brush_settings(layout, context, brush, popover):
    ''' 

    '''

    ...


def brush_settings_advanced(layout, context, brush, popover):
    ''' 

    '''

    ...


def brush_shared_settings(layout, context, brush, popover):
    ''' 

    '''

    ...


def brush_texture_settings(layout, brush, sculpt):
    ''' 

    '''

    ...


def draw_color_settings(context, layout, brush, color_type):
    ''' 

    '''

    ...

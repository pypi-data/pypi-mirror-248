import sys
import typing

GenericType = typing.TypeVar("GenericType")


class ShaderImageTextureWrapper:
    NODES_LIST: typing.Any
    ''' '''

    colorspace_is_data: typing.Any
    ''' '''

    colorspace_name: typing.Any
    ''' '''

    extension: typing.Any
    ''' '''

    grid_row_diff: typing.Any
    ''' '''

    image: typing.Any
    ''' '''

    is_readonly: typing.Any
    ''' '''

    node_dst: typing.Any
    ''' '''

    node_image: typing.Any
    ''' '''

    node_mapping: typing.Any
    ''' '''

    owner_shader: typing.Any
    ''' '''

    projection: typing.Any
    ''' '''

    rotation: typing.Any
    ''' '''

    scale: typing.Any
    ''' '''

    socket_dst: typing.Any
    ''' '''

    texcoords: typing.Any
    ''' '''

    translation: typing.Any
    ''' '''

    use_alpha: typing.Any
    ''' '''

    def copy_from(self, tex):
        ''' 

        '''
        ...

    def copy_mapping_from(self, tex):
        ''' 

        '''
        ...

    def extension_get(self):
        ''' 

        '''
        ...

    def extension_set(self, extension):
        ''' 

        '''
        ...

    def has_mapping_node(self):
        ''' 

        '''
        ...

    def image_get(self):
        ''' 

        '''
        ...

    def image_set(self, image):
        ''' 

        '''
        ...

    def node_image_get(self):
        ''' 

        '''
        ...

    def node_mapping_get(self):
        ''' 

        '''
        ...

    def projection_get(self):
        ''' 

        '''
        ...

    def projection_set(self, projection):
        ''' 

        '''
        ...

    def rotation_get(self):
        ''' 

        '''
        ...

    def rotation_set(self, rotation):
        ''' 

        '''
        ...

    def scale_get(self):
        ''' 

        '''
        ...

    def scale_set(self, scale):
        ''' 

        '''
        ...

    def texcoords_get(self):
        ''' 

        '''
        ...

    def texcoords_set(self, texcoords):
        ''' 

        '''
        ...

    def translation_get(self):
        ''' 

        '''
        ...

    def translation_set(self, translation):
        ''' 

        '''
        ...


class ShaderWrapper:
    NODES_LIST: typing.Any
    ''' '''

    is_readonly: typing.Any
    ''' '''

    material: typing.Any
    ''' '''

    node_out: typing.Any
    ''' '''

    node_texcoords: typing.Any
    ''' '''

    use_nodes: typing.Any
    ''' '''

    def node_texcoords_get(self):
        ''' 

        '''
        ...

    def update(self):
        ''' 

        '''
        ...

    def use_nodes_get(self):
        ''' 

        '''
        ...

    def use_nodes_set(self, val):
        ''' 

        '''
        ...


class PrincipledBSDFWrapper(ShaderWrapper):
    NODES_LIST: typing.Any
    ''' '''

    alpha: typing.Any
    ''' '''

    alpha_texture: typing.Any
    ''' '''

    base_color: typing.Any
    ''' '''

    base_color_texture: typing.Any
    ''' '''

    emission_color: typing.Any
    ''' '''

    emission_color_texture: typing.Any
    ''' '''

    emission_strength: typing.Any
    ''' '''

    emission_strength_texture: typing.Any
    ''' '''

    ior: typing.Any
    ''' '''

    ior_texture: typing.Any
    ''' '''

    is_readonly: typing.Any
    ''' '''

    material: typing.Any
    ''' '''

    metallic: typing.Any
    ''' '''

    metallic_texture: typing.Any
    ''' '''

    node_normalmap: typing.Any
    ''' '''

    node_out: typing.Any
    ''' '''

    node_principled_bsdf: typing.Any
    ''' '''

    node_texcoords: typing.Any
    ''' '''

    normalmap_strength: typing.Any
    ''' '''

    normalmap_texture: typing.Any
    ''' '''

    roughness: typing.Any
    ''' '''

    roughness_texture: typing.Any
    ''' '''

    specular: typing.Any
    ''' '''

    specular_texture: typing.Any
    ''' '''

    specular_tint: typing.Any
    ''' '''

    specular_tint_texture: typing.Any
    ''' '''

    transmission: typing.Any
    ''' '''

    transmission_texture: typing.Any
    ''' '''

    use_nodes: typing.Any
    ''' '''

    def alpha_get(self):
        ''' 

        '''
        ...

    def alpha_set(self, value):
        ''' 

        '''
        ...

    def alpha_texture_get(self):
        ''' 

        '''
        ...

    def base_color_get(self):
        ''' 

        '''
        ...

    def base_color_set(self, color):
        ''' 

        '''
        ...

    def base_color_texture_get(self):
        ''' 

        '''
        ...

    def emission_color_get(self):
        ''' 

        '''
        ...

    def emission_color_set(self, color):
        ''' 

        '''
        ...

    def emission_color_texture_get(self):
        ''' 

        '''
        ...

    def emission_strength_get(self):
        ''' 

        '''
        ...

    def emission_strength_set(self, value):
        ''' 

        '''
        ...

    def emission_strength_texture_get(self):
        ''' 

        '''
        ...

    def ior_get(self):
        ''' 

        '''
        ...

    def ior_set(self, value):
        ''' 

        '''
        ...

    def ior_texture_get(self):
        ''' 

        '''
        ...

    def metallic_get(self):
        ''' 

        '''
        ...

    def metallic_set(self, value):
        ''' 

        '''
        ...

    def metallic_texture_get(self):
        ''' 

        '''
        ...

    def node_normalmap_get(self):
        ''' 

        '''
        ...

    def node_texcoords_get(self):
        ''' 

        '''
        ...

    def normalmap_strength_get(self):
        ''' 

        '''
        ...

    def normalmap_strength_set(self, value):
        ''' 

        '''
        ...

    def normalmap_texture_get(self):
        ''' 

        '''
        ...

    def roughness_get(self):
        ''' 

        '''
        ...

    def roughness_set(self, value):
        ''' 

        '''
        ...

    def roughness_texture_get(self):
        ''' 

        '''
        ...

    def specular_get(self):
        ''' 

        '''
        ...

    def specular_set(self, value):
        ''' 

        '''
        ...

    def specular_texture_get(self):
        ''' 

        '''
        ...

    def specular_tint_get(self):
        ''' 

        '''
        ...

    def specular_tint_set(self, color):
        ''' 

        '''
        ...

    def specular_tint_texture_get(self):
        ''' 

        '''
        ...

    def transmission_get(self):
        ''' 

        '''
        ...

    def transmission_set(self, value):
        ''' 

        '''
        ...

    def transmission_texture_get(self):
        ''' 

        '''
        ...

    def update(self):
        ''' 

        '''
        ...

    def use_nodes_get(self):
        ''' 

        '''
        ...

    def use_nodes_set(self, val):
        ''' 

        '''
        ...


def rgb_to_rgba(rgb):
    ''' 

    '''

    ...


def rgba_to_rgb(rgba):
    ''' 

    '''

    ...


def values_clamp(val, minv, maxv):
    ''' 

    '''

    ...

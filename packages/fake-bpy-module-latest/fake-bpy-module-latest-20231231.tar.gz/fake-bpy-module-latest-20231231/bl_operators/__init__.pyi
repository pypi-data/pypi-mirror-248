import sys
import typing
from . import object
from . import freestyle
from . import mesh
from . import console
from . import view3d
from . import anim
from . import spreadsheet
from . import rigidbody
from . import object_align
from . import sequencer
from . import add_mesh_torus
from . import clip
from . import userpref
from . import geometry_nodes
from . import uvcalc_transform
from . import file
from . import uvcalc_lightmap
from . import uvcalc_follow_active
from . import object_quick_effects
from . import screen_play_rendered_anim
from . import node
from . import image
from . import assets
from . import wm
from . import vertexpaint_dirt
from . import bmesh
from . import presets
from . import constraint
from . import object_randomize_transform

GenericType = typing.TypeVar("GenericType")

def register(): ...
def unregister(): ...

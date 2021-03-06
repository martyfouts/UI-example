# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
bl_info = {
    "name" : "UI Example",
    "description" : "HOWTO examples for the user interface",
    "author" : "Marty Fouts <fouts@fogey.com>",
    "version" : (0, 0, 1),
    "blender" : (2, 93, 0),
    "location" : "View3D",
    "warning" : "",
    "support" : "COMMUNITY",
    "doc_url" : "",
    "category" : "3D View"
}

# This bit is here because Python doesn't do recursive reloading 
# This works for a single level but I don't know will it work
# if the imported modules import other modules for the package.
if 'bpy' in locals():
    print('UIX Reloading')
    from importlib import reload
    import sys
    for k, v in list(sys.modules.items()):
        if k.startswith('UI example.'):
            reload(v)
# End of recursive reload support

import types
import bpy
from bpy.types import Scene, Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty

from . uix_ops import (UIX_OT_hello,
                        UIX_OT_ConfirmOperator,
                        UIX_OT_PropConfirmOperator,
                        UIX_OT_ImportFiles,
                        UIX_OT_display_preferences,
)

from . uix_panel import (UIX_PT_side_panel, 
                        UIX_PT_additional_panel, 
                        UIX_PT_sub_panel, 
                        UIX_PT_fancy_panel,
)

# An example of Add-on specific preferences modified from
# https://docs.blender.org/api/current/bpy.types.AddonPreferences.html

class UIXAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    filepath: StringProperty(
        name="Example File Path",
        subtype='FILE_PATH',
        default=r'C:\tmp'
    )
    number: IntProperty(
        name="Example Number",
        default=4,
    )
    boolean: BoolProperty(
        name="Example Boolean",
        default=True,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="UIX demonstration preferences")
        layout.prop(self, "filepath")
        layout.prop(self, "number")
        layout.prop(self, "boolean")



classes = [
            UIX_OT_hello,
            UIX_PT_side_panel,
            UIX_PT_additional_panel,
            UIX_PT_sub_panel,
            UIX_PT_fancy_panel,
            UIX_OT_ConfirmOperator,
            UIX_OT_PropConfirmOperator,
            UIX_OT_ImportFiles,
            UIXAddonPreferences,
            UIX_OT_display_preferences,
]

#------------------------------------------------------------------------------
# This is a bit of a hack, simply to show various properties in use.
# You can't attach operator properties to a panel, so instead, this creates
# example properties and attaches them to the Scene type so they can be
# accessed in one of the panels
# see also https://docs.blender.org/api/current/bpy.props.html
#------------------------------------------------------------------------------
def add_properties():

    # Add a scene custom property for the greeting text
    bpy.types.Scene.GreetingText = bpy.props.StringProperty(
        name="Greeting",
        description="Words to use in greeting",
        default="kthxbai",
    )
    
    # This will track a single boolean. In a panel it is displayed as a checkbox,
    # with checked = True
    bpy.types.Scene.check_box = bpy.props.BoolProperty(
        name="Sample checkbox",
        description="This is a checkbox sample",
        default=True,
    )

    # This will track a range of 1 - 32 booleans. The panel entry for this
    # displays three different ways of displaying such an array
    bpy.types.Scene.boolArray = bpy.props.BoolVectorProperty(
        name = "bool vector",
        description = "sample of a Boolean Vector",
        size = 5,
        default = (False,) * 5,
    )

    # FloatVectorProperty is rather amusing because its subtype determines
    # both what it contains and how it appears in a panel or other display
    bpy.types.Scene.example_color = bpy.props.FloatVectorProperty(
    name='example color',
    description = 'pick a color',
    default=(0.8,0.8,0.8),
    min=0.0,
    max=1.0,
    subtype='COLOR',
)

def remove_properties():
    del bpy.types.Scene.example_color
    del bpy.types.Scene.check_box
    del bpy.types.Scene.GreetingText

def register():
    for c in classes:
        bpy.utils.register_class(c)
        if 'initialize' in dir(c):
            c.initialize()

    add_properties()

def unregister():
    for c in classes:
        if 'deinitialize' in dir(c):
            c.deinitialize()
        bpy.utils.unregister_class(c)

    remove_properties()

if __name__ == '__main__':
    register()
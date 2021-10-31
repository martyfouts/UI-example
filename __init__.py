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

import bpy

from . uix_ops import UIX_OT_hello
from . uix_panel import (UIX_PT_side_panel, 
                        UIX_PT_additional_panel, 
                        UIX_PT_sub_panel, 
                        UIX_PT_fancy_panel,
                        )

classes = [
            UIX_OT_hello,
            UIX_PT_side_panel,
            UIX_PT_additional_panel,
            UIX_PT_sub_panel,
            UIX_PT_fancy_panel,
            ]

def register():
    for c in classes:
        bpy.utils.register_class(c)
        if 'initialize' in dir(c):
            c.initialize()

    # Add a scene custom property for the greeting text
    bpy.types.Scene.GreetingText = bpy.props.StringProperty(
        name="Greeting",
        description="Words to use in greeting",
        default="kthxbai",
    )

def unregister():
    for c in classes:
        if 'deinitialize' in dir(c):
            c.deinitialize()
        bpy.utils.unregister_class(c)

    # remove he scene custom property for the greeting text
    del bpy.types.Scene.GreetingText

if __name__ == '__main__':
    register()
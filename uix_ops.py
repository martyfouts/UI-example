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

import bpy
from bpy.types import Operator, OperatorFileListElement
from bpy.props import CollectionProperty, StringProperty
from pathlib import Path

hello_keymap = None
default_directory = r'c:\tmp' # ugly Windows specificity fix later

def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):
    """ a hack that uses a popup menu as a message box"""
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

def mesh_add_menu_draw(self, context):
    """ adds a menu entry when the function is added to an existing menu"""
    self.layout.operator("uix.hello")

def UIX_menu_import(self, context):
    self.layout.operator("uix.import_files", text="Import files").directory=default_directory

class UIX_OT_hello(Operator):
    """A very stupid operator entirely for the purpose of demonstration"""
    bl_idname = "uix.hello"
    bl_label = "say hello"
    bl_description = "say hello"
    bl_options = {'REGISTER', 'UNDO'}

    name_from : bpy.props.StringProperty(
        name="who from",
        description="Name of the sender",
        default="Marty",
    )

    name_to : bpy.props.StringProperty(
        name="who to",
        description="Name of the receiver",
        default="Bruce",
    )

    @classmethod
    def poll(self, context):
        return True

    # You can't display operator properties on a panel so you need to use
    # invoke if you want to set them before you use them. This has the
    # unfortunate consequence of alway popping up the setting dialog
    # You can avoid this if you set the UNDO option in bl_options
    # That way the "last operator" panel will popup and allow the adjustment
    #    def invoke(self, context, event):
    #        wm = context.window_manager
    #        return wm.invoke_props_dialog(self)

    def execute(self, context):
        # display the message in a popup
        ShowMessageBox(context.scene.GreetingText, self.name_to, 'ERROR')

        # display the message on the system console
        print(f"{context.scene.GreetingText} {self.name_to} from {self.name_from}.")

        # display the message on the system console
        # and in the info window
        self.report({'INFO'}, f"{self.name_from} just wanted to say {context.scene.GreetingText}, {self.name_to}.")
        return {'FINISHED'}
    
    # Local convention.  If a class wants to add menus or keymaps or other
    # custom bits, it does so through an initialize routine that is called
    # from __init__'s register routine after the class is registered.
    def initialize():
        print('YOWZA')
        # the add->mesh menu is a bad place for this but
        # it is just a demo after all.
        bpy.types.VIEW3D_MT_mesh_add.append(mesh_add_menu_draw)
        # If you add it to the header it goes to the end
        bpy.types.VIEW3D_HT_header.append(mesh_add_menu_draw)

        # Next up we add a keymap entry
        # This is from a stackexchange answer but it is not clear to me
        # how key maps / shortcuts really work.
        key_config = bpy.context.window_manager.keyconfigs.addon
        if key_config:
            key_map = key_config.keymaps.new(name='3D View', space_type='VIEW_3D')
            key_entry = key_map.keymap_items.new(UIX_OT_hello.bl_idname,
                                                                type='W',
                                                                value='PRESS',
                                                                ctrl=True,
            )
            hello_keymap = (key_map, key_entry)


    # Local convention.  If a class has an initialize it might also need to
    # undo the initialization through this routine that is called from
    # __init__'s unregister routine before the class is unregistered.
    def deinitialize():
        print('AZWOY')
        if hello_keymap:
            key_map, key_entry = hello_keymap
            key_map.keymap_items.remove(key_entry)
            bpy.context.window_manager.keyconfigs.addon.keymaps.remove(key_map)

        bpy.types.VIEW3D_MT_mesh_add.remove(mesh_add_menu_draw)
        bpy.types.VIEW3D_HT_header.remove(mesh_add_menu_draw)

# see https://blender.stackexchange.com/questions/73286/how-to-call-a-confirmation-dialog-box
# for an explanation of these additional classes

# For a custom conformation dialog you can wrap the operator into another one and invoke
# invoke_confirm(operator, event) class method of the window-manager to confirm the
# execution by the user.

class UIX_OT_ConfirmOperator(bpy.types.Operator):
    """Confirm Really?"""
    bl_idname = "uix.custom_confirm_dialog"
    bl_label = "Do you really want to confirm that?"
    bl_description = "An operator that invokes a confirm popup"
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        self.report({'INFO'}, "YES!")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)
    

# In order to display a popup, some properties and an OK 'button' you can return 
# wm.invoke_props_dialog(self) instead:

class UIX_OT_PropConfirmOperator(bpy.types.Operator):
    """Confirm Prop Really?"""
    bl_idname = "uix.custom_prop_confirm_dialog"
    bl_label = "Do you really want to conform those properties?"
    bl_description = "An operator that invokes a confirm dialog with properties"
    bl_options = {'REGISTER', 'INTERNAL'}

    prop1: bpy.props.BoolProperty()
    prop2: bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        self.report({'INFO'}, "YES!")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        row = self.layout
        row.prop(self, "prop1", text="Property A")
        row.prop(self, "prop2", text="Property B")

# A class that has a menu entry that uses the file picker
class UIX_OT_ImportFiles(bpy.types.Operator):
    """deal with some files read selected through the file browser"""
    bl_idname = "uix.import_files"
    bl_label = "give me some files to play with"
    bl_description = "An operator that uses the file browser"
    bl_options = {'REGISTER', 'UNDO'}

    directory : StringProperty(subtype='DIR_PATH')
    files : CollectionProperty(type=OperatorFileListElement)

    def do_import(self, import_file):
        file = import_file.open()
        # insert code to read and process file here
        file.close()

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        base = Path(self.directory)                
        for f in self.files:
            self.report({'INFO'}, f"processing {base / f.name}")
            self.do_import(base / f.name)
        
        return {'FINISHED'}

    def initialize():
        bpy.types.TOPBAR_MT_file_import.append(UIX_menu_import)

    def deinitialize():
        bpy.types.TOPBAR_MT_file_import.remove(UIX_menu_import)
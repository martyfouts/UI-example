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
from bpy.types import Panel

def add_button(layout, 
            label_text="A Label",
            button_op="uix.hello",
            button_text="A Button"):
    """Helper function to add a labeled button to a layout"""
    layout.label(text=label_text)
    row = layout.row()
    row.operator(button_op, text=button_text)

# These panels will all appear when the "UIX" tab in the sidebar is selected.
# They are tied to that tab because the bl_category is "UIX".
#
# The  appear in the order they were registered,
# unless they are assign an order using bl_order

class UIX_panel_common:
    """mixin class with common properties shared by all the UIX panels"""
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "UIX"
    bl_options = {"DEFAULT_CLOSED"}

class UIX_PT_side_panel(Panel, UIX_panel_common):
    """This is the parent of the whole mess"""
    bl_label = "UIX top panel"

    def draw(self, context):
        add_button(self.layout, label_text="Top button", button_text="TP says hello")
  
class UIX_PT_additional_panel(Panel, UIX_panel_common):
    """More or less a dup of side_panel for now"""
    bl_label = "UIX panel 2"

    def draw(self, context):
        col = self.layout.column(align=True)
        col.operator("uix.hello",
                    text="hello?"
        )


# bl_parent_id  is the name of the panel class that this is added to as a subpanel.
class UIX_PT_sub_panel(Panel, UIX_panel_common):
    """A subpanel used to access the greetings property"""
    bl_label = "Greetings"
    bl_parent_id = "UIX_PT_side_panel"

    def draw(self, context):
        col = self.layout.column()
        col.prop(context.scene, "GreetingText")

# see https://docs.blender.org/api/current/bpy.types.Panel.html#bpy.types.Panel
# for details about the bl_* values
# see https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout
# for details about layout elements
class UIX_PT_fancy_panel(Panel, UIX_panel_common):
    bl_label = "UIX fancy panel" # Title in the panel
    bl_description = "A very fancy panel"
    # see https://docs.blender.org/api/current/bpy.types.Panel.html#bpy.types.Panel.bl_options
    # for a list of options that apply to panels

    @classmethod
    def poll(self, context):
        return context.mode == 'OBJECT'

    def draw(self, context):
        layout = self.layout

        # This is not working. I don't know why.
        layout.alignment = 'CENTER'

        # Overall label at top of panel.
        layout.label(text="fancy panel")

        # A wee bit of space.
        layout.separator()

        # A label consisting of just an icon.
        layout.label(icon="BLENDER")

        # A row, consisting of two columns.
        row = layout.row()
        # The first column goes on the left.
        # Here I put a simple operator.
        # Note the use of an icon.
        col = row.column()
        col.label(text="L")
        col.operator("uix.hello", text="fancy hello", icon='TRASH')
        # The second column goes on the right.
        # Here I duplicate the simple operator,
        # But without an icon.
        col = row.column()
        col.label(text='R')
        col.operator("uix.hello")

        # A new row, dedicated to custom properties.
        # It has a single column that contains several
        # examples of displays of custom properties
        # that are attached to the scene.
        row = layout.row()
        row.separator()
        col = row.column()
        col.label(text="Custom properties")
        col.prop(context.scene, 'check_box')
        col.prop(context.scene, 'example_color')

        # A new row, dedicated to examples of confirmation dialogs.
        # These are from a stack exchange answer (See uix_ops.py
        # for references and details.)
        row = layout.row()
        row.operator("uix.custom_prop_confirm_dialog",
                    text="Props")
        row = layout.row()
        row.operator("uix.custom_prop_confirm_dialog",
                    text="Confirm")
        row = layout.row()
        # When calling an operator via bpy.ops.* without any execution context
        # the execute() method of the respective operator runs by default. If
        # the operator provides any kind of 'user interaction' like a
        # 'confirmation dialog' in this case, then you can pass 'INVOKE_DEFAULT'
        # as execution context when calling the operator which will also run
        # its invoke() method:
        # Note that wm.read_homefile only asks for confirmation if the current
        # session is dirty.
        row.operator_context = 'INVOKE_DEFAULT' #'INVOKE_AREA'
        row.operator("wm.read_homefile", text="New", icon='FILE_NEW')
        row = layout.row()
        # A button to select the operator to display the add-on's addon preferences
        row.separator()
        col = row.column()
        col.label(text="Addon properties")
        col.operator("uix.display_preferences")
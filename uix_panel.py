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
# They are tied to that tab because the bl_category is "UIX"
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
        layout.alignment = 'CENTER'
        layout.label(text="fancy panel")
        layout.separator()
        layout.label(icon="BLENDER")
        row = layout.row()
        col = row.column()
        col.label(text="L")
        col.operator("uix.hello", text="fancy hello", icon='TRASH')
        col = row.column()
        col.label(text='R')
        col.operator("uix.hello")
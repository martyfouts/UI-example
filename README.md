This repository is now deprecated. The examples apply to Blender versions 3.x. It has not been tested on newer versions of Blender.

This Blender Add-on is a collection of examples of how to set up panels,
add menus, and other UI related aspects of an add-on.  Its only purpose
is to provide me with reminders of how to do these things, all collected
into one place.

The original operator, three properties, and panels were designed to
show various ways to set three parts of a text message, the sender
receiver and body, and use buttons to to display the message.

Additionally, they showed how to add a shortcut for the button and
place menu entries in various menus.

An additional class contains the skeleton of an importer that uses
the file browser.

# Operators
## `UIX_OT_hello`

The original operator from the project, when invoked it displays a message
in each of several ways:

- calls `ShowMessageBox` to display a message using a popup menu,
- prints the message (goes to the terminal window), and
- calls `report` to report the message as an info message.

The `initialize` routine also adds menu entries for the operator to two
menus as examples of how to add menu entries.  It additionally creates
a shortcut (CTRL-W) as a demonstration of how to do that.

The `deinitialize` routine removes the menu entries and shortcut.

## `UIX_OT_ConfirmOperator`

An example of how to invoke a dialog box using `window_manager.invoke_confirm`.

## `UIX_OT_PropConfirmOperator`

An example of how to invoke a dialog box with properties that can be
changed using `window_manager.invoke_props_dialog`.

## `UIX_OT_ImportFiles`

An example of an importer class using the file browser to select a collection
of files and then process each file separately.  The 'process' part is skeleton.

## `UIX_OT_display_preferences`

An example demonstration of the use of preferences. It displays the current value
of the preferences.

### `invoke`

Calls the window manager to invoke the file browser: 
`window_manager.fileselect_add`. This has the side effect of filling out the
`directory` and `files` properties.

### `execute`

Processes the `directory` and `files` properties, calling `self.do_import`
on each file to handle the import.

### `do_import`

Opens and closes the file. Currently has no error handling.  Would also need
to have code added to read and process the contents of the file.

### `initialize` and `deinitialize`

Add/remove an entry in the top bar File -> import menu.

# Panels

The panels are just examples of how panel layout works, demonstrating the row
and column layouts, the difference between additional panels and subpanels,
and finally a kitchen-sink panel with an ever growing collection of examples.

## `UIX_panel_common`

A mix-in class that contains the default values for all of the `bl_*` properties
that each of the other panels have in common.

## `UIX_PT_side_panel`

When the UIX tab in the sidebar is selected, this will be the top of the array of
panels shown.  It contains a label, a button, and a sub panel.

## `UIX_PT_additional_panel`

This panel appears second in the side panel. It simply contains a button.

## `UIX_PT_sub_panel`

This panel is given a `bl_parent_id` of `UIX_PT_side_panel`. That makes it a
subpanel of the top panel, so it appears before the additional panel, but
indented to indicate it is a subpanel.

Rather than a button, this panel contains a property, in this case attached
to the scene, that the panel can be used to change.

## `UIX_PT_fancy_panel`

This is a silly panel that shows various panel formatting techniques, as well
as demonstrating how to display certain non-intuitive properties, such as
Booleans as checkboxes and FloatVectors as color pickers.

# Preferences

Preferences are basically implemented by creating a class that inherits from `AddonPreferences`
and giving it a `draw` routine. The individual preferences are Blender Properties and the
draw routine sets up the layout used in the preferences section of the Add-on's description
in preferences -> add-ons.

## `UIXAddonPreferences` inherits from `bpy.types.AddonPreferences` and in the example
contains 3 properties.

# Keymap

The keymap code is not well written nor robust but it demonstrates a pattern for adding a 
custom keymap (in the ops class)

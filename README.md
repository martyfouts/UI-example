This Blender Add-on is a collection of examples of how to set up panels,
add menus, and other UI related aspects of an add-on.  Its only purpose
is to provide me with reminders of how to do these things, all collected
into one place.

# Operators
## `UIX_OT_hello`

The original operator from the project, when invoked it displays a message
in each of several ways

- calls `ShowMessageBox` to display a message using a popup menu
- prints the message (goes to the terminal window)
- calls `report` to report the message as an info message

The `initialize` routine also adds menu entries for the operator to two
menus as examples of how to add menu entries.  It additionall creates
a shortcut (CTRL-W) as a demonstration of how to do that.

The `deinintialize` routine removes the menu entries and shortcut.

## `UIX_OT_ConfirmOperator`

An example of how to invoke a dialog box using `window_manager.invoke_confirm`

## `UIX_OT_PropConfirmOperator`

An example of how to invoke a dialog box with properties that can be
changed using `window_manager.invoke_props_dialog`

## `UIX_OT_ImportFiles`

An example of an importer class using the file browser to select a collection
of files and then process each file separately.  The 'process' part is skeleton.

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

Add/remove an entry in the top bar File -> import menu
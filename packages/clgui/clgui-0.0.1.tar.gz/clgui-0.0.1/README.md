# clgui

Command-Line-GUI

# Docs

## Install clgui

`pip install clgui`

## Create new gui

button_list = clgui.ButtonList()
button1 = clgui.Button("Hello", lambda: print("Hello"))
button2 = clgui.Button("World", lambda: print("World"))
button_list.addButtons([button1, button2])

vertical_layout.add(button_list)
vertical_layout.add()
main.show()

```py
import clgui

vertical_layout = clgui.Layouts.VStack() # Currently the only layout is VStack, more are planned
main = clgui.GUI(layout=vertical_layout) # Initialize a new GUI

# Elements
button_list = clgui.ButtonList() # Currently the only element type is ButtonList, more are planned
button = clgui.Button("click me")

# Methods
button1 = clgui.Button("Hello", lambda: print("Hello")) # Create a new button
button2 = clgui.Button("World", lambda: print("World")) # Create a new button
button_list.addButtons([button1, button2]) # Add buttons to the button list

button_list.addButton(button1) # A single button can also be added

vertical_layout.add(button_list) # Add button list to the layout
main.show() # Show the main GUI
main.destroy() # Close the gui
```

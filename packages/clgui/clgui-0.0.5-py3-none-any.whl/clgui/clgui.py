import colorama, keyboard, sys
colorama.init()


class GUI:
	created = False
	def __init__(self, layout):
		if (self.created):
			raise Exception("A GUI has already been created.")
		self.layout = layout
		self.input_thread = None
		self.created = True
	
	def show(self):
		keyboard.hook(self.layout.handleKeyPress)
		self.layout.render()
		try:
			keyboard.wait()
		except KeyboardInterrupt:
			pass
		self.destroy()

	def destroy(self):
		keyboard.unhook_all()
		sys.exit()

class ButtonList:
	def __init__(self):
		self.buttons = []
		self.selected_index = 0

	def addButtons(self, buttons):
		for button in buttons:
			self.addButton(button)

	def addButton(self, button):
		self.buttons.append(button)
		
	def render(self, print_func, state):
		for i, button in enumerate(self.buttons):
			button.render(print_func, state, i == self.selected_index)

	def handleInput(self, key):
		initial_selected_index = self.selected_index
		match (key.name):
			case "up":
				self.selected_index = (self.selected_index - 1) % len(self.buttons)
			case "down":
				self.selected_index = (self.selected_index + 1) % len(self.buttons)
			case _:
				for i, button in enumerate(self.buttons):
					if (i == self.selected_index):
						return button.handleInput(key)
		return initial_selected_index != self.selected_index

	
class Button:
	def __init__(self, label, callback=None, data=None):
		self.label = label
		self.callback = callback
		self.data = data

	def render(self, print_func, state, isSelected=True):
		match (state):
			case 1:
				print_func(colorama.Fore.BLUE + self.label + colorama.Style.RESET_ALL)
			case 2:
				print_func(colorama.Fore.LIGHTBLACK_EX + self.label + colorama.Style.RESET_ALL)
			case _:
				style = colorama.Fore.WHITE
				if (isSelected and state == 3):
					style = colorama.Back.WHITE + colorama.Fore.BLACK
				print_func(style + self.label + colorama.Style.RESET_ALL)
				
	def handleInput(self, key):
		match (key.name):
			case "enter":
				if(self.callback):
					self.callback(self.data)
		return False
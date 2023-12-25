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
			if (type(state) == int and state == 0):
				print_func(colorama.Fore.WHITE + button.text + colorama.Style.RESET_ALL)
			elif (type(state) == int and state == 1):
				print_func(colorama.Fore.BLUE + button.text + colorama.Style.RESET_ALL)
			elif (state == False):
				print_func(colorama.Fore.LIGHTBLACK_EX + button.text + colorama.Style.RESET_ALL)
			else:
				if (i == self.selected_index):
					print_func(colorama.Back.WHITE + colorama.Fore.BLACK + button.text + colorama.Style.RESET_ALL)
				else:
					print_func(button.text)
			


	def handleInput(self, key):
		initial_selected_index = self.selected_index
		match (key.name):
			case "up":
				if (self.selected_index == 0):
					self.selected_index = len(self.buttons) - 1
				else:
					self.selected_index -= 1
				
			case "down":
				if (self.selected_index == len(self.buttons) - 1):
					self.selected_index = 0
				else:
					self.selected_index += 1

			case "enter":
				self.buttons[self.selected_index].click()

			case _:
				return False
		return initial_selected_index != self.selected_index

	
class Button:
	def __init__(self, text, callback=None):
		self.text = text
		self.callback = callback
	
	def click(self):
		if self.callback:
			self.callback()

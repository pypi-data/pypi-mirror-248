import os

class VStack:
	def __init__(self):
		self.children = []
		self.selected_index = 0
		self.previewing = False
		
	def add(self, child):
		self.children.append(child)
	
	def render(self):
		os.system("cls")
		for child in self.children:
			if (self.previewing):
				param = 0
				if (child == self.children[self.selected_index]):
					param = 1
				child.render(print, param)

			else:
				child.render(print, child == self.children[self.selected_index])

	def handleKeyPress(self, key):
		if (key.event_type != "down"):
			return

		if (self.previewing):
			match (key.name):
				case "up":
					if (self.selected_index == 0):
						self.selected_index = len(self.children) - 1
					else:
						self.selected_index -= 1
					
				case "down":
					if (self.selected_index == len(self.children) - 1):
						self.selected_index = 0
					else:
						self.selected_index += 1

				case "enter":
					self.previewing = False

			self.render()

		else:
			if (key.name == "esc"):
				self.previewing = True
				self.render()
				return

			if (self.children[self.selected_index].handleInput(key)):
				self.render()
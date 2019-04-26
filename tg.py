#!/usr/bin/env python3

import os # popen("stty size")
from math import sin, cos, pi

def clamp(a, b, value):
	return max(a, min(b, value))

class Window:
	def __init__(self):
		rows, cols = os.popen("stty size", "r").read().split()

		width = int(cols)
		height = int(rows)

		self.width = width
		self.height = height

		self.cursorx = 0
		self.cursory = 0

		# Frame timer. Used to check if the terminal has been resized.
		self.frame = 0
	
	def dot(self, x, y, color):
		if clamp(0, self.height - 1, y) == y:
			if clamp(0, self.width - 1, x) == x:
				self.grid[int(y)][int(x)]["fill"] = color
	
	def char(self, x, y, char, color):
		if clamp(0, self.height - 1, y) == y:
			if clamp(0, self.width - 1, x) == x:
				self.grid[int(y)][int(x)]["stroke"] = color
				self.grid[int(y)][int(x)]["char"] = char

	def write(self, *args):
		if len(args) == 2:
			x = self.cursorx
			y = self.cursory
			string = args[0]
			color = args[1]
		if len(args) == 4:
			x = args[0]
			y = args[1]
			string = args[2]
			color = args[3]

		for i in range(len(string)):
			self.char(x + i, y, string[i], color)

			self.cursorx = x + i + 1
		self.cursory = y
	
	def raytrace(self, x0, y0, x1, y1, color):
		dx = abs(x1 - x0)
		dy = abs(y1 - y0)
		x = x0
		y = y0
		n = 1 + dx + dy
		x_inc = (x1 > x0) and 1 or -1
		y_inc = (y1 > y0) and 1 or -1
		error = dx - dy
		dx *= 2
		dy *= 2

		while n > 0:
			n -= 1

			self.dot(x, y, color)

			if error > 0:
				x += x_inc
				error -= dy
			else:
				y += y_inc
				error += dx

	def line(self, x1, y1, x2, y2, color, end=True):
		self.dot(x1, y1, color)
		if end:
			self.dot(x2, y2, color)

		self.raytrace(x1, y1, x2, y2, color)
	
	def circle(self, x, y, r, color, fill=None, double=True):
		distance = r

		# d == 2 if double == True
		# d == 1 if double == False
		d = double and 2 or 1

		if fill:
			a = []
			for i in range(r * 2):
				a.append(i / 2)
			for j in a:
				for i in range(360):
					angle = (i / 360) * (2 * pi)
					
					self.dot(x + cos(angle) * j * d, y + sin(angle) * j, fill)

		for i in range(360):
			angle = (i / 360) * (2 * pi) # Radians

			self.dot(x + cos(angle) * r * d, y + sin(angle) * r, color)

	def ellipse(self, x1, y1, x2, y2, color):
		dx = x1 - x2
		dy = y1 - y2

		x = (x1 + x2) / 2
		y = (y1 + y2) / 2

		for i in range(360):
			angle = (i / 360) * (2 * pi)

			self.dot(x + cos(angle) * dx, y + sin(angle) * dy, color)

	def rect(self, x1, y1, x2, y2, color, fill=None):
		if fill:
			# Ugh. Fill in the rectangle with the color.
			for i in range(y1, y2):
				self.line(x1, i, x2, i, fill)

		self.line(x1, y1, x2, y1, color) # -----
		self.line(x1, y1, x1, y2, color) # |
		self.line(x2, y1, x2, y2, color) #     |
		self.line(x1, y2, x2, y2, color) # -----

	def display(self):
		# Window size checking.
		self.frame += 1
		if self.frame % 1 == 0:
			# Resize it.
			rows, cols = os.popen("stty size", "r").read().split()

			self.width = int(cols)
			self.height = int(rows)

		for i in range(self.height):
			for j in range(self.width):
				fill = self.grid[i][j]["fill"]
				stroke = self.grid[i][j]["stroke"]
				
				# Start printing with self.fillColor
				# Set Background Color
				r = fill[0]
				g = fill[1]
				b = fill[2]

				print("\x1b[48;2;{0};{1};{2}m".format(r, g, b), end="")

				# Set Foreground Color
				r = stroke[0]
				g = stroke[1]
				b = stroke[2]
				
				print("\x1b[38;2;{0};{1};{2}m".format(r, g, b), end="")

				# Print out a space
				print(self.grid[i][j]["char"], end="")

			# Don't start a new line if this is the last line
			if i != self.height - 1:
				print()
	
	def clear(self):
		# Reset the grid
		self.grid = []

		for i in range(self.height):
			g = []
			for j in range(self.width):
				g.append({ "fill": [0, 0, 0], "stroke": [255, 255, 255], "char": " "})
			self.grid.append(g)
	
	def backspace(self):
		# Seeks to the start of the terminal
		print("\033[F" * self.height, end="")

if __name__ == "__main__":
	# We're testing it
	window = Window()

	window.clear()

	while True:
		window.clear()

		window.circle(40, 40, 10, (0, 255, 0), (0, 150, 0))

		window.rect(17, 18, 56, 22, (70, 20, 20), (30, 6, 6))

		window.write(20, 20, "Hello, player. Your name is ", (255, 255, 255))
		window.write("Slime", (255, 0, 0))
		window.write("?", (255, 255, 255))

		window.display()
		window.backspace()


import os
import sys

os.chdir(sys.path[0])
sys.path.insert(1, "P://Python Projects/assets/")

from GUI import *

# arbitrary
divisor = 100

class Circle:
	allCircles = []

	def __init__(self, radius, start_angle, end_angle, color, translate=[width // 2, height // 2], step=1):
		n = radius / divisor
		self.vectices = []
		Circle.allCircles.append(self)
	
		for angle in range(int(start_angle * n), int(end_angle * n), step):
			theta = radians(angle / n)

			x = radius * cos(theta)
			y = radius * sin(theta)

			Point(x + translate[0], y + translate[1], color, 1, lists=[self.vectices])

	def Draw(self):
		for vertex in self.vectices:
			vertex.Draw()


class Ellipse:
	allElipses = []

	def __init__(self, radius_a, radius_b, start_angle, end_angle, color, translate=[width // 2, height // 2], step=1):
		n_a = radius_a / divisor
		n_b = radius_b / divisor
		n = max(n_a, n_b)
		Ellipse.allElipses.append(self)

		self.vectices = []

		for angle in range(int(start_angle * n), int(end_angle * n), step):
			theta_a = radians(angle / n)
			theta_b = radians(angle / n)

			x = radius_a * cos(theta_a)
			y = radius_b * sin(theta_b)

			Point(x + translate[0], y + translate[1], color, 1, lists=[self.vectices])

	def Draw(self):
		for vertex in self.vectices:
			vertex.Draw()


def sgn(angle):
	if angle > 0:
		return 1
	elif angle < 0:
		return -1
	else:
		return 0


class SuperEllipse:
	allSuperElipses = []

	def __init__(self, radius_a, radius_b, start_angle, end_angle, color, index, translate=[width // 2, height // 2], step=1):
		n_a = radius_a / divisor
		n_b = radius_b / divisor
		self.n = max(n_a, n_b)

		self.color = color

		self.start_angle = start_angle
		self.end_angle = end_angle
		self.step = step
		self.index = index
		self.radius_a = radius_a
		self.radius_b = radius_b
		self.translate = translate

		self.indexSlider = Slider((5, 5, width - 10, 50), (lightBlack, darkWhite), buttonData={"activeColor": lightRed}, inputData={"onValueChange": self.CreatePoints})
		self.indexLabel = Label((5, 60, 300, 50), (lightBlack, darkWhite), text=str(self.index), textData={"fontSize": 16})

		self.CreatePoints()

		SuperEllipse.allSuperElipses.append(self)

	def CreatePoints(self, index=None):
		if index == None:
			index = self.index

		else:
			# when 2 add .075 to account for slider inaccuracy 
			index = Map(index, 0, 1, 0, 3)

		self.vectices = []

		for angle in range(int(self.start_angle * self.n), int(self.end_angle * self.n), self.step):
			theta_a = radians(angle / self.n)
			theta_b = radians(angle / self.n)

			x = pow(abs(cos(theta_a)), abs(index)) * self.radius_a * sgn(cos(theta_a))
			y = pow(abs(sin(theta_b)), abs(index)) * self.radius_b * sgn(sin(theta_b))
			

			Point(x + self.translate[0], y + self.translate[1], self.color, 1, lists=[self.vectices])

		try:
			txt = str(round(2 / index, 2)).ljust(8, "0")
			txt = txt.zfill(8)
			self.indexLabel.UpdateText(txt)
		except ZeroDivisionError:
			self.indexLabel.UpdateText("Infinte")


	def Draw(self):
		for i, vertex in enumerate(self.vectices):
			pg.draw.line(screen, self.color, (vertex[0], vertex[1]), (self.vectices[i - 1][0], self.vectices[i - 1][1]))



# Circle(200, 0, 360, white)
# Ellipse(200, 100, 0, 360, white)
SuperEllipse(200, 200, 0, 360, white, 8)

def DrawLoop():
	screen.fill(darkGray)

	DrawAllGUIObjects()
	
	for circle in Circle.allCircles:
		circle.Draw()
	
	for ellipse in Ellipse.allElipses:
		ellipse.Draw()	

	for superEllipse in SuperEllipse.allSuperElipses:
		superEllipse.Draw()

	pg.display.update()


def HandleEvents(event):
	HandleGui(event)

def Update():	
	pass	

while running:
	clock.tick_busy_loop(fps)

	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				running = False

		HandleEvents(event)
	
	Update()
	DrawLoop()

import tkinter
from tkinter import ttk
import math
import datetime

# Physical Consts
mainMassRadius = float(6378.136)  # km

startingHeight = float(404)  # km
startingVelocityX = float(7.667)  # km/s
startingVelocityY = float(0)  # km/s

gravConstant = 6.6740831313131 * pow(10, -11)  # m3/kg*s2
mainMass = 5.9722 * pow(10, 24)  # kg

metersPerKm = 1000
gravAcceleration = gravConstant * mainMass / pow(mainMassRadius * metersPerKm, 2)
gravFactor = gravConstant * mainMass / pow(metersPerKm, 3)  #
heightFromCentre = mainMassRadius + startingHeight

# Model Consts
time = int(0)  # s
timeIncrement = float(1)  # s
modelDelay = int(1)  # ms
orbitTime = 0  # s
lastOrbitTime = 0  # s

windowSizeX = 800  # pixels
windowSizeY = 600  # pixels
pixelsPerKm = float(1 / 30)  # pixels/km

drawMassRadius = int(mainMassRadius * pixelsPerKm)

currentDirection = 1

# Draw Application
root = tkinter.Tk()
root.title('Astro')
canvas = tkinter.Canvas(root)
canvas.grid(row=0, columnspan=7)
canvas.config(width=windowSizeX, height=windowSizeY, bg='white')

# Draw Main Mass
drawMassCentreX = windowSizeX / 2
drawMassCentreY = windowSizeY / 2
canvas.create_oval(drawMassCentreX - drawMassRadius, drawMassCentreY - drawMassRadius,
                   drawMassCentreX + drawMassRadius, drawMassCentreY + drawMassRadius)

# Draw Object
startingX = float(0)
startingY = float(-heightFromCentre)
positionX = startingX
positionY = startingY
velocityX = startingVelocityX
velocityY = startingVelocityY
totalVelocity = startingVelocityX
minVelocity = startingVelocityX
maxVelocity = startingVelocityX
minHeight = float(heightFromCentre)
maxHeight = float(heightFromCentre)
x = drawMassCentreX + positionX * pixelsPerKm
y = drawMassCentreY + positionY * pixelsPerKm
noOfOrbits = 0;


class DisplayParams:
    def __init__(self, canvas):
        # Display 100 pixels scale
        canvas.create_line(20, windowSizeY / 2 - 100, 20, windowSizeY / 2, width=1)
        canvas.create_line(17, windowSizeY / 2 - 100, 24, windowSizeY / 2 - 100, width=1)
        canvas.create_line(17, windowSizeY / 2, 24, windowSizeY / 2, width=1)
        self.text_scale = canvas.create_text(25, windowSizeY / 2 - 50, anchor='nw')
        canvas.itemconfig(self.text_scale, text=str(100 / pixelsPerKm) + 'km')

        # Display parameters
        self.textAccel = canvas.create_text(10, 10, anchor='nw')
        canvas.itemconfig(self.textAccel, text='Acceleration: ' + str(gravAcceleration))
        self.textTime = canvas.create_text(10, 30, anchor='nw')
        self.textOrbitTime = canvas.create_text(10, 45, anchor='nw')
        self.textNoOrbits = canvas.create_text(10, 60, anchor='nw')

        self.textHeight = canvas.create_text(10, 80, anchor='nw')
        self.textMinHeight = canvas.create_text(10, 95, anchor='nw')
        self.textMaxHeight = canvas.create_text(10, 110, anchor='nw')

        self.textVelocity = canvas.create_text(10, 130, anchor='nw')
        self.textMinVelocity = canvas.create_text(10, 145, anchor='nw')
        self.textMaxVelocity = canvas.create_text(10, 160, anchor='nw')

    def update(self):
        canvas.itemconfig(self.textTime, text='Time: ' + str(datetime.timedelta(seconds=time)))
        canvas.itemconfig(self.textOrbitTime, text='Orbit Time: ' + str(datetime.timedelta(seconds=orbitTime)))
        canvas.itemconfig(self.textNoOrbits, text='No of Orbits: ' + str(noOfOrbits))

        canvas.itemconfig(self.textHeight, text='Height: ' + str(heightFromCentre - mainMassRadius))
        canvas.itemconfig(self.textMinHeight, text='Min Height: ' + str(minHeight - mainMassRadius))
        canvas.itemconfig(self.textMaxHeight, text='Max Height: ' + str(maxHeight - mainMassRadius))

        canvas.itemconfig(self.textVelocity, text='Velocity: ' + str(totalVelocity))
        canvas.itemconfig(self.textMinVelocity, text='Min Velocity: ' + str(minVelocity))
        canvas.itemconfig(self.textMaxVelocity, text='Max Velocity: ' + str(maxVelocity))


class Model:
    def __init__(self, canvas):
        self.canvas = canvas
        self.params = DisplayParams(self.canvas)
        self.calculate = Calculations()
        self.motion = False
        self.pointDefine(x, y)
        self.params.update()

    def pointDefine(self, x, y):
        self.lineY = canvas.create_line(x - 1, y, x + 2, y, width=5)
        self.lineX = canvas.create_line(x - 2, y, x + 3, y, width=3)

    def pointMove(self):
        self.params.update()
        self.calculate.updateVelocity()
        self.calculate.updatePosition()
        canvas.coords(self.lineY, x - 1, y, x + 2, y)
        canvas.coords(self.lineX, x - 2, y, x + 3, y)

    def draw(self):
        if self.motion == True:
            self.pointMove()
            self.canvas.after(modelDelay, self.draw)

    def start(self):
        self.motion = True
        self.draw()

    def stop(self):
        self.motion = False

    def reset(self):
        self.motion = False
        global positionX
        global positionY
        global heightFromCentre
        global velocityX
        global velocityY
        global totalVelocity
        global minVelocity
        global maxVelocity
        global minHeight
        global maxHeight
        global currentDirection
        global noOfOrbits
        global orbitTime
        global lastOrbitTime
        positionX = startingX
        positionY = startingY
        heightFromCentre = math.hypot(positionX, positionY)
        velocityX = startingVelocityX
        velocityY = startingVelocityY
        totalVelocity = startingVelocityX
        minVelocity = startingVelocityX
        maxVelocity = startingVelocityX
        minHeight = float(heightFromCentre)
        maxHeight = float(heightFromCentre)
        currentDirection = 1
        noOfOrbits = 0;
        orbitTime = 0
        lastOrbitTime = 0
        self.pointMove()

    def speedUp(self):
        global velocityX
        global velocityY
        if velocityX >= 0:
            velocityX += velocityX * 0.1
        else:
            velocityX -= velocityX * 0.1
        if velocityY >= 0:
            velocityY += velocityY * 0.1
        else:
            velocityY -= velocityY * 0.1

    def slowDown(self):
        global velocityX
        global velocityY
        if velocityX >= 0:
            velocityX -= velocityX * 0.1
        else:
            velocityX += velocityX * 0.1
        if velocityY >= 0:
            velocityY -= velocityY * 0.1
        else:
            velocityY += velocityY * 0.1


class Calculations:
    def updateVelocity(self):
        global velocityX
        global velocityY
        global heightFromCentre
        global totalVelocity
        global minVelocity
        global maxVelocity
        global minHeight
        global maxHeight
        global currentDirection
        global noOfOrbits
        global orbitTime
        global lastOrbitTime
        heightFromCentre = math.hypot(positionX, positionY)
        velocityX -= gravFactor * positionX * timeIncrement / pow(heightFromCentre, 3)
        velocityY -= gravFactor * positionY * timeIncrement / pow(heightFromCentre, 3)
        if heightFromCentre <= mainMassRadius:
            model.stop()
        previousDirection = currentDirection
        if velocityY >= 0:
            currentDirection = 1
        else:
            currentDirection = -1
        if previousDirection < currentDirection:
            noOfOrbits += 1
            orbitTime = time - lastOrbitTime
            lastOrbitTime = time

        totalVelocity = math.hypot(velocityX, velocityY)
        minVelocity = min(minVelocity, totalVelocity)
        maxVelocity = max(maxVelocity, totalVelocity)
        minHeight = min(minHeight, heightFromCentre)
        maxHeight = max(maxHeight, heightFromCentre)

    def updatePosition(self):
        global positionX
        global positionY
        global x
        global y
        global time
        time += timeIncrement
        positionX += (velocityX * timeIncrement)
        positionY += (velocityY * timeIncrement)
        x = drawMassCentreX + positionX * pixelsPerKm
        y = drawMassCentreY + positionY * pixelsPerKm


model = Model(canvas)

ttk.Button(root, text="Run", command=model.start).grid(row=1, column=0)
ttk.Button(root, text="Stop", command=model.stop).grid(row=1, column=1)
ttk.Button(root, text="Step", command=model.pointMove).grid(row=1, column=2)
ttk.Button(root, text="Reset", command=model.reset).grid(row=1, column=3)
ttk.Button(root, text="+10%", command=model.speedUp).grid(row=1, column=4)
ttk.Button(root, text="-10%", command=model.slowDown).grid(row=1, column=5)
ttk.Button(root, text="future_func", command=model.stop).grid(row=1, column=6)

root.mainloop()

import random
import math
import tkinter as tk
from tkinter import Canvas, BOTH
import numpy as np

Boids = []
refresh = 20
n = 5
width = 1000
height = 1000
vlim = 15
sep_dist = 15
bcolour = '#191970'
bradius = 5
targetweight = 16
alignmentweight = 8
cohesionweight = 100
windintro = 300
windcycle = 250
targetintro = 700
targetcycle = 200

count = 0
target = np.array([0,0])
margins = 150
wind = np.array([0,0])
speed = 1

class Boid(object):
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

def draw_boids():
    graph.delete('all')
    global target
    #If wind is active, show wind speed at top
    if count >= windintro:
            arrowOrigin = 15
            graph.create_polygon(arrowOrigin - wind[1]*5, arrowOrigin + wind[0]*5, arrowOrigin + wind[1]*5, arrowOrigin - wind[0]*5,
                                 arrowOrigin + wind[0]*12, arrowOrigin + wind[1]*10, fill='black')
            graph.create_line(arrowOrigin, arrowOrigin, arrowOrigin - wind[0]*5, arrowOrigin - wind[1]*5)
            graph.create_text(100,15, text="WIND SPEED:")
            graph.create_text(150,15, text=speed)
    #If targetting is active, show targeting at top
    if count > targetintro:
            graph.create_oval(target[0], target[1], target[0]+5, target[1]+5, fill='black')
            graph.create_text(200,15, text="TARGETING")
    for boid in Boids:
            x1, y1 = (boid.position[0]-bradius), (boid.position[1]-bradius)
            x2, y2 = (boid.position[0]+bradius), (boid.position[1]+bradius)
            graph.create_oval(x1, y1, x2, y2, fill=bcolour, outline='')
            tail = boid.position - boid.velocity * 1
            graph.create_line(tail[0], tail[1], boid.position[0], boid.position[1], fill=bcolour, width=2)
    graph.update()

def createGraph():
        global graph
        count = 0
        root = tk.Tk()
        graph = tk.Canvas(root, width=width, height=height)
        graph.configure(background='#eecbad')
        graph.pack()
        graph.after(refresh, updateGraph())
        root.mainloop()

def move_all_boids_to_new_position():
    for b in Boids:
        v1 = rule1(b, n)
        v2 = rule2(b, n)
        v3 = rule3(b, n)
        v4 = boundPosition(b)
        if count >= targetintro:
            v5 = targetDirection(b)
        else:
            v5 = np.array([0,0])
        b.velocity = b.velocity + v1 + v2 + v3 + v4 + v5
        limitVelocity(b)
        if count >= windintro:
            b.velocity = b.velocity + wind * speed
        b.position = b.position+b.velocity

def updateGraph():
        global count
        global target
        #Change target after 200 iterations
        if count % targetcycle == 0:
            randomizeTarget()
        #Change wind after 250 iterations
        if count % windcycle == 0:
            changeWind()
        count = count + 1
        print(count)
        draw_boids()
        move_all_boids_to_new_position()
        graph.after(refresh, lambda: updateGraph())

def initializeBoids(n):
        for i in range(n):
                pos = random_pos()
                vel = np.array([0,0])
                b = Boid(pos, vel)
                Boids.append(b)

def random_pos():
        return np.array([random.randint(1,width), random.randint(1, height)])

def boundPosition(b):
        #Setting boids boundaries
        xmin = margins
        xmax = width - margins
        ymin = margins
        ymax = height - margins
        v = np.array([0,0])
        #Check if the boid is outside of the boundaries.
        if b.position[0] < 0:
                v[0] = 5
        elif b.position[0] > width:
                v[0] = -5
        elif b.position[0] < xmin:
                v[0] = xmin/(b.position[0]+1)
        elif b.position[0] > xmax:
                v[0] = -xmin/(width - b.position[0]+1)
        if b.position[1] < 0:
                v[1] = 5
        elif b.position[1] > height:
                v[1] = -5
        elif b.position[1] < ymin:
                v[1] = xmin/(b.position[1]+1)
        elif b.position[1] > ymax:
                v[1] = -xmin/(height - b.position[1]+1)
        return v

def limitVelocity(b):
        v = np.array([0,0])
        mag = np.linalg.norm(b.velocity)
        if mag > vlim:
                b.velocity = (b.velocity / mag) * vlim

# Cohesion
def rule1(boid, n):
    centerOfMass = np.array([0,0])
    for i in range(n):
            if not(Boids[i] == boid):
                    centerOfMass = centerOfMass + Boids[i].position
    centerOfMass = centerOfMass/(n-1)
    velocity = (centerOfMass - boid.position)/cohesionweight
    return velocity

# Separation
def rule2(boid, n):
    velocity = np.array([0,0])
    for i in range(n):
            if not(Boids[i] == boid):
                    distance = Boids[i].position - boid.position
                    if np.linalg.norm(distance) < sep_dist:
                            velocity = velocity - distance
    return velocity

# Alignment
def rule3(boid, n):
        velocity = np.array([0,0])
        for i in range(n):
                if not(Boids[i] == boid):
                        velocity = velocity + Boids[i].velocity
        velocity = velocity/(n-1)
        velocity = (velocity - boid.velocity)/alignmentweight
        return velocity

def randomizeTarget():
        global target
        target = np.array([random.randint(margins,width-margins), random.randint(margins, height-margins)])

def targetDirection(b):
        direction = target - b.position
        direction = direction/targetweight
        return direction

def changeWind():
        global wind
        global speed
        wind = np.array([random.randint(-100,100), random.randint(-100,100)])
        wind = wind/np.linalg.norm(wind)
        speed = random.randint(0,3)
        
def main():
    initializeBoids(n)
    createGraph()
    
main()
    

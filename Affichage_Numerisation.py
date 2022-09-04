# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 10:24:57 2022

@author: Pierre-Alexandre
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import colorama
import time
import imageio

def progressBar(progress, total, prevTime, color=colorama.Fore.YELLOW):
    currentTime = time.time()
    progressSpeed = 1
    if progress == 0:
        prevTime = time.time()
    else:
        if currentTime != prevTime:
            progressSpeed = 1 / (currentTime - prevTime)
        else:
            progressSpeed = np.Inf
        prevTime = currentTime
    percent = 100 * progress / float(total)
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    if int(percent) == 100:
        print(colorama.Fore.GREEN + f'\r|{bar}| {percent:.2f}%, {progressSpeed:.2f} It/s')
        print(colorama.Fore.RESET)
    else:
        print(color + f'\r|{bar}| {percent:.2f}%, {progressSpeed:.2f} It/s', end='\r')

"""Class containing members and methods to plot digitisations"""
class Digitisation:
    def __init__(self, filename):
        try:
            f = open(filename, 'r')
        except:
            sys.exit(-1)
            
        self.filename = filename
        
        self.lines = []
        i = 0
        for line in f:
            digitizedLine = DigitisedLine(line)
            #digitizedLine.saveLine(i, "")
            self.lines.append(digitizedLine)
            i+=1
            #if i == 300:
            #    break
            
        
        print("Begin plotting :")
        progressBar(0, len(self.lines), 0)
        self.Xlines = np.array([])
        self.Ylines = np.array([])
        self.Zlines = np.array([])
        self.XCenters = np.array([])
        self.YCenters = np.array([])
        self.ZCenters = np.array([])
        for i in range(0, len(self.lines)):
            previousTime = time.time()
            self.Xlines = np.append(self.Xlines, [point[0] for point in self.lines[i].points])
            self.Ylines = np.append(self.Ylines, [point[1] for point in self.lines[i].points])
            self.Zlines = np.append(self.Zlines, [point[2] for point in self.lines[i].points])
            self.XCenters = np.append(self.XCenters, [self.lines[i].center[0]])
            self.YCenters = np.append(self.YCenters, [self.lines[i].center[1]])
            self.ZCenters = np.append(self.ZCenters, [self.lines[i].center[2]])
            progressBar(i, len(self.lines), previousTime)
        progressBar(len(self.lines), len(self.lines), previousTime)
        
    def rotateAllLines(self, rx, ry, rz):
        progressBar(0, len(self.lines), 0)
        self.Xlines = np.array([])
        self.Ylines = np.array([])
        self.Zlines = np.array([])        
        for i in range(0, len(self.lines)):
            previousTime = time.time()
            self.lines[i].rotateLine(rx, ry, rz)
            self.Xlines = np.append(self.Xlines, [point[0] for point in self.lines[i].points])
            self.Ylines = np.append(self.Ylines, [point[1] for point in self.lines[i].points])
            self.Zlines = np.append(self.Zlines, [point[2] for point in self.lines[i].points])
            progressBar(i, len(self.lines), previousTime)
        progressBar(len(self.lines), len(self.lines), previousTime)
            
    def plotLines(self, divider):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        X = [self.Xlines[i] for i in range(0, len(self.Xlines), divider)]
        Y = [self.Ylines[i] for i in range(0, len(self.Ylines), divider)]
        Z = [self.Zlines[i] for i in range(0, len(self.Zlines), divider)]
        popList = []
        for i in range(len(X)):
            if Z[i] > -221:
                popList.append(i)
        
        for i in range(len(popList)):
            X.pop(popList[i] - i)
            Y.pop(popList[i] - i)
            Z.pop(popList[i] - i)
        plt.colorbar(ax.scatter(X, Y, Z, s=1, c=Z, cmap='magma'))
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title(self.filename)
        
        #ax.set_xlim3d(300, max(self.Xlines))
        #ax.set_ylim3d(0, 250)
        #ax.set_zlim3d(-250, -200)
        plt.show()
        
    def imgSaveLines(self, filename, title):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        plt.colorbar(ax.scatter(self.Xlines, self.Ylines, self.Zlines, s=1, c=self.Zlines, cmap="magma"))
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        #ax.set_xlim3d(200, 600)
        #ax.set_ylim3d(0, 250)
        #ax.set_zlim3d(-250, -200)
        ax.set_title(self.filename + title)
        plt.savefig("Images/" + str(filename))
        plt.close()
        
    def plotCenter(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        plt.colorbar(ax.scatter(self.XCenters, self.YCenters, self.ZCenters, s=1, c=self.ZCenters, cmap="magma"))
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title(self.filename)
        #ax.set_xlim3d(200, 600)
        #ax.set_ylim3d(0, 250)
        #ax.set_zlim3d(-250, -200)
        plt.show()
        
"""Class used to manipulate a single digitised line"""
class DigitisedLine:
    def __init__(self, lineString):
        lineString = lineString.replace(',', '.')
        lineStringSplit = lineString.split()
        lineNumbers = [float(x) for x in lineStringSplit]
        point = [0, 0, 0]
        point[0] = lineNumbers[0]
        point[1] = lineNumbers[1]
        point[2] = lineNumbers[2]
        self.points = np.array([point])
        for i in range(1, len(lineNumbers)):
            point[i%3] = lineNumbers[i]
            if i % 3 == 2:
                self.points = np.concatenate((self.points, np.array([point])))
        self.center = self.points.mean(0)
        
        """images = []
        for i in range(361):
            self.rotateLine(np.pi / 180 , 0, 0)
            self.saveLine(i, "")
            images.append(imageio.imread("Images/"+str(i)+".png"))
        imageio.mimsave('./linesRotation.gif', images)"""
    
    def rotateLine(self, rx, ry, rz):
        homogeneousCenter = np.array([np.append(self.center, 1)])
        rotationMatrixX = np.matrix([[1, 0,          0],
                                     [0, np.cos(rx), -np.sin(rx)],
                                     [0, np.sin(rx), np.cos(rx)]])
        
        rotationMatrixYprime = np.matrix([[np.cos(ry),  0, np.sin(ry)],
                                          [0,           1, 0],
                                          [-np.sin(ry), 0, np.cos(ry)]])
        
        rotationMatrixZsecond = np.matrix([[np.cos(rz), -np.sin(rz),    0],
                                           [np.sin(rz), np.cos(rz),     0],
                                           [0,          0,              1]])
        rotationMatrix = rotationMatrixX * rotationMatrixYprime * rotationMatrixZsecond
            
        homogeneousMatrix = np.concatenate((rotationMatrix, np.array([[0,0,0]])), axis=0)
        homogeneousMatrix = np.concatenate((homogeneousMatrix, homogeneousCenter.T), axis=1)
        for i in range(len(self.points)):
            homogeneousPoint = np.array([np.append(self.points[i] - self.center, 1)])
            newHomogeneousPoint = (homogeneousMatrix * homogeneousPoint.T).T
            self.points[i] = np.delete(newHomogeneousPoint, -1)
    
    def plotLine(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        X = [self.points[i][0] for i in range(len(self.points))]
        Y = [self.points[i][1] for i in range(len(self.points))]
        Z = [self.points[i][2] for i in range(len(self.points))]
        
        plt.colorbar(ax.scatter(X, Y, Z, s=1, c=Z, cmap='magma'))
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        
        
        ax.set_xlim3d(300, 650)
        #ax.set_ylim3d(0, 250)
        ax.set_zlim3d(-250, -200)
        
        plt.show()
        
    def saveLine(self, filename, title):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.view_init(0,0)
        X = [self.points[i][0] for i in range(len(self.points))]
        Y = [self.points[i][1] for i in range(len(self.points))]
        Z = [self.points[i][2] for i in range(len(self.points))]
        
        plt.colorbar(ax.scatter(X, Y, Z, s=1, c=Z, cmap='magma'))
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        
        ax.set_xlim3d(300, 650)
        ax.set_ylim3d(-50,  0)
        ax.set_zlim3d(-250, -200)
        
        ax.set_title(str(filename) + title)
        plt.savefig("Images/" + str(filename))
        plt.close()

if __name__ == "__main__":
    digit1 = Digitisation("points_vrai2.txt")
    #digit1.plotCenter()
    digit1.plotLines(1)
    """
    step = 90
    for angle in range(0, 360, step):
        digit1.rotateAllLines(step * np.pi / 180, 0, 0)
        digit1.plotLines(20)#("rx" + str(angle) + ".png", r"Numérisation : $R_x = {}$".format(angle))
    digit1.rotateAllLines(np.pi / 2, 0, 0)
    
    for angle in range(0, 360, step):
        digit1.rotateAllLines(0, step * np.pi / 180, 0)
        digit1.plotLines(50)#("ry" + str(angle) + ".png", r"Numérisation : $R_y = {}$".format(angle))
    digit1.rotateAllLines(0, np.pi / 2, 0)
    
    for angle in range(0, 360, step):
        digit1.rotateAllLines(0, 0, step * np.pi / 180)
        digit1.plotLines(50)#("rz" + str(angle) + ".png", r"Numérisation : $R_z = {}$".format(angle))
"""
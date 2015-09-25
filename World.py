import numpy as np

class World():
    def __init__(self, sizeX, sizeY, scale = 1):
        #Saved Data
        self.Layers = ["Map", "Collisions", "Sphero", "Dog"]
        self.W = [np.zeros([sizeX,sizeY]) for i in self.Layers]
        self.SCALE = scale #in meters/block
        self.sizeX = sizeX
        self.sizeY = sizeY

        #Easy Names
        self.MAP = self["Map"]
        self.COLLISIONS = self["Collisions"]
        self.SPHERO = self["Sphero"]
        self.DOG = self["Dog"]

        #Fill
        self.SPHERO.fill(1./(sizeX*sizeY))
        self.DOG.fill(1./(sizeX*sizeY))
        self.COLLISIONS.fill(.5)
        self.MAP[0,:].fill(1)
        self.MAP[:,0].fill(1)
        self.MAP[-1,:].fill(1)
        self.MAP[:,-1].fill(1)
        
    def updateCollisions(self, collision = True):
        a1 = self.SPHERO
        a2 = self.COLLISIONS
        if collision:
            self.COLLISIONS = a1+(1-a1)*a2 #updates point-by-point favoring a1
            self.senseH()
        else:
            self.COLLISIONS = (1-a1)+(1-a1)*a2 #updates point-by-point favoring a2
            self.senseL()

    def __getitem__(self, key):
        i = self.Layers.index(key)
        return self.W[i]

    def move(self, vector):
        dX, dY = np.floor(vector[0]), np.floor(vector[1])
        diff = np.array(vector)-np.array([dX,dY])
        while dX != 0 and dY != 0:
            if dX > 0:
                self._move([1,0])
                dX -= 1
            else:
                self._move([-1,0])
                dX += 1
            if dY > 0:
                self._move([0,1])
                dY -= 1
            else:
                self._move([0,-1])
                dY += 1
        return diff

    #vector: takes one 1 and one 0, represents a quadrant
    def _move(self, vector):
        dX, dY = vector[0], vector[1]
        S = np.shape(self.SPHERO)
        newLoc = np.zeros(S)
        for x in range(S[0]-dX):
            for y in range(S[1]-dY):
                newLoc[x+dX,y+dY]=self.SPHERO[x,y]
        self.SPHERO = newLoc
        return newLoc

    def senseH(self):
        #Put a high uniform neighboring inside on walls
        S = np.shape(self.MAP)
        newMap = np.zeros(S)
        for x in S[0]:
            for y in S[1]:
                if neighbors(self.MAP,[x,y]).contains(1):
                    newMap[x,y] = 1

        #Sum normalized collisions
        newMap += normalize(self.COLLISIONS)
        
        #normalize
        newMap = normalize(newMap)
        
        #multiply by SPHERO
        newMap *= self.SPHERO

        #set SPHERO and return
        self.SPHERO = newMap
        return newMap

    def senseL(self):
        #Put a high uniform neighboring inside on walls
        S = np.shape(self.MAP)
        newMap = np.zeros(S)
        for x in S[0]:
            for y in S[1]:
                if neighbors(self.MAP,[x,y]).contains(1):
                    newMap[x,y] = 1

        #Sum normalized collisions
        newMap += normalize(self.COLLISIONS)
        
        #normalize
        newMap = normalize(newMap)
        
        #inverse
        newMap = inverse(newMap)
        
        #multiply by SPHERO
        newMap *= self.SPHERO

        #set SPHERO and return
        self.SPHERO = newMap
        return newMap
            

##    def moveSphero(self, velocity, dT, collision = True):
##        SmallP = .1
##        Delta = np.round(np.array(velocity))*dT/self.SCALE
##        x, y = Delta[0], Delta[1]
##        newSphero = self.SPHERO[:]
##
##        #For every location in Sphero, move it by x,y, taking MAP into account
##        for x1 in range(np.shape(self.SPHERO)[0]):
##            for y1 in range(np.shape(self.SPHERO)[1]):
##                #Colide with Walls
##                if collision:
##                    #treat out of bounds as collision
##                    while x1+x >= self.sizeX:
##                        x -= 1
##                    while y1+y >= self.sizeY:
##                        y -= 1
##                    last = (x1,y1)
##                    #print last, x, y
##                    for x2 in range(x+1):
##                        for y2 in range(y+1):
##                            #print self.MAP[x1+x2,y1+y2]
##                            if self.MAP[x1+x2,y1+y2] != 1:
##                                last = (x1+x2,y1+y2)
##                    print last, (x1, y1)
##                    newSphero[last[0],last[1]] += self.SPHERO[x1,y1]
##                        
##                elif x1+x < self.sizeX and y1+y < self.sizeY: #delete out-of-bounds
##                    newSphero[x1+x, y1+y]+=self.SPHERO[x1,y1]
##                
##                
##        #convolve newSphero with error distribution
##        self.SPHERO = normalize(newSphero[:])
##        return self.SPHERO

def normalize(A):
    return A/sum(A)

def inverse(A):
##    S = np.shape(A)
##    invA = np.zeros(S)
##    for x in range(S[0]):
##        for y in range(S[1]):
##            invA[x,y] = 1-A[x,y]
##    return invA
    return 1-A

def neighbors(A,loc):
    out = []
    for v in [(1,1),(1,0),(0,1),(-1,0),(0,-1),(-1,-1)]:
        try:
            out.append(A[v[0]+loc[0],v[1]+loc[1]])
        except KeyError:
            pass
        
W = World(5,5)

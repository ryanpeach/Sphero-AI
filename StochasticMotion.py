from PIL import Image
import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def stochastic_value(grid, costML, goal, cost_step, collision_cost, incentive, N=10, tol = .001, vec_out = False):
    from scipy.signal import convolve2d
    
    # Puts the walls back in after convolution
    wall = np.vectorize(lambda x, y: y if y > 0 else x)
    
    # Gets the policy matrix
    if vec_out:
        p = np.vectorize(vec_policy)
    else:
        p = np.vectorize(calc_policy)                           
    
    # The main method
    value, change, i = grid, grid, 0
    while i < N and np.max(change) > tol:
        # Generating possibilities from rotations
        possibilities = []
        for costM in costML:
            update = convolve2d(value, costM, mode='same', boundary='fill', fillvalue=collision_cost)
            update = update + cost_step
            update = wall(update,grid)
            possibilities.append(update)
            #print(update)
            
        # Mixing all grids
        m1 = possibilities[0]
        for m2 in possibilities[1:]:
            m1 = np.minimum(m1,m2)

        replaced = m1[goal]
        m1[goal] = incentive
        
        #print(m1)
        i += 1
        change = np.abs(m1 - value)
        y,x = goal
        #print(change[y-20:y+10,x-5:x+5])
        #print(np.max(change))
        value = m1
    
    value[goal] = replaced
    
    # Sometimes, the goal doesn't overcome the cost of collision, in that case,
    # only part of the map will gradient towards the goal, the rest will prefer collision
    if np.max(value) > collision_cost:
        raise ValueError("Goal did not propogate, decrease collision_cost.")
        
    # Generate arrays for policy
    i, j = value.shape
    padded = np.ones((i+1,j+1))*collision_cost*1000
    padded[0:i,0:j] = value

    u = np.roll(padded,1,axis=0)[0:i,0:j]
    r = np.roll(padded,-1 ,axis=1)[0:i,0:j]
    l = np.roll(padded,1,axis=1)[0:i,0:j]
    d = np.roll(padded,-1 ,axis=0)[0:i,0:j]

    policy = p(value,u,r,l,d,grid)
    
    if not vec_out:
        policy[goal] = 'x'
    
    return value, policy
    
        
def calc_policy(x,u,r,l,d,g):
    best = min(u,r,l,d)
    if g <= 0:
        if x == 0:
            return 'x'
        else:
            if u == best:
                return '^'
            elif r == best:
                return '>'
            elif l == best:
                return '<'
            elif d == best:
                return 'v'
    else:
        return 'w'
        
def vec_policy(x,u,r,l,d,g):
    best = min(u,r,l,d)
    if g <= 0:
        if x == 0:
            return (0,0)
        else:
            if u == best:
                return (0,1)
            elif r == best:
                return (1,0)
            elif l == best:
                return (-1,0)
            elif d == best:
                return (0,-1)
    else:
        return (0,0)
    

def test():
    grid = np.array([[0, 1, 1, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 1, 1, 0]])
                     
    costM = np.array([[0.  ,.5,0.  ],
                      [.25  ,0. ,.25],
                      [0.  ,0. ,0.  ]])
    costM /= np.sum(costM)  # Cost Matrix must be normalized
                      
    # Generating rotation matricies
    rotML = [np.rot90(costM,i) for i in range(4)]
    
    # Some other necessary values
    goal = (0, 0)
    cost_step = 1
    collision_cost = 255
    grid *= collision_cost

    val, policy = stochastic_value(grid, rotML, goal, cost_step, collision_cost, incentive = 0)

    return val, policy
    
def apartment(w1=100):
    from random import randint
    
    # Import the map from Map.png
    apt_map = Image.open("Map.png")
    apt_map = apt_map.convert('L')
    
    # Resize, maintaining aspect ratio
    w0, h0 = apt_map.size
    h1 = int(float(h0)/float(w0)*w1)
    apt_map = apt_map.resize((w1,h1))
    
    # Convert to an array
    M = np.array(apt_map)
    M = M[:,:]
    t = np.vectorize(lambda x: 1. if x<255 else 0.)
    grid = t(M)
    
    costM = np.array([[2,3,4,3,2],
                      [3,4,5,4,3],
                      [2,3,1,3,2],
                      [1,2,1,2,1],
                      [0,1,0,1,0]],dtype='float64')

    costM /= np.sum(costM)  # Cost Matrix must be normalized
 
    # Generating rotation matricies
    rotML = [np.rot90(costM,i) for i in range(4)]
    
    # Some other necessary values
    cost_step = 1.
    collision_cost = 1

    grid *= collision_cost  # Use the collision_cost as the wall value
    
    # Find a random goal
    goal = (randint(0,grid.shape[0]-1), randint(0,grid.shape[1]-1))
    while grid[goal] != 0:   # While the goal is not a wall
        goal = (randint(0,grid.shape[0]-1), randint(0,grid.shape[1]-1))
    
    # Run the stochasic pathfinder
    val, policy = stochastic_value(grid, rotML, goal, cost_step, collision_cost, N=1000, incentive = -1e10, tol = .1, vec_out = True)
    px, py = policy
    
    # Plot it
    #X, Y = np.meshgrid([y for y in range(grid.shape[0])], [x for x in range(grid.shape[1])])
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.imshow(apt_map)
    plt.pcolor(val,cmap=plt.cm.Reds)
    plt.colorbar()
    plt.quiver(px,py)
    c = plt.Circle((goal[1],goal[0]), radius=1, color='r')
    ax.add_patch(c)
    
    plt.savefig('plot.png')
    
if __name__=="__main__":
    # Run Method Tests
    val, policy = test()
    a = (np.round(val) == np.array([[ 137.,  255.,  255.,  160.],
                                    [  18.,   24.,   35.,   68.],
                                    [  31.,   24.,   29.,   46.],
                                    [  64.,   36.,   38.,   70.],
                                    [ 159.,  255.,  255.,  161.]])).all()
    b = (policy == np.array([['x', 'w', 'w', 'v'],
                             ['>', '<', '<', '<'],
                             ['^', '^', '<', '<'],
                             ['^', '^', '^', '<'],
                             ['^', 'w', 'w', '^']])).all()
    print("Testing stochastic_value: Value: {0}, Policy: {1}".format(a,b))
    #print(val)
    #print(policy)
    apartment()
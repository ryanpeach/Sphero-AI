# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that 
# returns two grids. The first grid, value, should 
# contain the computed value of each cell as shown 
# in the video. The second grid, policy, should 
# contain the optimum policy for each cell.
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

map = Image.open("Map.png")
M = np.array(map)
M = M[:,:,3]
t = np.vectorize(lambda x: 255 if x>0 else 0)
grid = t(M)

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

# ---------------------------------------------
#  Modify the function stochastic_value below
# --------------------------------------------        
def stochastic_value(grid,goal,cost_step,collision_cost,success_prob):
    def valid(loc,grid):
        x, y = loc
        if x >= 0 and y >= 0 and x < len(grid) and y < len(grid[x]) and grid[x][y] == 0:
            return True
        else:
            return False

    def run(loc):
        x, y = loc
        return [(x+x2,y+y2) for x2, y2 in delta]
    
    def rotate(L,n):
        return L[n:] + L[:n]

    def score(loc,M,P):
        failure_prob = (1.0 - success_prob)/2.0  # Probability(stepping left) = prob(stepping right) = failure_prob
        x,y = loc
        if tuple(loc) == tuple(goal):
            return 0, [0,0], M[x][y] != 0
        else:
            N = [l2 for l2 in run(loc)]
            vN, eN = [l2 for l2 in N if valid(l2,grid)], [l2 for l2 in N if not valid(l2,grid)]
            if len(vN) > 0:
                Scores   = [M[x2][y2] if (x2,y2) in vN else collision_cost for x2,y2 in N]
                L, R     = rotate(Scores,1), rotate(Scores,-1)
                V = [Scores[n] * success_prob + L[n] * failure_prob + R[n] * failure_prob + cost_step for n in range(len(Scores))]
                v = min(V)
                x2, y2 = N[V.index(v)]
                dx, dy = x2-x, y2-y
                p = [dy, dx]

                if v < M[x][y]:
                    return v,p,True
                else:
                    return M[x][y],P[x][y],False
            else:
                return M[x][y],P[x][y],False
    
    value = [[collision_cost for col in range(len(grid[0]))] for row in range(len(grid))]
    policy = [[[0,0] for col in range(len(grid[0]))] for row in range(len(grid))]
    
    changed = True
    n = 0
    while changed:
        n += 1
        changed = False
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                #print(x,y,len(grid),len(grid[x]))
                if valid((x,y),grid):
                    #print(x,y,len(grid),len(grid[x]))
                    new, p, c = score((x,y),value,policy)
                    if c:
                        value[x][y] = new
                        policy[x][y] = p
                        changed = True
    
    return value, policy

# ---------------------------------------------
#  Use the code below to test your solution
# ---------------------------------------------

#grid = [[0, 0, 0, 0],
#        [0, 0, 0, 0],
#        [0, 0, 0, 0],
#        [0, 1, 1, 0]]
goal = [30, 30] # Goal is in top right corner
cost_step = 1
collision_cost = 255
success_prob = 0.8
print(grid)
value,policy = stochastic_value(grid,goal,cost_step,collision_cost,success_prob)
#for row in value:
#    print row
#for row in policy:
#    print row

policy = np.array(policy)
print(policy)
#X, Y = np.meshgrid(M.shape)
plt.quiver(policy[:,:,0],policy[:,:,1])
plt.show()

# Expected outputs:
#
# [57.9029, 40.2784, 26.0665,  0.0000]
# [47.0547, 36.5722, 29.9937, 27.2698]
# [53.1715, 42.0228, 37.7755, 45.0916]
# [77.5858, 100.00, 100.00, 73.5458]
#
# ['>', 'v', 'v', '*']
# ['>', '>', '^', '<']
# ['>', '^', '^', '<']
# ['^', ' ', ' ', '^']
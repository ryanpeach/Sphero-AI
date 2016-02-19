class Particle:
  def __init__(self, map, shape, mass, score = 1, loc = None, vel = None):
    self.map   = map
    self.shape = shape
    self.mass  = mass
    self.score = score
    
    if loc is None:
      loc = (random.randint(0,map.height),random.randint(0,map.width))
    if vel is None:
      speed = random.randint(0,map.maxspeed)
      dir   = random.uniform(0,2*np.PI)
      vel = (speed*np.sin(dir),speed*np.cos(dir))
      
  def copy():
    return Particle(self.map, self.shape, self.mass, self.score, self.loc, self.vel)
    

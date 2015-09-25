from CoreLibrary import *

spheroAtt = {"Cornered": ["Danger", "True", "False"],
          "Near-Wall": bool,
          "Near-Dog": bool,
          "Near-Hiding": bool,
          "Collision": bool,
          "Caught": bool
          "Action": Script,
          "Location": (int,int),
          "Gyroscope": (int,int,int),
          "Accelerometer": (int,int,int),
          "Motor": (int,int)}

dogAtt = {"Dog-State": ["Laying-Down", "Standing", "Walking", "Running", "Jumping"],
       "Dog-Behavior": ["Chasing", "Searching", "Alert", "Tired"]
       "Location": (int,int),
       "SpeedVector": (int,int)}

Sphero = Frame(spheroAtt)
Dog = Frame(dogAtt)

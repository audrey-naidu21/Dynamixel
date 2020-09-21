from ax12a import *

motor1 = AX_12A(id = 1)
motor1.connect()
i = AX_12A.listInstances()
print(i)
pos = AX_12A.getAll('getPresentPosition')
nowpos = pos[0]
print(pos)
print(nowpos)
speed = AX_12A.setAll('setMovingSpeed', 100)
print(motor1.getMovingSpeed())
nowpos = nowpos+20
motor1.setGoalPosition(nowpos)

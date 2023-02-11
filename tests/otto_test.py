"""
Otto All moves python test 
OttDIY Python Project, 2020 | sfranzyshen
"""
import time
import ottolib.otto9 as otto9

Otto = otto9.Otto9()
# Otto.init(5, 12, 13, 14, True, 0, 1, 2, 3)
# Otto.init(5, 4, 0, 2, True, -1, -1, -1, -1)
# Otto.initHUMANOID(14, 12, 13, 15, 5, 4, True, -1, -1, -1, -1) # d1 mini pins
Otto.initHUMANOID(7, 9, 11, 12, 35, 33, True, -1, -1, -1, -1)  # s2 mini pins
Otto.home()

Otto.walk(2, 1000, 1)  # -- 2 steps, "TIME". IF HIGHER THE VALUE THEN SLOWER (from 600 to 1400), 1 FORWARD
Otto.walk(2, 1000, -1)  # -- 2 steps, T, -1 BACKWARD
Otto.turn(2, 1000, 1)  # -- 3 steps turning LEFT
Otto.home()
time.sleep_ms(100)
Otto.turn(2, 1000, -1)  # -- 3 steps turning RIGHT
Otto.bend(1, 500, 1)  # -- usually steps =1, T=2000
Otto.bend(1, 2000, -1)
Otto.shakeLeg(1, 1500, 1)
Otto.home()

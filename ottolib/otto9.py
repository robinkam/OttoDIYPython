# -- OttoDIY Python Project, 2020

import math

import utime
from machine import Pin, ADC
from micropython import const

from ottolib import oscillator, gestures, store
from ottolib.us import us


def DEG2RAD(g):
    return (g * math.pi) / 180


class Otto9:
    # -- Constants
    FORWARD = const(1)
    BACKWARD = const(-1)
    LEFT = const(1)
    RIGHT = const(-1)
    SMALL = const(5)
    MEDIUM = const(15)
    BIG = const(30)

    def __init__(self):
        self._servo = [oscillator.Oscillator(), oscillator.Oscillator(), oscillator.Oscillator(),
                       oscillator.Oscillator(), oscillator.Oscillator(), oscillator.Oscillator()]
        self._servo_pins = [-1, -1, -1, -1, -1, -1]
        self._servo_trim = [0, 0, 0, 0, 0, 0]
        self._servo_position = [90, 90, 90, 90, 90, 90]  # -- initialised to what the oscillator code defaults to
        self._servo_totals = 0
        self._final_time = 0
        self._partial_time = 0
        self._increment = [0, 0, 0, 0, 0, 0]
        self._isOttoResting = True
        self.usTrigger = -1
        self.usEcho = -1
        self.buzzer = -1
        self.noiseSensor = -1
        self.battery = None

    def deinit(self):
        self.detachServos()

    # --  Otto9 or Otto9Humanoid initialization
    def init(self, YL, YR, RL, RR, load_calibration, NoiseSensor, Buzzer, USTrigger, USEcho, LA=-1, RA=-1):
        self._servo_pins[0] = YL
        self._servo_pins[1] = YR
        self._servo_pins[2] = RL
        self._servo_pins[3] = RR
        self._servo_totals = 4
        if LA != -1:
            self._servo_pins[4] = LA
            self._servo_pins[5] = RA
            self._servo_totals = 6
        self.attachServos()
        self.setRestState(False)
        if load_calibration:
            trims = store.load('Trims', [0, 0, 0, 0, 0, 0])
            for i in range(0, self._servo_totals):
                servo_trim = trims[i]
                if servo_trim > 128:
                    servo_trim -= 256
                self._servo[i].SetTrim(servo_trim)
        for i in range(0, self._servo_totals):  # -- this could be eliminated as we already initialize
            self._servo_position[i] = 90  # -- the array from __init__() above ...

        self.noiseSensor = NoiseSensor
        self.buzzer = Buzzer
        self.usTrigger = USTrigger
        self.usEcho = USEcho

        if self.usTrigger >= 0 and self.usEcho >= 0:
            self.us = us(self.usTrigger, self.usEcho)

        if self.buzzer >= 0:
            self.buzzerPin = Pin(self.buzzer, Pin.OUT)
            self.buzzerPin.value(0)

        if self.noiseSensor >= 0:
            self.noiseSensorPin = ADC(Pin(NoiseSensor))
            self.noiseSensorPin.atten(ADC.ATTN_11DB)  # read the full voltage 0-3.6V

    # --  Otto9Humanoid initialization (depreciated)
    def initHUMANOID(self, YL, YR, RL, RR, LA, RA, load_calibration, NoiseSensor, Buzzer, USTrigger, USEcho):
        self.init(YL, YR, RL, RR, load_calibration, NoiseSensor, Buzzer, USTrigger, USEcho, LA, RA)

    # -- Attach & Detach Functions
    def attachServos(self):
        for i in range(0, self._servo_totals):
            self._servo[i].attach(self._servo_pins[i])

    def detachServos(self):
        for i in range(0, self._servo_totals):
            self._servo[i].detach()

    # -- Oscillator trims
    def setTrims(self, YL, YR, RL, RR, LA=0, RA=0):
        self._servo[0].SetTrim(0 if YL is None else YL)
        self._servo[1].SetTrim(0 if YR is None else YR)
        self._servo[2].SetTrim(0 if RL is None else RL)
        self._servo[3].SetTrim(0 if RR is None else RR)
        if self._servo_totals > 4:
            self._servo[4].SetTrim(0 if LA is None else LA)
            self._servo[5].SetTrim(0 if RA is None else RA)

    def saveTrimsOnEEPROM(self):
        trims = [0, 0, 0, 0, 0, 0]
        for i in range(0, self._servo_totals):
            trims[i] = self._servo[i].getTrim()
        store.save('Trims', trims)

    # -- Basic Motion Functions
    def _moveServos(self, T, servo_target):
        self.attachServos()
        if self.getRestState():
            self.setRestState(False)
        if T > 10:
            for i in range(0, self._servo_totals):
                self._increment[i] = ((servo_target[i]) - self._servo_position[i]) / (T / 10.0)
            self._final_time = utime.ticks_ms() + T
            iteration = 1
            while utime.ticks_ms() < self._final_time:
                self._partial_time = utime.ticks_ms() + 10
                for i in range(0, self._servo_totals):
                    self._servo[i].SetPosition(int(self._servo_position[i] + (iteration * self._increment[i])))
                while utime.ticks_ms() < self._partial_time:
                    pass  # pause
                iteration += 1
        else:
            for i in range(0, self._servo_totals):
                self._servo[i].SetPosition(servo_target[i])
        for i in range(0, self._servo_totals):
            self._servo_position[i] = servo_target[i]

    def _moveSingle(self, position, servo_number):
        if position > 180 or position < 0:
            position = 90
        self.attachServos()
        if self.getRestState() == True:
            self.setRestState(False)
        self._servo[servo_number].SetPosition(position)
        self._servo_position[servo_number] = position

    def oscillateServos(self, A, O, T, phase_diff, cycle=1.0):
        for i in range(0, self._servo_totals):
            self._servo[i].SetO(O[i])
            self._servo[i].SetA(A[i])
            self._servo[i].SetT(T)
            self._servo[i].SetPh(phase_diff[i])

        ref = float(utime.ticks_ms())
        x = ref
        while x <= T * cycle + ref:
            for i in range(0, self._servo_totals):
                self._servo[i].refresh()
            x = float(utime.ticks_ms())

    def _execute(self, A, O, T, phase_diff, steps=1.0):
        self.attachServos()
        if self.getRestState() == True:
            self.setRestState(False)

        # -- Execute complete cycles
        cycles = int(steps)
        if cycles >= 1:
            i = 0
            while i < cycles:
                self.oscillateServos(A, O, T, phase_diff)
                i += 1
        # -- Execute the final not complete cycle
        self.oscillateServos(A, O, T, phase_diff, float(steps - cycles))

    def getRestState(self):
        return self._isOttoResting

    def setRestState(self, state):
        self._isOttoResting = state

    # -- Predetermined Motion Sequences

    # -- Otto movement: HOME Otto at rest position
    def home(self):
        if self.getRestState() == False:  # -- Go to rest position only if necessary
            homes = [90, 90, 90, 90, 90, 90]  # -- All the servos at rest position
            self._moveServos(500, homes)  # -- Move the servos in half a second
            self.detachServos()
            self.setRestState(True)

    # -- Otto movement: Jump
    # --  Parameters:
    # --    steps: Number of steps
    # --    T: Period
    def jump(self, steps, T):
        up = [90, 90, 150, 30, 110, 70]
        down = [90, 90, 90, 90, 90, 90]
        self._moveServos(T, up)
        self._moveServos(T, down)

    # -- Otto gait: Dash  (forward or backward, no arm movement)
    # --  Parameters:
    # --    * steps:  Number of steps
    # --    * T : Period
    # --    * Dir: Direction: FORWARD / BACKWARD
    def dash(self, steps, T, dir):
        # -- Oscillator parameters for walking
        # -- Hip sevos are in phase
        # -- Feet servos are in phase
        # -- Hip and feet are 90 degrees out of phase
        # --      -90 : Walk forward
        # --       90 : Walk backward
        # -- Feet servos also have the same offset (for tiptoe a little bit)
        A = [30, 30, 20, 20, 0, 0]
        O = [0, 0, 4, -4, self._servo_position[4]-90, self._servo_position[5]-90]
        phase_diff = [0, 0, DEG2RAD(dir * -90), DEG2RAD(dir * -90), 0, 0]

        # -- Let's oscillate the servos!
        self._execute(A, O, T, phase_diff, steps)

    # -- Otto gait: Walking  (forward or backward)
    # --  Parameters:
    # --    * steps:  Number of steps
    # --    * T : Period
    # --    * Dir: Direction: FORWARD / BACKWARD
    def walk(self, steps, T, dir):
        # -- Oscillator parameters for walking
        # -- Hip sevos are in phase
        # -- Feet servos are in phase
        # -- Hip and feet are 90 degrees out of phase
        # --      -90 : Walk forward
        # --       90 : Walk backward
        # -- Feet servos also have the same offset (for tiptoe a little bit)
        A = [30, 30, 20, 20, 90, 90]
        O = [0, 0, 4, -4, 0, 0]
        phase_diff = [0, 0, DEG2RAD(dir * -90), DEG2RAD(dir * -90), 0, 0]

        # -- Let's oscillate the servos!
        self._execute(A, O, T, phase_diff, steps)

    # -- Otto gait: Turning (left or right)
    # --  Parameters:
    # --   * Steps: Number of steps
    # --   * T: Period
    # --   * Dir: Direction: LEFT / RIGHT
    def turn(self, steps, T, dir):
        # -- Same coordination than for walking (see Otto.walk)
        # -- The Amplitudes of the hip's oscillators are not igual
        # -- When the right hip servo amplitude is higher, steps taken by
        # -- the right leg are bigger than the left. So, robot describes an left arc
        A = [30, 30, 20, 20, 90, 90]
        O = [0, 0, 4, -4, 0, 0]
        phase_diff = [0, 0, DEG2RAD(-90), DEG2RAD(-90), 0, 0]
        if dir == LEFT:
            A[0] = 30  # -- Left hip servo
            A[1] = 10  # -- Right hip servo
        else:
            A[0] = 10
            A[1] = 30

        # -- Let's oscillate the servos!
        self._execute(A, O, T, phase_diff, steps)

    # -- Otto gait: Lateral bend
    # --  Parameters:
    # --    steps: Number of bends
    # --    T: Period of one bend
    # --    dir: RIGHT=Right bend LEFT=Left bend
    def bend(self, steps, T, dir):
        # -- Parameters of all the movements. Default: Left bend
        bend1 = [90, 90, 40, 35, 120, 60]
        bend2 = [90, 90, 40, 105, 60, 120]
        homes = [90, 90, 90, 90, 90, 90]

        # -- Time of one bend, in order to avoid movements too fast.
        # T = max(T, 600)

        # -- Changes in the parameters if right direction is chosen
        if dir == RIGHT:
            bend1[2] = 180 - 50
            bend1[3] = 180 - 80  # -- Not 65. Otto is unbalanced
            bend2[2] = 180 - 105
            bend2[3] = 180 - 60

        # -- Time of the bend movement. Fixed parameter to avoid falls
        T2 = 800

        # -- Bend movement
        i = 0
        while i < steps:
            self._moveServos(T2 / 2, bend1)
            self._moveServos(T2 / 2, bend2)
            utime.sleep_ms(int((T * 0.8)))
            self._moveServos(500, homes)
            i += 1

    # -- Otto gait: Shake a leg
    # --  Parameters:
    # --    steps: Number of shakes
    # --    T: Period of one shake
    # --    dir: RIGHT=Right leg LEFT=Left leg
    def shakeLeg(self, steps, T, dir):
        # -- This variable change the amount of shakes
        numberLegMoves = 2

        shakeDelta1 = [-30, -90]
        shakeDelta2 = [-30, 20]
        shakeDelta3 = [-30, -20]

        # -- Parameters of all the movements. Default: Right leg
        shake_leg1 = [90, 90, 90 + shakeDelta1[0], 90 + shakeDelta1[1], 90, 90]
        shake_leg2 = [90, 90, 90 + shakeDelta2[0], 90 + shakeDelta2[1], 100, 80]
        shake_leg3 = [90, 90, 90 + shakeDelta3[0], 90 + shakeDelta3[1], 80, 100]
        homes = [90, 90, 90, 90, 90, 90]

        # -- Changes in the parameters if right leg is chosen
        if dir == LEFT:
            shake_leg1[2] = 90 - shakeDelta1[1]
            shake_leg1[3] = 90 - shakeDelta1[0]
            shake_leg2[2] = 90 - shakeDelta2[1]
            shake_leg2[3] = 90 - shakeDelta2[0]
            shake_leg3[2] = 90 - shakeDelta3[1]
            shake_leg3[3] = 90 - shakeDelta3[0]

        # -- Time of the bend movement. Fixed parameter to avoid falls
        T2 = 500

        # -- Time of one shake, in order to avoid movements too fast.
        T = T - T2
        T = max(T, 200 * numberLegMoves)

        j = 0
        while j < steps:
            # -- Bend movement
            self._moveServos(T2 / 2, shake_leg1)
            self._moveServos(T2 / 2, shake_leg2)

            # -- Shake movement
            i = 0
            while i < numberLegMoves:
                self._moveServos(T / (2 * numberLegMoves), shake_leg3)
                self._moveServos(T / (2 * numberLegMoves), shake_leg2)
                i += 1
            self._moveServos(500, homes)  # -- Return to home position
            j += 1
        utime.sleep_ms(T)

    # -- Otto movement: up & down
    # --  Parameters:
    # --    * steps: Number of jumps
    # --    * T: Period
    # --    * h: Jump height: SMALL / MEDIUM / BIG
    # --              (or a number in degrees 0 - 90)
    def updown(self, steps, T, h):
        # -- Both feet are 180 degrees out of phase
        # -- Feet amplitude and offset are the same
        # -- Initial phase for the right foot is -90, that it starts
        # --   in one extreme position (not in the middle)
        A = [0, 0, h, h, h, h]
        O = [0, 0, h, -h, h, -h]
        phase_diff = [0, 0, DEG2RAD(-90), DEG2RAD(90), DEG2RAD(-90), DEG2RAD(90)]

        # -- Let's oscillate the servos!
        self._execute(A, O, T, phase_diff, steps)

    # -- Otto movement: swinging side to side
    # --  Parameters:
    # --     steps: Number of steps
    # --     T : Period
    # --     h : Amount of swing (from 0 to 50 aprox)
    def swing(self, steps, T, h):
        # -- Both feets are in phase. The offset is half the amplitude
        # -- It causes the robot to swing from side to side
        A = [0, 0, h, h, h, h]
        O = [0, 0, h / 2, -h / 2, h, -h]
        phase_diff = [0, 0, DEG2RAD(0), DEG2RAD(0), DEG2RAD(0), DEG2RAD(0)]

        # -- Let's oscillate the servos!
        self._execute(A, O, T, phase_diff, steps)

    # -- Otto movement: swinging side to side without touching the floor with the heel
    # --  Parameters:
    # --     steps: Number of steps
    # --     T : Period
    # --     h : Amount of swing (from 0 to 50 aprox)
    def tiptoeSwing(self, steps, T, h):
        # -- Both feets are in phase. The offset is not half the amplitude in order to tiptoe
        # -- It causes the robot to swing from side to side
        A = [0, 0, h, h, h, h]
        O = [0, 0, h, -h, h, -h]
        phase_diff = [0, 0, 0, 0, 0, 0]

        # -- Let's oscillate the servos!
        self._execute(A, O, T, phase_diff, steps)

    # -- Otto gait: Jitter
    # --  Parameters:
    # --    steps: Number of jitters
    # --    T: Period of one jitter
    # --    h: height (Values between 5 - 25)
    def jitter(self, steps, T, h):
        # -- Both feet are 180 degrees out of phase
        # -- Feet amplitude and offset are the same
        # -- Initial phase for the right foot is -90, that it starts
        # --   in one extreme position (not in the middle)
        # -- h is constrained to avoid hit the feets
        h = min(25, h)
        A = [h, h, 0, 0, 0, 0]
        O = [0, 0, 0, 0, 0, 0]
        phase_diff = [DEG2RAD(-90), DEG2RAD(90), 0, 0, 0, 0]

        # -- Let's oscillate the servos!
        self._execute(A, O, T, phase_diff, steps)

    # -- Otto gait: Ascending & turn (Jitter while up&down)
    # --  Parameters:
    # --    steps: Number of bends
    # --    T: Period of one bend
    # --    h: height (Values between 5 - 15)
    def ascendingTurn(self, steps, T, h):
        # -- Both feet and legs are 180 degrees out of phase
        # -- Initial phase for the right foot is -90, that it starts
        # --   in one extreme position (not in the middle)
        # -- h is constrained to avoid hit the feets
        h = min(13, h)
        A = [h, h, h, h, 40, 40]
        O = [0, 0, h + 4, -h + 4, 0, 0]
        phase_diff = [DEG2RAD(-90), DEG2RAD(90), DEG2RAD(-90), DEG2RAD(90), 0, 0]

        # -- Let's oscillate the servos!
        self._execute(A, O, T, phase_diff, steps)

    # -- Otto gait: Moonwalker. Otto moves like Michael Jackson
    # --  Parameters:
    # --    Steps: Number of steps
    # --    T: Period
    # --    h: Height. Typical valures between 15 and 40
    # --    dir: Direction: LEFT / RIGHT
    def moonwalker(self, steps, T, h, dir):
        # -- This motion is similar to that of the caterpillar robots: A travelling
        # -- wave moving from one side to another
        # -- The two Otto's feet are equivalent to a minimal configuration. It is known
        # -- that 2 servos can move like a worm if they are 120 degrees out of phase
        # -- In the example of Otto, two feet are mirrored so that we have:
        # --    180 - 120 = 60 degrees. The actual phase difference given to the oscillators
        # --  is 60 degrees.
        # --  Both amplitudes are equal. The offset is half the amplitud plus a little bit of
        # -   offset so that the robot tiptoe lightly
        A = [0, 0, h, h, h, h]
        O = [0, 0, h / 2 + 2, -h / 2 - 2, -h, h]
        phi = -dir * 90
        phase_diff = [0, 0, DEG2RAD(phi), DEG2RAD(-60 * dir + phi), DEG2RAD(phi), DEG2RAD(phi)]

        # -- Let's oscillate the servos!
        self._execute(A, O, T, phase_diff, steps)

    # -- Otto gait: Dodge. moonwalk but no arm movement
    # --  Parameters:
    # --    Steps: Number of steps
    # --    T: Period
    # --    h: Height. Typical valures between 15 and 40
    # --    dir: Direction: LEFT / RIGHT
    def dodge(self, steps, T, h, dir):
        # -- This motion is similar to that of the caterpillar robots: A travelling
        # -- wave moving from one side to another
        # -- The two Otto's feet are equivalent to a minimal configuration. It is known
        # -- that 2 servos can move like a worm if they are 120 degrees out of phase
        # -- In the example of Otto, two feet are mirrored so that we have:
        # --    180 - 120 = 60 degrees. The actual phase difference given to the oscillators
        # --  is 60 degrees.
        # --  Both amplitudes are equal. The offset is half the amplitud plus a little bit of
        # -   offset so that the robot tiptoe lightly
        A = [0, 0, h, h, 0, 0]
        O = [0, 0, h / 2 + 2, -h / 2 - 2, self._servo_position[4]-90, self._servo_position[5]-90]
        phi = -dir * 90
        phase_diff = [0, 0, DEG2RAD(phi), DEG2RAD(-60 * dir + phi), DEG2RAD(phi), DEG2RAD(phi)]

        # -- Let's oscillate the servos!
        self._execute(A, O, T, phase_diff, steps)

    # -- Otto gait: Crusaito. A mixture between moonwalker and walk
    # --   Parameters:
    # --     steps: Number of steps
    # --     T: Period
    # --     h: height (Values between 20 - 50)
    # --     dir:  Direction: LEFT / RIGHT
    def crusaito(self, steps, T, h, dir):
        A = [25, 25, h, h, 0, 0]
        O = [0, 0, h / 2 + 4, -h / 2 - 4, 0, 0]
        phase_diff = [90, 90, DEG2RAD(0), DEG2RAD(-60 * dir), 0, 0]

        # -- Let's oscillate the servos!
        self._execute(A, O, T, phase_diff, steps)

    # -- Otto gait: Flapping
    # --  Parameters:
    # --    steps: Number of steps
    # --    T: Period
    # --    h: height (Values between 10 - 30)
    # --    dir: direction: FOREWARD, BACKWARD
    def flapping(self, steps, T, h, dir):
        A = [12, 12, h, h, 0, 0]
        O = [0, 0, h - 10, -h + 10, 0, 0]
        phase_diff = [DEG2RAD(0), DEG2RAD(180), DEG2RAD(-90 * dir), DEG2RAD(90 * dir), 0, 0]

        # -- Let's oscillate the servos!
        self._execute(A, O, T, phase_diff, steps)

    # -- Otto arm movement
    # --  Parameters:
    # --    T: Period
    # --    h: height (Values between -45 ~ 90, positive value means raising arm)
    # --    dir: direction: LEFT, RIGHT
    def moveArm(self, T, h, dir):
        if self._servo_totals > 4:
            shallowCopy = self._servo_position[:]
            if dir == RIGHT:
                shallowCopy[5] = h + 90
                self._moveServos(T, shallowCopy)
            if dir == LEFT:
                shallowCopy[4] = abs(h - 90)
                self._moveServos(T, shallowCopy)

    # -- Otto movement: Hands up
    def handsup(self):
        if self._servo_totals > 4:
            homes = [90, 90, 90, 90, 20, 160]
            self._moveServos(1000, homes)

    # -- Otto movement: Wave , either left or right
    def handwave(self, dir):
        if self._servo_totals > 4:
            if dir == RIGHT:
                A = [0, 0, 0, 0, 0, 30]
                O = [0, 0, 0, 0, 0, 30]
                phase_diff = [0, 0, 0, 0, 0, 0]
                # -- Let's oscillate the servos!
                self._execute(A, O, 1000, phase_diff, 2)
            if dir == LEFT:
                A = [0, 0, 0, 0, 30, 0]
                O = [0, 0, 0, 0, -30, 0]
                phase_diff = [0, 0, 0, 0, 0, 0]
                # -- Let's oscillate the servos!
                self._execute(A, O, 1000, phase_diff, 2)

    # -- Otto get US distance
    # -- returns distance in cm
    def getDistance(self):
        return self.us.distance_cm()


    # -- Gestures

    # -- Play Gesture
    # -- Parameters:
    # --    gesture: which gesture to do
    def playGesture(self, gesture):
        if gesture == gestures.OTTOHAPPY:
            self.swing(1, 800, 20)
            self.home()
        elif gesture == gestures.OTTOSUPERHAPPY:
            self.tiptoeSwing(1, 500, 20)
            self.tiptoeSwing(1, 500, 20)
            self.home()
        elif gesture == gestures.OTTOSAD:
            self._moveServos(700, [110, 70, 20, 160, 90, 90])
            utime.sleep_ms(500)

            self.home()
            utime.sleep_ms(300)
        elif gesture == gestures.OTTOSLEEPING:
            self._moveServos(700, [100, 80, 60, 120, 90, 90])
            self.home()
        elif gesture == gestures.OTTOFART:
            self._moveServos(500, [90, 90, 145, 122, 90, 90])
            utime.sleep_ms(300)
            utime.sleep_ms(250)
            self._moveServos(500, [90, 90, 80, 122, 90, 90])
            utime.sleep_ms(300)
            utime.sleep_ms(250)
            self._moveServos(500, [90, 90, 145, 80, 90, 90])
            utime.sleep_ms(300)
            utime.sleep_ms(300)

            self.home()
            utime.sleep_ms(500)
        elif gesture == gestures.OTTOCONFUSED:
            self._moveServos(300, [110, 70, 90, 90, 90, 90])
            utime.sleep_ms(500)

            self.home()
        elif gesture == gestures.OTTOLOVE:
            self.crusaito(2, 1500, 25, 1)

            self.home()
        elif gesture == gestures.OTTOANGRY:
            self._moveServos(300, [90, 90, 70, 110, 90, 90])

            utime.sleep_ms(400)
            self._moveServos(200, [110, 110, 90, 90, 90, 90])
            self._moveServos(200, [70, 70, 90, 90, 90, 90])

            self.home()
        elif gesture == gestures.OTTOFRETFUL:
            utime.sleep_ms(300)

            for i in range(4):
                self._moveServos(100, [90, 90, 90, 110, 90, 90])
                self.home()

            utime.sleep_ms(500)

            self.home()
        elif gesture == gestures.OTTOVICTORY:
            for i in range(60):
                self._moveServos(10, [9, 90, 90 + i, 90 - i, 90, 90])

            for i in range(60):
                self._moveServos(10, [90, 90, 150 - i, 30 + i, 90, 90])

            self.tiptoeSwing(1, 500, 20)
            self.tiptoeSwing(1, 500, 20)

            self.home()
        elif gesture == gestures.OTTOFAIL:
            self._moveServos(300, [90, 90, 70, 35, 90, 90])
            self._moveServos(300, [90, 90, 55, 35, 90, 90])
            self._moveServos(300, [90, 90, 42, 35, 90, 90])
            self._moveServos(300, [90, 90, 34, 35, 90, 90])

            self.detachServos()

            utime.sleep_ms(600)
            self.home()

# end

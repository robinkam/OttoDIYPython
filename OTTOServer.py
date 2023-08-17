import machine
from micropython import const
from webserver import ESPWebServer
import ottolib.otto9 as otto9
import time

otto = otto9.Otto9()

MODE_ONCE = const(0)  # on demand mode
MODE_REPEAT = const(1)  # continuous mode
ACTION_IDLE = 'idle'
LED_GPIO_NUM = const(15)  # Builtin led (Wemos S2 mini)

mode = MODE_ONCE
action = ACTION_IDLE
params = {}

# Get pin object for controlling builtin LED
ledPin = machine.Pin(LED_GPIO_NUM, machine.Pin.OUT)


def handleAction(socket, args, act):
    global action, params, mode
    action = act
    params = args
    print('handleAction', action, params, 'mode=', mode)
    ESPWebServer.ok(socket, "200", act)


# Handler for path "/cmd/home"
def handleHome(socket, args):
    otto.home()
    handleAction(socket, args, "home")


# Handler for path "/cmd/handsup"
def handleHandsUp(socket, args):
    otto.handsup()
    handleAction(socket, args, "handsup")


# Handler for path "/cmd/handwave?direction=[1|-1]"
def handleHandWave(socket, args):
    otto.handwave(int(args['direction']))
    handleAction(socket, args, "handwave")


# Handler for path "/cmd/jump?steps=[1,10]&period=[600,1400]"
def handleJump(socket, args):
    handleAction(socket, args, 'jump')


# Handler for path "/cmd/dash?steps=[1,10]&period=[600,1400]&direction=[1|-1]"
def handleDash(socket, args):
    handleAction(socket, args, 'dash')


# Handler for path "/cmd/walk?steps=[1,10]&period=[600,1400]&direction=[1|-1]"
def handleWalk(socket, args):
    handleAction(socket, args, 'walk')


# Handler for path "/cmd/turn?steps=[1,10]&period=[600,1400]&direction=[1|-1]"
def handleTurn(socket, args):
    handleAction(socket, args, 'turn')


# Handler for path "/cmd/bend?steps=[1,10]&period=[600,1400]&direction=[1|-1]"
def handleBend(socket, args):
    otto.bend(int(args['steps']), int(args['period']), int(args['direction']))
    handleAction(socket, args, "bend")


# Handler for path "/cmd/shakeLeg?steps=[1,10]&period=[600,1400]&direction=[1|-1]"
def handleShakeLeg(socket, args):
    otto.shakeLeg(int(args['steps']), int(args['period']), int(args['direction']))
    handleAction(socket, args, "shakeLeg")


# Handler for path "/cmd/moveArm?period=[100,1400]&height=[-45,90]&direction=[1|-1]"
def handleMoveArm(socket, args):
    otto.moveArm(int(args['period']), int(args['height']), int(args['direction']))
    handleAction(socket, args, "moveArm")


# Handler for path "/cmd/moonwalker?steps=[1,10]&period=[600,1400]&height=[15,40]&direction=[1|-1]"
def handleMoonwalker(socket, args):
    handleAction(socket, args, 'moonwalker')


# Handler for path "/cmd/crusaito?steps=[1,10]&period=[600,1400]&height=[20,50]&direction=[1|-1]"
def handleCrusaito(socket, args):
    handleAction(socket, args, 'crusaito')


# Handler for path "/cmd/flapping?steps=[1,10]&period=[600,1400]&height=[10,30]&direction=[1|-1]"
def handleFlapping(socket, args):
    handleAction(socket, args, "flapping")


# Handler for path "/cmd/updown?steps=[1,10]&period=[600,1400]&height=[0,90]"
def handleUpdown(socket, args):
    handleAction(socket, args, "updown")


# Handler for path "/cmd/swing?steps=[1,10]&period=[600,1400]&height=[0,90]"
def handleSwing(socket, args):
    handleAction(socket, args, "swing")


# Handler for path "/cmd/tiptoeSwing?steps=[1,10]&period=[600,1400]&height=[0,90]"
def handleTiptoeSwing(socket, args):
    handleAction(socket, args, "tiptoeSwing")


# Handler for path "/cmd/ascendingTurn?steps=[1,10]&period=[600,1400]&height=[0,90]"
def handleAscendingTurn(socket, args):
    handleAction(socket, args, "ascendingTurn")


# Handler for path "/cmd/jitter?steps=[1,10]&period=[600,1400]&height=[0,90]"
def handleJitter(socket, args):
    handleAction(socket, args, "jitter")


# Handler for path "/cmd/playGesture"
def handleGesture(socket, args):
    otto.playGesture(int(args["gesture"]))
    ESPWebServer.ok(socket, "200", "playGesture")


# Handler for path "/cmd/saveTrims"
def handleSaveTrims(socket, args):
    otto.setTrims(int(args["YL"]), int(args["YR"]), int(args["RL"]), int(args["RR"]), int(args["LA"]), int(args["RA"]))
    otto.saveTrimsOnEEPROM()
    ESPWebServer.ok(socket, "200", "saveTrims")


# Handler for path "/cmd/toggleMode"
def handleToggleMode(socket, args):
    global mode
    mode = int(args["mode"])
    ESPWebServer.ok(socket, "200", "toggleMode")


class OTTOServer:
    def __init__(self):
        pass

    @staticmethod
    def setup():
        otto.initHUMANOID(12, 11, 9, 7, 33, 35, True, -1, -1, 18, 5)  # s2 mini + IO shields pins
        # otto.home()  # Sometimes, call home() may cause sudden high electric current consumption and make OTTO 'cramp'.

        # Start the server @ port 8899
        # ESPWebServer.begin(8899)
        ESPWebServer.begin()  # use default 80 port

        # Register handler for each path
        # ESPWebServer.onPath("/", handleRoot)
        ESPWebServer.onPath("/cmd/home", handleHome)
        ESPWebServer.onPath("/cmd/handsup", handleHandsUp)
        ESPWebServer.onPath("/cmd/jump", handleJump)
        ESPWebServer.onPath("/cmd/handwave", handleHandWave)

        ESPWebServer.onPath("/cmd/dash", handleDash)
        ESPWebServer.onPath("/cmd/walk", handleWalk)
        ESPWebServer.onPath("/cmd/turn", handleTurn)

        ESPWebServer.onPath("/cmd/bend", handleBend)
        ESPWebServer.onPath("/cmd/shakeLeg", handleShakeLeg)
        ESPWebServer.onPath("/cmd/moveArm", handleMoveArm)
        ESPWebServer.onPath("/cmd/moonwalker", handleMoonwalker)
        ESPWebServer.onPath("/cmd/crusaito", handleCrusaito)
        ESPWebServer.onPath("/cmd/flapping", handleFlapping)

        ESPWebServer.onPath("/cmd/swing", handleSwing)
        ESPWebServer.onPath("/cmd/updown", handleUpdown)
        ESPWebServer.onPath("/cmd/tiptoeSwing", handleTiptoeSwing)
        ESPWebServer.onPath("/cmd/ascendingTurn", handleAscendingTurn)
        ESPWebServer.onPath("/cmd/jitter", handleJitter)

        ESPWebServer.onPath("/cmd/playGesture", handleGesture)

        ESPWebServer.onPath("/cmd/saveTrims", handleSaveTrims)
        ESPWebServer.onPath("/cmd/toggleMode", handleToggleMode)

        # Setting the path to documents
        ESPWebServer.setDocPath("/webroot")

        # Setting maximum Body Content Size. Set to 0 to disable posting. Default: 1024
        ESPWebServer.setMaxContentLength(1024)

    @staticmethod
    def start():
        ledPin.on()  # Turn LED off (it use sinking input)

        lastDistanceDetectionTime = time.ticks_us()

        try:
            while True:

                # Let server process requests
                ESPWebServer.handleClient()

                global action, params, mode
                args = params


                if action == 'jump':
                    otto.jump(int(args['steps']), int(args['period']))
                elif action == 'dash':
                    otto.dash(int(args['steps']), int(args['period']), int(args['direction']))
                elif action == 'walk':
                    otto.walk(int(args['steps']), int(args['period']), int(args['direction']))
                elif action == 'turn':
                    otto.turn(int(args['steps']), int(args['period']), int(args['direction']))
                elif action == 'moonwalker':
                    otto.moonwalker(int(args['steps']), int(args['period']), int(args['height']), int(args['direction']))
                elif action == 'crusaito':
                    otto.crusaito(int(args['steps']), int(args['period']), int(args['height']), int(args['direction']))
                elif action == 'flapping':
                    otto.flapping(int(args['steps']), int(args['period']), int(args['height']), int(args['direction']))
                elif action == 'updown':
                    otto.updown(int(args['steps']), int(args['period']), int(args['height']))
                elif action == 'swing':
                    otto.swing(int(args['steps']), int(args['period']), int(args['height']))
                elif action == 'tiptoeSwing':
                    otto.tiptoeSwing(int(args['steps']), int(args['period']), int(args['height']))
                elif action == 'ascendingTurn':
                    otto.ascendingTurn(int(args['steps']), int(args['period']), int(args['height']))
                elif action == 'jitter':
                    otto.jitter(int(args['steps']), int(args['period']), int(args['height']))

                if mode == MODE_ONCE:
                    action = ACTION_IDLE

                # avoid obstacles with ultrasonic sensor
                if hasattr(otto, 'us'):  # us = ultra-sonic
                    now = time.ticks_us()
                    deltaTime = now - lastDistanceDetectionTime
                    if deltaTime > 1000000:  # detect distance per 1 second
                        lastDistanceDetectionTime = now
                        distance = otto.getDistance()
                        if distance < 10:
                            print('Attention! Obstacles are ' + str(distance) + 'cm away. Back up now.')
                            otto.walk(2, 1000, -1)
                            action = ACTION_IDLE  # walk backward for 2 steps and stop moving.
                        else:
                            print('front distance: ', str(distance))

        except OSError as error:
            print(error)
            ledPin.off()
            ESPWebServer.close()

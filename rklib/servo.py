from machine import Pin, PWM


class Servo:
    frequency = 50  # 50Hz = 20ms/周期

    def __init__(self, pin):
        print('Servo init')
        self.servo = PWM(Pin(pin))
        self.servo.freq(Servo.frequency)

    def angle(self, angle, time=0):
        # PWM高电平占整个周期的时间	舵机旋转角度
        # 0.5ms	0°
        # 1ms	45°
        # 1.5ms	90°
        # 2ms	135°
        # 2.5ms	180°
        if 0 <= angle <= 180:
            pulseDuration = angle / 180 * 2 + 0.5
            self.servo.duty(int(pulseDuration / 20 * 1023))

    def speed(self, speed, time=0):  # speed取值范围[-1,1]，-1表示反向最大速度，1表示正向最大速度，0表示静止
        # PWM 信号与360舵机转速的关系：
        # 0.5ms 正向最大转速；
        # 1.5ms 速度为0；
        # 2.5ms 反向最大转速；
        if -1 <= speed <= 1:
            pulseDuration = speed + 1.5
            self.servo.duty(int(pulseDuration / 20 * 1023))

    def __del__(self):
        self.servo.deinit()

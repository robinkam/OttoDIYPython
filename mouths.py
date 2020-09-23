#-- Mouths sorted by numbers, and after, by happy to sad mouths
#-- OttDIY Python Project, 2020

ZERO = 0
ONE = 1
TWO = 2
THREE = 3
FOUR = 4
FIVE = 5
SIX = 6
SEVEN = 7
EIGHT = 8
NINE = 9
SMILE = 10
HAPPYOPEN = 11
HAPPYCLOSED = 12
HEART = 13
BIGSURPRISE = 14
SMALLSURPRISE = 15
TONGUEOUT = 16
VAMP1 = 17
VAMP2 = 18
LINEMOUTH = 19
CONFUSED = 20
DIAGONAL = 21
SAD = 22
SADOPEN = 23
SADCLOSED = 24
OKMOUTH = 25
XMOUTH = 26
INTERROGATION = 27
THUNDER = 28
CULITO = 29
ANGRY = 30

mouths = [
    0b00001100010010010010010010001100,  # zero_code
    0b00000100001100000100000100001110,  # one_code
    0b00001100010010000100001000011110,  # two_code
    0b00001100010010000100010010001100,  # three_code
    0b00010010010010011110000010000010,  # four_code
    0b00011110010000011100000010011100,  # five_code
    0b00000100001000011100010010001100,  # six_code
    0b00011110000010000100001000010000,  # seven_code
    0b00001100010010001100010010001100,  # eight_code
    0b00001100010010001110000010001110,  # nine_code
    0b00000000100001010010001100000000,  # smile_code
    0b00000000111111010010001100000000,  # happyOpen_code
    0b00000000111111011110000000000000,  # happyClosed_code
    0b00010010101101100001010010001100,  # heart_code
    0b00001100010010100001010010001100,  # bigSurprise_code
    0b00000000000000001100001100000000,  # smallSurprise_code
    0b00111111001001001001000110000000,  # tongueOut_code
    0b00111111101101101101010010000000,  # vamp1_code
    0b00111111101101010010000000000000,  # vamp2_code
    0b00000000000000111111000000000000,  # lineMouth_code
    0b00000000001000010101100010000000,  # confused_code
    0b00100000010000001000000100000010,  # diagonal_code
    0b00000000001100010010100001000000,  # sad_code
    0b00000000001100010010111111000000,  # sadOpen_code
    0b00000000001100011110110011000000,  # sadClosed_code
    0b00000001000010010100001000000000,  # okMouth_code
    0b00100001010010001100010010100001,  # xMouth_code
    0b00001100010010000100000100000100,  # interrogation_code
    0b00000100001000011100001000010000,  # thunder_code
    0b00000000100001101101010010000000,  # culito_code
    0b00000000011110100001100001000000  # angry_code
]

# -- mouth animations

LITTLEUUH = 0
DREAMMOUTH = 1
ADIVINAWI = 2
WAVE = 3

aniMouths = [
    [
        0b00000000000000001100001100000000,
        0b00000000000000000110000110000000,
        0b00000000000000000011000011000000,
        0b00000000000000000110000110000000,
        0b00000000000000001100001100000000,
        0b00000000000000011000011000000000,
        0b00000000000000110000110000000000,
        0b00000000000000011000011000000000
    ],
    [
        0b00000000000000000000110000110000,
        0b00000000000000010000101000010000,
        0b00000000011000100100100100011000,
        0b00000000000000010000101000010000
    ],
    [
        0b00100001000000000000000000100001,
        0b00010010100001000000100001010010,
        0b00001100010010100001010010001100,
        0b00000000001100010010001100000000,
        0b00000000000000001100000000000000,
        0b00000000000000000000000000000000
    ],
    [
        0b00001100010010100001000000000000,
        0b00000110001001010000100000000000,
        0b00000011000100001000010000100000,
        0b00000001000010000100001000110000,
        0b00000000000001000010100100011000,
        0b00000000000000100001010010001100,
        0b00000000100000010000001001000110,
        0b00100000010000001000000100000011,
        0b00110000001000000100000010000001,
        0b00011000100100000010000001000000
    ]
]

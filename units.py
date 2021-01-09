class Unit:
    def __init__(self, combat, sustain=False, ground=False, bombard=False):
        self.combat = combat
        self.sustain = sustain
        self.ground = ground
        self.bombard = bombard

    def __repr__(self):
        return "<Combat: %s, Sustain: %s>" % (self.combat, self.sustain)


def fighter():
    return Unit(9)


def dread():
    return Unit(5, sustain=True, bombard=5)


def infantry():
    return Unit(8, ground=True)


def mech():
    return Unit(6, sustain=True, ground=True)





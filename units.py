class Unit:
    def __init__(self, combat, sustain=False, ground=False, bombard=[], afb=[], cannon=[], shield=False, fighter=False):
        self.combat = combat
        self.sustain = sustain
        self.ground = ground
        self.bombard = bombard
        self.afb = afb
        self.cannon = cannon
        self.fighter = fighter

    def __repr__(self):
        return "<Combat: %s, Sustain: %s>" % (self.combat, self.sustain)


def warsun():
    return Unit([3, 3, 3], sustain=True, bombard=[3, 3, 3])


def cruiser():
    return Unit([7])


def cruiser2():
    return Unit([6])


def dread():
    return Unit([5], sustain=True, bombard=5)


def destroyer():
    return Unit([9], afb=[9, 9])


def destroyer2():
    return Unit([8], afb=[6, 6, 6])


def pds():
    return Unit([], cannon=[6], shield=True)


def pds2():
    return Unit([], cannon=[5], shield=True)


def carrier():
    return Unit([9])


def fighter():
    return Unit([9], fighter=True)


def fighter2():
    return Unit([8], fighter=True)


def infantry():
    return Unit([8], ground=True)


def infantry2():
    return Unit([7], ground=True)


def mech():
    return Unit([6], sustain=True, ground=True)





class Unit:
    def __init__(self, combat, sustain=False, ground=False, bombard=[], afb=[], cannon=[], shield=False, fighter=False,
                 pds=False, disable_shield=False):
        self.combat = combat
        self.sustain = sustain
        self.ground = ground
        self.bombard = bombard
        self.afb = afb
        self.cannon = cannon
        self.shield = shield
        self.fighter = fighter
        self.pds = pds
        self.disable_shield = disable_shield

    def __repr__(self):
        return "<Combat: %s, Sustain: %s>" % (self.combat, self.sustain)


def flagship(faction):
    if faction == "Arborec":
        return Unit([7, 7], sustain=True)


def warsun(faction):
    return Unit([3, 3, 3], sustain=True, bombard=[3, 3, 3], disable_shield=True)


def cruiser(faction):
    return Unit([7])


def cruiser2(faction):
    return Unit([6])


def dread(faction):
    return Unit([5], sustain=True, bombard=5)


def destroyer(faction):
    return Unit([9], afb=[9, 9])


def destroyer2(faction):
    return Unit([8], afb=[6, 6, 6])


def pds(faction):
    return Unit([], cannon=[6], shield=True, pds=True)


def pds2(faction):
    return Unit([], cannon=[5], shield=True, pds=True)


def carrier(faction):
    return Unit([9])


def fighter(faction):
    return Unit([9], fighter=True)


def fighter2(faction):
    return Unit([8], fighter=True)


def infantry(faction):
    return Unit([8], ground=True)


def infantry2(faction):
    return Unit([7], ground=True)


def mech(faction):
    return Unit([6], sustain=True, ground=True)





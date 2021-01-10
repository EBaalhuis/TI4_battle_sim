class Unit:
    def __init__(self, combat, sustain=False, ground=False, bombard=[], afb=[], cannon=[], shield=False, fighter=False,
                 pds=False, disable_shield=False, direct_hit_immune=False):
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


def warsun(faction):
    return Unit([3, 3, 3], sustain=True, bombard=[3, 3, 3], disable_shield=True)


def cruiser(faction):
    return Unit([7])


def cruiser2(faction):
    return Unit([6])


def dread(faction):
    return Unit([5], sustain=True, bombard=5)


def dread2(faction):
    if faction == "L1Z1X":
        return Unit([4], sustain=True, bombard=4, direct_hit_immune=True)

    return Unit([5], sustain=True, bombard=5, direct_hit_immune=True)


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


def carrier2(faction):
    if faction == "Sol":
        return Unit([9], sustain=True)

    return Unit([9])


def fighter(faction):
    return Unit([9], fighter=True)


def fighter2(faction):
    return Unit([8], fighter=True)


def infantry(faction):
    if faction == "Sol":
        return Unit([7], ground=True)

    return Unit([8], ground=True)


def infantry2(faction):
    if faction == "Sol":
        return Unit([6], ground=True)

    return Unit([7], ground=True)


def mech(faction):
    if faction == "Arborec":
        return Unit([6], sustain=True, ground=True, shield=True)
    if faction == "L1Z1X":
        return Unit([6], sustain=True, ground=True, bombard=[8])

    return Unit([6], sustain=True, ground=True)


def flagship(faction):
    if faction == "Arborec":
        return Unit([7, 7], sustain=True)
    if faction == "Letnev":
        return Unit([5, 5], sustain=True, bombard=[5, 5, 5], disable_shield=True)
    if faction == "Saar":
        return Unit([5, 5], sustain=True, afb=[6, 6, 6, 6])
    if faction == "Muaat":
        return Unit([5, 5], sustain=True)
    if faction == "Hacan":
        return Unit([7, 7], sustain=True)
    if faction == "Sol":
        return Unit([5, 5], sustain=True)
    if faction == "Creuss":
        return Unit([5], sustain=True)
    if faction == "L1Z1X":
        return Unit([5, 5], sustain=True)
    if faction == "Mentak":
        return Unit([7, 7], sustain=True)
    if faction == "Naalu":
        return Unit([9, 9], sustain=True)
    if faction == "Nekro":
        return Unit([9, 9], sustain=True)
    if faction == "Sardakk":
        return Unit([5, 5], sustain=True)
    if faction == "Jol-Nar":
        return Unit([7, 7], sustain=True)
    if faction == "Winnu":
        return Unit([7], sustain=True)
    if faction == "Xxcha":
        return Unit([7, 7], sustain=True, cannon=[5, 5, 5])
    if faction == "Yin":
        return Unit([9, 9], sustain=True)
    if faction == "Yssaril":
        return Unit([5, 5], sustain=True)
    if faction == "Argent":
        return Unit([7, 7], sustain=True)
    if faction == "Empyrean":
        return Unit([5, 5], sustain=True)
    if faction == "Mahact":
        return Unit([5, 5], sustain=True)
    if faction == "Naaz-Rokha":
        return Unit([9, 9], sustain=True)
    if faction == "Nomad":
        return Unit([7, 7], sustain=True, afb=[8, 8, 8])
    if faction == "Titans":
        return Unit([7, 7], sustain=True)
    if faction == "Vuil'Raith":
        return Unit([5, 5], sustain=True, bombard=[5])


def flagship2(faction):
    if faction == "Nomad":
        return Unit([5, 5], sustain=True, afb=[5, 5, 5])

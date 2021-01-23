class Unit:
    def __init__(self, name, combat, sustain=False, ground=False, bombard=[], afb=[], cannon=[],
                 shield=False, fighter=False, pds=False, disable_shield=False, direct_hit_immune=False):
        self.name = name
        self.combat = combat
        self.sustain = sustain
        self.can_sustain = sustain
        self.ground = ground
        self.bombard = bombard
        self.afb = afb
        self.cannon = cannon
        self.shield = shield
        self.fighter = fighter
        self.pds = pds
        self.disable_shield = disable_shield
        self.direct_hit_immune = direct_hit_immune

    def __repr__(self):
        return "<Combat: %s, Sustain: %s>" % (self.combat, self.sustain)


def warsun(faction):
    if faction == "Sardakk":
        return Unit("warsun", [2, 2, 2], sustain=True, bombard=[3, 3, 3], disable_shield=True)

    return Unit("warsun", [3, 3, 3], sustain=True, bombard=[3, 3, 3], disable_shield=True)


def cruiser(faction):
    if faction == "Sardakk":
        return Unit("cruiser", [6])

    return Unit("cruiser", [7])


def cruiser2(faction):
    if faction == "Sardakk":
        return Unit("cruiser", [5])

    return Unit("cruiser", [6])


def dread(faction):
    if faction == "Sardakk":
        return Unit("dread", [4], sustain=True, bombard=[4, 4])

    return Unit("dread", [5], sustain=True, bombard=[5])


def dread2(faction):
    if faction == "L1Z1X":
        return Unit("dread2", [4], sustain=True, bombard=[4], direct_hit_immune=True)

    if faction == "Sardakk":
        return Unit("dread", [4], sustain=True, bombard=[4, 4], direct_hit_immune=True)

    return Unit("dread", [5], sustain=True, bombard=[5], direct_hit_immune=True)


def destroyer(faction):
    if faction == "Sardakk":
        return Unit("destroyer", [8], afb=[9, 9])

    return Unit("destroyer", [9], afb=[9, 9])


def destroyer2(faction):
    if faction == "Sardakk":
        return Unit("destroyer", [7], afb=[6, 6, 6])

    return Unit("destroyer", [8], afb=[6, 6, 6])


def pds(faction):
    return Unit("pds", [], cannon=[6], shield=True, pds=True)


def pds2(faction):
    return Unit("pds", [], cannon=[5], shield=True, pds=True)


def carrier(faction):
    if faction == "Sardakk":
        return Unit("carrier", [8])

    return Unit("carrier", [9])


def carrier2(faction):
    if faction == "Sol":
        return Unit("carrier", [9], sustain=True)

    if faction == "Sardakk":
        return Unit("carrier", [8])

    return Unit("carrier", [9])


def fighter(faction):
    if faction == "Sardakk":
        return Unit("fighter", [8], fighter=True)

    return Unit("fighter", [9], fighter=True)


def fighter2(faction):
    if faction == "Sardakk":
        return Unit("fighter", [7], fighter=True)

    return Unit("fighter", [8], fighter=True)


def infantry(faction):
    if faction == "Sol":
        return Unit("infantry", [7], ground=True)

    if faction == "Sardakk":
        return Unit("infantry", [7], ground=True)

    return Unit("infantry", [8], ground=True)


def infantry2(faction):
    if faction == "Sol":
        return Unit("infantry", [6], ground=True)

    if faction == "Sardakk":
        return Unit("infantry", [6], ground=True)

    return Unit("infantry", [7], ground=True)


def mech(faction):
    if faction == "Arborec":
        return Unit("mech", [6], sustain=True, ground=True, shield=True)
    if faction == "L1Z1X":
        return Unit("mech", [6], sustain=True, ground=True, bombard=[8])
    if faction == "Sardakk":
        return Unit("mech", [5], sustain=True, ground=True)

    return Unit("mech", [6], sustain=True, ground=True)


def flagship(faction):
    if faction == "Arborec":
        return Unit("flagship", [7, 7], sustain=True)
    if faction == "Letnev":
        return Unit("flagship", [5, 5], sustain=True, bombard=[5, 5, 5], disable_shield=True)
    if faction == "Saar":
        return Unit("flagship", [5, 5], sustain=True, afb=[6, 6, 6, 6])
    if faction == "Muaat":
        return Unit("flagship", [5, 5], sustain=True)
    if faction == "Hacan":
        return Unit("flagship", [7, 7], sustain=True)
    if faction == "Sol":
        return Unit("flagship", [5, 5], sustain=True)
    if faction == "Creuss":
        return Unit("flagship", [5], sustain=True)
    if faction == "L1Z1X":
        return Unit("flagship", [5, 5], sustain=True)
    if faction == "Mentak":
        return Unit("flagship", [7, 7], sustain=True)
    if faction == "Naalu":
        return Unit("flagship", [9, 9], sustain=True)
    if faction == "Nekro":
        return Unit("flagship", [9, 9], sustain=True)
    if faction == "Sardakk":
        return Unit("flagship", [5, 5], sustain=True)
    if faction == "Jol-Nar":
        return Unit("flagship", [7, 7], sustain=True)
    if faction == "Winnu":
        return Unit("flagship", [7], sustain=True)
    if faction == "Xxcha":
        return Unit("flagship", [7, 7], sustain=True, cannon=[5, 5, 5])
    if faction == "Yin":
        return Unit("flagship", [9, 9], sustain=True)
    if faction == "Yssaril":
        return Unit("flagship", [5, 5], sustain=True)
    if faction == "Argent":
        return Unit("flagship", [7, 7], sustain=True)
    if faction == "Empyrean":
        return Unit("flagship", [5, 5], sustain=True)
    if faction == "Mahact":
        return Unit("flagship", [5, 5], sustain=True)
    if faction == "Naaz-Rokha":
        return Unit("flagship", [9, 9], sustain=True)
    if faction == "Nomad":
        return Unit("flagship", [7, 7], sustain=True, afb=[8, 8, 8])
    if faction == "Titans":
        return Unit("flagship", [7, 7], sustain=True)
    if faction == "Vuil'Raith":
        return Unit("flagship", [5, 5], sustain=True, bombard=[5])


def flagship2(faction):
    if faction == "Nomad":
        return Unit("flagship", [5, 5], sustain=True, afb=[5, 5, 5])

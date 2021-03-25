class Unit:
    def __init__(self, name, combat, sustain=False, ground=False, bombard=[], afb=[], cannon=[],
                 shield=False, fighter=False, pds=False, disable_shield=False, direct_hit_immune=False,
                 noneuclidean=False):
        self.name = name
        self.combat = combat
        self.sustain = sustain
        self.can_sustain = sustain
        self.just_sustained = False
        self.noneuclidean = noneuclidean
        self.ground = ground
        self.bombard = bombard
        self.afb = afb
        self.cannon = cannon
        self.shield = shield
        self.fighter = fighter
        self.pds = pds
        self.disable_shield = disable_shield
        self.direct_hit_immune = direct_hit_immune
        self.non_fighter_ship = not ground and not fighter and not pds

    def get_copy(self):
        return Unit(self.name, self.combat, self.can_sustain, self.ground, self.bombard, self.afb, self.cannon, self.shield, self.fighter, self.pds, self.disable_shield, self.direct_hit_immune, self.noneuclidean)

    def __repr__(self):
        return "%s <Combat: %s, Sustain: %s>" % (self.name, self.combat, self.sustain)

    def use_sustain(self, risk_direct_hit=True):
        if self.sustain and (risk_direct_hit or self.direct_hit_immune):
            self.sustain = False
            self.just_sustained = True
            return 2 if self.noneuclidean else 1
        return 0


def warsun(faction):
    if faction == "Sardakk":
        return Unit("warsun", [2, 2, 2], sustain=True, bombard=[3, 3, 3], disable_shield=True)

    if faction == "Jol-Nar":
        return Unit("warsun", [4, 4, 4], sustain=True, bombard=[3, 3, 3], disable_shield=True)

    return Unit("warsun", [3, 3, 3], sustain=True, bombard=[3, 3, 3], disable_shield=True)


def cruiser(faction):
    if faction == "Sardakk":
        return Unit("cruiser", [6])

    if faction == "Jol-Nar":
        return Unit("cruiser", [8])

    return Unit("cruiser", [7])


def cruiser2(faction):
    if faction == "Sardakk":
        return Unit("cruiser", [5])

    if faction == "Jol-Nar":
        return Unit("cruiser", [7])

    if faction == "Titans":
        return Unit("cruiser", [6], sustain=True)

    return Unit("cruiser", [6])


def dread(faction):
    if faction == "Sardakk":
        return Unit("dread", [4], sustain=True, bombard=[4, 4])

    if faction == "Jol-Nar":
        return Unit("dread", [6], sustain=True, bombard=[5])

    return Unit("dread", [5], sustain=True, bombard=[5])


def dread2(faction):
    if faction == "L1Z1X":
        return Unit("dread", [4], sustain=True, bombard=[4], direct_hit_immune=True)

    if faction == "Sardakk":
        return Unit("dread", [4], sustain=True, bombard=[4, 4], direct_hit_immune=True)

    if faction == "Jol-Nar":
        return Unit("dread", [6], sustain=True, bombard=[5], direct_hit_immune=True)

    return Unit("dread", [5], sustain=True, bombard=[5], direct_hit_immune=True)


def destroyer(faction):
    if faction == "Sardakk":
        return Unit("destroyer", [8], afb=[9, 9])

    if faction == "Jol-Nar":
        return Unit("destroyer", [10], afb=[9, 9])

    if faction == "Argent":
        return Unit("destroyer", [8], afb=[9, 9])

    return Unit("destroyer", [9], afb=[9, 9])


def destroyer2(faction):
    if faction == "Sardakk":
        return Unit("destroyer", [7], afb=[6, 6, 6])

    if faction == "Jol-Nar":
        return Unit("destroyer", [9], afb=[6, 6, 6])

    if faction == "Argent":
        return Unit("destroyer", [7], afb=[6, 6, 6])

    return Unit("destroyer", [8], afb=[6, 6, 6])


def pds(faction):
    if faction == "Titans":
        return Unit("pds", [7], cannon=[6], shield=True, pds=True, sustain=True, ground=True)

    return Unit("pds", [], cannon=[6], shield=True, pds=True)


def pds2(faction):
    if faction == "Titans":
        return Unit("pds", [6], cannon=[5], shield=True, pds=True, sustain=True, ground=True)

    return Unit("pds", [], cannon=[5], shield=True, pds=True)


def carrier(faction):
    if faction == "Sardakk":
        return Unit("carrier", [8])

    if faction == "Jol-Nar":
        return Unit("carrier", [10])

    return Unit("carrier", [9])


def carrier2(faction):
    if faction == "Sol":
        return Unit("carrier", [9], sustain=True)

    if faction == "Sardakk":
        return Unit("carrier", [8])

    if faction == "Jol-Nar":
        return Unit("carrier", [10])

    return Unit("carrier", [9])


def fighter(faction):
    if faction == "Sardakk":
        return Unit("fighter", [8], fighter=True)

    if faction == "Naalu":
        return Unit("fighter", [8], fighter=True)

    if faction == "Jol-Nar":
        return Unit("fighter", [10], fighter=True)

    return Unit("fighter", [9], fighter=True)


def fighter2(faction):
    if faction == "Sardakk":
        return Unit("fighter", [7], fighter=True)

    if faction == "Naalu":
        return Unit("fighter", [7], fighter=True)

    if faction == "Jol-Nar":
        return Unit("fighter", [9], fighter=True)

    return Unit("fighter", [8], fighter=True)


def infantry(faction):
    if faction == "Sol":
        return Unit("infantry", [7], ground=True)

    if faction == "Sardakk":
        return Unit("infantry", [7], ground=True)

    if faction == "Jol-Nar":
        return Unit("infantry", [9], ground=True)

    return Unit("infantry", [8], ground=True)


def infantry2(faction):
    if faction == "Sol":
        return Unit("infantry", [6], ground=True)

    if faction == "Sardakk":
        return Unit("infantry", [6], ground=True)

    if faction == "Jol-Nar":
        return Unit("infantry", [8], ground=True)

    return Unit("infantry", [7], ground=True)


def mech(faction):
    if faction == "Arborec":
        return Unit("mech", [6], sustain=True, ground=True, shield=True, direct_hit_immune=True)
    if faction == "L1Z1X":
        return Unit("mech", [6], sustain=True, ground=True, bombard=[8], direct_hit_immune=True)
    if faction == "Sardakk":
        return Unit("mech", [5], sustain=True, ground=True, direct_hit_immune=True)
    if faction == "Jol-Nar":
        return Unit("mech", [7], sustain=True, ground=True, direct_hit_immune=True)
    if faction == "Xxcha":
        return Unit("mech", [6], cannon=[8], sustain=True, ground=True, direct_hit_immune=True)
    if faction == "Naaz-Rokha":
        return Unit("mech", [6, 6], sustain=True, ground=True, direct_hit_immune=True)

    return Unit("mech", [6], sustain=True, ground=True, direct_hit_immune=True)


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


def experimental_battlestation(faction):
    return Unit("experimental", [], cannon=[5, 5, 5], pds=True)

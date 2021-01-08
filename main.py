import random


class Unit:
    def __init__(self, combat, sustain=False):
        self.combat = combat
        self.sustain = sustain

    def __repr__(self):
        return "<Combat: %s, Sustain: %s>" % (self.combat, self.sustain)


def infantry():
    return Unit(8)


def mech():
    return Unit(6, sustain=True)


def generate_hits(units):
    result = 0
    for u in units:
        x = random.randint(1, 10)
        if x >= u.combat:
            result += 1
    return result


def assign_hits(units, hits):
    for u in units:
        if u.sustain:
            u.sustain = False
            hits -= 1
            if hits == 0:
                return units

    while hits > 0 and units:
        del units[0]
        hits -= 1

    return units


def combat_round(att_units, def_units):
    att_hits = generate_hits(att_units)
    def_hits = generate_hits(def_units)

    att_units = assign_hits(att_units, def_hits)
    def_units = assign_hits(def_units, att_hits)

    return att_units, def_units


def iteration(att_units, def_units):
    # 0 - tie
    # 1 - attacker won
    # 2 - defender won
    while att_units and def_units:
        att_units, def_units = combat_round(att_units, def_units)

    if not att_units and not def_units:
        return 0
    elif not att_units:
        return 2
    elif not def_units:
        return 1


a = Unit(3)
att_inf = 2
def_mech = 1

outcomes = [0, 0, 0]

it = 10000
for i in range(it):
    att_units = [infantry()] * att_inf
    def_units = [mech()] * def_mech
    res = iteration(att_units, def_units)
    outcomes[res] += 1

print("Attacker wins: %.1f%%" % (outcomes[1] / it * 100))
print("Tie: %.1f%%" % (outcomes[0] / it * 100))
print("Defender wins: %.1f%%" % (outcomes[2] / it * 100))

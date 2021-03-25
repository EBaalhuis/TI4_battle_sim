import app.calculator.units as units
import app.calculator.assign as assign
import app.calculator.util as util


def cannon_roll(val, jolnar_commander):
    x = util.roll()
    if x >= val:
        return 1

    # Jol-Nar commander
    elif jolnar_commander:
        x = util.roll()
        if x >= val:
            return 1

    return 0


def generate_space_cannon_hits(units, options, attacker):
    result = 0
    best_dice = 11
    jolnar_commander = (attacker and options["att_jolnar_commander"]) \
                       or (not attacker and options["def_jolnar_commander"])

    for u in units:
        for val in u.cannon:
            best_dice = min(best_dice, val)
            result += cannon_roll(val, jolnar_commander)

    # Plasma Scoring
    if (attacker and options["att_plasma"]) or (not attacker and options["def_plasma"]):
        result += cannon_roll(best_dice, jolnar_commander)

    # Argent Commander
    if (attacker and options["att_argent_commander"]) or (not attacker and options["def_argent_commander"]):
        result += cannon_roll(best_dice, jolnar_commander)

    return result


def space_cannon_offense(att_units, def_units, options):
    # Experimental Battlestation
    if options["def_experimental"]:
        def_units = [units.experimental_battlestation(options["def_faction"])] + def_units

    att_cannon_hits = generate_space_cannon_hits(att_units, options, attacker=True)
    def_cannon_hits = generate_space_cannon_hits(def_units, options, attacker=False)

    # Maneuvering Jets
    if options["def_maneuvering"]:
        att_cannon_hits = max(0, att_cannon_hits - 1)
    if options["att_maneuvering"]:
        def_cannon_hits = max(0, def_cannon_hits - 1)

    if options["def_graviton"]:
        att_units, options = assign.assign_nonfighters_first(att_units, def_cannon_hits, options["att_riskdirecthit"],
                                                      options["att_faction"], options, True)
    else:
        att_units, options = assign.assign_hits(att_units, def_cannon_hits, options["att_riskdirecthit"],
                                         options["att_faction"], options, True)
    if options["att_graviton"]:
        def_units, options = assign.assign_nonfighters_first(def_units, att_cannon_hits, options["def_riskdirecthit"],
                                                      options["def_faction"], options, False)
    else:
        def_units, options = assign.assign_hits(def_units, att_cannon_hits, options["def_riskdirecthit"],
                                         options["def_faction"], options, False)

    return att_units, def_units, options


def space_cannon_defense(att_units, def_units, options):
    cannon_hits = generate_space_cannon_hits(def_units, options, attacker=False)

    # Maneuvering Jets
    if options["att_maneuvering"]:
        cannon_hits = max(0, cannon_hits - 1)

    att_units, options = assign.assign_hits(att_units, cannon_hits, options["att_riskdirecthit"], options["att_faction"],
                                     options, False)

    return att_units, def_units, options

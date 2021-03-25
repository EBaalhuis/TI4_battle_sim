import app.calculator.assign as assign
import app.calculator.filters as filters
import app.calculator.tech_abilities as tech_abilities
import app.calculator.util as util


def bombard_roll(val, options, jolnar_commander):
    x = util.roll()
    if options["def_bunker"]:
        x -= 4
    if x >= val:
        return 1

    # Jol-Nar commander
    elif jolnar_commander:
        x = util.roll()
        if options["def_bunker"]:
            x -= 4
        if x >= val:
            return 1

    return 0


def bombardment(att_units, def_units, options):
    jolnar_commander = options["att_jolnar_commander"]  # Bobmardment is exclusively done by the attacker
    bombard_hits = 0
    best_dice = 11
    for u in att_units:
        if u.bombard:
            for val in u.bombard:
                best_dice = min(best_dice, val)
                bombard_hits += bombard_roll(val, options, jolnar_commander)

    # Plasma Scoring
    if options["att_plasma"]:
        bombard_hits += bombard_roll(best_dice, options, jolnar_commander)

    # Argent Commander
    if options["att_argent_commander"]:
        bombard_hits += bombard_roll(best_dice, options, jolnar_commander)

    if not options["att_x89"]:
        def_units, options = assign.assign_hits(def_units, bombard_hits, options["def_riskdirecthit"],
                                                options["def_faction"],
                                                options, False)
    else:
        def_units = tech_abilities.x89(def_units, bombard_hits)

    att_units, harrow_bombarders = filters.filter_bombardment(att_units, options["att_faction"])

    return att_units, def_units, harrow_bombarders, options


def harrow(def_units, harrow_bombarders, options):
    att_units, def_units, harrow_bombarders, options = bombardment(harrow_bombarders, def_units, options)
    return def_units, options

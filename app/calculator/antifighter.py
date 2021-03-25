import random
import app.calculator.assign as assign
import app.calculator.faction_abilities as faction_abilities


def antifighter_roll(val, swa2, jolnar_commander):
    x = random.randint(1, 10)
    swa2_hits = 0

    # Strike Wing Alpha II destroying infantry ability
    if swa2 and x >= 9:
        swa2_hits = 1

    if x >= val:
        return 1, swa2_hits

    # Jol-Nar commander
    elif jolnar_commander:
        x = random.randint(1, 10)

        # Strike Wing Alpha II destroying infantry ability
        if swa2 and x >= 9:
            swa2_hits = 1

        if x >= val:
            return 1, swa2_hits

    return 0, swa2_hits


def generate_antifighter_hits(units, swa2, options, attacker):
    jolnar_commander = (attacker and options["att_jolnar_commander"]) or \
                       (not attacker and options["def_jolnar_commander"])
    result = 0
    swa2_hits = 0
    best_dice = 11
    best_unit_destroyer = False
    for u in units:
        for val in u.afb:
            if val < best_dice:
                best_dice = val
                best_unit_destroyer = u.name == "destroyer"
            best_dice = min(best_dice, val)
            roll, swa2_roll = antifighter_roll(val, swa2 and u.name == "destroyer", jolnar_commander)
            result += roll
            swa2_hits += swa2_roll

    # Argent Commander
    if (attacker and options["att_argent_commander"]) or (not attacker and options["def_argent_commander"]):
        roll, swa2_roll = antifighter_roll(best_dice, swa2 and best_unit_destroyer, jolnar_commander)
        result += roll
        swa2_hits += swa2_roll

    return result, swa2_hits


def antifighter(att_units, def_units, options):
    att_afb_hits, att_swa2_infantry_hits = generate_antifighter_hits(att_units, options["att_faction"] == "Argent"
                                                                     and options["att_destroyer2"], options,
                                                                     attacker=True)
    def_afb_hits, def_swa2_infantry_hits = generate_antifighter_hits(def_units, options["def_faction"] == "Argent"
                                                                     and options["att_destroyer2"], options,
                                                                     attacker=False)

    # Strike Wing Alpha II infantry hits
    if att_swa2_infantry_hits > 0:
        def_units = faction_abilities.assign_swa2(def_units, att_swa2_infantry_hits)
    if def_swa2_infantry_hits > 0:
        att_units = faction_abilities.assign_swa2(att_units, def_swa2_infantry_hits)

    # Argent Flight Raid Formation
    if options["att_faction"] == "Argent" or options["def_faction"] == "Argent":
        att_units, def_units = faction_abilities.raid_formation(att_units, def_units, att_afb_hits, def_afb_hits,
                                                                options)

    # Assign hits, depending on Waylay
    if options["def_waylay"]:
        att_units, options = assign.assign_hits(att_units, def_afb_hits, options["att_riskdirecthit"],
                                                options["att_faction"],
                                                options, True)
    else:
        att_units, options = assign.assign_fighters_only(att_units, def_afb_hits, options, attacker=True)

    if options["att_waylay"]:
        def_units, options = assign.assign_hits(def_units, att_afb_hits, options["def_riskdirecthit"],
                                                options["def_faction"],
                                                options, False)
    else:
        def_units, options = assign.assign_fighters_only(def_units, att_afb_hits, options, attacker=False)

    return att_units, def_units, options

import app.calculator.faction_abilities as faction_abilities
import app.calculator.util as util


def shield_active(att_units, def_units, options):
    for u in att_units:
        if u.disable_shield:
            return False

    # L1Z1X commander
    if options["att_l1z1x_commander"]:
        return False

    for u in def_units:
        if u.shield:
            return True

    return False


def filter_ground(att_units, def_units, options):
    att_res, def_res = [], []

    shield = shield_active(att_units, def_units, options)
    for u in att_units:
        if u.ground:
            if shield:
                u.bombard = []
            att_res.append(u)
        elif u.bombard and not shield:
            att_res.append(u)

    for u in def_units:
        if u.ground or u.cannon:
            def_res.append(u)

    # Naalu flagship
    if options["att_faction"] == "Naalu" and util.has_flagship(att_units):
        att_res = faction_abilities.naalu_flagship(att_units) + att_res
    if options["def_faction"] == "Naalu" and util.has_flagship(def_units):
        def_res = faction_abilities.naalu_flagship(def_units) + def_res

    return att_res, def_res


def filter_space(att_units, def_units, options):
    if options["att_faction"] == "Nekro" and util.has_flagship(att_units):
        att_result = list(filter(lambda x: not x.ground or len(x.cannon) > 0 or x.name == "infantry", att_units))
    else:
        att_result = list(filter(lambda x: not x.ground or len(x.cannon) > 0, att_units))

    if options["def_faction"] == "Nekro" and util.has_flagship(def_units):
        def_result = list(filter(lambda x: not x.ground or len(x.cannon) > 0 or x.name == "infantry", def_units))
    else:
        def_result = list(filter(lambda x: not x.ground or len(x.cannon) > 0, def_units))

    return att_result, def_result


def filter_bombardment(units, faction):
    if faction != "L1Z1X":
        return list(filter(lambda x: x.ground, units)), []
    else:
        return list(filter(lambda x: x.ground, units)), list(filter(lambda x: not x.ground, units))

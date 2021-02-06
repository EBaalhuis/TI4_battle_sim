import app.calculator.units as units
import app.calculator.faction_abilities as faction_abilities


def parse_unit(unit_type, unit_dict, attacker, options):
    prefix = "att_" if attacker else "def_"

    faction = options[prefix + "faction"]
    amount = unit_dict[unit_type]
    upgraded = options[prefix + unit_type + "2"]

    if unit_type == "fighter":
        func = units.fighter2 if upgraded else units.fighter
    elif unit_type == "carrier":
        func = units.carrier2 if upgraded else units.carrier
    elif unit_type == "destroyer":
        func = units.destroyer2 if upgraded else units.destroyer
    elif unit_type == "cruiser":
        func = units.cruiser2 if upgraded else units.cruiser
    elif unit_type == "dread":
        func = units.dread2 if upgraded else units.dread
    elif unit_type == "flagship":
        func = units.flagship2 if upgraded else units.flagship
    elif unit_type == "warsun":
        func = units.warsun
    elif unit_type == "infantry":
        func = units.infantry2 if upgraded else units.infantry
    elif unit_type == "mech":
        func = units.mech
        # Naaz-Rokha mech (ship side)
        if faction == "Naaz-Rokha" and not options["ground_combat"]:
            func = faction_abilities.naaz_mech
    elif unit_type == "pds":
        func = units.pds2 if upgraded else units.pds

    return [func(faction) for _ in range(amount)]


def parse_units(unit_dict, attacker, options):
    unit_types = ["fighter", "carrier", "destroyer", "cruiser", "dread", "infantry", "mech", "flagship", "warsun",
                  "pds"]
    result = []
    for u in unit_types:
        result = result + parse_unit(u, unit_dict, attacker, options)

    return result

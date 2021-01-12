from collections import defaultdict


def options_from_form(form):
    labels = ["ground_combat", "att_faction", "def_faction", "att_antimass", "def_antimass", "att_graviton",
              "def_graviton", "att_plasma", "def_plasma", "def_magen", "def_magen_o", "att_bacterial", "att_duranium",
              "def_duranium", "att_assault", "def_assault"]
    options = {}

    for label in labels:
        options[label] = form[label].data

    return options


def units_from_form(form):
    attacker = defaultdict(lambda: 0)
    defender = defaultdict(lambda: 0)

    attacker["flagship"] = form.att_flagship.data
    defender["flagship"] = form.def_flagship.data

    attacker["warsun"] = form.att_warsun.data
    defender["warsun"] = form.def_warsun.data

    attacker["dread"] = form.att_dread.data
    defender["dread"] = form.def_dread.data

    attacker["cruiser"] = form.att_cruiser.data
    defender["cruiser"] = form.def_cruiser.data

    attacker["carrier"] = form.att_carrier.data
    defender["carrier"] = form.def_carrier.data

    attacker["destroyer"] = form.att_destroyer.data
    defender["destroyer"] = form.def_destroyer.data

    attacker["fighter"] = form.att_fighter.data
    defender["fighter"] = form.def_fighter.data

    attacker["mech"] = form.att_mech.data
    defender["mech"] = form.def_mech.data

    attacker["infantry"] = form.att_infantry.data
    defender["infantry"] = form.def_infantry.data

    attacker["pds"] = form.att_pds.data
    defender["pds"] = form.def_pds.data

    return attacker, defender

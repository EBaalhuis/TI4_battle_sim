from collections import defaultdict


def options_from_form(form):
    labels = ["ground_combat", "att_faction", "def_faction", "att_antimass", "def_antimass", "att_graviton",
              "def_graviton", "att_plasma", "def_plasma", "def_magen", "def_magen_o", "att_x89", "att_duranium",
              "def_duranium", "att_assault", "def_assault", "def_bunker", "def_experimental", "att_prototype",
              "def_prototype", "att_fireteam", "def_fireteam", "att_maneuvering", "def_maneuvering", "att_morale",
              "def_morale", "att_waylay", "def_waylay"]
    options = defaultdict(lambda: False)

    for label in labels:
        options[label] = form[label].data

    return options


def units_from_form(form):
    unit_names = ["flagship", "warsun", "dread", "cruiser", "carrier", "destroyer", "fighter", "mech", "infantry",
                  "pds"]
    attacker = defaultdict(lambda: 0)
    defender = defaultdict(lambda: 0)

    for u in unit_names:
        attacker[u] = form["att_" + u].data
        defender[u] = form["def_" + u].data

    return attacker, defender

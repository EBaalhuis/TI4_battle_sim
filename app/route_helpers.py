from collections import defaultdict


def options_from_form(form):
    misc = ["ground_combat", "att_faction", "def_faction", "def_nebula", "att_riskdirecthit", "def_riskdirecthit"]
    techs = ["att_antimass", "def_antimass", "att_graviton", "def_graviton", "att_plasma", "def_plasma", "def_magen",
             "def_magen_o", "att_x89", "att_duranium", "def_duranium", "att_assault", "def_assault"]
    cards = ["def_bunker", "def_experimental", "att_prototype", "def_prototype", "att_fireteam", "def_fireteam",
             "att_maneuvering", "def_maneuvering", "att_morale", "def_morale", "att_waylay", "def_waylay"]
    upgrades = ["att_flagship2", "def_flagship2", "att_dread2", "def_dread2", "att_cruiser2", "def_cruiser2",
                "att_carrier2", "def_carrier2", "att_destroyer2", "def_destroyer2", "att_fighter2", "def_fighter2",
                "att_infantry2", "def_infantry2", "att_pds2", "def_pds2"]
    agendas = ["publicize", "conventions"]
    promissories = ["att_argent_prom", "def_argent_prom", "att_warfunding", "def_warfunding", "att_warfunding_omega",
                    "def_warfunding_omega", "att_tekklar", "def_tekklar", "att_cavalry1", "def_cavalry1",
                    "att_cavalry2", "def_cavalry2"]
    agents = ["att_letnev_agent", "def_letnev_agent", "att_nomad_agent", "def_nomad_agent", "att_sol_agent",
              "def_sol_agent", "att_titans_agent", "def_titans_agent", "att_yin_agent", "def_yin_agent"]

    commander_factions = ["argent", "jolnar", "l1z1x", "letnev", "sol", "winnu"]
    commanders = ["att_" + c + "_commander" for c in commander_factions] + \
                 ["def_" + c + "_commander" for c in commander_factions]

    options = defaultdict(lambda: False)

    for label in misc + techs + cards + upgrades + agendas + promissories + agents + commanders:
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

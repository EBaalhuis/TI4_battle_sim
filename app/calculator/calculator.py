import random
import copy
import app.calculator.units as units
import app.calculator.assign as assign
import app.calculator.faction_abilities as faction_abilities
import app.calculator.tech_abilities as tech_abilities
import app.calculator.parser as parser
import app.calculator.filters as filters
import app.calculator.space_cannon as space_cannon
import app.calculator.antifighter as antifighter
import app.calculator.bombard as bombard
import app.calculator.util as util


def roll_for_hit(units, u, faction, bonus, prototype):
    x = random.randint(1, 10)
    extra_hits = 0

    # Jol-Nar flagship
    if faction == "Jol-Nar" and u.name == "flagship":
        if x >= 9:
            extra_hits += 2

    # Sardakk flagship
    if faction == "Sardakk" and util.has_flagship(units) and u.name != "flagship":
        x += 1

    # Morale Boost / Supercharge
    x += bonus

    # Prototype Fighter
    if prototype and u.fighter:
        x += 2

    return x, extra_hits


def generate_hits(units, faction, bonus, prototype, fire_team, war_funding, war_funding_o, sol_agent, letnev_agent):
    hits = 0
    non_fighter_hits = 0

    # Sol agent
    if sol_agent:
        units, modified_unit = faction_abilities.apply_sol_agent(units)

    # Letnev agent
    if letnev_agent:
        units, modified_unit = faction_abilities.apply_letnev_agent(units)

    for u in units:
        for val in u.combat:
            x, extra_hits = roll_for_hit(units, u, faction, bonus, prototype)
            hits += extra_hits

            if x >= val:
                # L1Z1X Flagship
                if faction == "L1Z1X" and util.has_flagship(units) and u.name in ["flagship", "dread"]:
                    non_fighter_hits += 1
                else:
                    hits += 1

            # Fire Team / War Funding re-roll
            else:
                if fire_team:  # re-roll if it was a miss, ground combat only (so no prototype, L1 flagship)
                    x = random.randint(1, 10)
                    x += bonus
                    if x >= val:
                        hits += 1

                if war_funding or war_funding_o:  # space combat only
                    x, extra_hits = roll_for_hit(units, u, faction, bonus, prototype)
                    hits += extra_hits
                    if x >= val:
                        hits += 1

    # Sol agent
    if sol_agent:
        # noinspection PyUnboundLocalVariable
        modified_unit.combat = modified_unit.combat[:-1]

    # Letnev agent
    if letnev_agent:
        modified_unit.combat = modified_unit.combat[:-1]

    return hits, non_fighter_hits


def combat_round(att_units, def_units, first_round, options):
    # Winnu flagship
    if options["att_faction"] == "Winnu" or options["def_faction"] == "Winnu":
        att_units, def_units = faction_abilities.winnu_flagship(att_units, def_units, options)

    att_bonus, def_bonus = 0, 0
    if first_round:
        if options["att_morale"]:
            att_bonus += 1
        # Naaz-Rokha Supercharge
        if options["att_naazrokha_supercharge_nekro_hide"]:
            att_bonus += 1
        if options["def_morale"]:
            def_bonus += 1
        # Naaz-Rokha Supercharge
        if options["def_naazrokha_supercharge_nekro_hide"]:
            def_bonus += 1

    att_options = {"faction": options["att_faction"],
                   "bonus": att_bonus,
                   "prototype": first_round and options["att_prototype"],
                   "fire_team": options["att_fireteam"] and first_round and options["ground_combat"],
                   "war_funding": options["att_warfunding"] and first_round and not options["ground_combat"],
                   "war_funding_o": options["att_warfunding_omega"] and first_round and not options["ground_combat"],
                   "sol_agent": first_round and options["att_sol_agent"] and options["ground_combat"],
                   "letnev_agent": first_round and options["att_letnev_agent"] and not options["ground_combat"]}

    def_options = {"faction": options["def_faction"],
                   "bonus": def_bonus,
                   "prototype": first_round and options["def_prototype"],
                   "fire_team": options["def_fireteam"] and first_round and options["ground_combat"],
                   "war_funding": options["def_warfunding"] and first_round and not options["ground_combat"],
                   "war_funding_o": options["def_warfunding_omega"] and first_round and not options["ground_combat"],
                   "sol_agent": first_round and options["def_sol_agent"] and options["ground_combat"],
                   "letnev_agent": first_round and options["def_letnev_agent"] and not options["ground_combat"]}

    att_hits, att_nonfighter_hits = generate_hits(att_units, **att_options)
    def_hits, def_nonfighter_hits = generate_hits(def_units, **def_options)

    # War Funding Omega
    if options["att_warfunding_omega"] and util.above_average(def_units, def_hits):
        def_hits, def_nonfighter_hits = generate_hits(def_units, **def_options)
    if options["def_warfunding_omega"] and util.above_average(att_units, att_hits):
        att_hits, att_nonfighter_hits = generate_hits(att_units, **att_options)

    # Magen Defense Grid
    if first_round and options["def_magen"] and options["ground_combat"] and \
            len(list(filter(lambda x: x.shield, def_units))) > 0:
        att_hits = 0

    # remove PDS as they do not participate in combat (cannot be assigned hits)
    if first_round:
        att_units = list(filter(lambda x: not x.pds or x.ground, att_units))
        def_units = list(filter(lambda x: not x.pds or x.ground, def_units))

    # Letnev flagship (repair)
    if options["att_faction"] == "Letnev" or options["def_faction"] == "Letnev":
        att_units, def_units = faction_abilities.letnev_flagship_repair(att_units, def_units, options)

    # Sardakk mech
    if options["att_faction"] == "Sardakk" or options["def_faction"] == "Sardakk":
        att_hits, def_hits = faction_abilities.sardakk_mechs(att_units, def_units, att_hits, def_hits, options)

    # Valkyrie Particle Weave
    if options["att_sardakk_valkyrie_nekro_hide"] and options["ground_combat"]:
        # The part after the "or" is in case opponent also has VPW - it is mandatory to use
        if def_hits > 0 or (options["def_sardakk_valkyrie_nekro_hide"] and options["ground_combat"] and att_hits > 0):
            att_hits += 1
    if options["def_sardakk_valkyrie_nekro_hide"] and options["ground_combat"]:
        if att_hits > 0:
            def_hits += 1

    att_units, options = assign.assign_hits(att_units, def_hits, options["att_riskdirecthit"], options["att_faction"],
                                            options, True)
    att_units, options = assign.assign_nonfighters_first(att_units, def_nonfighter_hits, options["att_riskdirecthit"],
                                                         options["att_faction"], options, True)
    def_units, options = assign.assign_hits(def_units, att_hits, options["def_riskdirecthit"], options["def_faction"],
                                            options, False)
    def_units, options = assign.assign_nonfighters_first(def_units, att_nonfighter_hits, options["def_riskdirecthit"],
                                                         options["def_faction"], options, False)

    # Duranium Armor
    if options["att_duranium"]:
        tech_abilities.duranium(att_units)
    if options["def_duranium"]:
        tech_abilities.duranium(def_units)

    return att_units, def_units


def start_of_space_combat(att_units, def_units, options):
    # Mentak Ambush
    if options["att_faction"] == "Mentak" or options["def_faction"] == "Mentak":
        att_hits, def_hits = faction_abilities.mentak_ambush(att_units, def_units, options)
        att_units, options = assign.assign_hits(att_units, def_hits, options["att_riskdirecthit"],
                                                options["att_faction"], options, True)
        def_units, options = assign.assign_hits(def_units, att_hits, options["def_riskdirecthit"],
                                                options["def_faction"], options, False)

    # Assault Cannon
    if options["att_assault"] and len(list(filter(lambda x: x.non_fighter_ship, att_units))) >= 3:
        def_units = tech_abilities.assault(def_units)
    if options["def_assault"] and len(list(filter(lambda x: x.non_fighter_ship, def_units))) >= 3:
        att_units = tech_abilities.assault(att_units)

    # Creuss Dimensional Splicer
    if options["att_creuss_dimensionalsplicer_nekro_hide"] \
            and any(map(lambda x: x.fighter or x.non_fighter_ship, att_units)):
        def_units = tech_abilities.dimensional_splicer(def_units)
    if options["def_creuss_dimensionalsplicer_nekro_hide"] \
            and any(map(lambda x: x.fighter or x.non_fighter_ship, def_units)):
        att_units = tech_abilities.dimensional_splicer(att_units)

    return att_units, def_units, options


def iteration(att_units, def_units, options):
    if not options["ground_combat"]:
        # space cannon offense
        att_units, def_units, options = space_cannon.space_cannon_offense(att_units, def_units, options)

        # start of space combat abilities
        att_units, def_units, options = start_of_space_combat(att_units, def_units, options)

        # anti-fighter barrage
        att_units, def_units, options = antifighter.antifighter(att_units, def_units, options)

    if options["ground_combat"]:
        # bombardment
        att_units, def_units, harrow_bombarders, options = bombard.bombardment(att_units, def_units, options)

        # Mentak mech
        if options["att_faction"] == "Mentak" or options["def_faction"] == "Mentak":
            att_units, def_units = faction_abilities.mentak_mech(att_units, def_units, options)

        # space cannon defense
        att_units, def_units, options = space_cannon.space_cannon_defense(att_units, def_units, options)

        # Magen Defense Grid Omega
        if options["def_magen_o"]:
            att_units = tech_abilities.magen_omega(att_units)
    else:
        harrow_bombarders = []

    first_round = True
    while att_units and def_units:
        att_units, def_units = combat_round(att_units, def_units, first_round, options)
        first_round = False
        if options["att_faction"] == "L1Z1X":
            def_units, options = bombard.harrow(def_units, harrow_bombarders, options)

    # Naalu flagship: remove fighters at end of ground combat
    if (options["att_faction"] == "Naalu" or options["def_faction"] == "Naalu") and options["ground_combat"]:
        att_units = list(filter(lambda x: not x.fighter, att_units))
        def_units = list(filter(lambda x: not x.fighter, def_units))

    if not att_units and not def_units:
        return 0
    elif not att_units:
        return 2
    elif not def_units:
        return 1


def mods_before_combat(att_units, def_units, options):
    # Non-Euclidean Shielding
    if options["att_letnev_noneuclidean_nekro_hide"]:
        att_units = tech_abilities.noneuclidean(att_units)
    if options["def_letnev_noneuclidean_nekro_hide"]:
        def_units = tech_abilities.noneuclidean(def_units)

    # Naaz-Rokha flagship
    if options["att_faction"] == "Naaz-Rokha" and util.has_flagship(att_units):
        att_units = faction_abilities.naaz_flagship(att_units)
    if options["def_faction"] == "Naaz-Rokha" and util.has_flagship(def_units):
        def_units = faction_abilities.naaz_flagship(def_units)

    # Winnu commander
    if options["att_winnu_commander"]:
        att_units = faction_abilities.winnu_commander(att_units)
    if options["def_winnu_commander"]:
        def_units = faction_abilities.winnu_commander(def_units)

    # Antimass Deflectors
    if options["att_antimass"]:
        for u in def_units:
            u.cannon = [x + 1 for x in u.cannon]
    if options["def_antimass"]:
        for u in att_units:
            u.cannon = [x + 1 for x in u.cannon]

    # Strike Wing Ambuscade
    if options["att_argent_prom"] or options["def_argent_prom"]:
        att_units, def_units = faction_abilities.argent_prom(att_units, def_units, options)

    # Titan agent
    if options["att_titans_agent"]:
        att_units = faction_abilities.titans_agent(att_units)
    if options["def_titans_agent"]:
        def_units = faction_abilities.titans_agent(def_units)

    if options["ground_combat"]:
        # Naalu mech / Nekro mech
        if options["att_naalu_mech_hide"] or options["att_nekro_mech_hide"]:
            att_units = faction_abilities.naalu_nekro_mech(att_units)
        if options["def_naalu_mech_hide"] or options["def_nekro_mech_hide"]:
            def_units = faction_abilities.naalu_nekro_mech(def_units)

        # Jol-Nar mech
        if options["att_faction"] == "Jol-Nar" and util.has_mech(att_units):
            att_units = faction_abilities.jol_nar_mech(att_units)
        if options["def_faction"] == "Jol-Nar" and util.has_mech(def_units):
            def_units = faction_abilities.jol_nar_mech(def_units)

        # L4 Disruptors
        if options["att_letnev_l4_nekro_hide"]:
            for u in def_units:
                u.cannon = []

        # Conventions of War
        if options["conventions"]:
            for u in att_units:
                u.bombard = []

        # Tekklar Legion
        if options["att_tekklar"] or options["def_tekklar"]:
            att_units, def_units = faction_abilities.tekklar(att_units, def_units, options)

        # Sol commander
        if options["def_sol_commander"] and any(map(lambda x: x.ground, def_units)):
            extra_infantry = [units.infantry2(options["def_faction"]) if options["def_infantry2"]
                              else units.infantry(options["def_faction"])]
            def_units = extra_infantry + def_units

    else:  # space combat
        # Mahact flagship
        if options["att_mahact_flagship_hide"]:
            att_units = faction_abilities.mahact_flagship(att_units)
        if options["def_mahact_flagship_hide"]:
            def_units = faction_abilities.mahact_flagship(def_units)

        # The Cavalry
        if options["att_cavalry1"] or options["att_cavalry2"]:
            att_units = faction_abilities.cavalry(att_units, upgraded=options["att_cavalry2"])
        if options["def_cavalry1"] or options["def_cavalry2"]:
            def_units = faction_abilities.cavalry(def_units, upgraded=options["def_cavalry2"])

        # Argent flagship
        if options["att_faction"] == "Argent" or options["def_faction"] == "Argent":
            att_units, def_units = faction_abilities.argent_flagship(att_units, def_units, options)

        # Mentak flagship
        if options["att_faction"] == "Mentak" or options["def_faction"] == "Mentak":
            att_units, def_units = faction_abilities.mentak_flagship(att_units, def_units, options)

        # Defending in Nebula
        if options["def_nebula"] and not options["ground_combat"]:
            for u in def_units:
                u.combat = [x - 1 for x in u.combat]

        # Publicize Weapon Schematics
        if options["publicize"]:
            for u in att_units + def_units:
                if u.name == "warsun":
                    u.sustain = False
                    u.can_sustain = False

        # Yin agent
        if options["att_yin_agent"]:
            options["att_yin_agent_active"] = True
        if options["def_yin_agent"]:
            options["def_yin_agent_active"] = True

    return att_units, def_units, options


def run_simulation(att_units, def_units, options, it):
    outcomes = [0, 0, 0]

    # Filter units based on ground combat vs space combat
    if options["ground_combat"]:
        att_units, def_units = filters.filter_ground(att_units, def_units, options)
    else:
        att_units, def_units = filters.filter_space(att_units, def_units, options)

    att_units, def_units, options = mods_before_combat(att_units, def_units, options)

    for i in range(it):        
        a_unit_cp = [a.get_copy() for a in att_units]
        d_unit_cp = [d.get_copy() for d in def_units]

        res = iteration(a_unit_cp, d_unit_cp, options)

        # Yin flagship
        if options["att_faction"] == "Yin" and util.has_flagship(att_units) and res == 2:
            res = 0
        if options["def_faction"] == "Yin" and util.has_flagship(def_units) and res == 1:
            res = 0

        outcomes[res] += 1

    return outcomes


def calculate(attacker_units, defender_units, options, test=True):
    it = 10000 if test else 3000

    att_units = parser.parse_units(attacker_units, attacker=True, options=options)
    def_units = parser.parse_units(defender_units, attacker=False, options=options)

    outcomes = run_simulation(att_units, def_units, options, it=it)
    outcomes = list(map(lambda x: int(round(x / it * 100, 0)), outcomes))

    return outcomes

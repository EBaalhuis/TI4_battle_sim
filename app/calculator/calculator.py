import random
import copy
import app.calculator.units as units
import app.calculator.faction_abilities as faction_abilities
import app.calculator.tech_abilities as tech_abilities
import app.calculator.parser as parser
import app.calculator.filters as filters
import app.calculator.util as util


def harrow(def_units, harrow_bombarders, options):
    hits = bombardment(harrow_bombarders, options)
    def_units, options = assign_hits(def_units, hits, True, options["def_faction"], options, False)
    return def_units, options


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
        modified_unit.combat = modified_unit.combat[:-1]

    # Letnev agent
    if letnev_agent:
        modified_unit.combat = modified_unit.combat[:-1]

    return hits, non_fighter_hits


def assign_hits(units, hits, risk_direct_hit, faction, options, attacker):
    # Letnev flagship (sustain)
    if faction == "Letnev":
        units, hits = faction_abilities.letnev_flagship_sustain(units, hits, risk_direct_hit)

    for u in units:
        if hits <= 0:
            return units, options
        hits -= u.use_sustain(risk_direct_hit)

    while hits > 0 and units:
        if units[0].sustain:
            hits -= u.use_sustain(risk_direct_hit=True)
            # Once one ship sustains and is not Direct Hit, assume its safe
            return assign_hits(units, hits, True, faction, options, attacker)
        else:
            # Check if only PDS are left
            if units[0].name == "pds" and not units[0].ground:  # second part rules out Titans PDS
                return units, options

            # Yin agent
            if (options["att_yin_agent_active"] and attacker) or (options["def_yin_agent_active"] and not attacker) \
                    and units[0].name in ["destroyer", "cruiser"]:
                units, options = faction_abilities.yin_agent(units, units[0], faction, options, attacker)
            else:
                del units[0]

            hits -= 1

    return units, options


def assign_fighters_only(units, hits):
    result = [u for u in units]
    for u in units:
        if hits <= 0:
            return result
        if u.fighter or u.name == "virtual":
            result.remove(u)
            hits -= 1
    return result


def assign_nonfighters_first(units, hits, risk_direct_hit, faction, options, attacker):
    # Letnev flagship (sustain)
    if faction == "Letnev":
        units, hits = faction_abilities.letnev_flagship_sustain(units, hits, risk_direct_hit)

    for u in units:
        if hits <= 0:
            return units, options
        hits -= u.use_sustain(risk_direct_hit)

    fighters = list(filter(lambda x: x.name == "fighter", units))
    non_fighters = list(filter(lambda x: x.name != "fighter", units))

    for u in non_fighters:
        if hits <= 0:
            return units, options
        if u.name == "pds" and not u.ground:  # second part rules out Titans PDS
            break
        if u.sustain:
            hits -= u.use_sustain(risk_direct_hit=True)
            # Once one ship sustains and is not Direct Hit, assume its safe
            return assign_nonfighters_first(units, hits, True, faction, options, attacker)
        else:
            # Yin agent
            if (options["att_yin_agent_active"] and attacker) or (options["def_yin_agent_active"] and not attacker) \
                    and units[0].name in ["destroyer", "cruiser"]:
                units, options = faction_abilities.yin_agent(units, u, faction, options, attacker)
            else:
                units.remove(u)

            hits -= 1

    for u in fighters:
        if hits <= 0:
            return units, options
        if u.name == "pds" and not u.ground:  # second part rules out Titans PDS
            return units, options
        units.remove(u)
        hits -= 1

    return units, options


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

    att_units, options = assign_hits(att_units, def_hits, options["att_riskdirecthit"], options["att_faction"], options,
                                     True)
    att_units, options = assign_nonfighters_first(att_units, def_nonfighter_hits, options["att_riskdirecthit"],
                                                  options["att_faction"], options, True)
    def_units, options = assign_hits(def_units, att_hits, options["def_riskdirecthit"], options["def_faction"], options,
                                     False)
    def_units, options = assign_nonfighters_first(def_units, att_nonfighter_hits, options["def_riskdirecthit"],
                                                  options["def_faction"], options, False)

    # Duranium Armor
    if options["att_duranium"]:
        tech_abilities.duranium(att_units)
    if options["def_duranium"]:
        tech_abilities.duranium(def_units)

    return att_units, def_units


def bombard_roll(val, options, jolnar_commander):
    x = random.randint(1, 10)
    if options["def_bunker"]:
        x -= 4
    if x >= val:
        return 1

    # Jol-Nar commander
    elif jolnar_commander:
        x = random.randint(1, 10)
        if options["def_bunker"]:
            x -= 4
        if x >= val:
            return 1

    return 0


def bombardment(units, options):
    jolnar_commander = options["att_jolnar_commander"]  # Bobmardment is exclusively done by the attacker
    result = 0
    best_dice = 11
    for u in units:
        if u.bombard:
            for val in u.bombard:
                best_dice = min(best_dice, val)
                result += bombard_roll(val, options, jolnar_commander)

    # Plasma Scoring
    if options["att_plasma"]:
        result += bombard_roll(best_dice, options, jolnar_commander)

    # Argent Commander
    if options["att_argent_commander"]:
        result += bombard_roll(best_dice, options, jolnar_commander)

    return result


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


def antifighter(units, swa2, options, attacker):
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


def cannon_roll(val, jolnar_commander):
    x = random.randint(1, 10)
    if x >= val:
        return 1

    # Jol-Nar commander
    elif jolnar_commander:
        x = random.randint(1, 10)
        if x >= val:
            return 1

    return 0


def space_cannon(units, options, attacker):
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


def iteration(att_units, def_units, options):
    # 0 - tie
    # 1 - attacker won
    # 2 - defender won

    # space cannon offense
    if not options["ground_combat"]:
        # Experimental Battlestation
        if options["def_experimental"]:
            def_units = [units.experimental_battlestation(options["def_faction"])] + def_units

        att_cannon_hits = space_cannon(att_units, options, attacker=True)
        def_cannon_hits = space_cannon(def_units, options, attacker=False)

        # Maneuvering Jets
        if options["def_maneuvering"]:
            att_cannon_hits = max(0, att_cannon_hits - 1)
        if options["att_maneuvering"]:
            def_cannon_hits = max(0, def_cannon_hits - 1)

        if options["def_graviton"]:
            att_units, options = assign_nonfighters_first(att_units, def_cannon_hits, options["att_riskdirecthit"],
                                                          options["att_faction"], options, True)
        else:
            att_units, options = assign_hits(att_units, def_cannon_hits, options["att_riskdirecthit"],
                                             options["att_faction"], options, True)
        if options["att_graviton"]:
            def_units, options = assign_nonfighters_first(def_units, att_cannon_hits, options["def_riskdirecthit"],
                                                          options["def_faction"], options, False)
        else:
            def_units, options = assign_hits(def_units, att_cannon_hits, options["def_riskdirecthit"],
                                             options["def_faction"], options, False)

    # Mentak Ambush
    if options["att_faction"] == "Mentak" or options["def_faction"] == "Mentak":
        att_hits, def_hits = faction_abilities.mentak_ambush(att_units, def_units, options)
        att_units, options = assign_hits(att_units, def_hits, options["att_riskdirecthit"], options["att_faction"],
                                         options, True)
        def_units, options = assign_hits(def_units, att_hits, options["def_riskdirecthit"], options["def_faction"],
                                         options, False)

    # Assault Cannon
    if not options["ground_combat"]:
        if options["att_assault"] and len(list(filter(lambda x: x.non_fighter_ship, att_units))) >= 3:
            def_units = tech_abilities.assault(def_units)
        if options["def_assault"] and len(list(filter(lambda x: x.non_fighter_ship, def_units))) >= 3:
            att_units = tech_abilities.assault(att_units)

    # anti-fighter barrage
    if not options["ground_combat"]:
        att_afb_hits, att_swa2_infantry_hits = antifighter(att_units,
                                                           options["att_faction"] == "Argent"
                                                           and options["att_destroyer2"], options, attacker=True)
        def_afb_hits, def_swa2_infantry_hits = antifighter(def_units,
                                                           options["def_faction"] == "Argent"
                                                           and options["att_destroyer2"], options, attacker=False)

        # Strike Wing Alpha II infantry hits
        if att_swa2_infantry_hits > 0:
            def_units = faction_abilities.assign_swa2(def_units, att_swa2_infantry_hits)
        if def_swa2_infantry_hits > 0:
            att_units = faction_abilities.assign_swa2(att_units, def_swa2_infantry_hits)

        # Argent Flight Raid Formation
        if options["att_faction"] == "Argent" or options["def_faction"] == "Argent":
            att_units, def_units = faction_abilities.raid_formation(att_units, def_units, att_afb_hits, def_afb_hits,
                                                                    options)

        if options["def_waylay"]:
            att_units, options = assign_hits(att_units, def_afb_hits, options["att_riskdirecthit"],
                                             options["att_faction"],
                                             options, True)
        else:
            att_units = assign_fighters_only(att_units, def_afb_hits)
        if options["att_waylay"]:
            def_units, options = assign_hits(def_units, att_afb_hits, options["def_riskdirecthit"],
                                             options["def_faction"],
                                             options, False)
        else:
            def_units = assign_fighters_only(def_units, att_afb_hits)

    # bombardment
    if options["ground_combat"]:
        bombard_hits = bombardment(att_units, options)
        if not options["att_x89"]:
            def_units, options = assign_hits(def_units, bombard_hits, options["def_riskdirecthit"],
                                             options["def_faction"],
                                             options, False)
        else:
            def_units = tech_abilities.x89(def_units, bombard_hits)
        att_units, harrow_bombarders = filters.filter_bombardment(att_units, options["att_faction"])
    else:
        harrow_bombarders = []

    # Mentak mech
    if options["ground_combat"]:
        if options["att_faction"] == "Mentak" or options["def_faction"] == "Mentak":
            att_units, def_units = faction_abilities.mentak_mech(att_units, def_units, options)

    # space cannon defense
    if options["ground_combat"]:
        cannon_hits = space_cannon(def_units, options, attacker=False)

        # Maneuvering Jets
        if options["att_maneuvering"]:
            cannon_hits = max(0, cannon_hits - 1)

        att_units, options = assign_hits(att_units, cannon_hits, options["att_riskdirecthit"], options["att_faction"],
                                         options, False)

    # Magen Defense Grid Omega
    if options["def_magen_o"] and options["ground_combat"]:
        att_units = tech_abilities.magen_omega(att_units)

    first_round = True
    while att_units and def_units:
        att_units, def_units = combat_round(att_units, def_units, first_round, options)
        first_round = False
        if options["att_faction"] == "L1Z1X":
            def_units, options = harrow(def_units, harrow_bombarders, options)

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
        att_units = tech_abilities.noneuclidean(def_units)

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
        res = iteration(copy.deepcopy(att_units), copy.deepcopy(def_units), copy.deepcopy(options))

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

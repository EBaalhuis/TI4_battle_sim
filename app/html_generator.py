def att_side(name, description, enabled, on, checked):
    deleter_open = "" if enabled else "<del>"
    deleter_close = "" if enabled else "</del>"
    disabler = '' if enabled else 'disabled="disabled"'

    checkbox = ('<input id="att_' + name + '" name="att_' + name + '" type="checkbox"' + disabler + checked + '>') \
        if on else ""

    result = ('<div class="col-sm-5" align="right">' + deleter_open + description + deleter_close + ' '
              + checkbox + '</div>')

    return result


def def_side(name, description, enabled, on, checked):
    deleter_open = "" if enabled else "<del>"
    deleter_close = "" if enabled else "</del>"
    disabler = '' if enabled else 'disabled="disabled"'

    checkbox = ('<input id="def_' + name + '" name="def_' + name + '" type="checkbox"' + disabler + checked + '> ') \
        if on else ""

    result = ('<div class="col-sm-5">' + checkbox + deleter_open + description + deleter_close + ''
              '</div>')

    return result


def line(checkboxes, hidden, name, description, def_name="", def_description="", tooltip="(tooltip not yet written)",
         def_tooltip="(tooltip not yet written)", enabled=True, both=True):
    att_on = both or len(name) > 0
    def_on = both or len(def_name) > 0
    if both:
        hidden_id = name
    elif att_on:
        hidden_id = "att_" + name
    else:
        hidden_id = "def_" + def_name
    div_id = hidden_id + "_row"
    hide = "none" if hidden[hidden_id] else "block"

    if def_name == "" and both:
        # default setting: same option for defender and attacker
        def_name = name
        def_description = description
    att_checked = checkboxes["att_" + name]
    def_checked = checkboxes["def_" + def_name]

    attacker_side = att_side(name, description, enabled, att_on, att_checked)
    defender_side = def_side(def_name, def_description, enabled, def_on, def_checked)
    if both and name != def_name:
        questionmark = '<img src="/static/question.png" alt="questionmark" data-toggle="tooltip" ' \
                       'data-boundary="viewport" title="' + tooltip + '" width=19/> ' + \
                       '<img src="/static/question.png" alt="questionmark" data-toggle="tooltip" ' \
                       'data-boundary="viewport" title="' + def_tooltip + '" width=19/>'

    else:
        questionmark = '<img src="/static/question.png" alt="questionmark" data-toggle="tooltip" ' \
                       'data-boundary="viewport" title="' + tooltip + '" width=19/>'


    result = '<div class="o-grid o-grid--no-gutter center-grid row" id="' + div_id + '" style="display: ' \
             '' + hide + ';">' + attacker_side + '<div class="col-sm-2" align="center">' + questionmark + '</div>' \
             + defender_side + '</div>'
    return result


def centered_line(checkboxes, hidden, name, description, tooltip="(tooltip not yet written)", enabled=True):
    div_id = name
    deleter_open = "" if enabled else "<del>"
    deleter_close = "" if enabled else "</del>"
    disabler = '' if enabled else 'disabled="disabled"'
    checked = checkboxes[name]
    questionmark = '<img src="/static/question.png" alt="questionmark" data-toggle="tooltip" data-boundary="viewport"' \
                   'title="' + tooltip + \
                   '" width=19/>'

    result = ('<div class="o-grid o-grid--no-gutter center-grid row" id="' + div_id + '">'
              '<div class="col-sm-12" align="center">'
              '<input id="' + name + '" name="' + name + '" type="checkbox"' + disabler + checked + '> ' 
              '' + deleter_open + description + deleter_close + ' ' + questionmark + '</div></div>')
    return result


def make_boxes(checkboxes, hidden):
    boxes = {"general": [line(checkboxes, hidden, "riskdirecthit", "Risk Direct Hit",
                              tooltip="Damage units vulnerable to Direct Hit before killing more expendable units"),
                         line(checkboxes, hidden, "", "", def_name="nebula", def_description="Defending in Nebula",
                              both=False, tooltip="+1 to combat rolls for ships defending in a nebula")],

             "hidden": [line(checkboxes, hidden, "mahact_flagship_hide", "Mahact Flagship Bonus", both=False,
                             tooltip="+2 to Flagship combat rolls against opponent whose command token is not in your "
                                     "fleet pool"),
                        line(checkboxes, hidden, "", "", "mahact_flagship_hide", "Mahact Flagship Bonus", both=False,
                             tooltip="+2 to Flagship combat rolls against opponent whose command token is not in your "
                                     "fleet pool"),
                        line(checkboxes, hidden, "naalu_mech_hide", "Naalu Mech Bonus", both=False,
                             tooltip="+2 to Mech combat rolls against opponent who has at least 1 relic fragment"),
                        line(checkboxes, hidden, "", "", "naalu_mech_hide", "Naalu Mech Bonus", both=False,
                             tooltip="+2 to Mech combat rolls against opponent who has at least 1 relic fragment"),
                        line(checkboxes, hidden, "nekro_mech_hide", "Nekro Mech Bonus", both=False,
                             tooltip="+2 to Mech combat rolls against opponent who has an X or Y token on 1 or more of "
                                     "their techs"),
                        line(checkboxes, hidden, "", "", "nekro_mech_hide", "Nekro Mech Bonus", both=False,
                             tooltip="+2 to Mech combat rolls against opponent who has an X or Y token on 1 or more of "
                                     "their techs"),
                        line(checkboxes, hidden, "mentak_hero_hide", "Mentak Hero", both=False, enabled=False),
                        line(checkboxes, hidden, "", "", "mentak_hero_hide", "Mentak Hero", both=False,
                             enabled=False),
                        line(checkboxes, hidden, "creuss_dimensionalsplicer_nekro_hide", "Dimensional Splicer", both=False,
                             enabled=False),
                        line(checkboxes, hidden, "", "", "creuss_dimensionalsplicer_nekro_hide", "Dimensional Splicer", both=False,
                             enabled=False),
                        line(checkboxes, hidden, "letnev_l4_nekro_hide", "L4 Disruptors", both=False),
                        line(checkboxes, hidden,
                                    "letnev_noneuclid_nekro_hide", "Non-Euclidean Shielding", both=False),
                        line(checkboxes, hidden,
                                    "", "", "letnev_noneuclid_nekro_hide", "Non-Euclidean Shielding", both=False),
                        line(checkboxes, hidden, "naazrokha_supercharge_nekro_hide", "Supercharge", both=False),
                        line(checkboxes, hidden,
                                    "", "", "naazrokha_supercharge_nekro_hide", "Supercharge", both=False),
                        line(checkboxes, hidden,
                                    "sardakk_valkyrie_nekro_hide", "Valkyrie Particle Weave", both=False),
                        line(checkboxes, hidden,
                                    "", "", "sardakk_valkyrie_nekro_hide", "Valkyrie Particle Weave", both=False),
                        ],

             "tech": [line(checkboxes, hidden, "antimass", "Antimass Deflectors",
                           tooltip="-1 to opponents' Space Cannon rolls"),
                      line(checkboxes, hidden, "graviton", "Graviton Laser System",
                           tooltip="Hits produced by Space Cannon must be assigned to non-fighter ships if able"),
                      line(checkboxes, hidden, "plasma", "Plasma Scoring",
                           tooltip="1 additional die on Bombardment and Space Cannon"),
                      line(checkboxes, hidden, "", "", def_name="magen", def_description="Magen Defense Grid",
                           both=False, tooltip="Opponent cannot make combat rolls first round of ground combat"),
                      line(checkboxes, hidden, "x89", "X-89 Bacterial Weapon Ω", def_name="magen_o",
                           def_description="Magen Defense Grid Ω"),
                      line(checkboxes, hidden, "duranium", "Duranium Armor",
                           tooltip="During each combat round, after you assign hits, repair 1 of your damaged units "
                                   "that did not use Sustain Damage this round"),
                      line(checkboxes, hidden, "assault", "Assault Cannon",
                           tooltip="At the start of space combat in a system that contains 3 or more of your "
                                   "non-fighter ships, your opponent must destroy 1 of their non-fighter ships")],

             "cards": [line(checkboxes, hidden, "", "", def_name="bunker", def_description="Bunker", both=False,
                            tooltip="-4 to Bobmardment"),
                       line(checkboxes, hidden, "", "", def_name="experimental",
                            def_description="Experimental Battlestation", both=False,
                            tooltip="1 space dock in or adjacent to active system uses Space Cannon 5 (x3)"),
                       line(checkboxes, hidden, "prototype", "Fighter Prototype",
                            tooltip="+2 to Fighter combat rolls first round"),
                       line(checkboxes, hidden, "fireteam", "Fire Team",
                            tooltip="Re-roll any number of your dice first round"),
                       line(checkboxes, hidden, "maneuvering", "Maneuvering Jets",
                            tooltip="Cancel 1 hit from Space Cannon"),
                       line(checkboxes, hidden, "morale", "Morale Boost 1st round",
                            tooltip="+1 to combat rolls first round"),
                       line(checkboxes, hidden, "waylay", "Waylay",
                            tooltip="Hits from AFB are produced against all ships, not just fighters")],

             "agendas": [centered_line(checkboxes, hidden, "conventions", "Conventions of War",
                                       tooltip="Players cannot use Bombardment against units that are on cultural "
                                               "planets"),
                         centered_line(checkboxes, hidden, "publicize", "Publicize Weapon Schematics",
                                       tooltip="All War Suns lose Sustain Damage")],

             "notes": [line(checkboxes, hidden, "argent_prom", "Strike Wing Ambuscade",
                            tooltip="1 unit rolls 1 additional die for a unit ability (AFB/Bombardment/Space Cannon"),
                       line(checkboxes, hidden, "tekklar", "Tekklar Legion",
                            tooltip="+1 to combat rolls during invasion combat. If your opponent is Sardakk, they "
                                    "get -1 to combat rolls this combat"),
                       line(checkboxes, hidden, "warfunding", "War Funding",
                            tooltip="Re-roll any number of your dice first round"),
                       line(checkboxes, hidden, "warfunding_omega", "War Funding Ω",
                            tooltip="After you and your opponent roll dice during space combat: you may re-roll all of"
                                    "your opponent's dice. You may reroll any number of your dice"),
                       line(checkboxes, hidden, "cavalry1", "The Cavalry (Memoria I)",
                            tooltip="During this combat, treat 1 of your non-fighter ships as if it has the "
                                    "Sustain Damage, combat value, and AFB of the Nomad's Flagship (not upgraded)"),
                       line(checkboxes, hidden, "cavalry2", "The Cavalry (Memoria II)",
                            tooltip="During this combat, treat 1 of your non-fighter ships as if it has the "
                                    "Sustain Damage, combat value, and AFB of the Nomad's Flagship (upgraded)"
                            )
                       ],

             "agents": [line(checkboxes, hidden, "letnev_agent", "Letnev Agent",
                             tooltip="1 ship rolls 1 additional die first round"),
                        # option_line(checkboxes, hidden, "nomad_agent", "Nomad Agent (Thundarian)", enabled=False),
                        line(checkboxes, hidden, "sol_agent", "Sol Agent",
                             tooltip="1 ground force rolls 1 additional die first round"),
                        line(checkboxes, hidden, "titans_agent", "Titans Agent",
                             tooltip="Cancel 1 hit (programmed to cancel the first possible hit)"),
                        line(checkboxes, hidden, "yin_agent", "Yin Agent",
                             tooltip="After your Destroyer or Cruiser is destroyed, place 2 Fighters")],

             "commanders": [line(checkboxes, hidden, "argent_commander", "Argent Commander",
                                 tooltip="For every unit ability (AFB/Bombardment/Space Cannon), 1 unit rolls"
                                         "1 additional die"),
                            line(checkboxes, hidden, "jolnar_commander", "Jol-Nar Commander",
                                 tooltip="After you roll dice for a unit ability: you may re-roll any of those dice"),
                            line(checkboxes, hidden, "letnev_commander", "Letnev Commander", enabled=False),
                            line(checkboxes, hidden, "winnu_commander", "Winnu Commander",
                                 tooltip="+2 to combat rolls in the Mecatol Rex system, your home system, and each "
                                         "system that contains a legendary planet"),
                            line(checkboxes, hidden, "att_l1z1x_commander", "L1Z1X Commander",
                                 "sol_commander", "Sol Commander")]
             }

    return boxes

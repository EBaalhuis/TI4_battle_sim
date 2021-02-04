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


def option_line(checkboxes, hidden, name, description, def_name="", def_description="", enabled=True, both=True):
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

    result = '<div class="o-grid o-grid--no-gutter center-grid row" id="' + div_id + '" style="display: ' + hide + ';">' + attacker_side + \
             '<div class="col-sm-2" align="center"></div>' + defender_side + \
             '</div>'
    return result


def centered_line(checkboxes, hidden, name, description, enabled=True):
    div_id = name
    deleter_open = "" if enabled else "<del>"
    deleter_close = "" if enabled else "</del>"
    disabler = '' if enabled else 'disabled="disabled"'
    checked = checkboxes[name]

    result = ('<div class="o-grid o-grid--no-gutter center-grid row" id="' + div_id + '">'
              '<div class="col-sm-12" align="center">'
              '<input id="' + name + '" name="' + name + '" type="checkbox"' + disabler + checked + '> ' 
              '' + deleter_open + description + deleter_close + '</div></div>')
    return result


def make_boxes(checkboxes, hidden):
    boxes = {"general": [option_line(checkboxes, hidden, "riskdirecthit", "Risk Direct Hit"),
                         option_line(checkboxes, hidden, "", "", def_name="nebula", def_description="Defending in Nebula", both=False)],

             "hidden": [option_line(checkboxes, hidden,
                                    "mahact_flagship_hide", "Mahact Flagship Bonus", both=False),
                        option_line(checkboxes, hidden,
                                    "", "", "mahact_flagship_hide", "Mahact Flagship Bonus", both=False),
                        option_line(checkboxes, hidden, "naalu_mech_hide", "Naalu Mech Bonus", both=False),
                        option_line(checkboxes, hidden, "", "", "naalu_mech_hide", "Naalu Mech Bonus", both=False),
                        option_line(checkboxes, hidden, "nekro_mech_hide", "Nekro Mech Bonus", both=False),
                        option_line(checkboxes, hidden, "", "", "nekro_mech_hide", "Nekro Mech Bonus", both=False),
                        option_line(checkboxes, hidden, "mentak_hero_hide", "Mentak Hero", both=False, enabled=False),
                        option_line(checkboxes, hidden, "", "", "mentak_hero_hide", "Mentak Hero", both=False,
                                    enabled=False),
                        option_line(checkboxes, hidden, "creuss_dimensionalsplicer_nekro_hide", "Dimensional Splicer", both=False,
                                    enabled=False),
                        option_line(checkboxes, hidden, "", "", "creuss_dimensionalsplicer_nekro_hide", "Dimensional Splicer", both=False,
                                    enabled=False),
                        option_line(checkboxes, hidden, "letnev_l4_nekro_hide", "L4 Disruptors", both=False),
                        option_line(checkboxes, hidden, "letnev_noneuclid_nekro_hide", "Non-Euclidean Shielding", both=False,
                                    enabled=False),
                        option_line(checkboxes, hidden, "", "", "letnev_noneuclid_nekro_hide", "Non-Euclidean Shielding", both=False,
                                    enabled=False),
                        option_line(checkboxes, hidden, "naazrokha_supercharge_nekro_hide", "Supercharge", both=False),
                        option_line(checkboxes, hidden,
                                    "", "", "naazrokha_supercharge_nekro_hide", "Supercharge", both=False),
                        option_line(checkboxes, hidden, "sardakk_valkyrie_nekro_hide", "Valkyrie Particle Weave", both=False,
                                    enabled=False),
                        option_line(checkboxes, hidden, "", "", "sardakk_valkyrie_nekro_hide", "Valkyrie Particle Weave", both=False,
                                    enabled=False),
                        ],

             "tech": [option_line(checkboxes, hidden, "antimass", "Antimass Deflectors"),
                      option_line(checkboxes, hidden, "graviton", "Graviton Laser System"),
                      option_line(checkboxes, hidden, "plasma", "Plasma Scoring"),
                      option_line(checkboxes, hidden, "", "", def_name="magen", def_description="Magen Defense Grid", both=False),
                      option_line(checkboxes, hidden, "x89", "X-89 Bacterial Weapon Ω", def_name="magen_o",
                                  def_description="Magen Defense Grid Ω"),
                      option_line(checkboxes, hidden, "duranium", "Duranium Armor"),
                      option_line(checkboxes, hidden, "assault", "Assault Cannon")],

             "cards": [option_line(checkboxes, hidden, "", "", def_name="bunker", def_description="Bunker", both=False),
                       option_line(checkboxes, hidden, "", "", def_name="experimental", def_description="Experimental Battlestation",
                                   both=False),
                       option_line(checkboxes, hidden, "prototype", "Fighter Prototype"),
                       option_line(checkboxes, hidden, "fireteam", "Fire Team"),
                       option_line(checkboxes, hidden, "maneuvering", "Maneuvering Jets"),
                       option_line(checkboxes, hidden, "morale", "Morale Boost 1st round"),
                       option_line(checkboxes, hidden, "waylay", "Waylay")],

             "agendas": [centered_line(checkboxes, hidden, "conventions", "Conventions of War"),
                         centered_line(checkboxes, hidden, "publicize", "Publicize Weapon Schematics")],

             "notes": [option_line(checkboxes, hidden, "argent_prom", "Strike Wing Ambuscade"),
                       option_line(checkboxes, hidden, "tekklar", "Tekklar Legion"),
                       option_line(checkboxes, hidden, "warfunding", "War Funding"),
                       option_line(checkboxes, hidden, "warfunding_omega", "War Funding Ω"),
                       option_line(checkboxes, hidden, "cavalry1", "The Cavalry (Memoria I)"),
                       option_line(checkboxes, hidden, "cavalry2", "The Cavalry (Memoria II)")],

             "agents": [option_line(checkboxes, hidden, "letnev_agent", "Letnev Agent"),
                        # option_line(checkboxes, hidden, "nomad_agent", "Nomad Agent (Thundarian)", enabled=False),
                        option_line(checkboxes, hidden, "sol_agent", "Sol Agent"),
                        option_line(checkboxes, hidden, "titans_agent", "Titans Agent"),
                        option_line(checkboxes, hidden, "yin_agent", "Yin Agent")],

             "commanders": [option_line(checkboxes, hidden, "argent_commander", "Argent Commander"),
                            option_line(checkboxes, hidden, "jolnar_commander", "Jol-Nar Commander"),
                            option_line(checkboxes, hidden, "letnev_commander", "Letnev Commander", enabled=False),
                            option_line(checkboxes, hidden, "winnu_commander", "Winnu Commander"),
                            option_line(checkboxes, hidden, "att_l1z1x_commander", "L1Z1X Commander", "sol_commander", "Sol Commander")]
             }

    return boxes

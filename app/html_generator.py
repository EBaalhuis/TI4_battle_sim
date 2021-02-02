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


def option_line(checkboxes, name, description, def_name="", def_description="", enabled=True, both=True):
    att_on = both or len(name) > 0
    def_on = both or len(def_name) > 0
    att_checked = checkboxes["att_" + name]
    def_checked = checkboxes["def_" + name]

    if def_name == "" and both:
        # default setting: same option for defender and attacker
        def_name = name
        def_description = description

    attacker_side = att_side(name, description, enabled, att_on, att_checked)
    defender_side = def_side(def_name, def_description, enabled, def_on, def_checked)

    result = '<div class="o-grid o-grid--no-gutter center-grid row">' + attacker_side + \
             '<div class="col-sm-2" align="center"></div>' + defender_side + \
             '</div>'
    return result


def centered_line(checkboxes, name, description, enabled=True):
    deleter_open = "" if enabled else "<del>"
    deleter_close = "" if enabled else "</del>"
    disabler = '' if enabled else 'disabled="disabled"'
    checked = checkboxes[name]

    result = ('<div class="o-grid o-grid--no-gutter center-grid row">'
              '<div class="col-sm-12" align="center">'
              '<input id="' + name + '" name="' + name + '" type="checkbox"' + disabler + checked + '> ' 
              '' + deleter_open + description + deleter_close + '</div></div>')
    return result


def make_boxes(checkboxes):
    boxes = {"general": [option_line(checkboxes, "riskdirecthit", "Risk Direct Hit"),
                         option_line(checkboxes, "", "", def_name="nebula", def_description="Defending in Nebula", both=False)],

             "tech": [option_line(checkboxes, "antimass", "Antimass Deflectors"),
                      option_line(checkboxes, "graviton", "Graviton Laser System"),
                      option_line(checkboxes, "plasma", "Plasma Scoring"),
                      option_line(checkboxes, "", "", def_name="magen", def_description="Magen Defense Grid", both=False),
                      option_line(checkboxes, "x89", "X-89 Bacterial Weapon Ω", def_name="magen_o",
                                  def_description="Magen Defense Grid Ω"),
                      option_line(checkboxes, "duranium", "Duranium Armor"),
                      option_line(checkboxes, "assault", "Assault Cannon")],

             "cards": [option_line(checkboxes, "", "", def_name="bunker", def_description="Bunker", both=False),
                       option_line(checkboxes, "", "", def_name="experimental", def_description="Experimental Battlestation",
                                   both=False),
                       option_line(checkboxes, "prototype", "Fighter Prototype"),
                       option_line(checkboxes, "fireteam", "Fire Team"),
                       option_line(checkboxes, "maneuvering", "Maneuvering Jets"),
                       option_line(checkboxes, "morale", "Morale Boost 1st round"),
                       option_line(checkboxes, "waylay", "Waylay")],

             "agendas": [centered_line(checkboxes, "conventions", "Conventions of War"),
                         centered_line(checkboxes, "publicize", "Publicize Weapon Schematics")],

             "notes": [option_line(checkboxes, "argent_prom", "Strike Wing Ambuscade"),
                       option_line(checkboxes, "tekklar", "Tekklar Legion"),
                       option_line(checkboxes, "warfunding", "War Funding"),
                       option_line(checkboxes, "warfunding_omega", "War Funding Ω"),
                       option_line(checkboxes, "cavalry1", "The Cavalry (Memoria I)"),
                       option_line(checkboxes, "cavalry2", "The Cavalry (Memoria II)")],

             "agents": [option_line(checkboxes, "letnev_agent", "Letnev Agent"),
                        # option_line(checkboxes, "nomad_agent", "Nomad Agent (Thundarian)", enabled=False),
                        option_line(checkboxes, "sol_agent", "Sol Agent"),
                        option_line(checkboxes, "titans_agent", "Titans Agent"),
                        option_line(checkboxes, "yin_agent", "Yin Agent", enabled=False)],

             "commanders": [option_line(checkboxes, "argent_commander", "Argent Commander", enabled=False),
                            option_line(checkboxes, "jolnar_commander", "Jol-Nar Commander", enabled=False),
                            option_line(checkboxes, "letnev_commander", "Letnev Commander", enabled=False),
                            option_line(checkboxes, "winnu_commander", "Winnu Commander"),
                            option_line(checkboxes, "att_l1z1x_commander", "L1Z1X Commander", "sol_commander", "Sol Commander")]
             }

    return boxes

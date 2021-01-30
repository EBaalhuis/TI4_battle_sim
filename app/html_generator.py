def att_side(name, description, enabled, on):
    deleter_open = "" if enabled else "<del>"
    deleter_close = "" if enabled else "</del>"
    disabler = '' if enabled else 'disabled="disabled"'

    checkbox = ('<input id="att_' + name + '" name="att_' + name + '" type="checkbox"' + disabler + ''
                '{{ checkboxes["att_' + name + '"] }}>') if on else ""

    result = ('<div class="col-sm-5" align="right">' + deleter_open + description + deleter_close + ' '
              + checkbox + '</div>')

    return result


def def_side(name, description, enabled, on):
    deleter_open = "" if enabled else "<del>"
    deleter_close = "" if enabled else "</del>"
    disabler = '' if enabled else 'disabled="disabled"'

    checkbox = ('<input id="att_' + name + '" name="def_' + name + '" type="checkbox"' + disabler + ''
                '{{ checkboxes["def_' + name + '"] }}> ') if on else ""

    result = ('<div class="col-sm-5">' + checkbox + deleter_open + description + deleter_close + ''
              '</div>')

    return result


def option_line(name, description, enabled=True, def_name="", def_description="", both=True):
    att_on = both or len(name) > 0
    def_on = both or len(def_name) > 0

    if def_name == "" and both:
        # default setting: same option for defender and attacker
        def_name = name
        def_description = description

    result = '<div class="o-grid o-grid--no-gutter center-grid row">' + att_side(name, description, enabled, att_on) + \
             '<div class="col-sm-2" align="center"></div>' + def_side(def_name, def_description, enabled, def_on) + \
             '</div>'
    return result


def centered_line(name, description, enabled=True):
    deleter_open = "" if enabled else "<del>"
    deleter_close = "" if enabled else "</del>"
    disabler = '' if enabled else 'disabled="disabled"'

    result = ('<div class="o-grid o-grid--no-gutter center-grid row">'
              '<div class="col-sm-12" align="center">'
              '<input id="' + name + '" name="' + name + '" type="checkbox"' + disabler + ''
              '{{ checkboxes["' + name + '"] }}> ' + deleter_open + description + deleter_close + ''
              '</div></div>')
    return result


def make_boxes():
    boxes = {"general": [option_line("riskdirecthit", "Risk Direct Hit"),
                         option_line("", "", def_name="nebula", def_description="Defending in Nebula", both=False)],

             "tech": [option_line("antimass", "Antimass Deflectors"),
                      option_line("graviton", "Graviton Laser System"),
                      option_line("plasma", "Plasma Scoring"),
                      option_line("", "", def_name="magen", def_description="Magen Defense Grid", both=False),
                      option_line("x89", "X-89 Bacterial Weapon Ω", def_name="magen_o",
                                  def_description="Magen Defense Grid Ω"),
                      option_line("duranium", "Duranium Armor"),
                      option_line("assault", "Assault Cannon"),],

             "cards": [option_line("", "", def_name="bunker", def_description="Bunker", both=False),
                       option_line("", "", def_name="experimental", def_description="Experimental Battlestation",
                                   both=False),
                       option_line("prototype", "Fighter Prototype"),
                       option_line("fireteam", "Fire Team"),
                       option_line("maneuvering", "Maneuvering Jets"),
                       option_line("morale", "Morale Boost 1st round"),
                       option_line("waylay", "Waylay"),],

             "agendas": [centered_line("conventions", "Conventions of War"),
                         centered_line("publicize", "Publicize Weapon Schematics")],

             "notes": [option_line("argent_prom", "Strike Wing Ambuscade"),
                       option_line("tekklar", "Tekklar Legion"),
                       option_line("warfunding", "War Funding"),
                       option_line("warfunding_omega", "War Funding Ω", enabled=False),
                       option_line("cavalry1", "The Cavalry (Memoria I)", enabled=False),
                       option_line("cavalry2", "The Cavalry (Memoria II)", enabled=False)],

             "agents": [option_line("letnev_agent", "Letnev Agent", enabled=False),
                        option_line("nomad_agent", "Nomad Agent (Thundarian)", enabled=False),
                        option_line("sol_agent", "Sol Agent", enabled=False),
                        option_line("titans_agent", "Titans Agent", enabled=False),
                        option_line("yin_agent", "Yin Agent", enabled=False)],

             "commanders": [option_line("argent_commander", "Argent Commander", enabled=False),
                            option_line("jolnar_commander", "Jol-Nar Commander", enabled=False),
                            option_line("l1z1x_commander", "L1Z1X Commander", enabled=False),
                            option_line("letnev_commander", "Letnev Commander", enabled=False),
                            option_line("sol_commander", "Sol Commander", enabled=False),
                            option_line("winnu_commander", "Winnu Commander", enabled=False)]
             }

    return boxes

def option_line_enabled(name, description):
    result = ('<div class="o-grid o-grid--no-gutter center-grid row">'
              '<div class="col-sm-5" align="right">' + description + ' '
              '<input id="att_' + name + '" name="att_' + name + '" type="checkbox"'
              '{{ checkboxes["att_' + name + '"] }}>'
              '</div>'
              '<div class="col-sm-2" align="center"></div>'
              '<div class="col-sm-5">'
              '<input id="def_' + name + '" name="def_' + name + '" type="checkbox"'
              '{{ checkboxes["def_' + name + '"]}}> ' + description + ''
              '</div>'
              '</div>')

    return result


def option_line_disabled(name, description):
    result = ('<div class="o-grid o-grid--no-gutter center-grid row">'
              '<div class="col-sm-5" align="right"><del>' + description + ' </del>'
              '<input id="att_' + name + '" name="att_' + name + '" type="checkbox" disabled="disabled"'
              '{{ checkboxes["att_' + name + '"] }}>'
              '</div>'
              '<div class="col-sm-2" align="center"></div>'
              '<div class="col-sm-5">'
              '<input id="def_' + name + '" name="def_' + name + '" type="checkbox" disabled="disabled"'
              '{{ checkboxes["def_' + name + '"]}}><del> ' + description + '</del>'
              '</div>'
              '</div>')

    return result


def option_line(name, description, enabled=True):
    if enabled:
        return option_line_enabled(name, description)
    else:
        return option_line_disabled(name, description)

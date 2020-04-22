def get_log_linear_buttons():
    log_linear = {
        "type": "buttons",
        'direction': 'right',
        'showactive': True,
        'x': 0.11,
        'xanchor': "left",
        'y': 1.1,
        'yanchor': "top",
        "buttons": [
            {"label": "linear", "method": "relayout", "args": ["yaxis", {"type": "linear"}]},
            {"label": "log", "method": "relayout", "args": ["yaxis", {"type": "log"}]},
        ]}

    return log_linear


# d = {'type': 'dropdown',
#      'direction': 'down',
#      'buttons': [
#          {'label': "deaths",
#           'method': "update",
#           'args': [{"visible": amount_countries * [True] + amount_countries * [False]}]},
#          {'label': "death_factor_increase",
#           'method': "update",
#           'args': [{"visible": amount_countries * [False] + amount_countries * [True]}]},
#      ]
#      }
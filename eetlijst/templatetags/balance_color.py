from django.template.defaulttags import register

@register.filter
def bal_color(balance):

    pos = [110, 185, 110]
    neg = [185, 110, 110]

    if balance >= 0:
        if balance > 30:
            rgba_color = str(pos[0]) + ', ' + str(pos[1]) + ', ' + str(pos[2]) + ', 1'
        else:
            rgba_color = str(round(255 - balance*(255-pos[0])/30,0)) + ', ' + str(round(255 - balance*(255-pos[1])/30,0)) + ', ' + str(round(255 - balance*(255-pos[2])/30,0)) + ', 1'

    else:
        if balance < -30:
            rgba_color = str(neg[0]) + ', ' + str(neg[1]) + ', ' + str(neg[2]) + ', 1'
        else:
            rgba_color = str(round(255 + balance*(255-neg[0])/30,0)) + ', ' + str(round(255 + balance*(255-neg[1])/30,0)) + ', ' + str(round(255 + balance*(255-neg[2])/30,0)) + ', 1'

    return rgba_color
from .models import *

import random
def check_profile(request):
    num1 = random.randint(0, 9)
    num2 = random.randint(0, 9)
    promo_percent = 0
    promo_rub = 0
    if request.user.is_authenticated:
        print('user')
        if request.user.promo_code:
            promo_percent = request.user.promo_code.discount
            promo_rub = request.user.promo_code.summ
    else:
        if not request.session.session_key:
            request.session.save()
        s_key = request.session.session_key
        print('s_key',s_key)
        try:
            guest = Guest.objects.get(session=s_key)
            print('guest found')
        except:
            guest = Guest.objects.create(session=s_key)
            print('guest created')
        if guest.promo_code:
            promo_percent = guest.promo_code.discount
            promo_rub = guest.promo_code.summ
    return locals()


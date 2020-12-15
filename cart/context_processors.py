import json
from .views import get_all_items
from .models import Cart, Guest

def format_number(num):
    if num % 1 == 0:
        return int(num)
    else:
        return num




def items_in_cart(request):
    if request.user.is_authenticated:
        all_items_in_cart = Cart.objects.filter(client_id=request.user.id)
        cart_items_ids = []
        for x in all_items_in_cart:
            cart_items_ids.append(x.item.id)
        print('Cart items for auth user')
        count_items_in_cart = all_items_in_cart.count()
        total_cart_price = 0
        for item in all_items_in_cart:
            total_cart_price += item.total_price

        total_cart_price_with_discount = total_cart_price

    else:
        s_key = request.session.session_key
        try:
            guest = Guest.objects.get(session=s_key)
            used_promo = guest.used_promo
            if not used_promo:
                promo_discount_value = 0

        except:
            guest = None
            used_promo = None
        if guest:
            all_items_in_cart = Cart.objects.filter(guest=guest)
            cart_items_ids = []
            for x in all_items_in_cart:
                cart_items_ids.append(x.item.id)
            print('Cart items for NOT auth user')
            count_items_in_cart = all_items_in_cart.count()
            total_cart_price = 0
            for item in all_items_in_cart:
                total_cart_price += item.total_price
            total_cart_price_with_discount = total_cart_price

    return locals()

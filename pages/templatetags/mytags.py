from django import template
from shop.models import *

register = template.Library()


@register.filter()
def get_num(store_id, item_id):
    try:
        at_store = ItemAtStore.objects.get(store_id=store_id,item_type_id=item_id)
        return at_store.item_number
    except:
        return 0



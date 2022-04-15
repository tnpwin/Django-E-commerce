from store.models import *
from .views import _card_id

def menu_items(request):
    links = Category.objects.all()
    return {'links':links}

def counter_items(request):
    count_items = 0
    # ถ้า admin เป็นคนซื้อของ ระบบจะไม่อนุญาตให้ซื้อ
    if 'admin' in request.path:
        return{}
    else:
        try:
            # query Card 
            card = Card.objects.get(card_id = _card_id(request))
            # query carditem
            card_item = CardItem.objects.all().filter(card = card)
            # ดึง id ของตระกร้าสินค้ามา พร้อมกับสินค้าที่อยู่ในตระกร้าของ id นั้น
            # loop ดูว่า สินค้ามีกี่ตัวกันนะ
            for item in card_item:
                count_items += item.quantity   
        except Card.DoesNotExist:
            count_items = 0      
            
    return {'count_items': count_items}
        
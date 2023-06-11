from Product.models import Users
from Cart.models import Cart
from django.utils import timezone

def check_anonymous_cart_products(request):
    anon_user = None
    if Users.objects.filter(username = "Anonymous User").exists():
        #If there is an Anonymous user, assign it
        anon_user = Users.objects.get(username = "Anonymous User")

    if Cart.objects.filter(user = anon_user).exists():
        #If there is a cart item(s) that belonged to anonymous user, delete that and
        #create a new cart item with the logged in user
        for item in Cart.objects.filter(user = anon_user):
            product = item.product
            Cart.objects.create(product= product,user= request.user,quantity = item.quantity)
        Users.objects.filter(username = "Anonymous User").delete() 

def get_products_from_cart_object(cart_items):
    products = {}
    count = Cart.objects.count()
    if count == 0:
        return products
    else:
        for item in cart_items:
            product = item.product
            products[product] = item.quantity
        return products
    
def checkDiscountChange(product):
    if product.discount != 0:
        dis = (product.price- ((product.price* product.discount)/100))
        if product.newPrice != dis:
            #discount changed
            return True
        else:
            #discount same
            return False
    else:
        return False


def price_quantity(cart_items):
    d = {}
    for item in cart_items:
        product = item.product
        if product.discount != 0:
            d[product] = product.newPrice * item.quantity
        else:
            price = item.quantity * product.price
            d[product] = price 
    return d
    
def total_price(cart_items):
    total = 0
    for item in cart_items:
        product = item.product
        if product.discount != 0:

            total += product.newPrice * item.quantity
        else:
            price = item.quantity * product.price
            total += price
    return total

def newPrice_calc(products):
    for product in products:
        if product.discount !=0:
            product.newPrice = (product.price- ((product.price* product.discount)/100))
            product.save()
        else: 
            product.nemPrice=0
            product.save()

def DaysRemain(products):
    dic = {}
    for product in products:
        today_date = timezone.now()
        product_date = product.date_added
        difference = today_date - product_date
        dic[product] = difference.days
    return dic

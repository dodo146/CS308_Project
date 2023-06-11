from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from Cart.models import PurchaseHistory,Refund
from Product.models import InStockProduct, OrderedProduct,Category,Users,PurchasedProduct
from .models import Account
from .forms import LoginForm,SignupForm
from .helper_functions import check_anonymous_cart_products,newPrice_calc,DaysRemain,checkDiscountChange
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    p = InStockProduct.objects.all()
    newPrice_calc(p)
    changed_discount_message = ""
    for product in p:
        if checkDiscountChange(product):
            #discount changed notify the user
            if changed_discount_message == "":
                changed_discount_message += "Discount changed for {}".format(product.name)
            else:
                changed_discount_message += ",{}".format(product.name)
    if changed_discount_message != "":
        #there is a success message
        changed_discount_message += "Check it out!"
        messages.success(changed_discount_message)

    if request.user.is_authenticated:
        check_anonymous_cart_products(request)
    if request.method == "POST":
        query = request.POST.get("search_field")
        command = request.POST.get("command")
        categories = Category.objects.all()
        #sad
        if command == "search":
            try:
                searched_products = InStockProduct.objects.filter(
                    Q(name__icontains=query) | Q(description__icontains=query))
                category_id = searched_products.first().category_id
                items = InStockProduct.objects.all()
            except:
                searched_products = None

            try:
                if category_id:
                    items = items.filter(category_id=category_id)
            except:
                items = None

            if query:
                try:
                    items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
                except:
                    items = None
            return render(request, 'index.html', {
                "instockproducts": items,
                "categories":categories
            })
        else:
            order = request.POST.get("order")
            if order == "descending":
                all_products = InStockProduct.objects.all()
                sorted_products = sorted(all_products,key = lambda x:x.price,reverse=True)
                messages.success(request, "Items sorted via price in descending order successfully")
                return render(request, 'index.html', {
                    "instockproducts": sorted_products,
                    "categories":categories
                })
            else:
                all_products = InStockProduct.objects.all()
                sorted_products = sorted(all_products,key = lambda x:x.price,reverse=False)
                messages.success(request, "Items sorted via price in ascending order successfully")
                return render(request, 'index.html', {
                    "instockproducts": sorted_products,
                    "categories":categories
                })
        
    if request.user.is_staff == True and request.user.is_superuser == True:
        return redirect("logout")
    
    #instockproducts = InStockProduct.objects.all()
    orderedproducts = OrderedProduct.objects.all()
    displayedcategories = Category.objects.all()
    selected_categories = request.GET.getlist("category")
    category_ids = []
    for category_name in selected_categories:
        category = Category.objects.get(name=category_name)
        category_ids.append(category.id)
    if selected_categories:
        instockproducts = InStockProduct.objects.filter(category__in=category_ids)
    else:
        instockproducts = InStockProduct.objects.all()
    if not instockproducts:
        messages.success(request, "No products found")
    data = {
        "instockproducts": instockproducts,
        "orderedproducts": orderedproducts,
        #"users": Users.objects.all()
        "categories":displayedcategories
    }
    return render(request,"index.html", data)

@login_required
def accounts(request):
    if request.method == "POST":
        entered_balance = int(request.POST.get("balance"))
        accounts= Account.objects.filter(user = request.user)
        account = accounts[0]
        account.balance += entered_balance
        account.save()
        return render(request,"account.html",{"accounts":accounts})
    else:
        accounts = Account.objects.filter(user = request.user)
        return render(request,"account.html",{"accounts":accounts})

def login(request):
    next_url = request.GET.get('next')
    if request.method == "POST":
        form = LoginForm(data = request.POST)
        # databaseden formdaki bilgilerdeki usera ara
        username = form.data.get("username")
        password = form.data.get("password")
        if form.is_valid():
            user = authenticate(request,username = username,password = password)
            if user is not None:
                auth_login(request,user)
                count = Account.objects.count()
                if Account.objects.filter(user = request.user).exists():
                    pass
                else:
                    account = Account.objects.create(ID = count + 1,user = user)
                    account.save()
                next_url = request.POST.get("next")
                if next_url:
                    return redirect("cart")
                else:
                    return redirect("index")
            else:
                return HttpResponse(form.error_messages["invalid_login"])
        else:
            return render(request,"login.html",{"form":form,"next":next_url})
            
    else:
        form = LoginForm()
        return render(request,"login.html",{"form":form,"next":next_url})

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            count = Account.objects.count()
            user = Users.objects.last()
            account = Account.objects.create(ID = count + 1,user = user)
            account.save()
            messages.success(request,f"Account created for {request.POST.get('username')}")
            return redirect("login")
        else:
            return render(request,"signup.html",{"form":form})
    else:
        form = SignupForm()
        return render(request,"signup.html",{"form":form})
    
def logout_view(request):
    logout(request)
    return redirect("/")
   
def delivery(request):
    if request.method == "POST":
        command = request.POST.get("command")
        product_id = request.POST.get("product_id")
        if command == "delete":
            said_ordered_product = OrderedProduct.objects.get(ID = product_id)
            purchased_product_id = said_ordered_product.InstockID
            said_purchased_product = PurchasedProduct.objects.get(ID = purchased_product_id)
            said_purchased_item = PurchaseHistory.objects.get(product = said_purchased_product)
            OrderedProduct.objects.get(ID = product_id).delete()
            said_purchased_product.purchased = False
            said_purchased_product.save()
            PurchaseHistory.objects.get(product = said_purchased_product).delete()

    if request.user.is_authenticated:
        ordered_products = OrderedProduct.objects.filter(recipient = request.user)
        #ordered_products = OrderedProduct.objects.all()
        return render(request,"delivery.html",{"products":ordered_products})
    else:
        products = []
        return render(request,"delivery.html",{"products":products})

def purchased(request):
    if request.method == "POST":
        command = request.POST.get("command")
        purchased_id = request.POST.get("product_id")
        if command == "return":
            #create a refund request
            purchased_product = get_object_or_404(PurchaseHistory,pk=purchased_id)
            refund = Refund.objects.create(ID = Refund.objects.count() + 1,product = purchased_product.product,
            user = purchased_product.user)
            refund.save()
            purchased_product.refund_requested = True
            purchased_product.save()
            history = PurchaseHistory.objects.filter(user = request.user)
            days_remain = DaysRemain(history)
            return render(request,"purchased.html",{"products":history,"days":days_remain})
    else:
        if request.user.is_authenticated:
            it = 0
            if Refund.objects.count() != 0:
                refunds = Refund.objects.filter(user = request.user)
                for refund in refunds:
                    if refund.Approved == True:
                        said_purchased_product = refund.product
                        said_product = InStockProduct.objects.get(name = said_purchased_product.name)
                        purchased_item = PurchaseHistory.objects.filter(product = said_purchased_product)
                        purchased_item = purchased_item[it]
                        if purchased_item.refund_accepted == True:
                            pass
                        else:
                            purchased_item.refund_accepted = True
                            purchased_item.save()

                            said_product.quantity_in_stocks += 1
                            said_product.save()
                            said_accounts = Account.objects.filter(user = request.user)
                            said_account = said_accounts[0]
                            if said_product.discount != 0:
                                #discountlu price geri dönecek
                                said_account.balance += said_product.newPrice
                                said_account.save()
                            else:
                                #normal price geri dönecek
                                said_account.balance += said_product.price
                                said_account.save()
                    else:
                        it += 1
                        continue
                    it += 1
            purchased_history = PurchaseHistory.objects.filter(user = request.user)
            days_remain = DaysRemain(purchased_history)
            return render(request,"purchased.html",{"products":purchased_history,"days":days_remain})
        else:
            products = []
            return render(request,"purchased.html",{"products":products})
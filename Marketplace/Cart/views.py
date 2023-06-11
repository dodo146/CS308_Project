from django.shortcuts import render,redirect,get_object_or_404
from .models import Cart,PurchaseHistory
from Main.models import Account
from Main.helper_functions import check_anonymous_cart_products,get_products_from_cart_object,total_price,price_quantity
from Product.models import InStockProduct,OrderedProduct,Users,PurchasedProduct
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers
# Create your views here.
import json
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def create_pdf(name,items,email):
    class PDF(FPDF):
        def header(self):
            # Logo
            self.image('download.png', 10, 8, 25)
            # font
            self.set_font('helvetica', 'B', 20)
            # Padding
            self.cell(40)
            # Title
            self.cell(120, 10, 'Thanks for Shoping with us', border=True, ln=1, align='C')
            # Line break
            self.ln(20)

        # Page footer
        def footer(self):
            # Set position of the footer
            self.set_y(-15)
            # set font
            self.set_font('helvetica', 'I', 8)
            # Set font color grey
            self.set_text_color(169, 169, 169)
            # Page number
            self.cell(0, 10, f'Page {self.page_no()}', align='C')

    # Create a PDF object
    pdf = PDF('P', 'mm', 'Letter')

    # get total page numbers
    pdf.alias_nb_pages()

    # Set auto page break
    pdf.set_auto_page_break(auto = True, margin = 15)

    #Add Page
    pdf.add_page()

    # specify font
    pdf.set_font('helvetica', 'BIU', 16)

    pdf.set_font('times', '', 12)
    pdf.cell(0, 10, f'Dear '+ name +' thanks for chossing us', ln=1)
    pdf.cell(0, 10, f'', ln=1)

    pdf.cell(0, 10, f'Dear ' + name + ' Here your items: ', ln=1)
    for i in range(len(items)//3):
        pdf.cell(0, 10, f'item: '+ items[i*3]+'     amount: '+ items[i*3+1] +'    price: '+items[i*3+2]+'', ln=1)

    pdf.output('pdf_2.pdf')

    print("*****************************************************************************")
    mail_content = '''Bizzi tercih etdiğiniz için teşşekür ederiz
    '''
    sender_address = 'cs308shopping@gmail.com'
    sender_pass = 'oeiuyzfbjqvzvimc'
    receiver_address = email

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'test'
    # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = 'pdf_2.pdf'
    attach_file = open(attach_file_name, 'rb')  # Open the file as binary mode
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload)  # encode the attachment
    # add payload header with filename
    payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    payload.add_header('Content-Disposition', "attachment; filename= %s" % attach_file_name)
    message.attach(payload)
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security

    session.login(sender_address, sender_pass)  # login with mail_id and password


    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


def cart(request):
    anon_user = None
    related_user = None
    if request.user.is_authenticated:
        check_anonymous_cart_products(request)
    if request.method == "POST":
        command = request.POST.get("command")
        product_id = request.POST.get("product_id")
        if command == "delete":
            #delete that item from cart
            Cart.objects.get(product_id = product_id).delete()
            messages.success(request,f"Item deleted succesfully")
            return redirect("cart")
        else:
            # add a product to the cart
            record_count = Cart.objects.count()
            if record_count != 0:
                if Cart.objects.filter(product_id = product_id).exists():
                    messages.error(request,f"This item is already in your cart. Cannot add this item")
                    return redirect('detail',pk=product_id)
            product = get_object_or_404(InStockProduct,pk = product_id)
            quantity = int(request.POST.get("quantity"))
            if quantity == 0:
                messages.error(request,f"You selected qunatity as zero! Please choose another quantity!")
                return redirect('detail',pk=product_id)
            if product.quantity_in_stocks == 0:
                messages.error(request,f"This item is out of stock. Cannot add this item")
                return redirect('detail',pk=product_id)
            if request.user.is_authenticated:
                # a logged in user adds an item to the cart
                cart_item = Cart.objects.create(product= product,user= request.user,quantity = quantity)
                cart_item.save()
            else:
                # Anonymous user adds an item to the cart
                if Users.objects.filter(username = "Anonymous User").exists():
                    anon_user = Users.objects.get(username = "Anonymous User")
                else:
                    anon_user = Users.objects.create_user(is_active = False,role = "Anonymous User")
                cart_item = Cart.objects.create(product= product,user = anon_user,quantity = quantity)
                cart_item.save()
    
    if Users.objects.filter(username = "Anonymous User").exists():
        anon_user = Users.objects.get(username = "Anonymous User")
    else:
        pass

    if not request.user.is_authenticated:
        cart_items = Cart.objects.filter(user = anon_user)
        related_user = anon_user
    else:
        cart_items = Cart.objects.filter(user = request.user)
        related_user = request.user
    products_dict = get_products_from_cart_object(cart_items)
    products = list(products_dict.keys())
    for ind,p in enumerate(products):
        p.quantity = (cart_items[ind].quantity)
        p.save()
    product_to_price = price_quantity(cart_items)
    
    total = total_price(cart_items)

    return render(request,"cart.html",{"products":products,"user":related_user,"total_price":total,"prices":product_to_price})

@login_required
def buy(request):
    if request.method == "POST":
        check_anonymous_cart_products(request)
        command = request.POST.get("command")
        if command == "buy_all":
            #Buy all items in the cart
            cart_items = Cart.objects.filter(user = request.user)
            products = get_products_from_cart_object(cart_items)
            #the products above is a dict with product as key and its quantity as value
            user = request.user
            for product in products:
                record_count_o = OrderedProduct.objects.count()
                record_count_purchased = PurchasedProduct.objects.count()
                record_count_p = PurchaseHistory.objects.count()
                quantity = products[product]
                if product.discount != 0:
                    ordered_item = OrderedProduct.objects.create(ID = record_count_o + 1,name= product.name,model=product.model,
                    number=product.number,description=product.description,price= product.newPrice,
                    warranty_status=product.warranty_status,distributor_info=product.distributor_info,
                    order_number=str(record_count_o + 1),delivery_address = "",recipient=user,quantity= quantity,purchased_price = product.newPrice,
                    InstockID = product.ID)

                    purchased = PurchasedProduct.objects.create(ID = record_count_purchased + 1,name= ordered_item.name,model=ordered_item.model,
                    number=ordered_item.number,description=ordered_item.description,price= ordered_item.purchased_price,
                    warranty_status=ordered_item.warranty_status,distributor_info=ordered_item.distributor_info,
                    user=user,quantity= quantity,purchased_price = product.newPrice)
                    purchased.save()
                    product.purchased_price = product.newPrice
                    ordered_item.save()
                else:
                    ordered_item = OrderedProduct.objects.create(ID = record_count_o + 1,name= product.name,model=product.model,
                    number=product.number,description=product.description,price=product.price,
                    warranty_status=product.warranty_status,distributor_info=product.distributor_info,
                    order_number=str(record_count_o + 1),delivery_address = "",recipient=user,quantity= quantity,purchased_price = product.price,
                    InstockID = product.ID)

                    purchased = PurchasedProduct.objects.create(ID = record_count_purchased + 1,name= ordered_item.name,model=ordered_item.model,
                    number=ordered_item.number,description=ordered_item.description,price= ordered_item.purchased_price,
                    warranty_status=ordered_item.warranty_status,distributor_info=ordered_item.distributor_info,
                    user=user,quantity= quantity,purchased_price = product.newPrice)
                    purchased.save()

                    product.purchased_price = product.price
                    ordered_item.save()
                Cart.objects.get(product_id = product.ID).delete()
                product.quantity_in_stocks -= quantity
                product.purchased = True
                product.save()
                
                purchased_item = PurchaseHistory.objects.create(ID = record_count_p + 1,product = purchased,user=user)
                purchased_item.save()
            messages.success(request,f"Products are bought successfully.You can check the delivery process in delivery tab")
            return render(request,"buy.html",{"products":products})
        else:
            #Buy a single item from the cart
            product_id = request.POST.get("product_id")
            quantity = int(request.POST.get("quantity"))
            record_count_o = OrderedProduct.objects.count()
            record_count_p = PurchaseHistory.objects.count()
            record_count_purchased = PurchasedProduct.objects.count()
            product = get_object_or_404(InStockProduct,pk = product_id)
            user = request.user
            # lst = [str(product), str(quantity), str(product.price)]
            # create_pdf(" to me ", lst, "cs308shopping@gmail.com")
            # create_pdf(str(user), lst, str(user.email))

            if product.discount != 0:

                
                ordered_item = OrderedProduct.objects.create(ID = record_count_o + 1,name= product.name,model=product.model,
                number=product.number,description=product.description,price=product.newPrice,
                warranty_status=product.warranty_status,distributor_info=product.distributor_info,
                order_number=str(record_count_o + 1),delivery_address = "",recipient=user,quantity= quantity,
                purchased_price = product.newPrice,InstockID = product.ID)
                ordered_item.save()

                purchased = PurchasedProduct.objects.create(ID = record_count_purchased + 1,name= ordered_item.name,model=ordered_item.model,
                number=ordered_item.number,description=ordered_item.description,price= ordered_item.purchased_price,
                warranty_status=ordered_item.warranty_status,distributor_info=ordered_item.distributor_info,
                user=user,quantity= quantity,purchased_price = product.newPrice)
                purchased.save()

                product.purchased_price = product.newPrice
            else:
                ordered_item = OrderedProduct.objects.create(ID = record_count_o + 1,name= product.name,model=product.model,
                number=product.number,description=product.description,price=product.price,
                warranty_status=product.warranty_status,distributor_info=product.distributor_info,
                order_number=str(record_count_o + 1),delivery_address = "",recipient=user,quantity= quantity,
                purchased_price = product.price,InstockID = product.ID)

                purchased = PurchasedProduct.objects.create(ID = record_count_purchased + 1,name= ordered_item.name,model=ordered_item.model,
                number=ordered_item.number,description=ordered_item.description,price= ordered_item.purchased_price,
                warranty_status=ordered_item.warranty_status,distributor_info=ordered_item.distributor_info,
                user=user,quantity= quantity,purchased_price = product.newPrice)
                purchased.save()

                product.purchased_price = product.price
                ordered_item.save()
            Cart.objects.get(product_id = product_id).delete()
            messages.success(request,f"Product is bought successfully.You can check the delivery process in delivery tab")
            product.quantity_in_stocks -= quantity
            product.purchased = True
            product.save()
            purchased_item = PurchaseHistory.objects.create(ID = record_count_p + 1,product = purchased,user=user)
            purchased_item.save()
            return render(request,"buy.html",{"product":product})
        

@login_required
def card_info(request):
    accounts = Account.objects.filter(user = request.user)
    account = accounts[0]
    if bool(request.POST):
        #request.post is not empty
        #client buys a single item
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity"))
        said_product = get_object_or_404(InStockProduct,pk = product_id)
        if said_product.discount != 0:
            final_price = said_product.newPrice * quantity
        else:
            final_price = said_product.price * quantity
        if account.balance - final_price < 0:
            messages.error(request,f"You have not enough money in your balance to buy this item!")
            return redirect('cart')
        else:
            account.balance = account.balance - final_price
            account.save()
        return render(request,"card_info.html",{"product_id":product_id,"quantity":quantity})
    else:
        #clients buys all the cart
        return render(request,"card_info.html")
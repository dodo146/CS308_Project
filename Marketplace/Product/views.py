from django.shortcuts import redirect, render,get_object_or_404
from .models import InStockProduct,Category,Comment

quantity = 0
# Create your views here.
def detail(request,pk):
    global quantity
    referrer = request.META.get("HTTP_REFERER")
    if referrer == f"http://127.0.0.1:8000/items/{pk}":
        pass
    else:
        quantity = 0
    product = get_object_or_404(InStockProduct,pk=pk)
    category = get_object_or_404(Category,id = product.category_id)
    comment = None
    comments = Comment.objects.all()
    #


    if request.method == 'POST':
        if "minus_button" in request.POST:
            current_quantity = request.POST.get("quantity_field")
            if current_quantity == 0:
                # do nothing
                pass
            else:
                quantity -= 1
                return redirect('detail',pk=pk)
        elif "plus_button" in request.POST:
            quantity += 1
            return redirect('detail',pk=pk)
        else:
            stars = request.POST.get('stars', 3)
            content = request.POST.get('content', '')

            comment = Comment.objects.create(product=product, user=request.user, stars=stars, content=content)
            comment.save()
            return redirect('detail',pk=pk)
    return render(request,"detail.html",{
            "product":product,
            "category":category,
            "comments":comments,
            "quantity":quantity,})

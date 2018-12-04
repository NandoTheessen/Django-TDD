from lists.models import Item
from django.shortcuts import render, redirect

# Create your views here.,
def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        # ^ neat shorthand to create a new Item
        return redirect('/')
    else:
        new_item_text = ''

    items = Item.objects.all()
    return render(request, 'home.html', {'items': items}) 
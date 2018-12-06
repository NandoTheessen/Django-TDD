from lists.models import Item
from django.shortcuts import render, redirect

# Create your views here.,
def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world')
        # ^ neat shorthand to create a new Item
    return render(request, 'home.html') 

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
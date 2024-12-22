
from django.contrib import messages
from django import forms
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth.models import User
from base.models import UserProfile,Dress,MyCart
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request,'base/index.html')

def items(request):
    q = request.GET.get('q')
    items = Dress.objects.filter(cat = q) if q else Dress.objects.all()
    return render(request,'base/items.html',{'items': items})

def contact(request):
    return render(request,'base/contact.html')


@login_required(login_url='accounts:login')  # Ensure the user is logged in
def mycart(request):
    try:
        # Get the cart for the logged-in user, assuming each user has one cart
        cart = MyCart.objects.get(user=request.user)
    except MyCart.DoesNotExist:
        cart = None  # In case the user doesn't have a cart yet

    context = {
        'cart': cart
    }
    return render(request, 'base/mycart.html', context)

@login_required(login_url='accounts:login')
def remove_from_cart(request, item_id):
    try:
        # Get the user's cart
        cart = MyCart.objects.get(user=request.user)
        item = Dress.objects.get(pk=item_id)
        
        # Remove the item from the cart
        cart.items.remove(item)
    except MyCart.DoesNotExist:
        pass  # If the cart doesn't exist, nothing happens
    except Dress.DoesNotExist:
        pass  # If the item doesn't exist, nothing happens

    return redirect('base:mycart')  # Redirect back to the cart page

@login_required(login_url='accounts:login')
def checkout(request):
    try:
        # Get the user's cart
        cart = MyCart.objects.get(user=request.user)
    except MyCart.DoesNotExist:
        cart = None  # If the cart doesn't exist

    if request.method == 'POST':
        # Here, you would process the payment and order logic.
        # For now, let's assume it's successful and clear the cart
        if cart:
            cart.items.clear()  # Clear items after checkout (for example, simulate the purchase)
            return redirect('base:order_confirmation')  # Redirect to a confirmation page

    context = {
        'cart': cart
    }
    return render(request, 'base/checkout.html', context)

@login_required(login_url='accounts:login')
def order_confirmation(request):
    return render(request, 'base/order_confirmation.html')


@login_required(login_url='accounts:login')
def update(request):
    if  request.user.userprofile.post == 'admin':
        dresses = Dress.objects.all()
        context = {'dresses' : dresses}
        return render(request,'base/update.html',context)
    else:
        return render(request,'base/notallowed.html')
    


@login_required(login_url='accounts:login')
def adddress(request):
    if request.user.userprofile.post == 'admin':
        if request.method == 'POST':
            try:
                name = request.POST['name']
                price = request.POST['price']
                cat = request.POST['category']
                description = request.POST['description']
                img = request.FILES.get('image', None)

                dress = Dress.objects.create(
                    name=name,
                    price=price,
                    cat=cat,
                    ds=description,
                    img=img,
                )
                dress.save()
                messages.success(request, "Dress added successfully!")
                return redirect('base:update')
            except KeyError as e:
                messages.error(request, f"Missing required field: {str(e)}")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        return render(request, 'base/add-dress.html')
    else:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('index')

class DressForm(forms.ModelForm):
    class Meta:
        model = Dress
        fields = ['name', 'price', 'ds', 'img']  # Include all fields you want to allow editing

@login_required(login_url='accounts:login')
def update_dress(request, pk):
    categories = ['Sarees','Kurtas','Lehengas']  # List of categories

    dress = get_object_or_404(Dress, pk=pk)

    if request.method == 'POST':
        cat = request.POST.get('cat') 
        if 'update' in request.POST:
            dress.cat = cat
            form = DressForm(request.POST, request.FILES, instance=dress)
            if form.is_valid():
                form.save()
                messages.success(request, "Dress updated successfully!")
                return redirect('base:update')  # Correct URL pattern with pk
        elif 'delete' in request.POST:
            dress.delete()
            messages.success(request, "Dress deleted successfully!")
            return redirect('base:update')  # Redirect to the update list page
    else:
        form = DressForm(instance=dress)

    context = {'form': form, 'dress': dress, 'categories': categories}
    return render(request, 'base/update_dress.html', context)

def ipage(request,pk):
    dress = Dress.objects.get(pk =pk)

    if request.method == 'POST':
        # Handle the "Add to Cart" logic here
        if 'Mycart' in request.POST:
            # Get or create a cart for the user
            cart, created = MyCart.objects.get_or_create(user=request.user)
            cart.items.add(dress)  # Add the selected dress to the cart
            # Optionally, redirect to the cart page or show a success message
            return redirect('base:mycart')
    context = {'dress' : dress}
    return render(request,'base/ipage.html',context)




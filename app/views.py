from django.shortcuts import render
from app.models import Product,Category
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404,redirect
from .forms import OrderModelForm,CommentModelForm,ProductModelForm
from django.contrib import messages
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from .utils import get_filter


# Create your views here.


def index(request,category_id = None):
    categories = Category.objects.all()
    search_query = request.GET.get('q','')
    filter_type = request.GET.get('filter','')
    

    if category_id:
        products = Product.objects.filter(category = category_id)
    else:
        products = Product.objects.all()
        
    if search_query:
        products = products.filter(name__icontains = search_query)
        
    products = products.annotate(avg_rating = Avg('comments__rating'))
    
    products = get_filter(filter_type,products)
    
    
    
    
    
    context = {
        'products':products,
        'categories':categories
        }
    return render(request,'app/home.html',context)


def product_detail(request,product_id):
    try:
        product = Product.objects.get(id = product_id)
        related_products = Product.objects.filter(category = product.category).exclude(id=product.id)
        context = {
            'product':product,
            'related_products':related_products
            }
        return render(request,'app/detail.html',context)
    except Product.DoesNotExist:
        return HttpResponse('Product Not Found')


def order_detail(request,product_id):
    # product = Product.objects.get(id=product_id)
    product =  get_object_or_404(Product,pk=product_id)
    form = OrderModelForm()
    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if product.quantity >= order.quantity:
                order.product = product
                product.quantity  -=  order.quantity
                product.save()
                order.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Product Successfully ordered'
                    
                )
                return redirect('product_detail',product_id)
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Dont have enough product quantity'
                )
                # error message
                
                
        # request.POST = {'name':'asdasd','phone':'213123','quantity':123}
    context = {
        'form':form,
        'product':product
    }
    
    return render(request,'app/detail.html',context)



def comment_create(request,pk):
    product = get_object_or_404(Product,pk=pk)
    form = CommentModelForm()
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        comment = form.save(commit=False)
        comment.product = product
        comment.save()
        return redirect('product_detail',pk)
    
    context = {
        'form':form,
        'product':product
    }
    return render(request,'app/detail.html',context)
        
    
# @login_required
def create_product(request):
    categories = Category.objects.all()
    form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        
    context = {
        'form':form,
        'categories':categories
    }
    
    return render(request,'app/product/product_add.html',context=context)


def delete_product(request,pk):
    product = Product.objects.get(id = pk)
    if product:
        product.delete()
        return redirect('index')
    
    return render(request,'app/detail.html')

def edit_product(request,pk):
    categories = Category.objects.all()
    product = get_object_or_404(Product, pk=pk)
    form = ProductModelForm(instance=product)
    if request.method == "POST":
        form = ProductModelForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect('index')
    
    context = {
        'form':form,
        'product':product,
        'categories':categories
        }
        
    return render(request,'app/product/edit_product.html',context)
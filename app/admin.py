from django.contrib import admin
from app.models import Product,Category,Order,Comment
from django.contrib.auth.models import User,Group

# Register your models here.


# admin.site.register(Product)

admin.site.register(Category)
admin.site.register(Order)

# category => categories

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','category']
    search_fields = ['name']
    list_filter = ['category']
    
    
admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.site_header = "Abdurahmon Admin"
admin.site.site_title = "Abdurahmon Admin Portal"
admin.site.index_title = "Welcome to UMSRA Researcher Portal"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','product','rating']
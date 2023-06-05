from django.contrib import admin
from tgbot_ema.models import Profile, Product, Category

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram_user_id', 'phoneNumber')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'description', 'price', 'image',)
    list_filter = ('category',)

# Register your models here.

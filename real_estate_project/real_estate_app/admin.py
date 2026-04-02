from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Property, Booking

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'phone_number', 'is_admin', 'is_owner', 'is_seeker', 'kyc_status', 'pincode']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('phone_number', 'pincode', 'kyc_status', 'is_admin', 'is_owner', 'is_seeker')}),
    )

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'owner', 'address', 'price', 'status')
    list_filter = ('status',)
    search_fields = ('address', 'owner__username')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'property', 'seeker', 'start_date', 'duration_months', 'total_amount', 'payment_status')
    list_filter = ('payment_status', 'start_date')
    search_fields = ('property__address', 'seeker__username')

admin.site.register(User, CustomUserAdmin)

# File: listings/admin.py

from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Count
from .models import CarListing, CarImage, Message, Review

# --- Admin view for Additional Images ---
class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3

# --- Admin view for Car Listings ---
class CarListingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'seller', 'price', 'status', 'location_city')
    list_filter = ('status', 'fuel_type', 'make')
    search_fields = ('make', 'model', 'seller__username')
    list_editable = ('status',)
    inlines = [CarImageInline]

# --- UPDATED: Admin view for Messages ---
class MessageAdmin(admin.ModelAdmin):
    # --- FIX: Added 'short_content' to the display ---
    list_display = ('sender', 'receiver', 'listing', 'short_content', 'timestamp', 'is_read')
    list_filter = ('is_read', 'listing__make')
    search_fields = ('sender__username', 'receiver__username', 'content')
    readonly_fields = ('sender', 'receiver', 'listing', 'content', 'timestamp', 'is_read')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    # --- NEW: A custom function to show a preview of the message ---
    def short_content(self, obj):
        # This will show the first 50 characters of the message content
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content Preview' # Sets the column header name

# --- Admin view for Reviews ---
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'seller', 'listing', 'rating', 'timestamp')
    list_filter = ('rating', 'listing__make')
    search_fields = ('reviewer__username', 'seller__username', 'comment')
    readonly_fields = ('reviewer', 'seller', 'listing', 'rating', 'comment', 'timestamp')

    def has_add_permission(self, request):
        return False

# --- Register all your models ---
try:
    admin.site.unregister(CarListing)
except admin.sites.NotRegistered:
    pass
admin.site.register(CarListing, CarListingAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Review, ReviewAdmin)


# --- CUSTOM ADMIN DASHBOARD SETUP (remains the same) ---
original_index = admin.site.index
def custom_index(request, *args, **kwargs):
    total_users = User.objects.count()
    total_listings = CarListing.objects.count()
    active_listings = CarListing.objects.filter(status='ACTIVE').count()
    sold_listings = CarListing.objects.filter(status='SOLD').count()
    listings_by_brand = CarListing.objects.values('make').annotate(count=Count('id')).order_by('-count')
    brand_labels = [item['make'] for item in listings_by_brand]
    brand_data = [item['count'] for item in listings_by_brand]
    listings_by_status = CarListing.objects.values('status').annotate(count=Count('id')).order_by('-count')
    status_labels = [item['status'].replace('_', ' ').title() for item in listings_by_status]
    status_data = [item['count'] for item in listings_by_status]
    kwargs['extra_context'] = {
        'total_users': total_users,
        'total_listings': total_listings,
        'active_listings': active_listings,
        'sold_listings': sold_listings,
        'brand_labels': brand_labels,
        'brand_data': brand_data,
        'status_labels': status_labels,
        'status_data': status_data,
    }
    return original_index(request, *args, **kwargs)

admin.site.index_template = 'admin/dashboard.html'
admin.site.index = custom_index

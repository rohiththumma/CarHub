# File: listings/admin.py
from itertools import chain
from django.urls import reverse
from django.utils.html import format_html
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
    # --- Existing analytics queries (remain the same) ---
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

    # --- CORRECTED: Fetch a larger pool of recent activities ---
    # This ensures we don't miss recent events from one category.
    recent_users = User.objects.order_by('-date_joined')[:10]
    recent_listings = CarListing.objects.order_by('-created_at')[:10]
    recent_reviews = Review.objects.order_by('-timestamp')[:10]

    # Add a custom 'activity_type' and 'timestamp' to each object
    for user in recent_users:
        user.activity_type = 'User'
        user.timestamp = user.date_joined
        
    for listing in recent_listings:
        listing.activity_type = 'Listing'
        listing.timestamp = listing.created_at

    for review in recent_reviews:
        review.activity_type = 'Review'
        # The 'timestamp' field already exists

    # Combine all activities into one list
    combined_activities = list(chain(recent_users, recent_listings, recent_reviews))

    # Sort the combined list by timestamp in descending order
    sorted_activities = sorted(combined_activities, key=lambda x: x.timestamp, reverse=True)

    # --- Populate the context for the template ---
    kwargs['extra_context'] = {
        'total_users': total_users,
        'total_listings': total_listings,
        'active_listings': active_listings,
        'sold_listings': sold_listings,
        'brand_labels': brand_labels,
        'brand_data': brand_data,
        'status_labels': status_labels,
        'status_data': status_data,
        # Get the top 10 most recent activities overall
        'activity_feed': sorted_activities[:10],
    }
    return original_index(request, *args, **kwargs)

admin.site.index_template = 'admin/dashboard.html'
admin.site.index = custom_index

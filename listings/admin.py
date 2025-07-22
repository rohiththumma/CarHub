# File: listings/admin.py

from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Count
from .models import CarListing

# This is the standard way to register your CarListing model
class CarListingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'seller', 'price', 'status', 'location_city')
    list_filter = ('status', 'fuel_type', 'make')
    search_fields = ('make', 'model', 'seller__username')
    list_editable = ('status',)

# Unregister the default admin site for CarListing if it's already registered
# This prevents errors if you run this code multiple times.
try:
    admin.site.unregister(CarListing)
except admin.sites.NotRegistered:
    pass

# Register your CarListing model with the custom admin options
admin.site.register(CarListing, CarListingAdmin)


# --- CUSTOM ADMIN DASHBOARD SETUP ---

# Override the default admin site's index template
admin.site.index_template = 'admin/dashboard.html'

# We need to add a custom context variable to the admin index view.
# First, we get the original index view.
original_index = admin.site.index

# Then, we create our own custom index view.
def custom_index(request, *args, **kwargs):
    # This is where we will calculate all our statistics.
    
    # 1. Metric Cards
    total_users = User.objects.count()
    total_listings = CarListing.objects.count()
    active_listings = CarListing.objects.filter(status='ACTIVE').count()
    sold_listings = CarListing.objects.filter(status='SOLD').count()

    # 2. Data for Charts
    # Listings by brand
    listings_by_brand = CarListing.objects.values('make').annotate(count=Count('id')).order_by('-count')
    
    # Prepare data in a format that Chart.js can understand
    brand_labels = [item['make'] for item in listings_by_brand]
    brand_data = [item['count'] for item in listings_by_brand]

    # Listings by status
    listings_by_status = CarListing.objects.values('status').annotate(count=Count('id')).order_by('-count')
    status_labels = [item['status'].replace('_', ' ').title() for item in listings_by_status]
    status_data = [item['count'] for item in listings_by_status]

    # Add our calculated data to the context that gets sent to the template.
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
    
    # Call the original index view with our modified context.
    return original_index(request, *args, **kwargs)

# Finally, replace the default index view with our custom one.
admin.site.index = custom_index

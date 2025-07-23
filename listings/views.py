# File: listings/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# --- Import CarImage ---
from .models import CarListing, Message, User, Review, Profile, CarImage
from .forms import (
    CarListingForm, UserUpdateForm, ProfileUpdateForm, 
    MessageForm, CarFilterForm, ReviewForm
)
from django.contrib.auth import logout
from django.db.models import Q, Avg

# ... (all other views from landing_page_view to logout_view remain the same) ...
def landing_page_view(request):
    featured_listings = CarListing.objects.filter(status='ACTIVE').order_by('-created_at')[:3]
    return render(request, 'landing.html', {'featured_listings': featured_listings})

def car_list_view(request):
    queryset = CarListing.objects.filter(status='ACTIVE').order_by('-created_at')
    query = request.GET.get('q')
    filter_form = CarFilterForm(request.GET)
    if query:
        queryset = queryset.filter(Q(make__icontains=query) | Q(model__icontains=query))
    if filter_form.is_valid():
        transmission = filter_form.cleaned_data.get('transmission')
        fuel_type = filter_form.cleaned_data.get('fuel_type')
        min_price = filter_form.cleaned_data.get('min_price')
        max_price = filter_form.cleaned_data.get('max_price')
        if transmission: queryset = queryset.filter(transmission=transmission)
        if fuel_type: queryset = queryset.filter(fuel_type=fuel_type)
        if min_price is not None: queryset = queryset.filter(price__gte=min_price)
        if max_price is not None: queryset = queryset.filter(price__lte=max_price)
    return render(request, 'car_list.html', {'listings': queryset, 'search_query': query, 'filter_form': filter_form})

def car_detail_view(request, pk):
    car = get_object_or_404(CarListing, id=pk, status='ACTIVE')
    message_form = MessageForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to contact a seller.")
            return redirect('login')
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.sender = request.user
            new_message.receiver = car.seller
            new_message.listing = car
            new_message.save()
            messages.success(request, f"Your message has been sent to {car.seller.username}.")
            return redirect('car-detail', pk=pk)
    return render(request, 'car_detail.html', {'car': car, 'message_form': message_form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account created for {form.cleaned_data.get("username")}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('landing-page')

# --- UPDATED post_car_view ---
@login_required
def post_car_view(request):
    if request.method == 'POST':
        form = CarListingForm(request.POST, request.FILES)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.seller = request.user
            new_listing.save()
            
            # Handle the multiple additional images
            images = request.FILES.getlist('additional_images')
            for image in images:
                CarImage.objects.create(listing=new_listing, image=image)
            
            messages.success(request, 'Your car has been listed! It is now pending admin approval.')
            return redirect('my-listings')
    else:
        form = CarListingForm()
    return render(request, 'post_car.html', {'form': form, 'page_title': 'Post Your Car for Sale'})

# ... (my_listings_view and my_listing_detail_view remain the same) ...
@login_required
def my_listings_view(request):
    user_listings = CarListing.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'my_listings.html', {'listings': user_listings, 'page_title': 'My Car Listings'})

@login_required
def my_listing_detail_view(request, pk):
    listing = get_object_or_404(CarListing, id=pk, seller=request.user)
    return render(request, 'car_detail.html', {'car': listing})

# --- UPDATED edit_listing_view ---
@login_required
def edit_listing_view(request, pk):
    listing = get_object_or_404(CarListing, id=pk, seller=request.user)
    if request.method == 'POST':
        form = CarListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            
            # Handle any newly uploaded additional images
            images = request.FILES.getlist('additional_images')
            for image in images:
                CarImage.objects.create(listing=listing, image=image)
                
            messages.success(request, "Your listing has been updated successfully!")
            return redirect('my-listings')
    else:
        form = CarListingForm(instance=listing)
    return render(request, 'edit_listing.html', {'form': form, 'page_title': f"Editing: {listing.make} {listing.model}"})

# ... (all other views from delete_listing_view to the end remain the same) ...
@login_required
def delete_listing_view(request, pk):
    listing = get_object_or_404(CarListing, id=pk, seller=request.user)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, "Your listing has been successfully deleted.")
        return redirect('my-listings')
    return render(request, 'delete_listing_confirm.html', {'listing': listing})

@login_required
def mark_as_sold_view(request, pk):
    listing = get_object_or_404(CarListing, id=pk, seller=request.user)
    if listing.status == 'ACTIVE':
        listing.status = 'SOLD'
        listing.save()
        messages.success(request, f"Congratulations! You have marked '{listing}' as sold.")
    else:
        messages.error(request, "This listing is not active and cannot be marked as sold.")
    return redirect('my-listings')

@login_required
def wishlist_view(request):
    wishlist_items = request.user.wishlist_items.all().order_by('-created_at')
    return render(request, 'wishlist.html', {'listings': wishlist_items, 'page_title': 'My Wishlist'})

@login_required
def toggle_wishlist_view(request, pk):
    listing = get_object_or_404(CarListing, id=pk)
    if listing.wishlist.filter(id=request.user.id).exists():
        listing.wishlist.remove(request.user)
        messages.success(request, f"Removed {listing.make} {listing.model} from your wishlist.")
    else:
        listing.wishlist.add(request.user)
        messages.success(request, f"Added {listing.make} {listing.model} to your wishlist.")
    return redirect('car-detail', pk=pk)

def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    reviews = profile_user.reviews_received.all().order_by('-timestamp')
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    context = {'profile_user': profile_user, 'reviews': reviews, 'average_rating': average_rating}
    return render(request, 'profile.html', context)

@login_required
def edit_profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'page_title': 'Edit My Profile'
    }
    return render(request, 'edit_profile.html', context)

@login_required
def inbox_view(request):
    all_user_messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-timestamp')
    conversation_threads = {}
    for message in all_user_messages:
        other_user = message.sender if message.receiver == request.user else message.receiver
        thread_key = (message.listing.id, other_user.id)
        if thread_key not in conversation_threads:
            conversation_threads[thread_key] = {
                'latest_message': message,
                'other_user': other_user
            }
    context = {
        'conversation_threads': list(conversation_threads.values()),
        'page_title': 'My Inbox'
    }
    return render(request, 'inbox.html', context)

@login_required
def conversation_view(request, listing_pk, other_user_pk):
    listing = get_object_or_404(CarListing, id=listing_pk)
    other_user = get_object_or_404(User, id=other_user_pk)
    if listing.seller not in [request.user, other_user]:
        messages.error(request, "You are not authorized to view this conversation.")
        return redirect('inbox')
    if request.user == other_user:
        messages.error(request, "Invalid conversation.")
        return redirect('inbox')
    conversation_messages = Message.objects.filter(
        listing=listing,
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')
    if request.method == 'POST':
        reply_form = MessageForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.sender = request.user
            reply.receiver = other_user
            reply.listing = listing
            reply.save()
            messages.success(request, "Your reply has been sent.")
            return redirect('conversation', listing_pk=listing.pk, other_user_pk=other_user.pk)
    else:
        reply_form = MessageForm()
    context = {
        'listing': listing,
        'other_user': other_user,
        'messages': conversation_messages,
        'reply_form': reply_form,
        'page_title': f'Conversation about {listing.make} {listing.model}'
    }
    return render(request, 'conversation.html', context)

@login_required
def my_purchases_view(request):
    sold_listings = CarListing.objects.filter(status='SOLD')
    purchased_cars = []
    for listing in sold_listings:
        last_message = Message.objects.filter(listing=listing).order_by('-timestamp').first()
        if last_message:
            potential_buyer = None
            if last_message.sender == listing.seller:
                potential_buyer = last_message.receiver
            else:
                potential_buyer = last_message.sender
            if potential_buyer == request.user:
                has_reviewed = Review.objects.filter(reviewer=request.user, listing=listing).exists()
                purchased_cars.append({'car': listing, 'has_reviewed': has_reviewed})
    context = {
        'purchased_cars': purchased_cars, 
        'page_title': 'My Purchases'
    }
    return render(request, 'my_purchases.html', context)

@login_required
def leave_review_view(request, listing_pk):
    listing = get_object_or_404(CarListing, id=listing_pk, status='SOLD')
    if Review.objects.filter(reviewer=request.user, listing=listing).exists():
        messages.error(request, "You have already submitted a review for this purchase.")
        return redirect('my-purchases')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.seller = listing.seller
            review.listing = listing
            review.save()
            messages.success(request, f"Your review for {listing.seller.username} has been submitted!")
            return redirect('my-purchases')
    else:
        form = ReviewForm()
    context = {'form': form, 'listing': listing, 'page_title': f'Review Your Purchase: {listing.make} {listing.model}'}
    return render(request, 'leave_review.html', context)

def compare_cars_view(request):
    car_ids_str = request.GET.get('ids', '')
    cars_to_compare = []
    if car_ids_str:
        car_ids = car_ids_str.split(',')
        cars_to_compare = CarListing.objects.filter(id__in=car_ids)
    return render(request, 'compare.html', {'cars': cars_to_compare, 'page_title': 'Compare Cars'})

from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [
    path('', views.landing_page_view, name='landing-page'),
    path('cars/', views.car_list_view, name='car-list'),
    path('cars/<int:pk>/', views.car_detail_view, name='car-detail'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post-car/', views.post_car_view, name='post-car'),
    path('my-listings/', views.my_listings_view, name='my-listings'),
    path('my-listings/<int:pk>/', views.my_listing_detail_view, name='my-listing-detail'),
    path('my-listings/<int:pk>/edit/', views.edit_listing_view, name='edit-listing'),
    path('my-listings/image/<int:image_pk>/delete/', views.delete_car_image_view, name='delete-car-image'),
    path('my-listings/<int:pk>/mark-sold/', views.mark_as_sold_view, name='mark-as-sold'),
    path('my-listings/<int:pk>/delete/', views.delete_listing_view, name='delete-listing'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:pk>/', views.toggle_wishlist_view, name='toggle-wishlist'),
    path('profile/edit/', views.edit_profile_view, name='edit-profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html', success_url='/password-change/done/'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('compare/', views.compare_cars_view, name='compare-cars'),
    path('inbox/', views.inbox_view, name='inbox'),
    path('inbox/conversation/<int:listing_pk>/<int:other_user_pk>/', views.conversation_view, name='conversation'),
    path('my-purchases/', views.my_purchases_view, name='my-purchases'),
    path('my-purchases/<int:listing_pk>/review/', views.leave_review_view, name='leave-review'),
]
    
    
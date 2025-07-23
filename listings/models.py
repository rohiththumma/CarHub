from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator 

# ... (Choices remain the same) ...
TRANSMISSION_CHOICES = (
    ('Automatic', 'Automatic'),
    ('Manual', 'Manual'),
)

FUEL_TYPE_CHOICES = (
    ('Petrol', 'Petrol'),
    ('Diesel', 'Diesel'),
    ('Electric', 'Electric'),
    ('CNG', 'CNG'),
    ('LPG', 'LPG'),
)

LISTING_STATUS_CHOICES = (
    ('PENDING_APPROVAL', 'Pending Approval'),
    ('ACTIVE', 'Active'),
    ('SOLD', 'Sold'),
    ('REJECTED', 'Rejected'),
)


class CarListing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    
    make = models.CharField(max_length=50, help_text="e.g., Maruti Suzuki, Hyundai")
    model = models.CharField(max_length=50, help_text="e.g., Swift, Creta")
    year = models.PositiveIntegerField()
    price = models.PositiveIntegerField(help_text="Price in INR")
    
    # --- NEW FIELD ADDED ---
    kms_driven = models.PositiveIntegerField(help_text="Kilometers driven")
    
    # This is now the MAIN or COVER image for the listing
    image = models.ImageField(upload_to='car_images/', default='car_images/default.png', verbose_name="Main Image")

    mileage = models.PositiveIntegerField(help_text="Mileage in KMPL or KM/Charge")
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES)
    fuel_type = models.CharField(max_length=10, choices=FUEL_TYPE_CHOICES)
    noc_available = models.BooleanField(default=False, verbose_name="NOC Certificate Available")
    
    description = models.TextField()
    location_city = models.CharField(max_length=50)
    
    status = models.CharField(
        max_length=20, 
        choices=LISTING_STATUS_CHOICES, 
        default='PENDING_APPROVAL'
    )
    
    wishlist = models.ManyToManyField(User, related_name='wishlist_items', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model} - ₹{self.price}"

# --- NEW MODEL TO STORE ADDITIONAL IMAGES ---
class CarImage(models.Model):
    """
    A model to store multiple additional images for a single car listing.
    """
    listing = models.ForeignKey(CarListing, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='car_images/additional/')

    def __str__(self):
        return f"Image for {self.listing.make} {self.listing.model}"


# ... (Message, Review, and Profile models remain the same) ...
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    listing = models.ForeignKey(CarListing, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} re: {self.listing.make}"

class Review(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    listing = models.ForeignKey(CarListing, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.seller.username} by {self.reviewer.username} ({self.rating} stars)"

    class Meta:
        unique_together = ('reviewer', 'listing')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

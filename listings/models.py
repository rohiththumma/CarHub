from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator 

# Choices for dropdown menus
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
    # Link to the user who is selling the car
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Core car details
    make = models.CharField(max_length=50, help_text="e.g., Maruti Suzuki, Hyundai")
    model = models.CharField(max_length=50, help_text="e.g., Swift, Creta")
    year = models.PositiveIntegerField()
    price = models.PositiveIntegerField(help_text="Price in INR")
    
    image = models.ImageField(upload_to='car_images/', default='car_images/default.png')

    # Specifications
    mileage = models.PositiveIntegerField(help_text="Mileage in KMPL or KM/Charge")
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES)
    fuel_type = models.CharField(max_length=10, choices=FUEL_TYPE_CHOICES)
    noc_available = models.BooleanField(default=False, verbose_name="NOC Certificate Available")
    
    # Description and location
    description = models.TextField()
    location_city = models.CharField(max_length=50)
    
    # Platform status
    status = models.CharField(
        max_length=20, 
        choices=LISTING_STATUS_CHOICES, 
        default='PENDING_APPROVAL'
    )
    
    wishlist = models.ManyToManyField(User, related_name='wishlist_items', blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model} - ₹{self.price}"

class Message(models.Model):
    """
    Represents a message sent from a buyer to a seller about a specific car listing.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    listing = models.ForeignKey(CarListing, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} re: {self.listing.make}"


class Review(models.Model):
    """
    Represents a review and rating left by a buyer for a seller
    after a transaction.
    """
    # The user who is being reviewed (the seller)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    # The user who is writing the review (the buyer)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    # The car listing that the transaction was about
    listing = models.ForeignKey(CarListing, on_delete=models.CASCADE)
    
    # A star rating from 1 to 5
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    # The text content of the review
    comment = models.TextField()
    # The date the review was created
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.seller.username} by {self.reviewer.username} ({self.rating} stars)"

    class Meta:
        # This ensures that a buyer can only review a seller once for a specific car.
        unique_together = ('reviewer', 'listing')


class Profile(models.Model):
    """
    Extends the default User model to include a profile picture.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
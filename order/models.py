from django.db import models
from django.conf import settings
from store.models import Product, Variation

# ---------------- Payment Model ----------------
class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)  # total amount paid
    status = models.CharField(max_length=50)  # e.g. 'Completed', 'Pending'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_id} - {self.user.email}"


# ---------------- Order Model (User Order) ----------------
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='orders')
    assigned_delivery_man = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deliveries'
    )
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20, unique=True)
    
    # Customer Info
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.TextField(blank=True, null=True)
    
    # Pricing Info
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=50.00)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    is_ordered = models.BooleanField(default=False)
    ip = models.CharField(max_length=20, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def full_address(self):
        return f"{self.address_line_1} {self.address_line_2}"

    def __str__(self):
        return f"Order #{self.order_number} by {self.user.username if self.user else 'Guest'}"


# ---------------- Order Product Model ----------------
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.PositiveIntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    ordered = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.product_name} (x{self.quantity})"



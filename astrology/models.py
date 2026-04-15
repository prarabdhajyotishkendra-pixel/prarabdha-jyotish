from django.db import models

class PalmReading(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    ]
    PAYMENT_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid')
    ]
    
    image = models.ImageField(upload_to='palm_images/right_hand/')
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    payment_status = models.BooleanField(default=False)
    report = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"

class Kundali(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    ]
    PAYMENT_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid')
    ]
    
    name = models.CharField(max_length=200)
    dob = models.DateField(help_text="Format: YYYY-MM-DD")
    birth_time = models.TimeField(help_text="Format: HH:MM:SS")
    birth_place = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True, null=True)
    payment_status = models.BooleanField(default=False)
    report = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"

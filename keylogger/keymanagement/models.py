from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Staff Table
class Staff(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    staff_rfid = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.employee_id})"

# Key Table
class Key(models.Model):
    key_name = models.CharField(max_length=50)
    key_rfid = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.key_name

# Key Log Table
class KeyLog(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    key = models.ForeignKey(Key, on_delete=models.CASCADE)
    checkout_time = models.DateTimeField(auto_now_add=True)
    checkin_time = models.DateTimeField(null=True, blank=True)
    return_status = models.BooleanField(default=False)  # False = Not Returned, True = Returned

    def __str__(self):
        return f"Key {self.key.key_rfid} issued to {self.staff.name}"
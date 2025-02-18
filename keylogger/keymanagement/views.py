from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.utils.timezone import now
from .models import Staff, Key, KeyLog
import pandas as pd


# Create your views here.

# Security Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard
    return render(request, 'keymanagement/login.html')

# Security Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard View (Login Required)
@login_required
def dashboard(request):
    if request.method == "POST":
        staff_rfid = request.POST.get("staff_rfid")
        key_rfid = request.POST.get("key_rfid")

        # Check if staff RFID exists in the database
        try:
            staff = Staff.objects.get(staff_rfid=staff_rfid)
        except Staff.DoesNotExist:
            messages.error(request, "Invalid Staff RFID! Staff not found.")
            return redirect("dashboard")

        # Check if key RFID exists in the database
        try:
            key = Key.objects.get(key_rfid=key_rfid)
        except Key.DoesNotExist:
            messages.error(request, "Invalid Key RFID! Key not found.")
            return redirect("dashboard")

        # Check if key is already checked out
        log_entry = KeyLog.objects.filter(key=key, return_status=False).first()
        
        if log_entry:
            # If the key is already checked out, mark it as returned
            log_entry.checkin_time = now()
            log_entry.return_status = True
            log_entry.save()
            messages.success(request, f"Key returned successfully by {staff.staff_name}.")
        else:
            # Otherwise, log a new key check-out
            KeyLog.objects.create(staff=staff, key=key, checkout_time=now(), return_status=False)
            messages.success(request, f"Key issued successfully to {staff.staff_name}.")

        return redirect("dashboard")

    # Retrieve all logs for display
    logs = KeyLog.objects.all().order_by("-checkout_time")
    return render(request, "keymanagement/dashboard.html", {"logs": logs})

# Export Logs as Excel
@login_required
def export_logs(request):
    logs = KeyLog.objects.all().values('staff__name', 'key__key_name', 'checkout_time', 'checkin_time', 'return_status')
    df = pd.DataFrame(logs)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="key_logs.xlsx"'
    df.to_excel(response, index=False)
    return response

# Clear All Logs
@login_required
def clear_logs(request):
    KeyLog.objects.all().delete()
    return redirect('dashboard')
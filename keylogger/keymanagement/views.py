from django.shortcuts import render, redirect
from django.core.paginator import Paginator
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
        else:
            messages.error(request, "Invalid username or password.")
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

        # Validate Staff RFID
        try:
            staff = Staff.objects.get(staff_rfid=staff_rfid)
        except Staff.DoesNotExist:
            messages.error(request, "❌ Invalid Staff RFID! Staff not found.")
            return redirect("dashboard")

        # Validate Key RFID
        try:
            key = Key.objects.get(key_rfid=key_rfid)
        except Key.DoesNotExist:
            messages.error(request, "❌ Invalid Key RFID! Key not found.")
            return redirect("dashboard")

        # Check if the key is already checked out
        log_entry = KeyLog.objects.filter(key=key, return_status=False).first()

        if log_entry:
            # If key is checked out, mark it as returned
            log_entry.checkin_time = now()
            log_entry.return_status = True
            log_entry.save()
            messages.success(request, f"✔ Key '{key.key_name}' successfully returned by {staff.name}.")
        else:
            # Otherwise, issue a new key
            KeyLog.objects.create(staff=staff, key=key, checkout_time=now(), return_status=False)
            messages.success(request, f"✔ Key '{key.key_name}' successfully issued to {staff.name}.")

        return redirect("dashboard")

    # Retrieve all logs and verify valid staff and key entries
    logs = KeyLog.objects.all().order_by("-checkout_time")

    # Pass logs with proper validation for display
    valid_logs = []
    for log in logs:
        try:
            log.staff_name = Staff.objects.get(id=log.staff.id).name
            log.key_name = Key.objects.get(id=log.key.id).key_name
            valid_logs.append(log)
        except (Staff.DoesNotExist, Key.DoesNotExist):
            continue  # Skip invalid entries
    
    paginator = Paginator(valid_logs, 5)  
    page_number = request.GET.get("page")  
    logs = paginator.get_page(page_number)

    return render(request, "keymanagement/dashboard.html", {"logs": valid_logs})


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
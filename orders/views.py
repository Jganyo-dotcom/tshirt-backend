from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Order
from django.core.files.base import ContentFile
import base64

# Create your views here.

def index(request):
    return HttpResponse("🎯 T-Shirt backend is live!")




from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
@csrf_exempt
def submit_order(request):
    if request.method == "POST":
        name = request.POST.get("name")
        number = request.POST.get("number")
        email = request.POST.get("email")
        to_email = request.POST.get("to_email")
        notes = request.POST.get("notes")
        
        screenshot_data = request.POST.get("screenshot_data")

        # Send email to yourself
        send_mail(
            subject=f"🎨 New T-Shirt Order from {name}",
            message=f"""
You have a new T-shirt order:

Full Name: {name}
Email: {email}
Number of T-shirts: {number}
Notes: {notes}

(Screenshot or uploaded design is included in the backend files.)
""",
            from_email= None,
            recipient_list=['elikemejay@gmail.com'],  # Replace with your real email
        )

        return HttpResponse("✅ Order submitted and email sent.")
    return HttpResponse("❌ Please submit the form using POST.")





from django.core.mail import send_mail
from django.http import HttpResponse

def test_email(request):
    send_mail(
        subject='🎉 Test Email from T-shirt Customizer',
        message='This is a test email to confirm email setup is working.',
        from_email=None,  # Uses DEFAULT_FROM_EMAIL
        recipient_list=['your_email@gmail.com'],  # Replace with your actual email
        fail_silently=False,
    )
    return HttpResponse("✅ Test email sent!")


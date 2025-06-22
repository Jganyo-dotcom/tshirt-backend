from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.core.files.base import ContentFile
from django.http import JsonResponse
import base64
import threading
import time

# Background email sender
def send_order_email(mail):
    try:
        mail.send(fail_silently=False)
        print("✅ Email sent successfully")
    except Exception as e:
        print("❌ Error sending email in background:", e)

@csrf_exempt
def submit_order(request):
    start_time = time.time()

    if request.method == "POST":
        try:
            name = request.POST.get("name")
            number = request.POST.get("number")
            email = request.POST.get("email")
            to_email = request.POST.get("to_email")
            phone = request.POST.get("phone")
            notes = request.POST.get("notes")
            size = request.POST.get('size')
            screenshot_data = request.FILES.get("screenshot_data")


            message = f"""
You have a new T-shirt order:

Full Name: {name}
Email: {email}
Contact: {phone}
Number of T-shirts: {number}
size : {size}
Notes: {notes}

(Screenshot is attached if provided.)
"""

            mail = EmailMessage(
                subject=f"🎨 New T-Shirt Order from {name}",
                body=message,
                from_email=f"{email}",
                to=['elikemjjames@gmail.com','Kagoventures@gmail.com'],
            )

            if screenshot_data:
                if screenshot_data.size < 5_000_000:
                    mail.attach(screenshot_data.name, screenshot_data.read(), screenshot_data.content_type)
                else:
                    print("⚠️ Screenshot skipped due to large size")

            else:
                print("⚠️ No screenshot file received")


            # Send email in background
            threading.Thread(target=send_order_email, args=(mail,)).start()

            print("🕒 Order processed in", round(time.time() - start_time, 2), "seconds")
            return JsonResponse({
                'message': 'order recieved'
            })

        except Exception as e:
            print("❌ Order failed due to error:", e)

    # If not POST or failed
        return JsonResponse({
            'message': 'order recieved'
        })

@csrf_exempt    
def submit_specific_order(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        number = request.POST.get("number")
        email = request.POST.get("email")
        design = request.POST.get("id_name")
        phone = request.POST.get("phone")
        notes = request.POST.get("notes")
        size = request.POST.get('size')

        message = f"""
        📦 New T-Shirt Order:

        👤 Name: {name}
        📧 Email: {email}
        📱 Phone: {phone}
        🧥 Design ID: {design}
            size : {size}
            number :{number}
            note : {notes}
        """

        try:
            mail = EmailMessage(
                subject=f"🎨 New T-Shirt Order from {name}",
                body=message,
                from_email=f"{email}",
                to=['elikemjjames@gmail.com','Kagoventures@gmail.com'],
            )
            mail.send(fail_silently=False)
            return JsonResponse({'message': 'Order sent successfully!'})
        except Exception as e:
            return JsonResponse({'message': f'Error sending order: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request'}, status=400)




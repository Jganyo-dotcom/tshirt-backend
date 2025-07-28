from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.core.files.base import ContentFile
from django.http import JsonResponse
import base64
from .import models
import threading
import os
from django.utils.timezone import now
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
            location = request.POST.get("location")
            to_email = request.POST.get("to_email")
            phone = request.POST.get("phone")
            discount_code = request.POST.get('discount_code', '').strip().upper()
            notes = request.POST.get("notes")
            discount_status = request.POST.get('discount_status')
            size = request.POST.get('size')
            price = request.POST.get('price')
            width = int(request.POST.get('width'))
            height = int(request.POST.get('height'))
            screenshot_data = request.FILES.get("screenshot_data")
            area = width * height 
            estimated_amount = area
            if area <= 22500 :
                estimated_amount = 150

            elif area > 22500 and area <= 30000 :
                estimated_amount =  150
  
            elif area >30000 and area < 34000 :
                estimated_amount =   150

            elif area >34000 :
                estimated_amount =   150
  
            if discount_code == 'MAKEITYOURS' :
                price = estimated_amount * int(number)
                f_price = price * 0.80
                discount_status = 'Applied discount'
            
            else:
                f_price = estimated_amount * int(number)
                discount_status = 'Not eligible'

            message = f"""
You have a new T-shirt order:

Full Name: {name}
Location: {location}
WhatsApp Contact: {phone}
Number of T-shirts: {number}
Size : {size}
Notes: {notes}
Discount: {discount_status}
frontend price : {price}
final Price : {f_price}

(Screenshot is attached if provided.)
"""

            mail = EmailMessage(
                subject=f"🎨 New T-Shirt Order from {name}",
                body=message,
                from_email= os.getenv("EMAIL_HOST_USER"),   
                to=[ 'elikemjjames@gmail.com','Kagoventures@gmail.com'] #Kagoventures@gmail.com
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
            order = models.Order(name = name , number = number, email = location, to_email = to_email, size = size, notes = notes, screenshot = screenshot_data, phone = phone)
            order.save()

            print("🕒 Order processed in", round(time.time() - start_time, 2), "seconds")
            print(f"""
                    🎉🛍️ NEW ORDER RECEIVED! 🧾💥
                    ===============================
                    👤 Name: {name}
                    🎨 Number: {number}
                    👕 Phone: {phone}
                    ✅ Status: SUCCESSFULLY PLACED
                    📦 Packing it with style & love ❤️
                    🚚 On its way to greatness!

                    🕒 Time: {now().strftime('%Y-%m-%d %H:%M:%S')}
                    ===============================
                    """)
            return JsonResponse({
                'message': f"""
                 Your order has been recieved.
                 Total Price: {f_price}.
                 Discount: {discount_status}.
                 You will receive a confirmation whatsapp message within 24hour!
                  """
            })

        except Exception as e:
            print("❌ Order failed due to error:", e)
            return JsonResponse({
                'message': "Order Failed "
            })

   

@csrf_exempt    
def submit_specific_order(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        phrase = request.POST.get('phrase')
        price = request.POST.get('price')
        number = request.POST.get("number")
        location = request.POST.get("location")
        design = request.POST.get("id_name")
        phone = request.POST.get("phone")
        notes = request.POST.get("notes")
        size = request.POST.get('size')

        message = f"""
        📦 New T-Shirt Order:

            Full Name: {name}
            location: {location}
            Whatsapp Contact: {phone}
            Design ID: {design}
            Size : {size}
            Number of T-shirts:{number}
            Discount: {phrase}
            frontend price:{price}
            Notes : {notes}
        """

        try:
            mail = EmailMessage(
                subject=f"🎨 New T-Shirt Order from {name}",
                body=message,
                from_email=os.getenv("EMAIL_HOST_USER"),
                to=['elikemjjames@gmail.com','Kagoventures@gmail.com']
            )
            mail.send(fail_silently=False)
            order_two = models.Order_specific(name = name , number = number, email = location, size = size, notes = notes, design = design, phone = phone)
            order_two.save()
            print(f"""
                    🎉🛍️ NEW ORDER RECEIVED! 🧾💥
                    ===============================
                    👤 Name: {name}
                    🎨 Number: {number}
                    👕 Phone: {phone}
                    ✅ Status: SUCCESSFULLY PLACED
                    📦 Packing it with style & love ❤️
                    🚚 On its way to greatness!

                    🕒 Time: {now().strftime('%Y-%m-%d %H:%M:%S')}
                    ===============================
                    """)
            return JsonResponse({'message':
                                f"""Your order has been recieved.
                                Total:{price}
                                Discount:{phrase}
                                You will receive a confirmation whatsapp message within 24hours !
                                """})
        except Exception as e:
            return JsonResponse({'message': f'Error sending order: {str(e)}'}, status=500)

    return JsonResponse({'message': 'An error occured.'}, status=400)




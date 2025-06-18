from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
import base64
from django.core.files.base import ContentFile



def index(request) :
    return HttpResponse("🎯 T-Shirt backend is live!")


@csrf_exempt
def submit_order(request):
    if request.method == "POST":
        name = request.POST.get("name")
        number = request.POST.get("number")
        email = request.POST.get("email")
        to_email = request.POST.get("to_email")
        phone = request.POST.get("phone")
        notes = request.POST.get("notes")
        screenshot_data = request.POST.get("screenshot_data")

        # Prepare email content
        message = f"""
You have a new T-shirt order:

Full Name: {name}
Email: {email}
Contact: {phone}
Number of T-shirts: {number}
Notes: {notes}

(Screenshot is attached.)
"""

        # Create email
        mail = EmailMessage(
            subject=f"🎨 New T-Shirt Order from {name}",
            body=message,
            from_email='elikemejay@gmail.com',  # or settings.DEFAULT_FROM_EMAIL
            to=['elikemjjames@gmail.com'],#'Kagoventures@gmail.com' 
        )

        # Attach screenshot if it exists
        if screenshot_data:
            format, imgstr = screenshot_data.split(';base64,')
            ext = format.split('/')[-1]
            file_data = ContentFile(base64.b64decode(imgstr), name=f"screenshot.{ext}")
            mail.attach(file_data.name, file_data.read(), f'image/{ext}')

        # Send the email
        mail.send(fail_silently=False)

        return HttpResponse("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Order Submitted</title>
                <style>
                    body {
                        background: linear-gradient(to right, #e0f7fa, #e8f5e9);
                        height: 100vh;
                        margin: 0;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-family: 'Segoe UI', sans-serif;
                    }
                    .message {
                        padding: 30px 40px;
                        background-color: #d4edda;
                        color: #155724;
                        border: 2px solid #28a745;
                        border-radius: 12px;
                        font-size: 1.5rem;
                        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
                        animation: fadeInScale 1s ease-out;
                        text-align: center;
                    }

                    @keyframes fadeInScale {
                        0% {
                            opacity: 0;
                            transform: scale(0.9);
                        }
                        100% {
                            opacity: 1;
                            transform: scale(1);
                        }
                    }
                </style>
            </head>
            <body>
                <div class="message">
                    ✅ Order submitted and screenshot sent via email.
                </div>
            </body>
            </html>
        """)
    
    return HttpResponse("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Order Submitted</title>
                <style>
                    body {
                        background: linear-gradient(to right, #e0f7fa, #e8f5e9);
                        height: 100vh;
                        margin: 0;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-family: 'Segoe UI', sans-serif;
                    }
                    .message {
                        padding: 30px 40px;
                        background-color: #d4edda;
                        color: #155724;
                        border: 2px solid #28a745;
                        border-radius: 12px;
                        font-size: 1.5rem;
                        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
                        animation: fadeInScale 1s ease-out;
                        text-align: center;
                    }

                    @keyframes fadeInScale {
                        0% {
                            opacity: 0;
                            transform: scale(0.9);
                        }
                        100% {
                            opacity: 1;
                            transform: scale(1);
                        }
                    }
                </style>
            </head>
            <body>
                <div class="message">
                    Something went wrong please place order again under stable internet.
                </div>
            </body>
            </html>
        """)




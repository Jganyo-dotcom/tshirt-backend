from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.core.files.base import ContentFile
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
            screenshot_data = request.FILES.get("screenshot_data")


            message = f"""
You have a new T-shirt order:

Full Name: {name}
Email: {email}
Contact: {phone}
Number of T-shirts: {number}
Notes: {notes}

(Screenshot is attached if provided.)
"""

            mail = EmailMessage(
                subject=f"🎨 New T-Shirt Order from {name}",
                body=message,
                from_email='elikemejay@gmail.com',
                to=['elikemjjames@gmail.com'],
            )

            if screenshot_data:
                print("🖼 Screenshot length:", len(screenshot_data))  # For debugging
                if len(screenshot_data) < 5_000_000:  # Roughly < 5MB
                    format, imgstr = screenshot_data.split(';base64,')
                    ext = format.split('/')[-1]
                    file_data = ContentFile(base64.b64decode(imgstr), name=f"screenshot.{ext}")
                    mail.attach(file_data.name, file_data.read(), f'image/{ext}')
                else:
                    print("⚠️ Screenshot skipped due to large size")

            # Send email in background
            threading.Thread(target=send_order_email, args=(mail,)).start()

            print("🕒 Order processed in", round(time.time() - start_time, 2), "seconds")
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
                            0% { opacity: 0; transform: scale(0.9); }
                            100% { opacity: 1; transform: scale(1); }
                        }
                    </style>
                </head>
                <body>
                    <div class="message">
                        ✅ Order received, Thank you for your patience ❤️ ❤️
                    </div>
                </body>
                </html>
            """)

        except Exception as e:
            print("❌ Order failed due to error:", e)

    # If not POST or failed
    return HttpResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>❌ Failed</title>
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
                    background-color: #f8d7da;
                    color: #721c24;
                    border: 2px solid #f5c6cb;
                    border-radius: 12px;
                    font-size: 1.5rem;
                    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
                    animation: fadeInScale 1s ease-out;
                    text-align: center;
                }

                @keyframes fadeInScale {
                    0% { opacity: 0; transform: scale(0.9); }
                    100% { opacity: 1; transform: scale(1); }
                }
            </style>
        </head>
        <body>
            <div class="message">
                ❌ Something went wrong. Please try again with a stable internet connection.
            </div>
        </body>
        </html>
    """)

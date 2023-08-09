from django.shortcuts import render
from django.contrib import messages
from django.utils.safestring import mark_safe

# Email conf
from django.core.mail import EmailMessage
from django.http import JsonResponse
import json



def cv_view(request):
    return render(request, 'cv/cv.html')

def send_message(request, name, content, to_mail='vercixxx@gmail.com'):
    mail_subject = "Message from contact_me!"
    message = f'Message from {name}: {content}'
    
    email = EmailMessage(mail_subject, message, to=[to_mail])
    
    if email.send():
        message = f"Dear <b>{name}</b>, your message has been sent, thank you"
        return messages.warning(request, mark_safe(message))
    
    else:
        mesasge = f"An error occured when sending email, please try again."
        return messages.error(request, mark_safe(message))
    
    
def contact_me_message(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        content = data.get('content')
        
        send_message(request, name, content)

        response_data = {
            'success': True,
            'message': f"Dear {name}, your message has been sent, thank you"
        }
        return JsonResponse(response_data)
    else:
        response_data = {
            'success': False,
            'message': "Invalid request method"
        }
        return JsonResponse(response_data)

    
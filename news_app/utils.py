from django.core.signing import Signer
from django.core.mail import send_mail
from django.urls import reverse
from .models import Post
import os
from dotenv import load_dotenv
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

load_dotenv()
signer = Signer()

def generate_unsubscribe_token(user_id, category_id):
    data = f"{user_id}:{category_id}"
    return signer.sign(data)

def validate_unsubscribe_token(token, user_id, category_id):
    try:
        data = signer.unsign(token)
        return data == f"{user_id}:{category_id}"
    except:
        return False


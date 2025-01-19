from django.core.signing import Signer
from django.core.mail import send_mail
from django.urls import reverse

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

def send_news_to_subscribers(category, news_title, news_content):
    short_content = news_content[:50] + "..." if len(news_content) > 50 else news_content
    for user in category.subscribers.all():
        token = generate_unsubscribe_token(user.id, category.id)
        unsubscribe_url = f"http://127.0.0.1:8000{reverse('unsubscribe')}?category_id={category.id}&user_id={user.id}&token={token}"

        send_mail(
            subject=f"{news_title}. Здравствуй,{user.first_name or user.username}. Новая статья в твоём любимом разделе!",
            message=f"{news_content}\n\nОтписаться: {unsubscribe_url}",
            html_message=f"""
                <p>Новость в категории {category.name}:</p>
                <h3>{news_title}</h3>
                <p>{short_content}</p>
                <p><a href="{unsubscribe_url}">Отписаться</a></p>
            """,
            from_email="shatalovaleksei2@yandex.com",
            recipient_list=[user.email],
        )
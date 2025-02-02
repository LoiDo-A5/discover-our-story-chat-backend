from onesignal_sdk.client import Client
from django.conf import settings
import logging
import requests

logger = logging.getLogger(__name__)

def send_push_notification(title, message, user_id):
    client = Client(
        app_id=settings.ONESIGNAL_APP_ID,
        rest_api_key=settings.ONESIGNAL_API_KEY
    )
    logger.info(f"1111 - OneSignal App ID: {settings.ONESIGNAL_APP_ID}")
    notification = {
        "headings": {"en": title},
        "contents": {"en": message},
        "filters": [{"field": "tag", "key": "user_id", "relation": "=", "value": str(user_id)}],
    }

    try:
        response = client.send_notification(notification)
        if response.status_code == 200:
            logger.info(f"Notification sent successfully: {response.body}")
        else:
            logger.error(f"Error sending notification: {response.body}")
        return response
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        return None

def set_user_tag(user_id):
    logger.info(f"111111111111111111111111111111111")
    url = "https://onesignal.com/api/v1/players"
    headers = {
        "Authorization": f"Basic {settings.ONESIGNAL_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "app_id": settings.ONESIGNAL_APP_ID,
        "device_type": 6,  # Chrome Web Push (thay đổi theo loại thiết bị của bạn)
        "external_user_id": str(user_id),  # Gán external_user_id
        "tags": {
            "user_id": str(user_id)  # Gán tag user_id
        },
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            logger.info(f"Successfully set user_id tag for user_id: {user_id}")
        else:
            logger.error(f"Failed to set user_id tag: {response.json()}")
    except Exception as e:
        logger.error(f"Error setting tag for user_id {user_id}: {e}")


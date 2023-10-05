from flask import Blueprint, jsonify
import requests

notifikasi = Blueprint("notifikasi", __name__, url_prefix="/api/v2/notif")

ONE_SIGNAL_CONFIG = dict(
    app_id="bde3d405-e01e-4237-855f-c9bb4b4d9c75",
    api_key="NjhiODUzYmUtMDIwYi00MTliLTk2YWMtZGExZmExMDdjOTk2",
)


@notifikasi.get("send")
def push_notif_siswa():
    url = "https://onesignal.com/api/v1/notifications"

    # payload = {
    #     "app_id": f"{ONE_SIGNAL_CONFIG['app_id']}",
    #     "included_segments": ["Subscribed Users"],
    #     "contents": {"en": "English or Any Language Message", "es": "Spanish Message"},
    #     "name": "INTERNAL_CAMPAIGN_NAME",
    # }

    payload = dict(
        app_id=ONE_SIGNAL_CONFIG["app_id"],
        contents=dict(en="Test Push Notifications"),
        included_segments=["Subscribed Users"],
        content_available=True,
        small_icon="ic_notification_icon",
        data=dict(PushTitle="CUSTOM NOTIFICATION"),
    )
    headers = {
        "accept": "application/json",
        "Authorization": f"Basic {ONE_SIGNAL_CONFIG['api_key']}",
        "content-type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

    return jsonify(msg="success")

import requests

class Notifier:

    def __init__(self):
        self.activated = None
        self.baseurl = 'https://ntfy.sh'
        self.suscription = 'way2wb_notifier_fantaexotic'

    def set_activated(self) -> None:
        self.activated = True

    def set_deactivated(self) -> None:
        self.activated = False
    
    def send_notification(self, message: str) -> None:
        """sends notification via ntfy.sh service"""
        if not self.activated:
            return
        url = f'{self.baseurl}/{self.suscription}'
        headers = {
            'Priority': '5',  # highest priority
            'Tags': 'alert',
        }
        try:
            response = requests.post(url, data=message.encode('utf-8'), headers=headers)
            if response.status_code != 200:
                print(f'Notification could not be sent. Status code: {response.status_code}')
        except Exception as e:
            print(f'Error sending notification: {e}')

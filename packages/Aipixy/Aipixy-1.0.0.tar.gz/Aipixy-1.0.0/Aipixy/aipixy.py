import requests
import os

BASE_URL = 'https://api.aipixy.com'

class Aipixy:

    def __init__(self, api_key):
        self.api_key = api_key

    def retrieve_all_bots(self):
        url = f"{BASE_URL}/v1/bot"

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            response = requests.get(url, headers=headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def retrieve_all_videos(self):
        url = f"{BASE_URL}/v1/video"

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            response = requests.get(url, headers=headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def retrieve_bot(self, uid):
        url = f"{BASE_URL}/v1/bot/{uid}"

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            response = requests.get(url, headers=headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def retrieve_video(self, uid):
        url = f"{BASE_URL}/v1/video/{uid}"

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            response = requests.get(url, headers=headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def account(self):
        url = f"{BASE_URL}/v1/account"

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            response = requests.get(url, headers=headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None


    def delete_bot(self, uid):
        url = f"{BASE_URL}/v1/bot/{uid}"

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            response = requests.delete(url, headers=headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def delete_video(self, uid):
        url = f"{BASE_URL}/v1/video/{uid}"

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            response = requests.delete(url, headers=headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def create_video(self, create_video=False, webhook=None, clips=None):

        url = f"{BASE_URL}/v1/create_video"

        if not isinstance(clips, list) or clips is None:
            raise ValueError("The 'clips' parameter must be a non-empty list.")

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "process_done_webhook": webhook,
            "create_video": create_video,
            "clips": clips
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
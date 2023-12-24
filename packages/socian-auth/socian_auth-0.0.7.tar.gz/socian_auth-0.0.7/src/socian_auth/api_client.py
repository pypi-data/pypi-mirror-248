# socian_auth/api_client.py
import requests
import json
from socian_auth.models import IntentObject, UserData, TokenData

BASE_URL = "https://auth.socian.ai:8082/api"


class SocianAuthApiClient:
    def __init__(self, client_id, client_secret, ssh_public_key):
        self.client_id = client_id
        self.client_secret = client_secret
        self.ssh_public_key = ssh_public_key
        self.base_url = BASE_URL

    def get_intent(self, purpose, redirect_uri):
        endpoint = f"{self.base_url}/service-intents/"
        payload = json.dumps({
            "purpose": purpose,
            "redirect_uri": redirect_uri,
            "config": {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "ssh_public_key": self.ssh_public_key
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", endpoint, headers=headers, data=payload)
        try:
            response_json = response.json()
            intent_object_dict = response_json.get('intent_object', {})
            if intent_object_dict:
                return IntentObject(**intent_object_dict)
            else:
                raise Exception(f"{response.status_code}, {response.text}")
        except Exception as e:
            raise Exception(f"Error: {e}")

    def check_user_exists(self, intent_id, email):
        endpoint = f"{self.base_url}/user-exists/"
        payload = json.dumps({
            "intent_id": intent_id,
            "email": email,
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", endpoint, headers=headers, data=payload)
        try:
            response_json = response.json()
            return response_json["data"]
        except Exception as e:
            raise Exception(f"{response.status_code}, {response.text}")

    def user_signup(self, intent_id, name, email, password):
        endpoint = f"{self.base_url}/auth/signUp/"
        payload = json.dumps({
            "name": name,
            "email": email,
            "password": password,
        })
        headers = {
            'Content-Type': 'application/json',
            'Intent-Id': intent_id
        }
        response = requests.request("POST", endpoint, headers=headers, data=payload)
        try:
            response_json = response.json()
            user_object_dict = response_json.get('data', {})
            if user_object_dict:
                return UserData(**user_object_dict)
            else:
                raise Exception(f"{response.status_code}, {response.text}")
        except Exception as e:
            raise Exception(f"Error: {e}")

    def user_signin(self, email, password):
        endpoint = f"{self.base_url}/auth/signIn/"
        payload = json.dumps({
            "email": email,
            "password": password,
        })
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.request("POST", endpoint, headers=headers, data=payload)
        try:
            response_json = response.json()
            user_object_dict = response_json.get('data', {})
            if user_object_dict:
                return TokenData(**user_object_dict)
            else:
                raise Exception(f"{response.status_code}, {response.text}")
        except Exception as e:
            raise Exception(f"Error: {e}")

    def user_info(self, access_token):
        endpoint = f"{self.base_url}/auth/me/"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {access_token}"
        }
        response = requests.request("GET", endpoint, headers=headers)
        try:
            response_json = response.json()
            user_object_dict = response_json.get('data', {})
            if user_object_dict:
                return UserData(**user_object_dict)
            else:
                raise Exception(f"{response.status_code}, {response.text}")
        except Exception as e:
            raise Exception(f"Error: {e}")


# if __name__ == "__main__":
#     client = SocianAuthApiClient(
#         client_id="5c9403cabfc12d8b2ae3a6b57b831be45624bb56",
#         client_secret="JgZ4985smrY3aHk6ZgfFQPVEEcVfDKMk889xjzHur4Y=",
#         ssh_public_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDHOk0b7QfHUwkb8ckhZPdgZeYGByd9k3K26J85XJ/T6kdkazC57AIhFZ2CyC+AczzJrDW72NbnRnQGo400nXxDd0acEUuLAWBysklGbyS6cFDsNhJgVLvBMIOg5S5Nc9eVziHV3kYg32G6rcm0EeovgvUsqR39J3mhfHW4ZSI+LGKExtcrK6v5M9JWQCe3ycrOGg/PNv8OTONF+jKiLDf/N9lC8CKgqn0RqMVGELxHTw9fGYDhjpUYtmTU3oHtd/Z4YJOajqxX29R1MPNqApoN6Q6bgm7LX9HC/IGHT68sr7xBFH4iCGzvfVtOAtfUGeWF5fQDult2WUNjP/F+Ipdp"
#     )
#     intent_obj = client.get_intent("auth.signIn", "http://localhost:3000/auth/callback")
#     print('result', intent_obj)
#
#     email = "tamzid@socian.ai"
#
#     isUserExist = client.check_user_exists(intent_id=intent_obj.intent_id, email=email)
#     print('result', isUserExist)
#     if isUserExist:
#         loginData = client.user_signin(email=email,password="qwertyui321")
#         print('result', loginData)
#     else:
#         user_info = client.user_signup(intent_id=intent_obj.intent_id,name="tamzid",email=email,password="qwertyui321")
#         print('result', user_info)
#         loginData = client.user_signin(email=email,password="qwertyui321")
#         print('result', loginData)
#

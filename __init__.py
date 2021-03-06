import requests
from requests.auth import HTTPBasicAuth
#from pprint import pp

class VartaStoragePortalClient():
    api_url = 'https://www.varta-storage-portal.com/ws/app/'

    def __init__(self, locale="de-DE"):
        self.locale = locale
        self.auth_token = None
        self.current_user = None

    def login(self, username, password):
        params = dict()
        params["func"] = "login"

        headers = dict()
        headers["Accept-Language"] = self.locale
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["API-Version"] = "1"

        auth =  HTTPBasicAuth(username, password)
        res = requests.post(self.api_url, params=params, headers=headers, auth=auth)
        if res.status_code == 200:
            self.auth_token = res.headers.get('Auth-Token')
            self.current_user = res.json()
            return self.current_user
        else:
            self.auth_token = None
            self.current_user = None
            raise Exception("Login failed", res.status_code, res.text)

    # Available Service Names:
    # service (payload: {serial: storageSerialNumber})
    # status (payload: {})
    # gespeicherteEnergie (payload: {modus: ["tag", "monat", "jahr", "gesamt"],datum: date.isoformat...})
    # autarkie (payload: {modus: ["tag", "monat", "jahr", "gesamt"],datum: date.isoformat...})
    # betriebsdaten (payload: {modus: ["tag", "monat", "jahr", "gesamt"],datum: date.isoformat...})
    # kontakt (payload: {Betreff: , Nachricht: ....})
    def _callService(self, service_name, payload):
        params = dict()
        params["func"] = service_name

        headers = dict()
        headers["Accept-Language"] = self.locale
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["API-Version"] = "1"
        headers["Auth-Token"] = self.auth_token

        res = requests.post(self.api_url, params=params, headers=headers, json=payload)
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception("Service call failed", res.status_code, res.text)

if __name__ == "__main__":
    import os

    username = os.environ.get("VARTA_USER")
    password = os.environ.get("VARTA_PASSWORD")

    if username is None or password is None:
        raise ValueError("Invalid Credentials. Please supply your credentials for VartaStoragePortal through the env-variables 'VARTA_USER' and 'VARTA_PASSWORD'")

    client = VartaStoragePortalClient()
    login_result = client.login(username=username, password=password)
    print(client._callService('status', {"serial": username}))

import os
import json
from pickle import FALSE, NONE
import requests

from typing import Dict


class APIClient:
    r"""
    A wrapper of python reqeusts module
    It is to handle all GET,POST,PUT,DELETE requests
    """

    def __init__(self, backend_url: str, token: str):
        self.backend_url = backend_url
        self.auth_token = self.AUTH_TOKEN_REQ(token=token)
        self.header = {
            "X-Alectio-Flavor": "PRO",
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }

    def GET_REQUEST(self, end_point: str, payload: dict = {}):
        url = self.backend_url + end_point

        payload = json.dumps(payload)

        response = requests.request("GET", url, headers=self.header, data=payload)

        if response.status_code not in [200, 201, 202, 203, 204, 2005, 206]:
            return True, None
        else:
            return False, response.json()

    def POST_REQUEST(
        self, end_point: str, payload: dict = {}, auth: dict = {}, headers: dict = {}
    ):
        url = self.backend_url + end_point
        payload = json.dumps(payload)
        response = requests.request("POST", url, headers=self.header, data=payload)

        if response.status_code not in [200, 201, 202, 203, 204, 2005, 206]:
            return True, None
        else:
            return False, response.json()

    def AUTH_TOKEN_REQ(self, token):
        url = self.backend_url + f"/api/v2/python_client_auth/experiment_token/{token}"
        payload = {}
        headers = {"X-Alectio-Flavor": "PRO"}
        response = requests.request("GET", url, headers=headers, data=payload).json()
        return response["data"]["access_token"]
    

    def DOWNLOAD_FILE(self, to_path: str, filename: str ,url: str):
        url = self.backend_url + url    
        response = requests.get(url, headers=self.header ,stream=True)
        if response.status_code == 200:
            file_path = os.path.join(to_path, filename)

            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # Filter out keep-alive new chunks
                        f.write(chunk)

            print(f"✅  File downloaded successfully: {file_path}")
        else:
            print(f"Download failed with status code: {response.status_code}")


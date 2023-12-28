# Purpose: Integroh class
# Author: Marçal Junior
# Explanation: This class is responsible for the Integroh API requests and responses handling integroh connectors to integrate with services like keycloak and dropbox.
import json, requests
from .exceptions import ValidationError

DOC_URL = 'https://integroh.com/docs/integroh-connector-python'
REQUEST_METHODS = ['GET', 'POST', 'PUT', 'DELETE']
SERVICES = ['keycloak', 'dropbox']
NAME = 'integroh-sys'


class IntegrohConnector:
    def __init__(self):
        self.base_url = ''
        self.api_key = ''
        self.authorization = 'Bearer ' + self.api_key 
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': self.authorization
        }

    def validate_service(self, service):
        if service not in SERVICES:
            raise ValidationError(f'{NAME}: service invalid, you can found more information about this service in the documentation. {DOC_URL}')
        return service
    
    def validate_request_type(self, request_type):
        if request_type not in REQUEST_METHODS:
            raise ValidationError(f'{NAME}: request type invalid')
        return request_type

    def load_initfile(self):
        try:
            with open('integroh.ini', 'r') as f:
                file_data = f.read()
                print('file_data',file_data)
                data = json.loads(file_data)
                print(data)
                self.base_url = data['base_url']
                self.api_key = data['api_key']
                self.headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + self.api_key
                }
        except Exception as e:
            raise ValidationError(f"""
            {NAME}: configuration init file not found, you can found more information about this file in the documentation.
            {DOC_URL}""")
    
    def request_service(self, request_type, request_url, request_data):
        url = self.base_url + request_url
        self.validate_request_type(request_type)
        connection = requests.request(request_type, url, headers=self.headers, data=request_data)
        print(url, connection)
        return connection

    def connect(self, service, request_type, service_data):
        self.validate_service(service)
        self.load_initfile()
        try:
            return self.request_service(request_type, service, json.dumps(service_data) if service_data else None)
        except Exception as e:
            print(e)
        

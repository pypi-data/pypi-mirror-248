import requests

def get_app_settings():
    url = "https://assist.org/api/appsettings"
    
    if response.status_code == 200:
        return response
    else:
        return None

import requests


def get_lat_lon_opencage(address, api_key="ef6b72d9607e40e6a68d4a85b102fbba"):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={address}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if data['results']:
        location = data['results'][0]['geometry']
        return location['lat'], location['lng']
    return None, None

print(get_lat_lon_opencage("perinthalmanna, Malappuram"))
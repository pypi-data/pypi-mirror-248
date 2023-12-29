import requests


def get_denso_map_code_from_latlon(lat: float, lon: float) -> str:
    return f"https://www.google.com/maps/@{lat},{lon}"


def get_real_url(url: str):
    response = requests.get(url, allow_redirects=False)
    if response.status_code in [301, 302, 307, 308]:
        return response.headers['Location']
    else:
        return url

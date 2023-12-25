import base64
import hashlib
import hmac
import urllib.parse as urlparse

import requests

# Get signing secret from: https://developers.google.com/maps/documentation/streetview/digital-signature#sample-code-for-url-signing


def _sign_url(input_url, secret):
    """
    Sign a URL with a secret using HMAC SHA1.

    This function creates a signed URL that can be used with Google Maps services.
    It signs the path and query components of the URL.

    Args:
    input_url (str): The URL to be signed.
    secret (str): The URL-safe, base64-encoded secret key.

    Returns:
    str: The input URL with a signature parameter appended.
    """
    url = urlparse.urlparse(input_url)

    # We only need to sign the path+query part of the string
    url_to_sign = url.path + "?" + url.query

    # Decode the private key into its binary format
    # We need to decode the URL-encoded private key
    decoded_key = base64.urlsafe_b64decode(secret)

    # Create a signature using the private key and the URL-encoded
    # string using HMAC SHA1. This signature will be binary.
    signature = hmac.new(decoded_key, str.encode(url_to_sign), hashlib.sha1)

    # Encode the binary signature into base64 for use within a URL
    encoded_signature = base64.urlsafe_b64encode(signature.digest())

    original_url = url.scheme + "://" + url.netloc + url.path + "?" + url.query

    # Return signed URL
    return original_url + "&signature=" + encoded_signature.decode()


def _gms_static_map_signed_url(
    lat: str,
    lon: str,
    api_key: str,
    secret: str | None = None,
    size: int = 640,
    zoom: int = 16,
    maptype: str = "satellite",
    format: str = "jpg",
):
    """
    Generate a signed URL for Google Maps Static API.

    This function constructs a URL for fetching a static map image from Google Maps,
    and signs it if a secret key is provided.

    Args:
    lat (str): Latitude of the map's center.
    lon (str): Longitude of the map's center.
    api_key (str): Google Maps API key.
    secret (str, optional): Secret key for signing the URL.
    size (int, optional): Width and height of the map image in pixels. Default is 640.
    zoom (int, optional): Zoom level of the map. Default is 16.
    maptype (str, optional): Type of the map (e.g., "satellite", "roadmap").
    format (str, optional): Format of the map image (e.g., "jpg", "png").

    Returns:
    str: A URL to the static map image, signed if a secret is provided.
    """
    input_url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom={zoom}&size={size}x{size}&maptype={maptype}&format={format}&key={api_key}"
    if secret:
        return _sign_url(input_url, secret)
    else:
        return input_url


def _gms_static_map_request(signed_url: str):
    """
    Send a request to the Google Maps Static API.

    Fetches a static map image from Google Maps using a signed URL.

    Args:
    signed_url (str): The signed URL to fetch the static map.

    Returns:
    bytes: The content of the response, typically an image file.

    Raises:
    Exception: If the HTTP request fails.
    """
    response = requests.get(signed_url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


def gms_static_map(
    lat: str,
    lon: str,
    api_key: str,
    secret: str | None = None,
    size: int = 640,
    zoom: int = 16,
    maptype: str = "satellite",
    format: str = "jpg",
):
    """
    Main function to obtain a static map from Google Maps Static API.

    Constructs and signs a URL, then fetches the static map image.

    Args:
    lat (str): Latitude of the map's center.
    lon (str): Longitude of the map's center.
    api_key (str): Google Maps API key.
    secret (str, optional): Secret key for signing the URL.
    size (int, optional): Width and height of the map image in pixels. Default is 640.
    zoom (int, optional): Zoom level of the map. Default is 16.
    maptype (str, optional): Type of the map (e.g., "satellite", "roadmap").
    format (str, optional): Format of the map image (e.g., "jpg", "png").

    Returns:
    bytes: The content of the response, typically an image file.

    Example:
    gms_static_map(lat = 10.714728, lon = -73.998672, api_key=api_key, secret=secret)
    """
    signed_url = _gms_static_map_signed_url(
        lat=lat,
        lon=lon,
        api_key=api_key,
        secret=secret,
        size=size,
        zoom=zoom,
        maptype=maptype,
        format=format,
    )
    return _gms_static_map_request(signed_url)

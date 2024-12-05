import os
import pwd
import urllib.request
import json
import time
from sense_hat import SenseHat

sense = SenseHat()

def get_ip_geolocation():
    """
    sends a HTTP GET request to a free 3rd party API which returns geolocation data based on this device's IP address
    """

    # create request object
    req = urllib.request.Request("https://ipapi.co/json", method="GET")

    try:
        # send request and handle response
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode("utf-8")
            json_data = json.loads(response_data)
            return json_data

    except urllib.error.HTTPError as e:
        print(f"HTTP error occurred: {e.code} {e.reason}")
        return None

    except urllib.error.URLError as e:
        print(f"URL error occurred: {e.reason}")
        return None

# collecting geolocation data so it's readily available
geolocation = get_ip_geolocation()
latitude = geolocation["latitude"]
longitude = geolocation["longitude"]

# fetches current user from os
def get_user_identifier():
    return pwd.getpwuid(os.getuid())[0]

# gets humidity reading from sensor
def get_humidity():
    return sense.get_humidity()

# gets pressure reading from sensor
def get_pressure():
    return sense.get_pressure()

# gets temperature reading from sensor
def get_temperature():
    return sense.get_temperature()

def send_post_request(endpoint, payload):
    """
    sends a HTTP POST request with a JSON payload

    :param endpoint: the API endpoint (string)
    :param payload: the JSON payload (dict)
    :return: the response data as a string and the status code as an integer
    """

    headers = {"Content-Type": "application/json"}

    # url of backend API
    base_url = "https://iot-raspberrypi-backend-12a94ca200cf.herokuapp.com"

    # convert payload to JSON and encode to bytes
    payload_json = json.dumps(payload).encode("utf-8")

    # create request object
    req = urllib.request.Request(base_url + endpoint, data=payload_json, headers=headers, method="POST")

    try:
        # send request and handle response
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode("utf-8")
            return response_data, response.status

    except urllib.error.HTTPError as e:
        print(f"HTTP error occurred: {e.code} {e.reason}")
        return None, e.code

    except urllib.error.URLError as e:
        print(f"URL error occurred: {e.reason}")
        return None, None

# sends HTTP POST request containing the current humidity as the payload
def submit_humidity():
    payload = {
        "deviceId": get_user_identifier(),
        "value": str(get_humidity()),
        "latitude": str(latitude),
        "longitude": str(longitude)
    }

    response_data, status_code = send_post_request("/humidities", payload)

    if response_data is not None:
        print("Status Code:", status_code)
        print("Response Data:", response_data)
    else:
        print("Request failed.")

# sends HTTP POST request containing the current pressure as the payload
def submit_pressure():
    payload = {
        "deviceId": get_user_identifier(),
        "value": str(get_pressure()),
        "latitude": str(latitude),
        "longitude": str(longitude)
    }

    response_data, status_code = send_post_request("/pressures", payload)

    if response_data is not None:
        print("Status Code:", status_code)
        print("Response Data:", response_data)
    else:
        print("Request failed.")

# sends HTTP POST request containing the current temperature as the payload
def submit_temperature():
    payload = {
        "deviceId": get_user_identifier(),
        "value": str(get_temperature()),
        "latitude": str(latitude),
        "longitude": str(longitude)
    }

    response_data, status_code = send_post_request("/temperatures", payload)

    if response_data is not None:
        print("Status Code:", status_code)
        print("Response Data:", response_data)
    else:
        print("Request failed.")

# main loop to run all functions every 5 seconds (CTRL+C will stop the program)
try:
    while True:
        submit_humidity()
        submit_pressure()
        submit_temperature()

        time.sleep(5)
except KeyboardInterrupt:
    print("Program stopped by user.")
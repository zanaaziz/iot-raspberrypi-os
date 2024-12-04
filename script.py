import os
import pwd
import urllib.request
import json
import time

import random # temp: for testing




backend_api_url = "https://iot-raspberrypi-backend-12a94ca200cf.herokuapp.com"


# fetches current user from os
def get_user_identifier():
    return pwd.getpwuid(os.getuid())[0]

# fetches humidity from sensor
def getHumidity():
    return random.randint(0, 1000) # temp: for testing

# fetches temperature from sensor
def getTremperature():
    return random.randint(0, 1000) # temp: for testing

# fetches pressure from sensor
def getPressure():
    return random.randint(0, 1000) # temp: for testing






def send_post_request(endpoint, payload):
    """
    sends a HTTP POST request with a JSON payload

    :param endpoint: the API endpoint (string)
    :param payload: the JSON payload (dict)
    :return: the response data as a string and the status code as an integer
    """

    headers = {"Content-Type": "application/json"}

    # convert payload to JSON and encode to bytes
    payload_json = json.dumps(payload).encode("utf-8")

    # create request object
    req = urllib.request.Request(backend_api_url + endpoint, data=payload_json, headers=headers, method="POST")

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
def submitHumidity():
    payload = {
        "deviceId": get_user_identifier(),
        "value": str(getHumidity())
    }

    response_data, status_code = send_post_request("/humidities", payload)

    if response_data is not None:
        print("Status Code:", status_code)
        print("Response Data:", response_data)
    else:
        print("Request failed.")

# sends HTTP POST request containing the current pressure as the payload
def submitPressure():
    payload = {
        "deviceId": get_user_identifier(),
        "value": str(getPressure())
    }

    response_data, status_code = send_post_request("/pressures", payload)

    if response_data is not None:
        print("Status Code:", status_code)
        print("Response Data:", response_data)
    else:
        print("Request failed.")

# sends HTTP POST request containing the current temperature as the payload
def submitTemperature():
    payload = {
        "deviceId": get_user_identifier(),
        "value": str(getTremperature())
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
        submitHumidity()
        submitPressure()
        submitTemperature()

        time.sleep(5)
except KeyboardInterrupt:
    print("Program stopped by user.")
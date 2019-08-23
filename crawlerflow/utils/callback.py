import requests


def run_callback(callback):
    url = callback.get("url")
    method = callback.get("method", "get").lower()

    try:
        headers = callback.get("headers", {})
        if method == "get":
            req = requests.get(url, headers=headers)
            print("Response of the callback {}".format(req.status_code, req.content))
        elif method == "post":
            req = requests.post(url, headers=headers)
            print("Response of the callback {}".format(req.status_code, req.content))
    except Exception as e:
        print(e)
        print("Failed to ping the callback {}".format(url))

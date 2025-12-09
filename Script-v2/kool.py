from mitmproxy import http
import mitmproxy.http
import os

def request(flow: mitmproxy.http.HTTPFlow):
    url = flow.request.pretty_url
    print(f"[INFO] Intercepted request: {url}")

    user_folder = os.path.basename(os.path.expanduser("~"))
    base_path = os.path.join(
        os.path.expanduser("~"), "AppData", "Local", "DeadDOS", "Craftland Studio PC", "httptoolkit"
    )

    if "https://client.fe.garena.com/MajorLogin" in url:
        json_path = os.path.join(base_path, "MajorLogin.bin")
        print(f"[INFO] Serving MajorLogin.bin from {json_path}")
    elif "https://client.fe.garena.com" in url:
        json_path = os.path.join(base_path, "null.json")
        print(f"[INFO] Serving null.json from {json_path}")
    else:
        print(f"[INFO] No match for URL, passing through")
        return

    try:
        with open(json_path, "rb") as f:
            json_data = f.read()
        print(f"[INFO] Successfully read {json_path}")
        flow.response = http.Response.make(
            200,
            json_data,
            {"Content-Type": "application/json"}
        )
    except Exception as e:
        print(f"[ERROR] Error reading {json_path}: {str(e)}")
        flow.response = http.Response.make(
            500,
            f"Error reading file: {str(e)}",
            {"Content-Type": "text/plain"}
        )
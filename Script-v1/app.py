import os
import json
import subprocess
import time
import pygetwindow as gw
import pyautogui
from pathlib import Path
import sys

# Configuration
FOLDER_ICON_PATH = "folder_icon.png"  # Path to screenshot of folder icon
PROXY_PATH = r"C:\proxy"
RULES_FILE = "httptoolkit_rules.json"
SCREENSHOT_CONFIDENCE = 0.8  # Confidence level for image recognition (0-1)
CRAFTLAND_EXECUTABLE = r"C:\Program Files\Craftland Studio\Craftland Studio.exe"

def get_user_folder_name():
    """Get the user's folder name from their home directory."""
    home_path = os.path.expanduser("~")
    return os.path.basename(home_path)

def launch_craftland_studio():
    """Launch Craftland Studio PC."""
    try:
        process = subprocess.Popen(CRAFTLAND_EXECUTABLE, shell=True)
        print("Launched Craftland Studio")
        return process
    except Exception as e:
        print(f"Failed to launch Craftland Studio: {e}")
        return None

def close_craftland_studio():
    """Close Craftland Studio PC process."""
    try:
        # Use taskkill to forcefully terminate Craftland Studio
        subprocess.run('taskkill /IM "Craftland Studio.exe" /F', shell=True, check=False)
        print("Closed Craftland Studio")
        return True
    except Exception as e:
        print(f"Failed to close Craftland Studio: {e}")
        return False

def generate_httptoolkit_rules(user_folder):
    """Generate HTTP Toolkit rules with dynamic user folder."""
    rules = {
        "id": "root",
        "title": "HTTP Toolkit Rules",
        "isRoot": True,
        "items": [
            {
                "id": "d0629e63-fd60-45c3-a078-0c0498cea2e3",
                "type": "http",
                "activated": True,
                "matchers": [
                    {"method": 1, "type": "method", "uiType": "POST"},
                    {"host": "client.fe.garena.com", "type": "host"}
                ],
                "handler": {"status": 200, "type": "simple"},
                "completionChecker": {"type": "always"}
            },
            {
                "id": "fc1dac32-d564-4d98-95f5-7c9bb4a14ba2",
                "type": "http",
                "activated": True,
                "matchers": [
                    {"method": 1, "type": "method", "uiType": "POST"},
                    {"path": "https://client.fe.garena.com/MajorLogin", "type": "simple-path"}
                ],
                "handler": {
                    "status": 200,
                    "filePath": f"C:\\Users\\{user_folder}\\AppData\\Local\\DeadDOS\\Craftland Studio PC\\httptoolkit\\MajorLogin.bin",
                    "headers": {},
                    "type": "file"
                },
                "completionChecker": {"type": "always"}
            },
            {
                "id": "default-group",
                "title": "Default rules",
                "items": [
                    {
                        "id": "default-android-certificate",
                        "type": "http",
                        "activated": True,
                        "priority": 2,
                        "matchers": [
                            {"method": 0, "type": "method", "uiType": "GET"},
                            {"path": "http://android.httptoolkit.tech/config", "type": "simple-path"}
                        ],
                        "handler": {
                            "data": "{\"certificate\":\"-----BEGIN CERTIFICATE-----\\r\\nMIIDTzCCAjegAwIBAgIRCju6p0tQmUXZoqxR9JdYaTwwDQYJKoZIhvcNAQELBQAw\\r\\nQTEYMBYGA1UEAxMPSFRUUCBUb29sa2l0IENBMQswCQYDVQQGEwJYWDEYMBYGA1UE\\r\\nChMPSFRUUCBUb29sa2l0IENBMB4XDTI1MDEwNzEwMTcxMFoXDTI2MDEwODEwMTcx\\r\\nMFowQTEYMBYGA1UEAxMPSFRUUCBUb29sa2l0IENBMQswCQYDVQQGEwJYWDEYMBYG\\r\\nA1UEChMPSFRUUCBUb29sa2l0IENBMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB\\r\\nCgKCAQEAmnvfamzMlLPLQ8+e3rVdtkdcpKBbS7eUog5/3fiQSGXkpcn5KcAG2NC0\\r\\nOEzej8jZP84+vdaixeZU/jFOnCCKvc0vADCt4wr/RO2Bqyoa2VQlbQ0QL30ud2O9\\r\\nav2gT8tyAJ5QLWUEBwQp/Makj8Yr5OLT+rbgBaNBRNYYvPQB3tyuddZdFRBh0v5N\\r\\nPYPjswnOkraTXNHUge6dPELocawx4FfdfiAvOzaoUsc1o0NBYQ71rrl6c1FOVPGe\\r\\ntF3aeXAJaL0iIqUAsh2UBwdsr3HeEZznTsJ/xNjwcLY68vBBqi1CQ/vw4lWfunjS\\r\\ntpXacTTeuTgqh5sFNS4F0DVZwIU7WQIDAQABo0IwQDAPBgNVHRMBAf8EBTADAQH/\\r\\nMA4GA1UdDwEB/wQEAwIBxjAdBgNVHQ4EFgQU0uWf33o/D6Qv7TVa/a6rKgVRGTsw\\r\\nDQYJKoZIhvcNAQELBQADggEBABvRHBcDEthG09bS0yNspV/2+UgDT+m9o79Z676j\\r\\npW4pfZ3ueq+NRiVg6TRXW9kt+u7REmhAvS4My/vFC47jqkBbP/8CxJwgL9T2LEEe\\r\\nJ2buS3CJx43rL5tJAfwxB6d0ITAlQTAWHVrC8nCgD+knGwS0Ro71bbFz0G8Gf/20\\r\\nZ5pkXf9W+zGKubbpse2rpKz/OU+wbHzgMwOmKGhEiCJM3CaljME6QzAcBXlYsaUB\\r\\nkzhcIR+u6V25gnReqI/A7mpGAOLu6TxQ1awoQgwdZx4GIFyqBh8Krihad6zjOBwz\\r\\nSAZKEJKehUnxonnnUaSaTBba4mdxTfm1M+26Xjc9eLQYp24=\\r\\n-----END CERTIFICATE-----\\r\\n\"}",
                            "status": 200,
                            "headers": {"content-type": "application/json"},
                            "type": "simple"
                        },
                        "completionChecker": {"type": "always"}
                    },
                    {
                        "id": "default-amiusing",
                        "type": "http",
                        "activated": True,
                        "priority": 2,
                        "matchers": [
                            {"method": 0, "type": "method", "uiType": "GET"},
                            {"type": "regex-path", "regexSource": "^https?:\\/\\/amiusing\\.httptoolkit\\.tech\\/?$", "regexFlags": "", "uiType": "am-i-using"}
                        ],
                        "handler": {
                            "data": "<!DOCTYPE html>\n<html>\n<head>\n  <meta charset=\"UTF-8\">\n  <link rel='shortcut icon' type='image/x-icon' href='/favicon.ico' />\n  <script type=\"application/json\" id=\"amiusing\">\n    { \"amiusing\": true }\n  </script>\n  <title>\n    Are you using HTTP Toolkit? Yes!\n  </title>\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\">\n  <style>\n    html {\n      height: 100%;\n    }\n\n    body {\n      min-height: 100%;\n      box-sizing: border-box;\n      margin: 0;\n      padding: 8px;\n\n      background-color: #fafafa;\n      color: #1e2028;\n\n      font-family: \"DM Sans\", Arial, sans-serif;\n      letter-spacing: -0.5px;\n      line-height: 1.3;\n      display: flex;\n      flex-direction: column;\n      align-items: center;\n      justify-content: center;\n    }\n\n    .content {\n      max-width: 600px;\n    }\n\n    h1 {\n      font-size: 48px;\n      letter-spacing: -2px;\n    }\n\n    p {\n      font-size: 24px;\n    }\n\n    .logo {\n      display: block;\n      margin: 40px auto;\n      height: 200px;\n      width: 200px;\n    }\n\n    @media (prefers-color-scheme: dark) {\n      body {\n        background-color: #32343B;\n        color: #ffffff;\n      }\n    }\n\n    @media not (prefers-color-scheme: dark) {\n      body {\n        background-color: #fafafa;\n        color: #1e2028;\n      }\n    }\n  </style>\n</head>\n<body>\n  <div class=\"content\">\n    <h1>You're being intercepted by HTTP Toolkit</h1>\n    <p>\n      This response came from HTTP Toolkit, which is currently intercepting this connection.\n    </p>\n    <p>\n      All requests made by this browser will be recorded by HTTP Toolkit.\n      Take a look at the 'View' tab there now to see the request & response\n      that brought you this page, or start browsing elsewhere to collect more data.\n    </p>\n  </div>\n  <link href=\"https://fonts.cdnfonts.com/css/dm-sans\" rel=\"stylesheet\">\n</body>\n</html>",
                            "status": 200,
                            "headers": {"content-type": "text/html", "cache-control": "no-store", "httptoolkit-active": "true"},
                            "type": "simple"
                        },
                        "completionChecker": {"type": "always"}
                    },
                    {
                        "id": "default-certificate",
                        "type": "http",
                        "activated": True,
                        "priority": 2,
                        "matchers": [
                            {"method": 0, "type": "method", "uiType": "GET"},
                            {"path": "amiusing.httptoolkit.tech/certificate", "type": "simple-path"}
                        ],
                        "handler": {
                            "status": 200,
                            "filePath": f"C:\\Users\\{user_folder}\\AppData\\Local\\httptoolkit\\Config\\ca.pem",
                            "headers": {"content-type": "application/x-x509-ca-cert"},
                            "type": "file"
                        },
                        "completionChecker": {"type": "always"}
                    },
                    {
                        "id": "default-wildcard",
                        "type": "http",
                        "activated": True,
                        "matchers": [{"type": "wildcard", "uiType": "default-wildcard"}],
                        "handler": {"type": "passthrough"},
                        "completionChecker": {"type": "always"}
                    },
                    {
                        "id": "default-ws-wildcard",
                        "type": "websocket",
                        "activated": True,
                        "matchers": [{"type": "wildcard", "uiType": "default-ws-wildcard"}],
                        "handler": {"type": "ws-passthrough"},
                        "completionChecker": {"type": "always"}
                    }
                ]
            }
        ]
    }
    return rules

def generate_and_save_rules():
    """Generate HTTP Toolkit rules and save to C:\proxy."""
    user_folder = get_user_folder_name()
    print(f"User folder name: {user_folder}")

    # Generate rules
    rules = generate_httptoolkit_rules(user_folder)

    # Ensure C:\proxy exists
    proxy_dir = Path(PROXY_PATH)
    proxy_dir.mkdir(parents=True, exist_ok=True)

    # Write rules to C:\proxy\httptoolkit_rules.json
    rules_file_path = proxy_dir / RULES_FILE
    try:
        with open(rules_file_path, "w", encoding="utf-8") as f:
            json.dump(rules, f, indent=2)
        print(f"HTTP Toolkit rules written to {rules_file_path}")
        return True
    except Exception as e:
        print(f"Failed to write rules to {rules_file_path}: {e}")
        return False

def write_proxy_script(temp_script_path):
    """Write the MITM proxy script to a temporary file."""
    proxy_script_content = """
import mitmproxy.http
import os
import subprocess

class GarenaMonitor:
    def __init__(self):
        self.processed = False

    def response(self, flow: mitmproxy.http.HTTPFlow):
        target_url = "https://client.fe.garena.com/MajorLogin"

        if flow.request.url.startswith(target_url) and not self.processed:
            print(f"[INFO] Request to {target_url} detected.")

            with open("default.bin", "wb") as file:
                file.write(flow.response.content)
            print("[INFO] Response body saved to default.bin")

            # Automatically modify the hex pair
            modify_hex_pair("default.bin", os.path.join(os.path.expanduser("~"), "AppData", "Local", "DeadDOS", "Craftland Studio PC", "httptoolkit", "MajorLogin.bin"))

            # Switch proxy port to 8000
            set_proxy(8000)

            # Mark as processed and exit
            self.processed = True
            os._exit(0)  # Force mitmproxy to exit

addons = [GarenaMonitor()]

# In modify_hex_pair function
def modify_hex_pair(input_file, output_file):
    try:
        with open(input_file, 'rb') as file:
            data = bytearray(file.read())

        if len(data) < 21:
            print("Error: File is too small.")
            return

        data[20] = 0x00

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'wb') as file:
            file.write(data)

        print(f"Successfully modified {input_file} and saved as {output_file}.")
        
        # Delete default.bin after MajorLogin.bin is written
        try:
            os.remove(input_file)
            print(f"Deleted {input_file}")
        except OSError as e:
            print(f"Failed to delete {input_file}: {e}")

    except FileNotFoundError:
        print("Error: Input file not found.")

def set_proxy(port):
    print(f"[INFO] Setting proxy to 127.0.0.1:{port}")
    subprocess.run(f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f', shell=True)
    subprocess.run(f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyServer /t REG_SZ /d "127.0.0.1:{port}" /f', shell=True)
"""
    with open(temp_script_path, "w", encoding="utf-8") as f:
        f.write(proxy_script_content)

def run_mitm_proxy():
    """Run mitmproxy with the temporary script and wait for MajorLogin.bin."""
    user_folder = get_user_folder_name()
    downloads_path = Path.home() / "AppData" / "Local" / "DeadDOS" / "Craftland Studio PC" / "httptoolkit" / "MajorLogin.bin"
    temp_script_path = "temp_proxy_script.py"

    # Write the proxy script
    write_proxy_script(temp_script_path)

    # Set initial proxy to 8080
    set_proxy(8080)

    # Run mitmproxy
    try:
        print("[INFO] Starting mitmproxy...")
        subprocess.run(["mitmproxy", "-s", temp_script_path], check=False)
    except subprocess.CalledProcessError as e:
        print(f"Error running mitmproxy: {e}")
        return False
    finally:
        # Clean up temporary script
        if os.path.exists(temp_script_path):
            os.remove(temp_script_path)
            print(f"Removed temporary script {temp_script_path}")

    # Check if MajorLogin.bin was created
    if downloads_path.exists():
        print(f"[INFO] {downloads_path} created successfully")
        # Close Craftland Studio
        close_craftland_studio()
        return True
    else:
        print(f"[ERROR] {downloads_path} not found")
        return False

def set_proxy(port):
    """Set Windows proxy port."""
    print(f"[INFO] Setting proxy to 127.0.0.1:{port}")
    subprocess.run(f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f', shell=True)
    subprocess.run(f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyServer /t REG_SZ /d "127.0.0.1:{port}" /f', shell=True)

def launch_http_toolkit(user_folder):
    """Launch HTTP Toolkit."""
    HTTP_TOOLKIT_EXECUTABLE = f"C:\\Users\\{user_folder}\\AppData\\Local\\Programs\\httptoolkit\\HTTP Toolkit.exe"
    try:
        subprocess.Popen(HTTP_TOOLKIT_EXECUTABLE, shell=True)
        print("Launched HTTP Toolkit")
    except Exception as e:
        print(f"Failed to launch HTTP Toolkit: {e}")
        raise

def maximize_window(title_contains="HTTP Toolkit"):
    """Find and maximize the HTTP Toolkit window."""
    time.sleep(2)  # Wait for the window to appear
    for window in gw.getWindowsWithTitle(title_contains):
        if "HTTP Toolkit" in window.title:
            window.maximize()
            window.activate()
            print("Maximized HTTP Toolkit window")
            return True
    print("HTTP Toolkit window not found")
    return False

def simulate_ctrl_3():
    """Simulate Ctrl+3 to switch to Modify tab."""
    time.sleep(5)  # Ensure window is active
    pyautogui.hotkey("ctrl", "3")
    print("Simulated Ctrl+3 to switch to Modify tab")

def click_folder_icon():
    """Locate and click the folder icon using image recognition."""
    time.sleep(1)  # Wait for Modify tab to load
    try:
        location = pyautogui.locateCenterOnScreen(FOLDER_ICON_PATH, confidence=SCREENSHOT_CONFIDENCE)
        if location:
            pyautogui.click(location)
            print("Clicked folder icon")
            return True
        else:
            print("Folder icon not found on screen")
            return False
    except Exception as e:
        print(f"Error locating folder icon: {e}")
        return False

def open_file_in_explorer():
    """Interact with File Explorer to open httptoolkit_rules.json in C:\proxy."""
    time.sleep(1)  # Wait for File Explorer to open
    pyautogui.hotkey("ctrl", "l")  # Focus address bar
    time.sleep(0.5)
    pyautogui.write(PROXY_PATH)
    pyautogui.press("enter")
    time.sleep(0.5)
    pyautogui.write(RULES_FILE)
    pyautogui.press("enter")
    print(f"Opened {RULES_FILE} from {PROXY_PATH}")

def run_http_toolkit_automation():
    """Run the HTTP Toolkit automation steps."""
    user_folder = get_user_folder_name()

    # Verify proxy path and rules file exist
    proxy_dir = Path(PROXY_PATH)
    rules_file_path = proxy_dir / RULES_FILE
    if not proxy_dir.exists():
        print(f"Directory {PROXY_PATH} does not exist")
        return False
    if not rules_file_path.exists():
        print(f"File {rules_file_path} does not exist")
        return False
    if not os.path.exists(FOLDER_ICON_PATH):
        print(f"Folder icon screenshot {FOLDER_ICON_PATH} not found")
        return False

    # Step 1: Launch HTTP Toolkit
    launch_http_toolkit(user_folder)

    # Step 2: Maximize window
    if not maximize_window():
        return False

    # Step 3: Simulate Ctrl+3
    simulate_ctrl_3()

    # Step 4: Click folder icon
    if not click_folder_icon():
        return False

    # Step 5: Open file in File Explorer
    open_file_in_explorer()

    try:
        os.remove(rules_file_path)
        print(f"Deleted {rules_file_path}")
    except OSError as e:
        print(f"Failed to delete {rules_file_path}: {e}")

    # Step 6: Launch Craftland Studio again
    launch_craftland_studio()
    return True

def main():
    # Configure pyautogui
    pyautogui.FAILSAFE = True  # Move mouse to top-left to abort
    pyautogui.PAUSE = 0.5  # Pause between actions

    # Step 1: Launch Craftland Studio
    craftland_process = launch_craftland_studio()
    if not craftland_process:
        print("Continuing despite failure to launch Craftland Studio")

    # Step 2: Generate and save HTTP Toolkit rules
    if not generate_and_save_rules():
        print("Failed to generate or save rules")
        return

    # Step 3: Run MITM proxy and wait for MajorLogin.bin
    if not run_mitm_proxy():
        print("MITM proxy failed or MajorLogin.bin not created")
        return

    # Step 4: Run HTTP Toolkit automation
    if run_http_toolkit_automation():
        print("Automation completed successfully")
    else:
        print("HTTP Toolkit automation failed")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Script interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
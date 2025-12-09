import os
import subprocess
import time
from pathlib import Path
import sys
import logging
import socket

CRAFTLAND_EXECUTABLE = r"C:\Program Files\Craftland Studio\Craftland Studio.exe"
PROXY_PORT = 8080
SERVE_SCRIPT = "kool.py"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def get_user_folder_name():
    home_path = os.path.expanduser("~")
    return os.path.basename(home_path)

def create_null_json():
    null_json_path = os.path.join(
        os.path.expanduser("~"), "AppData", "Local", "DeadDOS", "Craftland Studio PC", "httptoolkit", "null.json"
    )
    null_json_content = ""
    with open(null_json_path, 'w', encoding='utf-8') as f:
        f.write(str(null_json_content))
    logging.info("Created null.json at %s", null_json_path)

def launch_craftland_studio(max_attempts=3, delay=2):
    for attempt in range(1, max_attempts + 1):
        try:
            subprocess.Popen(CRAFTLAND_EXECUTABLE, shell=True)
            logging.info("Launched Craftland Studio PC (attempt %d)", attempt)
            return True
        except Exception as e:
            logging.error("Failed to launch Craftland Studio PC (attempt %d): %s", attempt, e)
            if attempt < max_attempts:
                logging.info("Retrying in %d seconds...", delay)
                time.sleep(delay)
    logging.error("Failed to launch Craftland Studio PC after %d attempts. Your PC sucks!", max_attempts)
    return False

def close_craftland_studio():
    try:
        subprocess.run('taskkill /IM "Craftland Studio.exe" /F', shell=True, check=False)
        logging.info("Closed Craftland Studio PC")
        return True
    except Exception as e:
        logging.error("WTF! Failed to close Craftland Studio: %s", e)
        return False

def set_proxy(port):
    logging.info("Setting proxy to 127.0.0.1:%d", port)
    try:
        result_enable = subprocess.run(
            f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f',
            shell=True, capture_output=True, text=True
        )
        result_server = subprocess.run(
            f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyServer /t REG_SZ /d "127.0.0.1:{port}" /f',
            shell=True, capture_output=True, text=True
        )
        if result_enable.returncode == 0 and result_server.returncode == 0:
            logging.info("Proxy settings applied successfully!")
        else:
            logging.error("Nigga your PC sucks! It failed to set proxy: enable=%s, server=%s", result_enable.stderr, result_server.stderr)
    except Exception as e:
        logging.error("Gay porn is straighter than this shit. Error setting proxy: %s", e)

def write_proxy_script(temp_script_path, phase="capture"):
    user_folder = get_user_folder_name()
    major_login_path = os.path.join(
        os.path.expanduser("~"), "AppData", "Local", "DeadDOS", "Craftland Studio PC", "httptoolkit", "MajorLogin.bin"
    )
    null_json_path = os.path.join(
        os.path.expanduser("~"), "AppData", "Local", "DeadDOS", "Craftland Studio PC", "httptoolkit", "null.json"
    )
    major_login_path_escaped = major_login_path.replace("\\", "\\\\")
    null_json_path_escaped = null_json_path.replace("\\", "\\\\")

    if phase == "capture":
        proxy_script_content = f"""
import mitmproxy.http
import os

class GarenaMonitor:
    def __init__(self):
        self.processed = False

    def response(self, flow: mitmproxy.http.HTTPFlow):
        target_url = "https://client.fe.garena.com/MajorLogin"

        if flow.request.url.startswith(target_url) and not self.processed:
            print(f"[INFO] Request to {{target_url}} detected.")

            with open("default.bin", "wb") as file:
                file.write(flow.response.content)
            print("[INFO] Response body saved to default.bin")

            modify_hex_pair("default.bin", "{major_login_path_escaped}")

            self.processed = True
            os._exit(0)

addons = [GarenaMonitor()]

def modify_hex_pair(input_file, output_file):
    try:
        with open(input_file, 'rb') as file:
            data = bytearray(file.read())

        if len(data) < 21:
            print("Error: File is too small.")
            return

        for i in range(15, 25):
            if data[i] == 0x01:
                data[20] = 0x00

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'wb') as file:
            file.write(data)

        print(f"Successfully modified {{input_file}} and saved as {{output_file}}.")

        # Delete default.bin
        try:
            os.remove(input_file)
            print(f"Deleted {{input_file}}")
        except OSError as e:
            print(f"Failed to delete {{input_file}}: {{e}}")

    except FileNotFoundError:
        print("Error: Input file not found.")
"""
    else:
        proxy_script_content = f"""
from mitmproxy import http

def request(flow: http.HTTPFlow):
    url = flow.request.pretty_url
    print(f"[INFO] Intercepted request: {{url}}")

    if "client.fe.garena.com/MajorLogin" in url:
        json_path = "{major_login_path_escaped}"
        print(f"[INFO] Serving MajorLogin.bin from {{json_path}}")
    elif "client.fe.garena.com" in url:
        json_path = "{null_json_path_escaped}"
        print(f"[INFO] Serving null.json from {{json_path}}")
    else:
        print(f"[INFO] No match for URL, passing through")
        return

    try:
        with open(json_path, "rb") as f:
            json_data = f.read()
        print(f"[INFO] Successfully read {{json_path}}")
        flow.response = http.Response.make(
            200,
            json_data,
            {{"Content-Type": "application/json"}}
        )
    except Exception as e:
        print(f"[ERROR] Error reading {{json_path}}: {{str(e)}}")
        flow.response = http.Response.make(
            500,
            f"Error reading JSON file: {{str(e)}}",
            {{"Content-Type": "text/plain"}}
        )
"""
    with open(temp_script_path, "w", encoding="utf-8") as f:
        f.write(proxy_script_content)
    logging.info("Wrote proxy script to %s for %s phase", temp_script_path, phase)

def run_mitm_proxy(phase="capture"):
    downloads_path = Path.home() / "AppData" / "Local" / "DeadDOS" / "Craftland Studio PC" / "httptoolkit" / "MajorLogin.bin"
    temp_script_path = f"temp_proxy_script_{phase}.py"
    mitmproxy_process = None

    downloads_path.parent.mkdir(parents=True, exist_ok=True)
    logging.info("Ensured directory exists: %s", downloads_path.parent)

    write_proxy_script(temp_script_path, phase)

    set_proxy(PROXY_PORT)
    time.sleep(1)

    try:
        logging.info("Starting mitmproxy (%s phase)...", phase)
        if phase == "capture":
            subprocess.run(["mitmproxy", "-s", temp_script_path], timeout=60, check=False)
        else:
            mitmproxy_process = subprocess.Popen(["mitmproxy", "-s", temp_script_path])
            logging.info("mitmproxy started in background (PID: %d)", mitmproxy_process.pid)
            time.sleep(2)
            if mitmproxy_process.poll() is not None:
                logging.error("mitmproxy serve phase failed to start (PID: %d)", mitmproxy_process.pid)
                return False, None
            return True, mitmproxy_process
    except subprocess.CalledProcessError as e:
        logging.error("Error running mitmproxy (%s phase): %s", phase, e)
        return False, None
    except subprocess.TimeoutExpired:
        logging.error("mitmproxy (%s phase) timed out", phase)
        return False, None
    except Exception as e:
        logging.error("Unexpected error starting mitmproxy (%s phase): %s", phase, e)
        return False, None
    finally:
        if os.path.exists(temp_script_path):
            os.remove(temp_script_path)
            logging.info("Removed temporary script %s", temp_script_path)

    if phase == "capture":
        if downloads_path.exists():
            logging.info("%s created successfully", downloads_path)
            return True, None
        else:
            logging.error("%s not found", downloads_path)
            return False, None
    return True, None

def terminate_mitm_processes():
    """Terminates any running mitmproxy or mitmdump processes."""
    try:
        subprocess.run('taskkill /IM mitmproxy.exe /F', shell=True, check=False)
        subprocess.run('taskkill /IM mitmdump.exe /F', shell=True, check=False)
        logging.info("Terminated any running mitmproxy/mitmdump processes")
        time.sleep(1)
    except Exception as e:
        logging.error("Error terminating mitmproxy/mitmdump processes: %s", e)

def is_port_in_use(port):
    """Check if the specified port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def run_mitmdump():
    if not os.path.exists(SERVE_SCRIPT):
        logging.error("Serve script %s not found, aborting", SERVE_SCRIPT)
        return False

    if is_port_in_use(PROXY_PORT):
        logging.warning("Port %d is in use, terminating existing mitmproxy/mitmdump processes", PROXY_PORT)
        terminate_mitm_processes()
    
    try:
        logging.info("Starting mitmdump with %s...", SERVE_SCRIPT)
        mitmdump_process = subprocess.Popen(["mitmdump", "-s", SERVE_SCRIPT])
        logging.info("mitmdump started in background (PID: %d)", mitmdump_process.pid)
        time.sleep(2)
        if mitmdump_process.poll() is not None:
            logging.error("mitmdump failed to start (PID: %d)", mitmdump_process.pid)
            return False
        return True
    except Exception as e:
        logging.error("Error starting mitmdump: %s", e)
        return False

def main():
    mitmproxy_process = None
    try:
        logging.info("Starting script")
        if not launch_craftland_studio():
            logging.warning("Open Craftland Studio PC manually and log in to your account")

        logging.info("Starting capture phase")
        success, _ = run_mitm_proxy(phase="capture")
        if not success:
            logging.error("MITM proxy capture phase failed or MajorLogin.bin not created")
            return

        logging.info("Closing Craftland Studio PC")
        close_craftland_studio()

        create_null_json()

        logging.info("Terminating any existing mitmproxy processes before serve phase")
        terminate_mitm_processes()

        logging.info("Starting serve phase")
        success, mitmproxy_process = run_mitm_proxy(phase="serve")
        if not success:
            logging.error("MITM proxy serve phase failed!")
            return

        logging.info("Terminating any existing mitmproxy processes before mitmdump")
        terminate_mitm_processes()

        run_mitmdump()

        logging.info("Attempting to relaunch Craftland Studio PC")
        if launch_craftland_studio():
            logging.info("Automation completed successfully!")
        else:
            logging.error("Failed to relaunch Craftland Studio PC! Go and watch gay porn.")

    except KeyboardInterrupt:
        logging.info("nigga you interrupted the script!")
    except Exception as e:
        logging.error("An error occurred: %s", e)
    finally:
        if mitmproxy_process and mitmproxy_process.poll() is None:
            logging.info("Terminating mitmproxy process (PID: %d)", mitmproxy_process.pid)
            mitmproxy_process.terminate()
            try:
                mitmproxy_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logging.warning("mitmproxy process did not terminate gracefully, killing...")
                mitmproxy_process.kill()
        logging.info("Disabling Windows proxy")

if __name__ == "__main__":
    main()
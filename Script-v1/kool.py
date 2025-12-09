import os
import subprocess
import time
from pathlib import Path
import sys
import logging

# Configuration
CRAFTLAND_EXECUTABLE = r"C:\Program Files\Craftland Studio\Craftland Studio.exe"
PROXY_PORT = 8080

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def get_user_folder_name():
    """Get the user's folder name from their home directory."""
    home_path = os.path.expanduser("~")
    return os.path.basename(home_path)

def launch_craftland_studio(max_attempts=3, delay=2):
    """Launch Craftland Studio PC with retry logic."""
    for attempt in range(1, max_attempts + 1):
        try:
            subprocess.Popen(CRAFTLAND_EXECUTABLE, shell=True)
            logging.info("Launched Craftland Studio (attempt %d)", attempt)
            return True
        except Exception as e:
            logging.error("Failed to launch Craftland Studio (attempt %d): %s", attempt, e)
            if attempt < max_attempts:
                logging.info("Retrying in %d seconds...", delay)
                time.sleep(delay)
    logging.error("Failed to launch Craftland Studio after %d attempts", max_attempts)
    return False

def close_craftland_studio():
    """Close Craftland Studio PC process."""
    try:
        subprocess.run('taskkill /IM "Craftland Studio.exe" /F', shell=True, check=False)
        logging.info("Closed Craftland Studio")
        return True
    except Exception as e:
        logging.error("Failed to close Craftland Studio: %s", e)
        return False

def set_proxy(port):
    """Set Windows proxy port and verify."""
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
            logging.info("Proxy settings applied successfully")
        else:
            logging.error("Failed to set proxy: enable=%s, server=%s", result_enable.stderr, result_server.stderr)
    except Exception as e:
        logging.error("Error setting proxy: %s", e)

def write_proxy_script(temp_script_path, phase="capture"):
    """Write the MITM proxy script to a temporary file."""
    user_folder = get_user_folder_name()
    major_login_path = os.path.join(
        os.path.expanduser("~"), "AppData", "Local", "DeadDOS", "Craftland Studio PC", "httptoolkit", "MajorLogin.bin"
    )
    null_json_path = os.path.join(
        os.path.expanduser("~"), "AppData", "Local", "DeadDOS", "Craftland Studio PC", "httptoolkit", "null.json"
    )
    # Escape backslashes for Python string literal
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

            # Modify the hex pair
            modify_hex_pair("default.bin", "{major_login_path_escaped}")

            # Mark as processed and exit
            self.processed = True
            os._exit(0)  # Force mitmproxy to exit

addons = [GarenaMonitor()]

def modify_hex_pair(input_file, output_file):
    try:
        with open(input_file, 'rb') as file:
            data = bytearray(file.read())

        if len(data) < 21:
            print("Error: File is too small.")
            return

        data[20] = 0x00  # Change 21st byte to 00

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
    else:  # phase == "serve"
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
    """Run mitmproxy with the temporary script."""
    user_folder = get_user_folder_name()
    downloads_path = Path.home() / "AppData" / "Local" / "DeadDOS" / "Craftland Studio PC" / "httptoolkit" / "MajorLogin.bin"
    temp_script_path = f"temp_proxy_script_{phase}.py"
    mitmproxy_process = None

    # Ensure the MajorLogin.bin directory exists
    downloads_path.parent.mkdir(parents=True, exist_ok=True)
    logging.info("Ensured directory exists: %s", downloads_path.parent)

    # Write the proxy script
    write_proxy_script(temp_script_path, phase)

    # Set proxy port
    set_proxy(PROXY_PORT)
    time.sleep(1)  # Ensure proxy settings take effect

    # Run mitmproxy
    try:
        logging.info("Starting mitmproxy (%s phase)...", phase)
        if phase == "capture":
            # Run synchronously with timeout for capture phase
            subprocess.run(["mitmproxy", "-s", temp_script_path], timeout=60, check=False)
        else:
            # Run asynchronously for serve phase
            mitmproxy_process = subprocess.Popen(["mitmproxy", "-s", temp_script_path])
            logging.info("mitmproxy started in background (PID: %d)", mitmproxy_process.pid)
            time.sleep(2)  # Ensure mitmproxy is fully started
            # Check if process is alive
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
        # Clean up temporary script
        if os.path.exists(temp_script_path):
            os.remove(temp_script_path)
            logging.info("Removed temporary script %s", temp_script_path)

    # For capture phase, check if MajorLogin.bin was created
    if phase == "capture":
        if downloads_path.exists():
            logging.info("%s created successfully", downloads_path)
            return True, None
        else:
            logging.error("%s not found", downloads_path)
            return False, None
    return True, None

def main():
    mitmproxy_process = None
    try:
        # Step 1: Launch Craftland Studio
        logging.info("Starting script")
        if not launch_craftland_studio():
            logging.warning("Continuing despite failure to launch Craftland Studio")

        # Step 2: Run MITM proxy to capture MajorLogin.bin
        logging.info("Starting capture phase")
        success, _ = run_mitm_proxy(phase="capture")
        if not success:
            logging.error("MITM proxy capture phase failed or MajorLogin.bin not created")
            return

        # Step 3: Close Craftland Studio
        logging.info("Closing Craftland Studio")
        close_craftland_studio()

        # Step 4: Run MITM proxy to serve MajorLogin.bin and null.json
        logging.info("Starting serve phase")
        success, mitmproxy_process = run_mitm_proxy(phase="serve")
        if not success:
            logging.error("MITM proxy serve phase failed")
            return

        # Step 5: Relaunch Craftland Studio
        logging.info("Attempting to relaunch Craftland Studio")
        if launch_craftland_studio():
            logging.info("Automation completed successfully")
        else:
            logging.error("Failed to relaunch Craftland Studio")

    except KeyboardInterrupt:
        logging.info("Script interrupted by user")
    except Exception as e:
        logging.error("An error occurred: %s", e)
    finally:
        # Cleanup mitmproxy process if running
        if mitmproxy_process and mitmproxy_process.poll() is None:
            logging.info("Terminating mitmproxy process (PID: %d)", mitmproxy_process.pid)
            mitmproxy_process.terminate()
            try:
                mitmproxy_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logging.warning("mitmproxy process did not terminate gracefully, killing...")
                mitmproxy_process.kill()
        # Disable proxy
        logging.info("Disabling Windows proxy")

if __name__ == "__main__":
    main()
"""
This script sets up a Cloudflare tunnel to expose a local server to the internet and notifies a remote server with the
public URL of the tunnel. It handles downloading the `cloudflared` binary, starting the tunnel, and sending updates to a
specified server URL.

This script is Linux only and requires Python 3.x to run.
"""

# Imports
import subprocess
import platform
import requests
import time
import os
import shutil
import json

# Constants
CLOUDFLARED_PATH = "./cloudflared"
LOGFILE = "cloudflared.log"


def load_config():
    with open("config.json", "r") as f:
        cfg = json.load(f)
    return cfg


def get_config_value(key):
    cfg = load_config()
    return cfg.get(key)


# Config Variables
REMOTE_SERVER = get_config_value("remote_server")
LOCAL_SERVER = get_config_value("local_server")


def detect_architecture():
    arch = platform.machine()
    if arch in ["armv7l", "armhf"]:
        return "cloudflared-linux-arm"
    elif arch in ["aarch64", "arm64"]:
        return "cloudflared-linux-arm64"
    elif arch in ["x86_64"]:
        return "cloudflared-linux-amd64"
    elif arch in ["i386", "i686"]:
        return "cloudflared-linux-386"
    else:
        raise Exception(f"Unsupported architecture: {arch}")


def download_cloudflared():
    if os.path.exists(CLOUDFLARED_PATH):
        print("cloudflared already exists.")
        return

    arch_file = detect_architecture()
    url = f"https://github.com/cloudflare/cloudflared/releases/latest/download/{arch_file}"
    print(f"Downloading {arch_file} from {url} ...")

    response = requests.get(url, stream=True)
    with open(CLOUDFLARED_PATH, "wb") as f:
        shutil.copyfileobj(response.raw, f)

    os.chmod(CLOUDFLARED_PATH, 0o755)
    print("cloudflared downloaded and made executable.")


def start_tunnel():
    print("Starting tunnel...")
    process = subprocess.Popen(
        [CLOUDFLARED_PATH, "tunnel", "--url", LOCAL_SERVER],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )

    tunnel_url = None

    with open(LOGFILE, "w") as log_file:
        for line in process.stdout:
            print("LOG:", line.strip())
            log_file.write(line)

            if "trycloudflare.com" in line and not tunnel_url:
                tunnel_url = extract_url(line)
                if tunnel_url:
                    print(f"🌐 Public URL: {tunnel_url}")
                    notify_server(tunnel_url)

    print("Tunnel process exited.")
    return_code = process.wait()
    return return_code


def extract_url(text):
    import re
    match = re.search(r"https://\S*trycloudflare.com", text)
    return match.group(0) if match else None


def notify_server(url):
    try:
        print(f"Sending tunnel URL to server: {url}")
        response = requests.post(REMOTE_SERVER, json={"url": url}, timeout=5)
        print(f"URL sent successfully. Response: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Failed to send URL: {e}")


def main():
    download_cloudflared()

    while True:
        try:
            exit_code = start_tunnel()
            print(f"Restarting tunnel in 5 seconds (code {exit_code})...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("Exiting on user interrupt.")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()

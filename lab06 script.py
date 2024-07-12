import requests
import hashlib
import os
import subprocess

def get_expected_sha256():
    url = "https://get.videolan.org/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe.sha256"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.splitlines()[0].split()[0]
    else:
        return None

def download_installer():
    url = "https://get.videolan.org/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        return response.content
    else:
        return None

def installer_ok(installer_data, expected_sha256):
    installer_hash = hashlib.sha256(installer_data).hexdigest()
    return installer_hash == expected_sha256

def save_installer(installer_data):
    temp_folder = os.getenv('TEMP')
    installer_path = os.path.join(temp_folder, "vlc-3.0.17.4-win64.exe")
    with open(installer_path, "wb") as f:
        f.write(installer_data)
    return installer_path

def run_installer_silently(installer_path):
    subprocess.run([installer_path, "/L=1033", "/S"], shell=True)

def delete_installer_file(installer_path):
    os.remove(installer_path)

def main():
    expected_sha256 = get_expected_sha256()
    installer_data = download_installer()
    if installer_data is not None:
        if installer_ok(installer_data, expected_sha256):
            installer_path = save_installer(installer_data)
            run_installer_silently(installer_path)
            delete_installer_file(installer_path)
        else:
            print("Installer integrity verification failed")
    else:
        print("Failed to download VLC installer")

if __name__ == "__main__":
    main()
import os
import subprocess
import json

# Ruta del archivo JSON
user_windows = os.environ["USERNAME"]
config_directory = f"C://Users//{user_windows}//Apple"
config_file = f"{config_directory}//config.json"

def create_config(user, password, route):
    if not os.path.exists(config_directory):
        os.makedirs(config_directory)
    config = {
        "user": user,
        "password": password,
        "route": route
    }
    with open(config_file, 'w') as json_file:
        json.dump(config, json_file, indent=4)
    # print(f"Configuración guardada en {config_file}")

def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as json_file:
            config = json.load(json_file)
        return config
    return None

def run_command(command):
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return result.stdout
    except subprocess.CalledProcessError as e:
        # print(f"An error occurred: {e}")
        return None

def authenticate(config, user, password):
    login_command = [config['route'], "auth", "login", "-e", user, "-p", password, "--non-interactive", "--keychain-passphrase", '0000']
    output = run_command(login_command)

def extract_value(output, key):
    key_str = f'"{key}":"'
    start_idx = output.find(key_str) + len(key_str)
    end_idx = output.find('"', start_idx)
    return output[start_idx:end_idx]

def search_app(config, term, limit=1):
    search_command = [config['route'], "search", term, "--limit", str(limit), "--non-interactive", "--keychain-passphrase", '0000']
    output = run_command(search_command)
    if output:
        bundle_id = extract_value(output, "bundleID")
        name = extract_value(output, "name")
        version = extract_value(output, "version")
        return bundle_id, name, version
    return None, None, None

def download_app(config, bundle_id, name, version, progress_callback=None):
    if bundle_id and name and version:
        download_command = [config['route'], "download", "-b", bundle_id, "--output", f"{name} v{version}.ipa", "--non-interactive", "--keychain-passphrase", '0000']
        process = subprocess.Popen(download_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)

        for line in process.stdout:
            decoded_line = line.decode('utf-8').strip()
            # print(decoded_line)
            if "Downloading" in decoded_line:
                percentage = float(decoded_line.split('%')[0].split()[-1]) / 100.0
                if progress_callback:
                    progress_callback(percentage)
        
        process.stdout.close()
        process.wait()
        
        if process.returncode == 0:
            # print(f"Download of {name} v{version} completed successfully.")
            if progress_callback:
                progress_callback(1.0)
        else:
            # print(f"Download of {name} v{version} failed.")
            if progress_callback:
                progress_callback(0.0)
    # else:
    #     print("Could not extract all values.")

if __name__ == "__main__":
    config = load_config()

    if not config:
        route = './assets/ipatool.exe'
        # user = input('Introduce el usuario: ')
        # password = input('Introduce la contraseña: ')
        # create_config(user, password, route)
        config = load_config()
    else:
        user = config.get('user')
        password = config.get('password')

    authenticate(config, user, password)
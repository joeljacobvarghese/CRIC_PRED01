import os
import requests
import zipfile
from urllib.parse import urljoin
import shutil
import subprocess

# Define paths and URLs using os.path for compatibility
base_dir = os.getcwd()  # Docker-friendly base directory
zip_path = os.path.join(base_dir, 'odis_json.zip')
extract_path = os.path.join(base_dir, 'extracted_odis')
dataset_dir = os.path.join(base_dir, 'ODI_DATASET')
buffer_file_path = os.path.join(base_dir, 'buffer.txt')
odi_csv_path = os.path.join(dataset_dir, 'odi.csv')
odi_csv_backup_path = os.path.join(dataset_dir, 'odi_backup.csv')

base_url = 'https://cricsheet.org'
file_path = '/downloads/odis_json.zip'
full_url = urljoin(base_url, file_path)


model_training_script_path = os.path.join(base_dir, 'model_training.py')
api_server_script_path = os.path.join(base_dir, 'api_server.py')
cleaning_script_path = os.path.join(base_dir, 'data_cleaning.py')


api_server_module = 'api_server'
api_app_object = 'app' 

# Ensure dataset and extracted directories exist
os.makedirs(dataset_dir, exist_ok=True)
os.makedirs(extract_path, exist_ok=True)

def run_model_training_script(script_path):
    try:
        subprocess.run(['python3', script_path], check=True)
        print('Model training script executed successfully.')
    except subprocess.CalledProcessError as e:
        print(f"Model training script failed to execute. Error: {e}")

def run_cleaning_script(script_path):
    try:
        # Use 'python3' instead of 'python', adjust according to your Docker container's environment
        subprocess.run(['python3', script_path], check=True)
        print('Cleaning script executed successfully.')
        # If successful, remove the backup if it exists
        if os.path.exists(odi_csv_backup_path):
            os.remove(odi_csv_backup_path)
    except subprocess.CalledProcessError as e:
        print(f"Cleaning script failed to execute. Error: {e}")
        # On failure, restore the backup if necessary
        if not os.path.exists(odi_csv_path) and os.path.exists(odi_csv_backup_path):
            shutil.move(odi_csv_backup_path, odi_csv_path)


def restart_fastapi_server():
    try:
        
        subprocess.run(['pkill', '-f', 'uvicorn'])
        print('FastAPI server stop attempt made.')  
        
        # Start the server again
        subprocess.run(['uvicorn', f'{api_server_module}:{api_app_object}', '--host', '0.0.0.0', '--port', '8000'], check=True)
        print('FastAPI server restarted successfully.')
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart FastAPI server. Error: {e}")



def cleanup():
    """Cleanup temporary files and directories."""
    if os.path.exists(zip_path):
        os.remove(zip_path)
    if os.path.exists(buffer_file_path):
        os.remove(buffer_file_path)
    if os.path.exists(extract_path):
        shutil.rmtree(extract_path, ignore_errors=True)
    print("Cleanup executed successfully.")

def download_file(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f'File downloaded successfully and saved as {save_path}')
    except requests.RequestException as e:
        print(f"Failed to download the file. Error: {e}")
        return False
    return True

def extract_zip(zip_path, extract_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        print(f"File extracted successfully to {extract_path}")
    except zipfile.BadZipFile as e:
        print(f"Error extracting the zip file. Error: {e}")
        return False
    return True

def update_buffer(new_files, buffer_path):
    try:
        if new_files:
            with open(buffer_path, 'a') as buffer_file:
                for file_name in new_files:
                    buffer_file.write(file_name + '\n')
            print(f"Appended names of {len(new_files)} new files to {buffer_path}")
    except Exception as e:
        print(f"Failed to update buffer file. Error: {e}")

def move_new_files_to_dataset(new_files, extract_path, dataset_dir):
    for file_name in new_files:
        shutil.move(os.path.join(extract_path, file_name), os.path.join(dataset_dir, file_name))
    print(f'Moved {len(new_files)} new files to the dataset directory.')


try:
    if download_file(full_url, zip_path) and extract_zip(zip_path, extract_path):
        extracted_files = os.listdir(extract_path)
        existing_files = os.listdir(dataset_dir)
        new_files = set(extracted_files) - set(existing_files)
        
        if len(new_files) >= 10:
            update_buffer(new_files, buffer_file_path)
            move_new_files_to_dataset(new_files, extract_path, dataset_dir)
            if os.path.exists(odi_csv_path):
                shutil.move(odi_csv_path, odi_csv_backup_path)
            cleanup()
            run_cleaning_script(cleaning_script_path)
            run_model_training_script(model_training_script_path)
            restart_fastapi_server()
            
        else:
            print(f"Only found {len(new_files)} new files, not enough to retrain the model.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    cleanup()


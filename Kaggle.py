import os
import time
import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import subprocess

# Step 1: Automate the download from Kaggle
def download_kaggle_data(kaggle_url, download_dir = r"D:\\wwwch\\Documents\\Kaggle"):
    # Set up Chrome options for Selenium
    chrome_options = Options()
    prefs = {"download.default_directory": download_dir}
    chrome_options.add_experimental_option("prefs", prefs)

    # Launch the browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Navigate to the Kaggle competition URL
        driver.get(kaggle_url)

        # Wait until the "Download All" button is clickable
        wait = WebDriverWait(driver, 30)
        download_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Download All')]"))
        )
        
        # Click the "Download All" button
        download_button.click()
        print("Download initiated...")

        # Wait for the download to complete
        time.sleep(30)  # Adjust the sleep time as per your internet speed
    finally:
        driver.quit()

# Step 2: Extract the ZIP file into a folder
def extract_zip_file(download_dir , folder_name):
    zip_path = os.path.join(download_dir, f"{folder_name}.zip")
    extract_dir = os.path.join(download_dir, folder_name)

    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"{zip_path} not found!")

    # Create a folder for extraction
    os.makedirs(extract_dir, exist_ok=True)

    # Extract the ZIP file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    print(f"Files extracted to {extract_dir}")

# Step 3: Create a virtual environment
def create_virtual_environment(folder_path):
    venv_path = os.path.join(folder_path, "venv")
    subprocess.run(["python", "-m", "venv", venv_path], check=True)
    print(f"Virtual environment created at {venv_path}")

# Step 4: Launch VS Code
def launch_vs_code(folder_path):
    subprocess.run(["code", "."], cwd=folder_path, check=True)
    print("VS Code launched successfully!")

# step 5: verify download
def verify_download(download_dir, filename):
    file_path = os.path.join(download_dir, filename)
    max_wait = 60  # maximum wait time in seconds
    wait_time = 0
    while wait_time < max_wait:
        if os.path.exists(file_path):
            return True
        time.sleep(1)
        wait_time += 1
    raise TimeoutError(f"Download timeout after {max_wait} seconds")

def extract_competition_name(kaggle_url):
    try:
        # Split the URL by '/' and get the competition name
        parts = kaggle_url.split('/')
        # The competition name will be after 'competitions' in the URL
        competition_index = parts.index('competitions')
        competition_name = parts[competition_index + 1]
        return competition_name
    except (ValueError, IndexError):
        raise ValueError("Invalid Kaggle competition URL format")

# Main automation script
def main():
    # kaggle_url = "https://www.kaggle.com/competitions/{competition-name}/data" 
    kaggle_url = str(input("Enter the Kaggle competition URL: "), end='') 
    download_dir = r"D:\\wwwch\\Documents\\Kaggle"  
    folder_name = extract_competition_name(kaggle_url) or "kaggle-compettition"

    # Perform automation steps
    download_kaggle_data(kaggle_url, download_dir)
    extract_zip_file(download_dir, folder_name)

    # Path to the extracted folder
    folder_path = os.path.join(download_dir, folder_name)

    create_virtual_environment(folder_path)
    launch_vs_code(folder_path)

if __name__ == "__main__":
    main()

import os

# Set the path to kaggle.json before importing KaggleApi
os.environ['KAGGLE_CONFIG_DIR'] = r"D:\wwwch\Documents\\Kaggle\\automation"

import subprocess
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

# Import internal organization modules
from ntpath import join
from os import makedirs
from genericpath import exists

# Step 1: Download all data from the competition page
def download_competition_data(kaggle_url, base_dir):
    # Extract competition name from URL
    competition_name = extract_competition_name(kaggle_url)
    
    # Authenticate with Kaggle API
    api = KaggleApi()
    api.authenticate()
    
    # Create the competition directory
    competition_dir = join(base_dir, competition_name)
    if not exists(competition_dir):
        makedirs(competition_dir)
    
    # Download the competition files
    print(f"Downloading competition files for '{competition_name}'...")
    api.competition_download_files(competition_name, path=competition_dir)
    
    # Unzip the downloaded files
    zip_path = join(competition_dir, f"{competition_name}.zip")
    if exists(zip_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(competition_dir)
        os.remove(zip_path)
        print(f"Files extracted to '{competition_dir}'")
    else:
        raise FileNotFoundError(f"Zip file '{zip_path}' not found after download.")
    
    return competition_dir

def extract_competition_name(kaggle_url):
    # Remove trailing slashes and split the URL
    parts = kaggle_url.strip('/').split('/')
    # Find the index of 'competitions' and get the next part as competition name
    try:
        idx = parts.index('competitions')
        competition_name = parts[idx + 1]
        return competition_name
    except ValueError:
        raise ValueError("Invalid Kaggle competition URL format.")

# Step 2: Create a virtual environment
def create_virtual_environment(competition_dir):
    venv_path = join(competition_dir, "venv")
    print(f"Creating virtual environment at '{venv_path}'...")
    subprocess.run(["python", "-m", "venv", venv_path], check=True)

# Step 3: Open VS Code inside the competition folder
def open_vscode(competition_dir):
    print("Opening VS Code at " + competition_dir)
    subprocess.run([r"D:\\Program Files\\Microsoft VS Code\\Code.exe", competition_dir], check=True)

# Step 4: Activate the virtual environment
def activate_virtual_environment(competition_dir):
    activate_script = join(competition_dir, "venv", "Scripts", "activate.bat")
    if exists(activate_script):
        print(f"To activate the virtual environment, run:\n{activate_script}")
    else:
        raise FileNotFoundError("Activation script not found.")

# Step 5: Create an empty Jupyter Notebook file
def create_jupyter_notebook(competition_dir):
    notebook_name = os.path.basename(competition_dir) + ".ipynb"
    notebook_path = join(competition_dir, notebook_name)
    print(f"Creating Jupyter Notebook at '{notebook_path}'...")
    # Create an empty notebook file
    with open(notebook_path, 'w', encoding='utf-8') as f:
        f.write('{\n "cells": [],\n "metadata": {},\n "nbformat": 4,\n "nbformat_minor": 4\n}')
    print(f"Notebook '{notebook_name}' created.")

def main():
    kaggle_url = input("Enter the Kaggle competition URL: ")
    base_dir = r"D:\wwwch\Documents\\Kaggle"
    
    try:
        # Step 1: Download data
        competition_dir = download_competition_data(kaggle_url, base_dir)
        
        # Step 2: Create virtual environment
        create_virtual_environment(competition_dir)
        
        # Step 3: Open VS Code
        open_vscode(competition_dir)
        
        # Step 4: Activate virtual environment
        activate_virtual_environment(competition_dir)
        
        # Step 5: Create an empty Jupyter Notebook
        create_jupyter_notebook(competition_dir)
        
        print("Setup completed successfully.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
"""
Example script demonstrating various ways to use the Cloudinary Bulk Uploader
"""

import os
import json
from cloudinary_uploader import CloudinaryUploader

def load_config(config_file='config.json'):
    """Load configuration from JSON file"""
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}

def example_basic_upload():
    """Basic upload example"""
    # Initialize uploader with direct credentials
    uploader = CloudinaryUploader(
        cloud_name="your_cloud_name",
        api_key="your_api_key",
        api_secret="your_api_secret"
    )

    # Upload files
    results = uploader.upload_files(
        file_paths=["example1.jpg", "example2.pdf"],
        folder="basic_upload",
        output_file="basic_upload_results.txt"
    )

    print("\nBasic Upload Results:")
    for item in results:
        print(f"Uploaded {item['name']} to {item['url']}")

def example_config_file_upload():
    """Upload using configuration file"""
    config = load_config()
    
    uploader = CloudinaryUploader(
        cloud_name=config['cloud_name'],
        api_key=config['api_key'],
        api_secret=config['api_secret']
    )

    results = uploader.upload_files(
        file_paths=["example3.mp4", "example4.mp3"],
        folder=config.get('default_folder'),
        output_file=config.get('output_file')
    )

    print("\nConfig File Upload Results:")
    for item in results:
        print(f"Uploaded {item['name']} to {item['url']}")

def example_env_vars_upload():
    """Upload using environment variables"""
    uploader = CloudinaryUploader(
        cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_API_SECRET')
    )

    results = uploader.upload_files(
        file_paths=["example5.png", "example6.gif"],
        folder="env_vars_upload"
    )

    print("\nEnvironment Variables Upload Results:")
    for item in results:
        print(f"Uploaded {item['name']} to {item['url']}")

def example_bulk_upload_with_types():
    """Example of bulk upload with different file types"""
    config = load_config()
    
    uploader = CloudinaryUploader(
        cloud_name=config['cloud_name'],
        api_key=config['api_key'],
        api_secret=config['api_secret']
    )

    # Get all files from a directory
    files = []
    for root, _, filenames in os.walk('upload_directory'):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    results = uploader.upload_files(
        file_paths=files,
        folder="bulk_upload",
        output_file="bulk_results.txt"
    )

    print("\nBulk Upload Results:")
    for item in results:
        print(f"Uploaded {item['name']} ({item['resource_type']}) to {item['url']}")

if __name__ == "__main__":
    print("Running Cloudinary Bulk Uploader Examples...")
    
    # Uncomment the examples you want to run
    # example_basic_upload()
    # example_config_file_upload()
    # example_env_vars_upload()
    # example_bulk_upload_with_types()
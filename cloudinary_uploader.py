import os
import sys
import json
import argparse
import asyncio
import cloudinary
import cloudinary.uploader
from pathlib import Path
from typing import List, Optional, Dict, Any
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from mimetypes import guess_type

class CloudinaryUploader:
    def __init__(self, cloud_name: str = None, api_key: str = None, api_secret: str = None, config_file: str = None):
        """Initialize the Cloudinary uploader with credentials or config file."""
        # Try loading from config file
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
        else:
            config = {}

        # Priority: constructor args > config file > environment variables
        self.cloud_name = cloud_name or config.get('cloud_name') or os.getenv('CLOUDINARY_CLOUD_NAME')
        api_key = api_key or config.get('api_key') or os.getenv('CLOUDINARY_API_KEY')
        api_secret = api_secret or config.get('api_secret') or os.getenv('CLOUDINARY_API_SECRET')

        if not all([self.cloud_name, api_key, api_secret]):
            raise ValueError("Cloudinary credentials not found in arguments, config file, or environment variables")

        # Load additional configuration
        self.default_folder = config.get('default_folder', '')
        self.max_file_size = config.get('max_file_size', 100000000)  # 100MB default
        self.concurrent_uploads = config.get('concurrent_uploads', 3)
        self.allowed_types = config.get('allowed_types', ['*/*'])

        cloudinary.config(
            cloud_name=self.cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )

    def upload_files(self, 
                    file_paths: List[str], 
                    folder: Optional[str] = None, 
                    output_file: Optional[str] = None) -> List[dict]:
        """
        Upload multiple files to Cloudinary.
        
        Args:
            file_paths: List of file paths to upload
            folder: Optional folder name in Cloudinary
            output_file: Optional file path to save the URLs
        
        Returns:
            List of dictionaries containing file information and URLs
        """
        results = []
        
        # Create progress bar
        pbar = tqdm(total=len(file_paths), desc="Uploading files")
        
        for file_path in file_paths:
            try:
                # Prepare upload parameters
                upload_params = {"resource_type": "auto"}  # Auto-detect file type
                if folder:
                    upload_params["folder"] = folder

                # Upload file
                result = cloudinary.uploader.upload(file_path, **upload_params)
                
                # Store result
                file_info = {
                    "name": os.path.basename(file_path),
                    "url": result["secure_url"],
                    "resource_type": result["resource_type"],
                    "format": result.get("format", ""),
                    "size": result.get("bytes", 0)
                }
                results.append(file_info)
                
                pbar.update(1)
                
            except Exception as e:
                print(f"\nError uploading {file_path}: {str(e)}", file=sys.stderr)
        
        pbar.close()
        
        # Save URLs to file if output_file is specified
        if output_file:
            self._save_urls_to_file(results, output_file)
        
        return results

    def _save_urls_to_file(self, results: List[dict], output_file: str):
        """Save upload results to a file."""
        # Keep the existing grouped/detailed output (markdown-like)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Cloudinary Upload Results\n\n")
            
            # Group by resource type
            resource_groups = {}
            for item in results:
                resource_type = item.get("resource_type", "file").capitalize()
                if resource_type not in resource_groups:
                    resource_groups[resource_type] = []
                resource_groups[resource_type].append(item)
            
            # Write grouped results
            for resource_type, items in resource_groups.items():
                f.write(f"\n## {resource_type} Files\n")
                for item in items:
                    size_mb = item.get("size", 0) / (1024 * 1024)
                    f.write(f"\n{item['name']} ({size_mb:.2f}MB):\n{item['url']}\n")

    def _save_plain_text(self, results: List[dict], output_file: str):
        """Save a simple plain text file with one 'name: url' per line."""
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in results:
                # Only include successful uploads
                if item.get('status', 'success') == 'success' or 'url' in item:
                    f.write(f"{item['name']}: {item.get('url', '')}\n")

def main():
    parser = argparse.ArgumentParser(description="Upload files to Cloudinary")
    parser.add_argument("--cloud-name", required=True, help="Cloudinary cloud name")
    parser.add_argument("--api-key", required=True, help="Cloudinary API key")
    parser.add_argument("--api-secret", required=True, help="Cloudinary API secret")
    parser.add_argument("--folder", help="Optional folder name in Cloudinary")
    parser.add_argument("--output", help="Output file to save URLs")
    parser.add_argument("files", nargs="+", help="Files to upload")
    
    args = parser.parse_args()
    
    uploader = CloudinaryUploader(args.cloud_name, args.api_key, args.api_secret)
    results = uploader.upload_files(args.files, args.folder, args.output)
    
    if not args.output:
        # Print results to console if no output file specified
        print("\nUpload Results:")
        for item in results:
            print(f"\n{item['name']}:")
            print(f"URL: {item['url']}")
            print(f"Type: {item['resource_type']}")
            print(f"Size: {item['size'] / (1024 * 1024):.2f}MB")

if __name__ == "__main__":
    main()
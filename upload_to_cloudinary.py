import os
import cloudinary
import cloudinary.uploader
from pathlib import Path

# Configure Cloudinary
cloudinary.config(
    cloud_name = "ds8i1mwhj",
    api_key = "329861375235323",
    api_secret = "-slYzm_pfhnBbjIIMHRCMTVpf1g"
)

def upload_images():
    # Get the base directory
    base_dir = Path(__file__).parent
    image_urls = []
    
    # Walk through directories
    for folder in ['tv', 'electricity', 'betting', '.']:
        folder_path = base_dir / folder
        if folder_path.exists():
            for file in folder_path.glob('*.webp'):
                try:
                    # Upload file to Cloudinary
                    result = cloudinary.uploader.upload(
                        str(file),
                        public_id=f"{folder}/{file.stem}" if folder != '.' else file.stem,
                        overwrite=True
                    )
                    
                    # Store the result
                    relative_path = str(file.relative_to(base_dir)).replace('\\', '/')
                    image_urls.append(f"{file.stem}: {result['secure_url']}")
                    print(f"Uploaded: {relative_path}")
                except Exception as e:
                    print(f"Error uploading {file}: {e}")
    
    # Write URLs to file
    with open(base_dir / 'image_urls.txt', 'w') as f:
        f.write('\n'.join(image_urls))
    print("\nAll URLs have been saved to image_urls.txt")

if __name__ == "__main__":
    upload_images()
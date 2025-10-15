import os
from pathlib import Path
from cloudinary_uploader import CloudinaryUploader

# Configuration - replace or use environment variables
CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
API_KEY = os.getenv('CLOUDINARY_API_KEY')
API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

def find_files(base_dir: Path, exts=None):
    if exts is None:
        exts = ['.webp', '.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webm', '.mp3', '.pdf']
    files = []
    for root, _, filenames in os.walk(base_dir):
        for fn in filenames:
            if any(fn.lower().endswith(e) for e in exts):
                files.append(os.path.join(root, fn))
    return files

def main():
    base = Path(__file__).parent
    # Load credentials from env or prompt
    cloud = CLOUD_NAME or input('Cloudinary cloud name: ').strip()
    key = API_KEY or input('Cloudinary API key: ').strip()
    secret = API_SECRET or input('Cloudinary API secret: ').strip()

    uploader = CloudinaryUploader(cloud, key, secret)

    files = find_files(base)
    print(f'Found {len(files)} files to upload')

    if not files:
        return

    results = uploader.upload_files(files, folder=uploader.default_folder)

    # Save plain text file
    txt_out = base / 'cloudinary_urls.txt'
    uploader._save_plain_text(results, str(txt_out))
    print(f'Plain text URLs saved to: {txt_out}')

if __name__ == '__main__':
    main()

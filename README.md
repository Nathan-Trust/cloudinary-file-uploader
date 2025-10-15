# Cloudinary Bulk Uploader

A versatile tool for bulk uploading files to Cloudinary, available both as a web interface and a Python package.

## 🌟 Features

- **Multiple File Types Support**: Upload images, videos, PDFs, audio files, and more
- **Bulk Upload**: Upload multiple files at once
- **Progress Tracking**: Real-time upload progress monitoring
- **Flexible Organization**: Optional folder organization in Cloudinary
- **Multiple Interfaces**: Web UI and Python CLI/Package
- **Detailed Results**: Get organized results with file types, sizes, and URLs
- **Error Handling**: Robust error handling and reporting

## 🚀 Quick Start

### Web Interface

1. Clone this repository
2. Open `index.html` in your browser or deploy to Vercel
3. Enter your Cloudinary credentials
4. Select files and upload

### Python Package

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Command Line Usage:

```bash
python cloudinary_uploader.py --cloud-name YOUR_CLOUD_NAME --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET --folder optional_folder --output urls.txt file1.jpg file2.pdf
```

3. Python Module Usage:

```python
from cloudinary_uploader import CloudinaryUploader

uploader = CloudinaryUploader(
    cloud_name="your_cloud_name",
    api_key="your_api_key",
    api_secret="your_api_secret"
)

results = uploader.upload_files(
    file_paths=["file1.jpg", "file2.pdf"],
    folder="my_uploads",
    output_file="urls.txt"
)
```

## 📖 Documentation

### Web Interface

The web interface provides a user-friendly way to upload files:

- **Cloud Name**: Your Cloudinary cloud name
- **API Key**: Your Cloudinary API key
- **API Secret**: Your Cloudinary API secret
- **Folder Name**: (Optional) Destination folder in Cloudinary
- **File Type**: Select the type of files to upload
- **Progress Tracking**: Visual progress bar
- **Results**: Downloadable list of uploaded file URLs

### Python Package

#### Installation

```bash
pip install -r requirements.txt
```

#### Command Line Arguments

- `--cloud-name`: Your Cloudinary cloud name (required)
- `--api-key`: Your Cloudinary API key (required)
- `--api-secret`: Your Cloudinary API secret (required)
- `--folder`: Optional folder name in Cloudinary
- `--output`: Output file to save URLs
- `files`: One or more files to upload

#### Python Module Usage

```python
from cloudinary_uploader import CloudinaryUploader

# Initialize uploader
uploader = CloudinaryUploader(
    cloud_name="your_cloud_name",
    api_key="your_api_key",
    api_secret="your_api_secret"
)

# Upload files
results = uploader.upload_files(
    file_paths=["file1.jpg", "file2.pdf"],
    folder="my_uploads",  # optional
    output_file="urls.txt"  # optional
)

# Process results
for item in results:
    print(f"File: {item['name']}")
    print(f"URL: {item['url']}")
    print(f"Type: {item['resource_type']}")
    print(f"Size: {item['size'] / (1024 * 1024):.2f}MB")
```

## ⚙️ Configuration

### Using Environment Variables

You can use environment variables for Cloudinary credentials:

```bash
export CLOUDINARY_CLOUD_NAME="your_cloud_name"
export CLOUDINARY_API_KEY="your_api_key"
export CLOUDINARY_API_SECRET="your_api_secret"
```

### Using Configuration File

Create a `config.json` file:

```json
{
  "cloud_name": "your_cloud_name",
  "api_key": "your_api_key",
  "api_secret": "your_api_secret",
  "default_folder": "my_uploads"
}
```

## 🌟 Advanced Features

- **Auto File Type Detection**: Automatically detects and handles different file types
- **Grouped Results**: Results are grouped by file type in the output file
- **Size Information**: File size information included in results
- **Progress Tracking**: Real-time progress bars for both interfaces
- **Error Recovery**: Continues uploading even if some files fail
- **Flexible Output**: Choose between console output or file output

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- [Cloudinary Documentation](https://cloudinary.com/documentation)
- [Report Issues](https://github.com/your-username/cloudinary-bulk-uploader/issues)

## 🙏 Acknowledgments

- Cloudinary for their excellent service and API
- The open-source community for inspiration and tools

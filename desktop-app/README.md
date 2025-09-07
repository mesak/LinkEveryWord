﻿# LinkEveryWord Desktop Application

<p align="center"><img src="../shared/image.png" width="128"></p>

A high-performance Windows desktop application that provides lightning-fast local file search capabilities powered by the voidtools Everything search engine.

## Key Features

- **⚡ Millisecond Search**: Lightning-fast file search powered by Everything SDK
- **🔄 Smart Fallback**: Automatic switching between Everything, Windows Search, and demo modes
- **🌐 Modern Web UI**: Responsive web-based interface with real-time results
- **📦 Portable**: Single 15MB executable with zero installation requirements
- **⚙️ Highly Configurable**: Comprehensive customization via `config.yml`
- **🎯 Demo Mode**: Full functionality preview without Everything dependency
- **🔒 Instance Protection**: File-lock based single instance management
- **📊 Advanced Logging**: Multi-level logging with rotation and console output
- **🌍 Internationalization**: Full Traditional Chinese interface support
- **🔍 Wildcard Support**: Advanced pattern matching (*.txt, *.pdf, etc.)
- **📋 Rich Metadata**: File size, modification time, and detailed information display

## Quick Start

### Production Use (Recommended)
```bash
# Download and run the standalone executable
./dist/EverythingFlaskSearch.exe
```
The application will automatically open your default browser and display the search interface.

### Development Mode
```bash
# Prerequisites: Python 3.13+
pip install -r requirements.txt

# Run development server
python app_standalone.py
```

## System Requirements

- **Operating System**: Windows 10/11 (64-bit)
- **Everything**: voidtools Everything (recommended, not required)
- **Browser**: Chrome, Firefox, Edge, or any modern browser
- **Memory**: Minimum 50MB available RAM
- **Disk Space**: 20MB for installation

## Usage

### Basic Operations
1. **Launch Application**: Run `EverythingFlaskSearch.exe` - browser opens automatically
2. **Search Files**: Enter keywords in the search box
   - Supports filename, path, and extension searches
   - Use wildcards like `*.txt` for specific file types
3. **View Results**: Click filenames to open files, view metadata, and explore paths

### Advanced Search Patterns
```bash
# File type search
*.pdf *.docx

# Path-based search
folder:documents

# Size-based search (if supported by backend)
size:>1MB

# Date-based search
modified:today
```

## Project Structure

```
desktop-app/
├── app_standalone.py          # Main application entry point
├── config.yml                 # Application configuration
├── requirements.txt           # Python dependencies
├── utils/                     # Core modules and SDKs
│   ├── everything_sdk.py      # Everything search integration
│   ├── windows_search.py      # Windows Search fallback
│   └── demo_mode.py          # Demo mode implementation
├── templates/                 # Jinja2 web interface templates
├── static/                   # Static assets (CSS, JS, images)
├── build.bat                 # Automated build script
├── app_standalone.spec       # PyInstaller build specification
└── dist/                     # Build output directory
    └── EverythingFlaskSearch.exe
```

## Technology Stack

- **Backend**: Python 3.13 + Flask framework
- **Frontend**: Modern HTML5 + CSS3 + Vanilla JavaScript
- **Search Engine**: voidtools Everything SDK integration
- **CORS Support**: Flask-CORS for cross-origin requests
- **Packaging**: PyInstaller 6.15.0 for executable generation
- **Configuration**: YAML-based configuration management

## API Documentation

### Search Endpoints
```http
# POST search with JSON payload
POST /search
Content-Type: application/json

{
  "query": "search keywords",
  "max_results": 50
}

# GET search with query parameters
GET /api/search/{query}?limit=50

# Status check
GET /status
```

### Response Format
```json
{
  "results": [
    {
      "name": "filename.txt",
      "path": "C:\\Users\\Documents\\filename.txt",
      "size": 1024,
      "modified": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1,
  "engine": "everything"
}
```

## Configuration

The application supports extensive customization via `config.yml`. If the file doesn't exist, a default configuration is created on first launch.

### Configurable Options
- **Server Settings**: `host`, `port`, `debug` mode
- **Application Behavior**: `browser_delay`, auto-open settings
- **Logging System**: `level`, `filename`, `max_size`, rotation

For detailed configuration options, see [CONFIG.md](CONFIG.md) and [LOGGER_GUIDE.md](LOGGER_GUIDE.md).

## Building from Source

### Prerequisites
```bash
# Install Python 3.13+
# Install required packages
pip install -r requirements.txt
```

### Build Process
```bash
# Create executable
python -m PyInstaller app_standalone.spec --clean

# Or use the build script
./build.bat
```

## Troubleshooting

### Everything Not Installed
- Application automatically switches to demo mode
- Displays simulated search results for testing

### Executable Won't Start
- Check Windows Defender exclusions
- Verify sufficient memory availability
- Try running as administrator
- Check antivirus software interference

### Empty Search Results
- Ensure Everything service is running
- Verify search keywords are correct
- Visit `/status` endpoint to check system status
- Check Everything database indexing status

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see [LICENSE](../LICENSE) for details.
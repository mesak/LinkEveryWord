# LinkEveryWord Chrome Extension

A powerful Chrome extension that bridges web browsing and local file search, enabling instant file discovery from any webpage text selection.

## Features

- **🔍 Instant Text Search**: Select any text on web pages and search your local files instantly
- **📋 Elegant Side Panel**: Clean, responsive interface for displaying search results
- **⚙️ Flexible Configuration**: Customizable backend API endpoints and search parameters
- **⌨️ Smart Shortcuts**: Configurable keyboard shortcuts for seamless workflow integration
- **🎨 Modern UI**: Built with shadcn/ui components and Tailwind CSS for a polished experience

## Installation

### Development Setup
```bash
# Clone and install dependencies
git clone <repository-url>
cd chrome-extension
npm install

# Start development server
npm run dev

# Load extension in Chrome
# 1. Open Chrome Extensions (chrome://extensions/)
# 2. Enable Developer mode
# 3. Click "Load unpacked" and select build/chrome-mv3-dev directory
```

### Production Build
```bash
npm run build
npm run package
```

## Usage

### Quick Start
1. **Select text** on any webpage
2. **Press shortcut** `Ctrl+Shift+F` (customizable)
3. **View results** in the automatically opened side panel

### Configuration
Access extension settings via:
- Click extension icon → Options
- Configure backend API URL (e.g., `http://127.0.0.1:5000/search`)
- Set query parameter key (default: `q`)
- Customize keyboard shortcuts

## Technology Stack

- **Framework**: React 18 + TypeScript
- **UI Library**: shadcn/ui + Tailwind CSS
- **Build Tool**: Plasmo Framework
- **Manifest**: Chrome Extension Manifest V3
- **Architecture**: Modern component-based design with hooks

## Development

```bash
# Install dependencies
npm install

# Development mode with hot reload
npm run dev

# Production build
npm run build

# Create distribution package
npm run package

# Type checking
npm run type-check

# Linting
npm run lint
```

## Project Structure

```
chrome-extension/
├── assets/              # Static assets and icons
├── components/          # React components
│   └── ui/             # shadcn/ui component library
├── contents/           # Content scripts for web page interaction
├── lib/                # Utility functions and helpers
├── locales/            # Internationalization files
├── background.ts       # Service worker (background script)
├── sidepanel.tsx       # Main search interface
├── options.tsx         # Extension settings page
└── package.json        # Project configuration
```

## API Integration

### Backend Requirements
The extension expects a REST API endpoint that accepts GET requests:

```http
GET {backendUrl}?{queryKey}={selectedText}
```

### Response Format
```json
{
  "results": [
    {
      "title": "File or result title",
      "description": "Brief description or file path",
      "url": "Optional direct link to result"
    }
  ]
}
```

### Example Integration
Works seamlessly with the LinkEveryWord Desktop Application:
```bash
# Default configuration
Backend URL: http://127.0.0.1:5000/search
Query Key: q
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see [LICENSE](../LICENSE) for details.

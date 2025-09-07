# LinkEveryWord Web Platform

A modern, multilingual web platform built with Cloudflare Pages and Hono that serves as the central hub for LinkEveryWord project documentation, installation guides, and privacy policies.

## Features

- **🌍 Multilingual Support**: Seamless language switching between English and Traditional Chinese
- **📱 Responsive Design**: Mobile-first approach with modern UI components
- **⚡ Edge Performance**: Powered by Cloudflare Pages for global low-latency delivery
- **🔒 Privacy Compliant**: Comprehensive privacy policy management and hosting
- **📖 Documentation Hub**: Centralized installation guides and project information
- **🎨 Modern Stack**: Built with Hono framework and TypeScript for type safety

## Architecture

### Technology Stack
- **Framework**: Hono (lightweight web framework)
- **Runtime**: Cloudflare Workers/Pages Functions
- **Language**: TypeScript for type safety
- **Deployment**: Cloudflare Pages with automatic CI/CD
- **Routing**: File-based routing with dynamic language support

### Route Structure
```
/                    # Project homepage
/install/chrome      # Chrome extension installation guide
/install/desktop     # Desktop application installation guide
/privacy             # Privacy policy page
```

## Development

### Prerequisites
- Node.js 18+
- Internet access (for Wrangler bootstrapping)
- Cloudflare account (for deployment)

### Local Development
```bash
# Clone and setup
cd web
npm install

# Start development server
npm run dev

# Open browser to displayed URL (e.g., http://localhost:8788)
```

### Language Switching
Access different languages via URL parameters:
```bash
# Traditional Chinese (default)
http://localhost:8788/?lang=zh
http://localhost:8788/install/chrome?lang=zh

# English
http://localhost:8788/?lang=en
http://localhost:8788/install/desktop?lang=en
```

## Content Management

### Privacy Policy System
The platform features an automated privacy policy management system:

**Source Files** (in `web/content/`):
- `privacy-policy.md` (Traditional Chinese)
- `privacy-policy.en.md` (English)

**Generated Files** (auto-generated):
- `src/content/privacy.zh.ts`
- `src/content/privacy.en.ts`

**Sync Process**:
```bash
# Sync privacy policies from markdown to TypeScript
npm run sync:privacy
```

### Asset Management
Shared assets are automatically synchronized:
```bash
# Asset mapping
shared/app_icon.svg → web/assets/logo.svg
shared/image.png → web/assets/image.png

# Sync assets
npm run sync:assets
```

## Deployment

### Cloudflare Pages Deployment
```bash
# Deploy to production
npm run deploy

# Preview deployment
npm run preview
```

### Configuration
The platform uses Cloudflare Pages Functions via `functions/[[path]].ts` with Hono for:
- Dynamic routing
- Language detection
- Content serving
- API endpoints

## Project Structure

```
web/
├── src/
│   ├── content/           # Generated content files
│   ├── components/        # Reusable UI components
│   └── utils/            # Utility functions
├── functions/
│   └── [[path]].ts       # Cloudflare Pages Functions entry
├── content/              # Source markdown files
├── assets/               # Static assets
└── package.json          # Dependencies and scripts
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with `npm run dev`
5. Submit a pull request

## License

MIT License - see [LICENSE](../LICENSE) for details.

import type { Dict } from './types'

export const en: Dict = {
  common: {
    brand: 'LinkEveryWord',
  nav: { home: 'Home', chrome: 'Install Chrome', desktop: 'Install Desktop', privacy: 'Privacy', github: 'GitHub', lang: 'Language', donate: 'Buy me a coffee' },
  },
  home: {
    title: 'Link everything, fast',
    intro: 'Two parts: a Chrome extension and a Windows desktop app to help you find and connect information quickly.',
    quickStart: 'Get Started',
    items: {
      chrome: 'Chrome Extension',
      desktop: 'Windows Desktop App',
    },
  },
  chrome: {
    title: 'Chrome Extension Installation',
    installFromStore: 'Install from Chrome Web Store',
    steps: [
      'Click the "Install from Chrome Web Store" button below.',
      'On the Chrome Store page that opens, click "Add to Chrome".',
      'After installation, we recommend pinning the extension to your toolbar for quick access.'
    ],
    usageTitle: 'Basic usage',
    usageItems: [
      'Select text on a page and press Ctrl+Shift+F (customizable).',
      'The side panel shows results from your configured backend.',
      'Open extension settings to configure backend API, query key, shortcuts.',
    ],
    privacyNote: 'We respect your privacy. See the full policy on the Privacy page.',
    detailsNote: 'See chrome-extension/README.md for details.',
  },
  desktop: {
    title: 'Desktop App installation',
    method1: ['Method 1: Run binary (recommended)', 'Download the release archive (if available) and extract.', 'Run dist/EverythingFlaskSearch.exe.'],
    method2: [
      'Method 2: Dev mode',
      'Install Python 3.13+.',
      'Go to desktop-app, install deps: pip install flask flask-cors.',
      'Start: python app_standalone.py.',
    ],
    reqTitle: 'Requirements',
    reqList: ['Windows 10/11', 'Everything recommended (optional; demo mode available)'],
    more: 'See desktop-app/README.md for details and troubleshooting.',
  },
  privacy: {
    title: 'Privacy Policy',
    enNotice: '(Rendered from the repository markdown)'
  },
}

export default en

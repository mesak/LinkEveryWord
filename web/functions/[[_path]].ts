import { Hono } from 'hono'
import type { Context } from 'hono'
import { serveStatic } from 'hono/cloudflare-pages'
import { html, raw } from 'hono/html'
import { marked } from 'marked'
// Use generated TS content files (created by postinstall sync script)
// @ts-ignore
import privacyZh from '../src/content/privacy.zh'
// @ts-ignore
import privacyEn from '../src/content/privacy.en'
import { zh } from '../src/i18n/zh'
import { en } from '../src/i18n/en'
import type { Dict } from '../src/i18n/types'

const app = new Hono()

// Serve static assets from the `/assets` directory
app.use('/assets/*', serveStatic())

const getLang = (c: Context): { dict: Dict; code: 'zh' | 'en' } => {
  const url = new URL(c.req.url)
  const qp = url.searchParams.get('lang') as 'zh' | 'en' | null
  if (qp === 'zh' || qp === 'en') {
    // Persist preference in cookie
    c.header('Set-Cookie', `lang=${qp}; Path=/; Max-Age=31536000; SameSite=Lax`)
    return { dict: qp === 'en' ? en : zh, code: qp }
  }
  // Try cookie
  const cookie = c.req.header('cookie') || ''
  const m = /(?:^|; )lang=(zh|en)(?:;|$)/.exec(cookie)
  if (m && (m[1] === 'zh' || m[1] === 'en')) {
    return { dict: m[1] === 'en' ? en : zh, code: m[1] as 'zh' | 'en' }
  }
  // Fallback: Accept-Language
  const al = (c.req.header('accept-language') || '').toLowerCase()
  const code: 'zh' | 'en' = al.includes('zh') ? 'zh' : 'en'
  return { dict: code === 'en' ? en : zh, code }
}

const withLangQuery = (url: string, lang: 'zh' | 'en') => (url.includes('?') ? `${url}&lang=${lang}` : `${url}?lang=${lang}`)

const Layout = (c: Context, content: any, opts?: { title?: string }) => {
  const { dict, code } = getLang(c)
  const title = opts?.title ?? dict.common.brand
  return c.html(html`<!doctype html>
    <html lang="${code === 'en' ? 'en' : 'zh-Hant'}">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>${title}</title>
  <link rel="icon" type="image/svg+xml" href="/assets/logo.svg" />
        <style>
          :root {
            color-scheme: light dark;
            --bg-primary: #0a0a0b;
            --bg-secondary: #111113;
            --bg-tertiary: #1a1a1d;
            --bg-card: #1e1e21;
            --border-primary: rgba(255, 255, 255, 0.08);
            --border-secondary: rgba(255, 255, 255, 0.12);
            --text-primary: #ffffff;
            --text-secondary: #a1a1aa;
            --text-muted: #71717a;
            --accent-primary: #3b82f6;
            --accent-secondary: #8b5cf6;
            --accent-success: #10b981;
            --accent-warning: #f59e0b;
            --accent-gradient: linear-gradient(135deg, #3b82f6, #8b5cf6);
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
          }

          * {
            box-sizing: border-box;
          }

          body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans TC', 'Helvetica Neue', Arial, sans-serif;
            margin: 0;
            line-height: 1.7;
            background: var(--bg-primary);
            color: var(--text-primary);
            font-size: 16px;
            overflow-x: hidden;
          }

          /* Header Styles */
          header {
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 16px 0;
            background: rgba(10, 10, 11, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border-primary);
          }

          .header-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
          }

          .logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 20px;
            font-weight: 700;
            color: var(--text-primary);
            text-decoration: none;
          }

          .logo img {
            width: 32px;
            height: 32px;
            border-radius: 8px;
          }

          .nav-container {
            display: flex;
            align-items: center;
            gap: 32px;
          }

          nav {
            display: flex;
            align-items: center;
            gap: 24px;
          }

          nav a {
            color: var(--text-secondary);
            text-decoration: none;
            font-weight: 500;
            padding: 8px 12px;
            border-radius: 8px;
            transition: all 0.2s ease;
            position: relative;
          }

          nav a:hover {
            color: var(--text-primary);
            background: var(--bg-tertiary);
          }

          nav a.active {
            color: var(--accent-primary);
            background: rgba(59, 130, 246, 0.1);
          }

          .lang-switcher {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px 12px;
            background: var(--bg-tertiary);
            border-radius: 8px;
            border: 1px solid var(--border-primary);
          }

          .lang-switcher span {
            color: var(--text-muted);
            font-size: 14px;
          }

          .lang-switcher a {
            color: var(--text-secondary);
            text-decoration: none;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 14px;
            transition: all 0.2s ease;
          }

          .lang-switcher a:hover {
            color: var(--accent-primary);
            background: rgba(59, 130, 246, 0.1);
          }

          .donate-btn {
            padding: 10px 20px;
            border-radius: 12px;
            background: linear-gradient(135deg, #f59e0b, #f97316);
            color: #000;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s ease;
            box-shadow: var(--shadow-sm);
          }

          .donate-btn:hover {
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
            filter: brightness(1.05);
          }

          /* Main Content */
          main {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 24px;
          }

          /* Hero Section */
          .hero {
            padding: 80px 0 120px;
            position: relative;
            overflow: hidden;
          }

          .hero::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(ellipse at center top, rgba(59, 130, 246, 0.15), transparent 70%);
            pointer-events: none;
          }

          .hero-grid {
            display: grid;
            grid-template-columns: 1.2fr 0.8fr;
            gap: 60px;
            align-items: center;
            position: relative;
            z-index: 1;
          }

          .hero-content h1 {
            font-size: clamp(2.5rem, 5vw, 4rem);
            font-weight: 800;
            line-height: 1.1;
            margin: 0 0 24px;
            background: linear-gradient(135deg, var(--text-primary), var(--text-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
          }

          .hero-content p {
            font-size: 1.25rem;
            color: var(--text-secondary);
            margin: 0 0 32px;
            line-height: 1.6;
          }

          .hero-actions {
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
          }

          .hero-image {
            position: relative;
          }

          .hero-image img {
            width: 100%;
            height: auto;
            border-radius: 16px;
            border: 1px solid var(--border-secondary);
            box-shadow: var(--shadow-xl);
            transition: transform 0.3s ease;
          }

          .hero-image:hover img {
            transform: scale(1.02);
          }

          /* Buttons */
          .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 14px 28px;
            border-radius: 12px;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s ease;
            border: none;
            cursor: pointer;
            font-size: 16px;
          }

          .btn-primary {
            background: var(--accent-gradient);
            color: white;
            box-shadow: var(--shadow-md);
          }

          .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
            filter: brightness(1.1);
          }

          .btn-secondary {
            background: var(--bg-card);
            color: var(--text-primary);
            border: 1px solid var(--border-secondary);
          }

          .btn-secondary:hover {
            background: var(--bg-tertiary);
            border-color: var(--border-secondary);
          }

          /* Cards */
          .card {
            background: var(--bg-card);
            border: 1px solid var(--border-primary);
            border-radius: 16px;
            padding: 32px;
            margin: 32px 0;
            box-shadow: var(--shadow-sm);
            transition: all 0.2s ease;
          }

          .card:hover {
            border-color: var(--border-secondary);
            box-shadow: var(--shadow-md);
          }

          .card h2, .card h3 {
            margin-top: 0;
            color: var(--text-primary);
          }

          .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 24px;
            margin: 64px 0;
          }

          .feature-card {
            background: var(--bg-card);
            border: 1px solid var(--border-primary);
            border-radius: 16px;
            padding: 32px;
            text-align: center;
            transition: all 0.3s ease;
          }

          .feature-card:hover {
            transform: translateY(-4px);
            border-color: var(--accent-primary);
            box-shadow: var(--shadow-lg);
          }

          .feature-icon {
            width: 64px;
            height: 64px;
            margin: 0 auto 20px;
            background: var(--accent-gradient);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
          }

          .feature-card h3 {
            margin: 0 0 16px;
            font-size: 1.25rem;
          }

          .feature-card p {
            color: var(--text-secondary);
            margin: 0;
          }

          /* Lists */
          ol, ul {
            padding-left: 24px;
          }

          li {
            margin: 12px 0;
            color: var(--text-secondary);
          }

          li::marker {
            color: var(--accent-primary);
          }

          /* Links */
          a {
            color: var(--accent-primary);
            text-decoration: none;
            transition: color 0.2s ease;
          }

          a:hover {
            color: var(--accent-secondary);
          }

          /* Code */
          pre, code {
            font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
            background: var(--bg-secondary);
            border: 1px solid var(--border-primary);
            border-radius: 8px;
          }

          code {
            padding: 2px 6px;
            font-size: 0.875rem;
          }

          pre {
            padding: 16px;
            overflow-x: auto;
          }

          /* Footer */
          footer {
            margin-top: 120px;
            padding: 48px 0;
            background: var(--bg-secondary);
            border-top: 1px solid var(--border-primary);
          }

          .footer-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 24px;
            text-align: center;
          }

          .footer-donate {
            margin-bottom: 32px;
          }

          .footer-donate img {
            border-radius: 8px;
            transition: transform 0.2s ease;
          }

          .footer-donate img:hover {
            transform: scale(1.05);
          }

          .footer-info {
            color: var(--text-muted);
            font-size: 14px;
            line-height: 1.6;
          }

          .footer-info a {
            color: var(--text-secondary);
          }

          /* Responsive Design */
          @media (max-width: 768px) {
            .header-container {
              padding: 0 16px;
              flex-direction: column;
              gap: 16px;
            }

            .nav-container {
              flex-direction: column;
              gap: 16px;
            }

            nav {
              flex-wrap: wrap;
              justify-content: center;
              gap: 16px;
            }

            main {
              padding: 0 16px;
            }

            .hero {
              padding: 48px 0 80px;
            }

            .hero-grid {
              grid-template-columns: 1fr;
              gap: 40px;
              text-align: center;
            }

            .hero-content h1 {
              font-size: 2.5rem;
            }

            .hero-actions {
              justify-content: center;
            }

            .features-grid {
              grid-template-columns: 1fr;
              margin: 48px 0;
            }

            .card {
              padding: 24px;
              margin: 24px 0;
            }
          }

          @media (max-width: 480px) {
            .btn {
              padding: 12px 20px;
              font-size: 14px;
            }

            .hero-actions {
              flex-direction: column;
            }

            .lang-switcher {
              flex-direction: column;
              gap: 4px;
            }
          }
        </style>
      </head>
      <body>
        <header>
          <div class="header-container">
            <a href="${withLangQuery('/', code)}" class="logo">
              <img src="/assets/logo.svg" alt="logo" />
              ${dict.common.brand}
            </a>
            <div class="nav-container">
              <nav>
                <a class="${c.req.path === '/' ? 'active' : ''}" href="${withLangQuery('/', code)}">${dict.common.nav.home}</a>
                <a class="${c.req.path.startsWith('/install/chrome') ? 'active' : ''}" href="${withLangQuery('/install/chrome', code)}">${dict.common.nav.chrome}</a>
                <a class="${c.req.path.startsWith('/install/desktop') ? 'active' : ''}" href="${withLangQuery('/install/desktop', code)}">${dict.common.nav.desktop}</a>
                <a class="${c.req.path.startsWith('/privacy') ? 'active' : ''}" href="${withLangQuery('/privacy', code)}">${dict.common.nav.privacy}</a>
                <a href="https://github.com/mesak/LinkEveryWord" target="_blank" rel="noreferrer">${dict.common.nav.github}</a>
              </nav>
              <div style="display: flex; align-items: center; gap: 16px;">
                <div class="lang-switcher">
                  <span>${dict.common.nav.lang}:</span>
                  <a href="${withLangQuery(c.req.path, 'zh')}">繁中</a>
                  <a href="${withLangQuery(c.req.path, 'en')}">EN</a>
                </div>
                <a class="donate-btn" href="https://www.buymeacoffee.com/mesak" target="_blank" rel="noreferrer">${dict.common.nav.donate}</a>
              </div>
            </div>
          </div>
        </header>
        <main>${content}</main>
        <footer>
          <div class="footer-content">
            <div class="footer-donate">
              <a href="https://www.buymeacoffee.com/mesak" target="_blank" rel="noreferrer">
                <img src="https://img.buymeacoffee.com/button-api/?text=Buy me a beer&emoji=🍺&slug=mesak&button_colour=FFDD00&font_colour=000000&font_family=Bree&outline_colour=000000&coffee_colour=ffffff" alt="Buy me a coffee" />
              </a>
            </div>
            <div class="footer-info">
              © ${new Date().getFullYear()} LinkEveryWord • MIT License<br>
              Created by <a href="https://github.com/mesak">Mesak</a> • 
              Hosted on <a href="https://pages.cloudflare.com/" target="_blank" rel="noreferrer">Cloudflare Pages</a>
            </div>
          </div>
        </footer>
      </body>
    </html>`)
}

app.get('/', (c: Context) => {
  const { dict, code } = getLang(c)
  return Layout(
    c,
    html`<section class="hero">
        <div class="hero-grid">
          <div class="hero-content">
            <h1>${dict.home.title}</h1>
            <p>${dict.home.intro}</p>
            <div class="hero-actions">
              <a class="btn btn-primary" href="${withLangQuery('/install/chrome', code)}">
                🚀 ${dict.home.quickStart}
              </a>
              <a class="btn btn-secondary" href="https://github.com/mesak/LinkEveryWord" target="_blank" rel="noreferrer">
                📖 ${dict.common.nav.github}
              </a>
            </div>
          </div>
          <div class="hero-image">
            <img src="/assets/image.png" alt="${dict.common.brand} preview" />
          </div>
        </div>
      </section>

      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">🔍</div>
          <h3>${dict.home.items.chrome}</h3>
          <p>${dict.chrome.usageItems[0]}</p>
          <div style="margin-top: 20px;">
            <a class="btn btn-primary" href="${withLangQuery('/install/chrome', code)}">${dict.chrome.title}</a>
          </div>
        </div>
        <div class="feature-card">
          <div class="feature-icon">💻</div>
          <h3>${dict.home.items.desktop}</h3>
          <p>${dict.desktop.reqList[0]} • ${dict.desktop.reqList[1]}</p>
          <div style="margin-top: 20px;">
            <a class="btn btn-primary" href="${withLangQuery('/install/desktop', code)}">${dict.desktop.title}</a>
          </div>
        </div>
      </div>`,
    { title: `${dict.common.brand}` }
  )
})

app.get('/install/chrome', (c: Context) => {
  const { dict, code } = getLang(c)
  const storeUrl = `https://chromewebstore.google.com/detail/linkeveryword-extension/lkpkimhpldonggkkcoidicbeembcpemj?hl=${code}`
  return Layout(
    c,
    html`<div style="padding: 48px 0;">
      <div style="text-align: center; margin-bottom: 48px;">
        <h1 style="font-size: 2.5rem; margin-bottom: 16px;">${dict.chrome.title}</h1>
        <p style="font-size: 1.125rem; color: var(--text-secondary); max-width: 600px; margin: 0 auto;">
          ${dict.home.intro}
        </p>
      </div>

      <div class="card">
        <h2 style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
          <span style="background: var(--accent-gradient); padding: 8px; border-radius: 8px; font-size: 1.2rem;">📦</span>
          ${dict.chrome.installFromStore}
        </h2>
        <ol style="margin-bottom: 32px;">
          ${dict.chrome.steps.map((s) => html`<li style="margin: 16px 0; font-size: 1.1rem;">${s}</li>`)}
        </ol>
        <div style="text-align: center;">
          <a href="${storeUrl}" class="btn btn-primary" target="_blank" rel="noopener noreferrer" style="font-size: 1.1rem; padding: 16px 32px;">
            🚀 ${dict.chrome.installFromStore}
          </a>
        </div>
      </div>

      <div class="card">
        <h2 style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
          <span style="background: var(--accent-gradient); padding: 8px; border-radius: 8px; font-size: 1.2rem;">⚡</span>
          ${dict.chrome.usageTitle}
        </h2>
        <ul style="margin-bottom: 24px;">
          ${dict.chrome.usageItems.map((s) => html`<li style="margin: 12px 0; font-size: 1.05rem;">${s}</li>`)}
        </ul>
        <div style="padding: 16px; background: var(--bg-tertiary); border-radius: 8px; border-left: 4px solid var(--accent-primary);">
          <p style="margin: 0; color: var(--text-secondary); font-size: 0.95rem;">
            💡 ${dict.chrome.detailsNote}
          </p>
        </div>
      </div>

      <div class="card">
        <h3 style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
          <span style="background: var(--accent-gradient); padding: 6px; border-radius: 6px; font-size: 1rem;">🔒</span>
          ${dict.privacy.title}
        </h3>
        <p style="margin: 0; font-size: 1.05rem;">
          ${code === 'en'
            ? 'We respect your privacy. See the full policy on the '
            : '我們尊重你的隱私。完整政策見 '}
          <a href="${withLangQuery('/privacy', code)}" style="font-weight: 600;">${dict.privacy.title}</a>.
        </p>
      </div>
    </div>`,
    { title: `${dict.common.brand} - ${dict.chrome.title}` }
  )
})

app.get('/install/desktop', (c: Context) => {
  const { dict } = getLang(c)
  return Layout(
    c,
    html`<div style="padding: 48px 0;">
      <div style="text-align: center; margin-bottom: 48px;">
        <h1 style="font-size: 2.5rem; margin-bottom: 16px;">${dict.desktop.title}</h1>
        <p style="font-size: 1.125rem; color: var(--text-secondary); max-width: 600px; margin: 0 auto;">
          ${dict.home.intro}
        </p>
      </div>

      <div class="card">
        <h2 style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
          <span style="background: var(--accent-gradient); padding: 8px; border-radius: 8px; font-size: 1.2rem;">⚡</span>
          ${dict.desktop.method1[0]}
        </h2>
        <ol style="margin-bottom: 24px;">
          ${dict.desktop.method1.slice(1).map((s) => html`<li style="margin: 16px 0; font-size: 1.1rem;">${raw(s)}</li>`)}
        </ol>
        <div style="padding: 16px; background: var(--bg-tertiary); border-radius: 8px; border-left: 4px solid var(--accent-success);">
          <p style="margin: 0; color: var(--text-secondary); font-size: 0.95rem;">
            ✅ 推薦方式：直接下載執行檔，無需安裝 Python 環境
          </p>
        </div>
      </div>

      <div class="card">
        <h2 style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
          <span style="background: var(--accent-gradient); padding: 8px; border-radius: 8px; font-size: 1.2rem;">🛠️</span>
          ${dict.desktop.method2[0]}
        </h2>
        <ol style="margin-bottom: 24px;">
          <li style="margin: 16px 0; font-size: 1.1rem;">${dict.desktop.method2[1]}</li>
          <li style="margin: 16px 0; font-size: 1.1rem;">${dict.desktop.method2[2]}</li>
          <li style="margin: 16px 0; font-size: 1.1rem;">${dict.desktop.method2[3]}</li>
        </ol>
        <div style="padding: 16px; background: var(--bg-tertiary); border-radius: 8px; border-left: 4px solid var(--accent-warning);">
          <p style="margin: 0; color: var(--text-secondary); font-size: 0.95rem;">
            ⚠️ 開發模式：需要 Python 環境，適合開發者使用
          </p>
        </div>
      </div>

      <div class="card">
        <h2 style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
          <span style="background: var(--accent-gradient); padding: 8px; border-radius: 8px; font-size: 1.2rem;">📋</span>
          ${dict.desktop.reqTitle}
        </h2>
        <ul style="margin-bottom: 24px;">
          ${dict.desktop.reqList.map((req) => html`<li style="margin: 12px 0; font-size: 1.05rem;">${req}</li>`)}
        </ul>
        <div style="padding: 16px; background: var(--bg-tertiary); border-radius: 8px; border-left: 4px solid var(--accent-primary);">
          <p style="margin: 0; color: var(--text-secondary); font-size: 0.95rem;">
            💡 ${dict.desktop.more}
          </p>
        </div>
      </div>
    </div>`,
    { title: `${dict.common.brand} - ${dict.desktop.title}` }
  )
})

app.get('/privacy', (c: Context) => {
  const { dict, code } = getLang(c)
  const src = code === 'en' ? (privacyEn as string) : (privacyZh as string)
  return Layout(
    c,
    html`<div style="padding: 48px 0;">
      <div style="text-align: center; margin-bottom: 48px;">
        <h1 style="font-size: 2.5rem; margin-bottom: 16px; display: flex; align-items: center; justify-content: center; gap: 16px;">
          <span style="background: var(--accent-gradient); padding: 12px; border-radius: 12px; font-size: 1.5rem;">🔒</span>
          ${dict.privacy.title}
        </h1>
        <p style="font-size: 1.125rem; color: var(--text-secondary); max-width: 600px; margin: 0 auto;">
          ${code === 'en' 
            ? 'We are committed to protecting your privacy and being transparent about our data practices.'
            : '我們致力於保護您的隱私，並對我們的數據處理方式保持透明。'}
        </p>
      </div>
      
      <article class="card" style="max-width: 800px; margin: 0 auto;">
        <div style="prose prose-invert max-w-none">
          ${raw(marked(src))}
        </div>
      </article>
    </div>`,
    { title: `${dict.common.brand} - ${dict.privacy.title}` }
  )
})

// Use a relaxed type here to avoid workers-types mismatch across toolchains
export const onRequest = (context: any) => app.fetch(context.request, context.env, context)

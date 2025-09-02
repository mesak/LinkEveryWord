import { Hono } from 'hono'
import type { Context } from 'hono'
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
          :root{color-scheme: light dark; --bg:#0b1220; --fg:#e5e7eb; --muted:#94a3b8; --primary:#6366f1; --primary2:#8b5cf6}
          body{font-family: system-ui, -apple-system, Segoe UI, Roboto, Noto Sans TC, sans-serif; margin: 0; line-height: 1.6; background:#0b1220; color:#e5e7eb}
          header, footer{padding:16px 20px; background: #0f172a; color: #e2e8f0}
          a{color: #93c5fd; text-decoration: none}
          a:hover{text-decoration: underline}
          nav a{color:#e2e8f0; margin-right: 12px}
          .active{font-weight:700; text-decoration:underline}
          .donate{margin-left:10px; padding:6px 10px; border-radius:8px; background:linear-gradient(135deg, #f59e0b, #f97316); color:black; font-weight:700}
          main{max-width: 980px; margin: 0 auto; padding: 28px 20px}
          .hero{padding:24px 20px; border-bottom:1px solid rgba(148,163,184,.2); background:linear-gradient(135deg, rgba(99,102,241,.14), rgba(139,92,246,.08) 60%, transparent)}
          .title{font-size:28px; font-weight:800; letter-spacing:.2px}
          .subtitle{color:#cbd5e1}
          .card{background: #0b1220; border: 1px solid rgba(148,163,184,.25); border-radius: 12px; padding: 16px}
          .btn{display:inline-block; padding:8px 12px; border-radius:8px; background:linear-gradient(135deg, var(--primary), var(--primary2)); color:white}
          .btn:hover{filter:brightness(1.05)}
          .hero-grid{display:grid; grid-template-columns: 1.2fr .8fr; gap:18px; align-items:center}
          .hero img{max-width:100%; border-radius:12px; border:1px solid rgba(148,163,184,.25)}
          h1,h2,h3{line-height:1.2}
          pre, code{font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace}
        </style>
      </head>
      <body>
        <header>
          <strong style="display:inline-flex;align-items:center;gap:8px">
            <img src="/assets/logo.svg" alt="logo" width="20" height="20" /> ${dict.common.brand}
          </strong>
          <nav style="float:right">
            <a class="${c.req.path === '/' ? 'active' : ''}" href="${withLangQuery('/', code)}">${dict.common.nav.home}</a>
            <a class="${c.req.path.startsWith('/install/chrome') ? 'active' : ''}" href="${withLangQuery('/install/chrome', code)}">${dict.common.nav.chrome}</a>
            <a class="${c.req.path.startsWith('/install/desktop') ? 'active' : ''}" href="${withLangQuery('/install/desktop', code)}">${dict.common.nav.desktop}</a>
            <a class="${c.req.path.startsWith('/privacy') ? 'active' : ''}" href="${withLangQuery('/privacy', code)}">${dict.common.nav.privacy}</a>
            <a href="https://github.com/mesak/LinkEveryWord" target="_blank" rel="noreferrer">${dict.common.nav.github}</a>
            <a class="donate" href="https://www.buymeacoffee.com/mesak" target="_blank" rel="noreferrer">${dict.common.nav.donate}</a>
            <span style="margin-left:12px; color:#94a3b8">${dict.common.nav.lang}:</span>
            <a href="${withLangQuery(c.req.path, 'zh')}">繁中</a>
            <a href="${withLangQuery(c.req.path, 'en')}" style="margin-left:6px">EN</a>
          </nav>
          <div style="clear:both"></div>
        </header>
        <main>${content}</main>
        <footer>
          <center><a href="https://www.buymeacoffee.com/mesak" target="_blank" rel="noreferrer"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a beer&emoji=🍺&slug=mesak&button_colour=FFDD00&font_colour=000000&font_family=Bree&outline_colour=000000&coffee_colour=ffffff" /></a></center>
          <small>
            © ${new Date().getFullYear()} LinkEveryWord • MIT •
            <a href="mailto:mesakey@gmail.com" style="color:#cbd5e1">Mesak</a> •
            Hosted on <a href="https://pages.cloudflare.com/" target="_blank" rel="noreferrer">Cloudflare Pages</a>
          </small>
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
          <div>
            <div class="title">${dict.home.title}</div>
            <p class="subtitle">${dict.home.intro}</p>
            <p style="margin-top:8px"><a class="btn" href="${withLangQuery('/install/chrome', code)}">${dict.home.quickStart}</a></p>
          </div>
          <div>
            <img src="/assets/image.png" alt="${dict.common.brand} preview" />
          </div>
        </div>
      </section>
      <div style="height:14px;"></div>
      <div class="card">
        <h2>${dict.home.quickStart}</h2>
        <ul>
          <li><a href="${withLangQuery('/install/chrome', code)}">${dict.home.items.chrome}</a></li>
          <li><a href="${withLangQuery('/install/desktop', code)}">${dict.home.items.desktop}</a></li>
        </ul>
      </div>`,
    { title: `${dict.common.brand}` }
  )
})

app.get('/install/chrome', (c: Context) => {
  const { dict, code } = getLang(c)
  const storeUrl = `https://chromewebstore.google.com/detail/linkeveryword-extension/lkpkimhpldonggkkcoidicbeembcpemj?hl=${code}`
  return Layout(
    c,
    html`<h1>${dict.chrome.title}</h1>
    <ol>
      ${dict.chrome.steps.map((s) => html`<li>${s}</li>`)}
    </ol>
    <div style="text-align: center; margin: 2.5rem 0;">
      <a href="${storeUrl}" class="btn" target="_blank" rel="noopener noreferrer" style="padding:12px 18px; font-size:16px;">
        ${dict.chrome.installFromStore}
      </a>
    </div>
    <div class="card">
      <h2>${dict.chrome.usageTitle}</h2>
      <ul>
        ${dict.chrome.usageItems.map((s) => html`<li>${s}</li>`)}
      </ul>
      <p>${dict.chrome.detailsNote}</p>
    </div>
    <div class="card">
      <h3>${dict.privacy.title}</h3>
      <p>${code === 'en'
        ? 'We respect your privacy. See the full policy on the '
        : '我們尊重你的隱私。完整政策見 '}<a href="${withLangQuery('/privacy', code)}">${dict.privacy.title}</a>.</p>
    </div>`,
    { title: `${dict.common.brand} - ${dict.chrome.title}` }
  )
})

app.get('/install/desktop', (c: Context) => {
  const { dict } = getLang(c)
  const desktopMd = `# ${dict.desktop.title}\n\n` +
    `${dict.home.intro}\n\n` +
    `## ${dict.desktop.method1[0]}\n` +
    `1. ${dict.desktop.method1[1]}\n` +
    `2. ${dict.desktop.method1[2]}\n\n` +
    `## ${dict.desktop.method2[0]}\n` +
    `1. ${dict.desktop.method2[1]}\n` +
    `2. ${dict.desktop.method2[2]}\n` +
    `3. ${dict.desktop.method2[3]}\n\n` +
    `## ${dict.desktop.reqTitle}\n- ${dict.desktop.reqList.join('\n- ')}\n\n` +
    `${dict.desktop.more}`
  const content = marked(desktopMd)
  return Layout(c, html`${raw(content)}`, { title: `${dict.common.brand} - ${dict.desktop.title}` })
})

app.get('/privacy', (c: Context) => {
  const { dict, code } = getLang(c)
  const src = code === 'en' ? (privacyEn as string) : (privacyZh as string)
  return Layout(
    c,
    html`<h1>${dict.privacy.title}</h1><article class="card">${raw(marked(src))}</article>`,
    { title: `${dict.common.brand} - ${dict.privacy.title}` }
  )
})

// Use a relaxed type here to avoid workers-types mismatch across toolchains
export const onRequest = (context: any) => app.fetch(context.request, context.env, context)

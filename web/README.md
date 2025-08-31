# LinkEveryWord Web (Cloudflare Pages + Hono)

This site introduces the project, provides install guides for the Chrome extension and Desktop app, and hosts the Privacy Policy page.

## Develop locally

Prereqs:
- Node.js 18+
- Internet access (Wrangler bootstraps)

Steps:

```powershell
cd web
npm install
npm run dev
```

Open the URL shown by Wrangler (e.g. http://localhost:8788).

## Deploy to Cloudflare Pages

```powershell
cd web
npm run deploy
```

Notes:
- Uses Pages Functions via `functions/[[path]].ts` with Hono.
- Routes: `/`, `/install/chrome`, `/install/desktop`, `/privacy`.

### 多語系切換

- 透過網址參數 `?lang=zh` 或 `?lang=en` 切換語言，例如：
	- `http://localhost:8788/?lang=zh`
	- `http://localhost:8788/install/chrome?lang=en`

## Privacy Policy

- Canonical files live in `web/content/`:
	- `web/content/privacy-policy.md` (zh)
	- `web/content/privacy-policy.en.md` (en)
- On install or `npm run sync:privacy`, these are converted into:
	- `src/content/privacy.zh.ts` and `src/content/privacy.en.ts`
	- If an English version is missing, zh content is used as fallback.

## Assets

- The sync script copies shared assets into `web/assets/`:
	- `shared/app_icon.svg` → `assets/logo.svg` (favicon and header logo)
	- `shared/image.png` → `assets/image.png` (home hero image)

## License

MIT

# Accredited Interchange — website

Source for accreditedinterchange.com. The site is built in GoHighLevel: in the Accredited Interchange sub-account, under Sites → Websites → **Accredited Interchange**. Each page holds one Custom Code element, and everything else loads from this repo through GitHub Pages. Make changes here, not in GHL.

## How it works

Each page's custom-code embed contains only:

```html
<div id="ai-root" data-page="home"></div>
<script src="https://mylaunchpartner.github.io/accredited-interchange/loader.js"></script>
```

`loader.js` fetches `pages/<data-page>.html`, puts it on the page, and runs its scripts (nav, savings calculator, FAQ, the GHL form and the GHL calendar).

## Pages

| Live URL | `data-page` | File | GHL page ID |
|---|---|---|---|
| `/` | `home` | `pages/home.html` | zppNaKK0HX30CsqpM4su |
| `/contact-us` | `contact` | `pages/contact.html` (includes GHL form GTv5oyghEW1j6kvJYelQ) | bF9LBsEUViON4CdCaMFY |
| `/message-received` | `message-received` | `pages/message-received.html` (includes GHL calendar 0NjpVBFobathv2dyZnxF) | B2GyAsZhIE8XAFqgivvW |
| `/specialty-peptide-payment-processing` | `peptides` | `pages/peptides.html` | zy9z9vOPkUSzCpMmAotz |
| `/privacy-policy` | `privacy` | `pages/privacy.html` | GsChR8xUe3enzd04vWPI |
| `/terms-of-service` | `terms` | `pages/terms.html` | HTWoRa8GEP0swGWxEKCf |

Page titles and meta descriptions are set in GHL (builder → SEO & AI search optimization), not in these files. The loader also strips GHL's section/row padding so pages run edge to edge.

Preview a GHL page before the domain points to it: `https://sites.leadconnectorhq.com/preview/<GHL page ID>?notrack=true`

## Making a change

1. Edit the page file in `pages/` and commit to `main`.
2. GitHub Pages republishes in about a minute. Visitors see it within about 10 minutes, depending on cache.

## Preview without the live site

`https://mylaunchpartner.github.io/accredited-interchange/?page=peptides`

## Assets

Logos are in `assets/`. The pages still load the logo from the Webflow CDN (cdn.prod.website-files.com). Switch them to `assets/ai-logo-mark.png` before the Webflow site is cancelled.

# Accredited Interchange — website

Source for accreditedinterchange.com. The site is built in GoHighLevel: in the Accredited Interchange sub-account, under Sites → Websites → **Accredited Interchange**. Each page holds one Custom Code element, and everything else loads from this repo through GitHub Pages. Make changes here, not in GHL.

## How it works

Each page's custom-code embed contains only:

```html
<div id="ai-root" data-page="home"></div>
<script src="https://mylaunchpartner.github.io/accredited-interchange/loader.js"></script>
```

`loader.js` is a tiny stub that loads `core.js` with a cache key that changes every minute. `core.js` fetches `pages/<data-page>.html`, puts it on the page, and runs its scripts (nav, savings calculator, FAQ, the GHL form and the GHL calendar).

## Pages

| Live URL | `data-page` | File | GHL page ID |
|---|---|---|---|
| `/` | `home` | `pages/home.html` | zppNaKK0HX30CsqpM4su |
| `/contact-us` | `contact` | `pages/contact.html` (includes GHL form GTv5oyghEW1j6kvJYelQ) | bF9LBsEUViON4CdCaMFY |
| `/message-received` | `message-received` | `pages/message-received.html` (includes GHL calendar 0NjpVBFobathv2dyZnxF) | B2GyAsZhIE8XAFqgivvW |
| `/specialty-peptide-payment-processing` | `peptides` | `pages/peptides.html` | zy9z9vOPkUSzCpMmAotz |
| `/privacy-policy` | `privacy` | `pages/privacy.html` | GsChR8xUe3enzd04vWPI |
| `/terms-of-service` | `terms` | `pages/terms.html` | HTWoRa8GEP0swGWxEKCf |
| `/about` | `about` | `pages/about.html` | XPc0G6Mb1cL9B4fh1aRU |
| `/ownership` | `ownership` | `pages/ownership.html` | B8rxAKoyyWim4w6CY6bI |
| `/samantha-martinez` | `samantha-martinez` | `pages/samantha-martinez.html` | lXSXtBYotHiKEH75NPOy |

Page titles and meta descriptions are set in GHL (builder → SEO & AI search optimization), not in these files. The loader also strips GHL's section/row padding so pages run edge to edge.

Preview a GHL page before the domain points to it: `https://sites.leadconnectorhq.com/preview/<GHL page ID>?notrack=true`

## Shared parts

The header, footer and contact block are shared across every page. Edit them once here:

- `partials/header.html`: logo, main menu, mobile menu
- `partials/footer.html`: footer columns and legal line
- `partials/nap.html`: company name, legal name, address, phone and email. The loader inserts it wherever a page has `<!--ai:nap-->` (footer, contact, about, ownership), so it matches character for character everywhere.
- `partials/shell.css`: styles for the header and footer

Pages mark where these go with `<!--ai:header-->` and `<!--ai:footer-->`.

## Structured data

`seo/schema-head.html` is the Organization + Person JSON-LD. It lives in GHL under Websites → Accredited Interchange → Settings → Head tracking code. Edit it here first, then paste it into GHL.

## Blog

The GHL blog site "Accredited Interchange Blog" is at accreditedinterchange.com/blog. The author is Samantha Martinez, linking to /samantha-martinez. Categories: From the Owner, Payments Guides, Industry Guides, Payroll & Insurance, Arizona Business.

The blog home (and its category pages, which share the template) has one Custom Code element above GHL's Blog Posts element, with `data-page="blog"`. `pages/blog.html` adds the site header, the blog hero with category links, a statement-review call to action and the footer, and restyles GHL's post list into cards (newest post featured, keyword tags hidden, dates shown as "Oct 22, 2026"). New posts still come from GHL automatically. The footer block is marked `data-ai-append-body`, so `core.js` moves it to the end of the page, below the post list. Individual post pages (`/post/<slug>`) are not styled by this yet.

## Making a change

1. Edit the page file in `pages/` and commit to `main`.
2. GitHub Pages republishes in about a minute. Visitors see it within about 10 minutes, depending on cache.

## Preview without the live site

`https://mylaunchpartner.github.io/accredited-interchange/?page=peptides`

## Assets

Logos are in `assets/`. Add Samantha's headshot as `assets/samantha-martinez-accredited-interchange.jpg`; the home, about and author pages show it automatically, and show "SM" initials until it exists. Pages load the logo from `assets/ai-logo-mark.png` on GitHub Pages, so nothing depends on Webflow.

## SEO

- **Crawlable copy:** the page HTML that GHL serves would otherwise be empty, because each page loads from here with JavaScript. `seo/embeds/<page>.html` is the full Custom Code embed for each GHL page. It holds a plain copy of the page text and page-level structured data (breadcrumbs, services, FAQ), and `core.js` swaps in the designed page on load. After changing a page's copy, run `python3 tools/build-seo-embeds.py` and paste the changed embed into that page's Custom Code element in GHL.
- **Share images:** `assets/accredited-og-home.jpg` and `assets/accredited-og-peptides.jpg` (1200×630), set in GHL → SEO & AI search optimization → Images.
- **Site-wide schema** (Organization, Person) stays in `seo/schema-head.html`, pasted in GHL's head tracking code.

## Photos

Licensed from Envato: hero `assets/hero-merchant-register.jpg` ("Woman Calculates Finances in Stylish Clothing Store"). `merchant-counter-tap.jpg` and the three `ruo-*.jpg` photos are the same Envato photos used on starfipay.com.

## Design

Layout matches starfipay.com; styling keeps Accredited's own identity: Space Grotesk headings, Inter body, indigo `#4F46FF` for actions, deep indigo `#161335` for dark bands, green `#12B76A`/`#2FD08A` for payroll and savings. Avoid pill labels above headings, colored words inside headlines, glow gradients, scroll-in animations and graph-paper backgrounds.

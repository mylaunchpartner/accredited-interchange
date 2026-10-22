# Accredited Interchange — website

Source for accreditedinterchange.com. The site builder (currently Webflow; works the same in GHL) holds one small embed per page, and everything else loads from this repo through GitHub Pages. Make changes here, not in the builder.

## How it works

Each page's custom-code embed contains only:

```html
<div id="ai-root" data-page="home"></div>
<script src="https://mylaunchpartner.github.io/accredited-interchange/loader.js"></script>
```

`loader.js` fetches `pages/<data-page>.html`, puts it on the page, and runs its scripts (nav, savings calculator, FAQ, the GHL form and the GHL calendar).

## Pages

| Live URL | `data-page` | File |
|---|---|---|
| `/` | `home` | `pages/home.html` |
| `/contact-us` | `contact` | `pages/contact.html` (includes GHL form GTv5oyghEW1j6kvJYelQ) |
| `/message-received` | `message-received` | `pages/message-received.html` (includes GHL calendar 0NjpVBFobathv2dyZnxF) |
| `/specialty-peptide-payment-processing` | `peptides` | `pages/peptides.html` |
| `/privacy-policy` | `privacy` | `pages/privacy.html` |
| `/terms-of-service` | `terms` | `pages/terms.html` |

Set page titles and meta descriptions in the builder's page settings, not in these files.

## Making a change

1. Edit the page file in `pages/` and commit to `main`.
2. GitHub Pages republishes in about a minute. Visitors see it within about 10 minutes, depending on cache.

## Preview without the live site

`https://mylaunchpartner.github.io/accredited-interchange/?page=peptides`

## Assets

Logos are in `assets/`. The pages currently load the logo from the Webflow CDN. It can be switched to `assets/ai-logo-mark.png` if the site moves off Webflow.

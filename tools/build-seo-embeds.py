#!/usr/bin/env python3
"""Build the GHL Custom Code embed for every page, with a crawlable copy of the page text.

Each GHL page holds one Custom Code element. The page itself loads from GitHub with
JavaScript, so the HTML that GHL serves has no readable copy in it. Search engines and
AI tools that don't run JavaScript would see an empty page.

This script writes seo/embeds/<page>.html: the usual embed snippet, but with a plain,
semantic copy of the page's text (headings, paragraphs, lists, links) inside #ai-root,
plus page-level structured data (FAQ, services, breadcrumbs). core.js replaces that copy
with the designed page as soon as it loads, so visitors only ever see the design; the
text is the same words, so this is not cloaking.

Run after changing page copy:  python3 tools/build-seo-embeds.py
Then paste each changed seo/embeds/<page>.html into that page's Custom Code element in GHL.
"""
import json, os, re
from bs4 import BeautifulSoup, Comment

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://accreditedinterchange.com'
LOADER = 'https://mylaunchpartner.github.io/accredited-interchange/loader.js'

# data-page -> (live path, breadcrumb name)
PAGES = {
    'home': ('/', 'Home'),
    'contact': ('/contact-us', 'Contact'),
    'message-received': ('/message-received', 'Message received'),
    'peptides': ('/specialty-peptide-payment-processing', 'RUO peptide payment processing'),
    'privacy': ('/privacy-policy', 'Privacy policy'),
    'terms': ('/terms-of-service', 'Terms of service'),
    'about': ('/about', 'About'),
    'ownership': ('/ownership', 'Ownership'),
    'samantha-martinez': ('/samantha-martinez', 'Samantha Martinez'),
    'blog': ('/blog', 'Blog'),
    'payroll': ('/payroll-services', 'Payroll services'),
    'insurance': ('/business-insurance', 'Business insurance'),
}

KEEP = {'h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'li', 'dl', 'dt', 'dd', 'a', 'strong', 'em', 'b',
        'br', 'section', 'article', 'header', 'footer', 'nav', 'figure', 'figcaption', 'address',
        'table', 'thead', 'tbody', 'tr', 'th', 'td', 'img', 'blockquote'}
DROP = {'style', 'script', 'svg', 'noscript', 'form', 'input', 'button', 'select', 'textarea',
        'iframe', 'label'}

ORG = {'@id': SITE + '/#organization'}


def abs_url(href):
    if not href or href.startswith(('http', 'mailto:', 'tel:')):
        return href
    if href.startswith('#'):
        return href
    return SITE + (href if href.startswith('/') else '/' + href)


def clean(html):
    soup = BeautifulSoup(html, 'html.parser')
    for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
        c.extract()
    for t in soup.find_all(list(DROP)):
        t.decompose()
    for t in soup.find_all(True):
        if t.name not in KEEP:
            t.insert_before(' '); t.insert_after(' ')  # keep words in separate spans/divs apart
            t.unwrap()
            continue
        if t.name == 'img':
            if not t.get('alt'):
                t.decompose()
                continue
            t.attrs = {'src': t.get('src'), 'alt': t['alt']}
        elif t.name == 'a':
            t.attrs = {'href': abs_url(t.get('href', ''))}
        else:
            t.attrs = {}
    # drop empty block elements
    for t in soup.find_all(['p', 'li', 'h2', 'h3', 'h4', 'dt', 'dd', 'section', 'ul', 'ol', 'dl', 'figure']):
        if not t.get_text(strip=True) and not t.find('img'):
            t.decompose()
    out = str(soup)
    out = re.sub(r'[ \t]+', ' ', out)
    out = re.sub(r'\n\s*\n+', '\n', out)
    return out.strip()


def faq_schema(raw):
    soup = BeautifulSoup(raw, 'html.parser')
    items = []
    for it in soup.select('.faq-item'):
        q = it.select_one('.faq-q'); a = it.select_one('.faq-a')
        if q and a:
            items.append({'@type': 'Question', 'name': q.get_text(' ', strip=True),
                          'acceptedAnswer': {'@type': 'Answer', 'text': a.get_text(' ', strip=True)}})
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': items} if items else None


def services_schema(page, url):
    if page == 'home':
        svcs = [('Payment processing', 'Interchange-plus credit card processing, POS terminals, ecommerce gateways, virtual terminal, ACH and recurring billing.'),
                ('Payroll services', 'Automated payroll with tax filing in all 50 states, direct deposit, employee portal, W-2s and 1099s.'),
                ('Business insurance', 'General liability, workers’ compensation, commercial auto, professional liability and business owner’s policies.')]
    elif page == 'peptides':
        svcs = [('RUO peptide payment processing', 'Payment processing for Research Use Only peptide eCommerce merchants: individual underwriting, fraud prevention, chargeback management and Shopify-compatible processing.')]
    elif page == 'payroll':
        svcs = [('Payroll services', 'Automated, compliant payroll for small and midsize businesses: scheduled pay runs with no per-run fees, payroll tax filing in all 50 states, direct deposit, an employee portal, and W-2s and 1099s.')]
    elif page == 'insurance':
        svcs = [('Business insurance', 'Business insurance shopped across top-rated carriers and placed for you: general liability, workers’ compensation, commercial auto, professional liability, business owner’s policies and group benefits.')]
    else:
        return []
    return [{'@context': 'https://schema.org', '@type': 'Service', 'name': n, 'description': d,
             'serviceType': n, 'provider': ORG, 'areaServed': {'@type': 'Country', 'name': 'United States'},
             'url': url} for n, d in svcs]


def breadcrumb(page):
    path, name = PAGES[page]
    items = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'}]
    if page != 'home':
        items.append({'@type': 'ListItem', 'position': 2, 'name': name, 'item': SITE + path})
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items}


NAV = ('<nav aria-label="Site"><ul>'
       + ''.join(f'<li><a href="{SITE}{p}">{n}</a></li>' for k, (p, n) in PAGES.items() if k != 'message-received')
       + '</ul></nav>')


def build(page):
    raw = open(os.path.join(ROOT, 'pages', page + '.html'), encoding='utf-8').read()
    nap = open(os.path.join(ROOT, 'partials', 'nap.html'), encoding='utf-8').read()
    body = raw.replace('<!--ai:header-->', '').replace('<!--ai:footer-->', '').replace('<!--ai:nap-->', nap)
    path = PAGES[page][0]
    text = clean(body)
    ld = [breadcrumb(page)] + services_schema(page, SITE + path)
    f = faq_schema(raw)
    if f:
        ld.append(f)
    ld_html = '\n'.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False, separators=(',', ':')) + '</script>' for x in ld)
    return (f'<div id="ai-root" data-page="{page}" style="visibility:hidden;min-height:100vh">\n'
            f'<main class="ai-seo-copy">\n{text}\n</main>\n{NAV}\n{clean(nap)}\n</div>\n'
            f'{ld_html}\n'
            f'<script src="{LOADER}"></script>\n')


if __name__ == '__main__':
    os.makedirs(os.path.join(ROOT, 'seo', 'embeds'), exist_ok=True)
    for page in PAGES:
        out = build(page)
        with open(os.path.join(ROOT, 'seo', 'embeds', page + '.html'), 'w', encoding='utf-8') as fh:
            fh.write(out)
        print(f'{page:20s} {len(out):6d} bytes')

"""Generates the 2026-10-30 lead-content pages (English source). Translations go through i18n.py as usual.

  python _i18n/new_pages_2026_10.py
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://marketingkamran.com"
DATE, DATE_H = "2026-10-30", "30 Oct 2026"
MARKETS = ["United Kingdom", "United States", "Canada", "Australia"]


def head_prefix(template):
    src = open(os.path.join(ROOT, template), encoding="utf-8").read()
    return src[:src.index("<title>")].lstrip("﻿")


def ld(obj):
    return '<script type="application/ld+json">\n%s\n</script>' % json.dumps(obj, ensure_ascii=False, indent=2)


def faq_ld(faq):
    return ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})


def meta(title, desc, url, og_type, base):
    return f"""<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Kamran Arshad">
<meta property="og:locale" content="en_GB">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/og-image.png">
<link rel="icon" type="image/svg+xml" href="{base}KA_favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Instrument+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
"""


GTM_NS = """<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-5GXJPTNK"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>"""


def related_html(items, heading="Related"):
    links = "\n".join(f'      <a href="{h}">{t}<span>{s}</span></a>' for h, t, s in items)
    return f'    <div class="related">\n      <h2>{heading}</h2>\n{links}\n    </div>'


def service_page(p):
    url = f"{SITE}/{p['slug']}.html"
    faq_html = "\n".join(f"      <details><summary>{q}</summary><p>{a}</p></details>" for q, a in p["faq"])
    mkts = "".join(f"<span>{m}</span>" for m in MARKETS)
    head = head_prefix("carpet-cleaning-marketing.html") + meta(p["title"], p["desc"], url, "website", "") + \
        '<link rel="stylesheet" href="service.css">\n' + "\n".join([
            ld({"@context": "https://schema.org", "@type": "Service", "name": p["svc_name"], "serviceType": p["svc_type"],
                "description": p["desc"], "url": url,
                "provider": {"@type": "ProfessionalService", "name": "Kamran Arshad", "url": SITE + "/",
                             "address": {"@type": "PostalAddress", "addressLocality": "Islamabad", "addressCountry": "PK"}},
                "areaServed": [{"@type": "Country", "name": m} for m in MARKETS]}),
            ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": p["crumb"], "item": url}]}),
            faq_ld(p["faq"])]) + "\n</head>\n"
    return head + f"""<body>
{GTM_NS}
<a class="skip" href="#main">Skip to content</a>
<div class="topbar">
  <div class="container">
    <a class="brand" href="./">Kamran Arshad</a>
    <nav class="topnav" aria-label="Main">
      <a href="./#services">Services</a>
      <a href="./#work">Case Studies</a>
      <a href="blog/">Field Notes</a>
      <a class="btn" href="./#contact">Get Free Audit</a>
    </nav>
  </div>
</div>
<header class="post-head">
  <div class="container narrow">
    <div class="crumb"><a href="./">Home</a> &nbsp;/&nbsp; <a href="./#services">Services</a> &nbsp;/&nbsp; {p['crumb']}</div>
    <h1>{p['h1']}</h1>
    <div class="byline"><span>Kamran Arshad</span><span>Updated <time datetime="{DATE}">{DATE_H}</time></span></div>
    <div class="mkts" aria-label="Markets served">{mkts}</div>
  </div>
</header>
<main id="main">
<article>
  <div class="container narrow">
{p['body']}
    <h2>Common questions</h2>
    <div class="faq">
{faq_html}
    </div>
    <div class="cta">
      <h2>{p['cta_h']}</h2>
      <p>{p['cta_p']}</p>
      <a class="btn" href="./#contact">{p['cta_b']} &rarr;</a>
    </div>
{related_html(p['related'])}
  </div>
</article>
</main>
<a class="float-cta" href="./#contact">Free audit</a>
<footer>
  <div class="container">
    <span>&copy; 2026 Kamran Arshad. Paid ads, SEO and tracking. Islamabad, Pakistan, working remotely.</span>
    <span><a href="./">Home</a> &middot; <a href="blog/">Field Notes</a> &middot; <a href="alphamart.html">AlphaMart</a> &middot; <a href="the-body-essential.html">The Body Essential</a> &middot; <a href="smile-line-dental.html">Smile Line Dental</a> &middot; <a href="mr-expert-carpet-cleaning.html">Mr Expert</a> &middot; <a href="brizaa.html">Brizaa</a> &middot; <a href="privacy-policy.html">Privacy</a></span>
  </div>
</footer>
<script src="consent.js" defer></script>
</body>
</html>
"""


def blog_page(p):
    url = f"{SITE}/blog/{p['slug']}.html"
    faq_html = "\n".join(f"    <h3>{q}</h3>\n    <p>{a}</p>" for q, a in p["faq"])
    head = head_prefix("blog/google-ads-call-tracking-local-business.html") + meta(p["title"], p["desc"], url, "article", "../") + \
        '<link rel="stylesheet" href="post.css">\n' + "\n".join([
            ld({"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["desc"],
                "datePublished": DATE, "dateModified": DATE,
                "author": {"@type": "Person", "name": "Kamran Arshad", "url": SITE + "/", "jobTitle": "Paid Ads & Conversion Tracking Specialist"},
                "publisher": {"@type": "Person", "name": "Kamran Arshad"},
                "mainEntityOfPage": {"@type": "WebPage", "@id": url}, "image": SITE + "/og-image.png"}),
            ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Field Notes", "item": SITE + "/blog/"},
                {"@type": "ListItem", "position": 3, "name": p["crumb"]}]}),
            faq_ld(p["faq"])]) + "\n</head>\n"
    return head + f"""<body>
{GTM_NS}
<div class="topbar">
  <div class="container">
    <a class="brand" href="../">Kamran Arshad</a>
    <nav class="topnav">
      <a href="./">Field Notes</a>
      <a href="../#work">Case Studies</a>
      <a href="../#services">Services</a>
      <a class="btn" href="../#contact">Get Free Audit</a>
    </nav>
  </div>
</div>
<header class="post-head">
  <div class="container narrow">
    <div class="crumb"><a href="./">Field Notes</a> &nbsp;/&nbsp; {p['section']}</div>
    <h1>{p['h1']}</h1>
    <div class="byline"><span>Kamran Arshad</span><span>{DATE_H}</span><span>{p['read']} min read</span></div>
  </div>
</header>
<main>
<article>
  <div class="container narrow">
{p['body']}
    <h2>Common questions</h2>
{faq_html}
    <div class="cta">
      <h2>{p['cta_h']}</h2>
      <p>{p['cta_p']}</p>
      <a class="btn" href="../#contact">{p['cta_b']} &rarr;</a>
    </div>
{related_html(p['related'], 'Related field notes')}
  </div>
</article>
</main>
<footer>
  <div class="container">
    <span>&copy; 2026 Kamran Arshad. Paid Ads &amp; Tracking Specialist</span>
    <span><a href="../">Home</a> &middot; <a href="./">Field Notes</a> &middot; <a href="../privacy-policy.html">Privacy</a></span>
  </div>
</footer>
<script src="../consent.js" defer></script>
</body>
</html>
"""


# ---- shared proof blocks -------------------------------------------------------------------
MR_EXPERT = """    <div class="proof">
      <span class="tag">Case study</span>
      <h3>Mr Expert Carpet Cleaning, Slough UK</h3>
      <p>{text}</p>
      <p><a href="mr-expert-carpet-cleaning.html">Read the Mr Expert Carpet Cleaning case study &rarr;</a></p>
    </div>"""

SAME_EVERYWHERE = "The fundamentals don't change with the country. Clicks and leads cost more in the UK and the US, which makes wasted spend more expensive and clean tracking more valuable."

# ---- real Keyword Planner data, loaded from the saved raw export (never retyped)
_raw = open(os.path.join(ROOT, "_i18n", "bids_2026_10.json"), encoding="utf-8").read()
BIDS = json.loads(_raw[_raw.index("{"):_raw.rindex("}") + 1])
UK_B = {r[0]: r for r in BIDS["United Kingdom"]["rows"]}
US_B = {r[0]: r for r in BIDS["United States"]["rows"]}


def bid_range(r):
    return f"{r[6]} to {r[7]}" if r[6] not in ("—", "") else "no estimate"


def vol_cell(v):
    # Thin space: reads correctly in every language, unlike a comma or a dot.
    return v.replace(",", "&#8239;")


def market_table(keys):
    rows = "\n".join(
        f'          <tr><td>{k}</td><td>{vol_cell(UK_B[k][1])}</td><td>{bid_range(UK_B[k])}</td><td>{vol_cell(US_B[k][1])}</td><td>{bid_range(US_B[k])}</td></tr>'
        for k in keys)
    return f"""    <div class="tbl-wrap">
      <table>
        <thead><tr><th>Search</th><th>UK searches/month</th><th>UK top-of-page bid</th><th>US searches/month</th><th>US top-of-page bid</th></tr></thead>
        <tbody>
{rows}
        </tbody>
      </table>
    </div>
    <p>Source: Google Ads Keyword Planner, checked 30 October 2026, average monthly searches for October 2025 to September 2026. Bids are Google's low and high estimates in pounds, because that is the account's currency. They are estimates and not what you would actually pay.</p>"""


def clicks(key, table, budget=1000):
    r = table[key]
    lo, hi = float(r[6].lstrip("£")), float(r[7].lstrip("£"))
    return int(budget // hi), int(budget // lo)


SERVICE_PAGES = [
{
 "slug": "google-ads-for-dentists", "crumb": "Google Ads for dentists",
 "title": "Google Ads for Dentists: PPC for Dental Practices | Kamran Arshad",
 "desc": "Google Ads for dental practices: search campaigns by treatment, local targeting, and calls and forms tracked back to the keyword. From a real dental clinic rebuild.",
 "svc_name": "Google Ads for dental practices", "svc_type": "Dental PPC and Google Ads management",
 "h1": "Google Ads for dentists: fill the chair with the treatments you want more of",
 "body": f"""    <div class="answer">
      <p>A dental practice doesn't need more clicks. It needs more enquiries for the treatments that pay, from people close enough to come in, and a way to see which searches produced them.</p>
      <p>I rebuild and run Google Ads accounts, and I have done it for a dental clinic: ad groups by treatment, with form submissions and phone calls tracked as conversions.</p>
    </div>
    <h2>What I would set up for your practice</h2>
    <div class="cause">
      <div class="cause-h"><span class="rank">01</span><h3>Campaigns split by treatment</h3></div>
      <p>Someone searching for implants and someone searching for a check-up are different patients with very different value. Implants, whitening, cleaning and emergency searches each get their own ad groups, ads and budget decisions.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">02</span><h3>Location targeting set to your catchment</h3></div>
      <p>Your ads only show where patients can realistically reach you. This sounds basic, but it is one of the first things I check, because the wrong default setting can spend budget far outside your area.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">03</span><h3>A negative keyword list</h3></div>
      <p>Dental searches attract people looking for jobs, courses, free treatment and information. A maintained negative list stops those clicks before you pay for them.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">04</span><h3>Calls and forms counted as conversions</h3></div>
      <p>Enquiries usually arrive by phone or form. Both are tracked through Google Tag Manager and imported into Google Ads, so bidding works towards patient enquiries and not just visits.</p>
    </div>
    <h2>What dental clicks cost right now</h2>
{market_table(["dentist near me", "dental implants", "invisalign", "teeth whitening"])}
    <p>The gap between treatments is why I split campaigns. Compare the high estimate for implants with whitening in the UK, then ask which one you would rather fill your diary with.</p>
    <h2>Direct dental experience</h2>
    <div class="proof">
      <span class="tag">Case study</span>
      <h3>Smile Line Dental</h3>
      <p>The clinic was already paying for Google Ads, but campaigns were targeting worldwide, Search and Display were mixed together, there were no negative keywords, and neither forms nor calls were tracked.</p>
      <p>I completed advertiser verification, rebuilt the account as Search only, split ad groups by service, set local targeting, built the negative list and added tracking. For the first time, the clinic could see which ads and keywords were producing patient enquiries.</p>
      <p><a href="smile-line-dental.html">Read the Smile Line Dental case study &rarr;</a></p>
    </div>
    <p>{SAME_EVERYWHERE} A dental account leaks money in the same places wherever it runs: broad targeting, irrelevant searches and enquiries nobody is counting.</p>
    <h2>What a dental account should be able to answer</h2>
    <ol class="steps">
      <li><b>Which treatments bring enquiries?</b>Spend and enquiries per treatment, so budget can follow the work you want.</li>
      <li><b>Which searches brought them?</b>The actual search terms behind each enquiry, reviewed and cleaned regularly.</li>
      <li><b>What does an enquiry cost?</b>Measured from your own tracked calls and forms, not from an industry average.</li>
      <li><b>Which enquiries became patients?</b>If your practice records this, it can be fed back to Google Ads so bidding learns from real bookings.</li>
    </ol>""",
 "faq": [
  ("Do you only work with dentists?", "No. I also run marketing for a UK carpet cleaning company and have worked on online stores. Dental is one of the areas where I have direct account experience."),
  ("Can you guarantee a number of new patients?", "No, and be careful with anyone who does. Results depend on your location, competition, offer and how enquiries are handled. What I can promise is a clean account and honest tracking of what it produces."),
  ("Do you also help with Google Maps?", "Yes. Many patients choose from the Maps results, so I can work on your Google Business Profile and local pages alongside your ads."),
  ("How does working with you start?", "With a free audit of your ad account, website and tracking. You get the findings in plain language before you decide anything, and you keep ownership of your Google Ads account."),
 ],
 "cta_h": "Do you know which searches bring your patients?",
 "cta_p": "Send me your practice website. I'll review your ads and tracking and tell you the first things I'd fix.",
 "cta_b": "Get my free dental ads audit",
 "related": [
  ("smile-line-dental.html", "Smile Line Dental case study", "A dental clinic's Google Ads rebuild and first-ever lead tracking."),
  ("google-ads-management.html", "Google Ads management", "Search campaigns with call and form tracking."),
  ("med-spa-marketing.html", "Med spa marketing", "Ads for aesthetic clinics, within Google and Meta rules."),
  ("blog/google-ads-account-audit-lead-generation.html", "Google Ads Account Audit Checklist", "Six checks, taken from rebuilding a dental clinic's account."),
 ],
},
{
 "slug": "marketing-for-plumbers", "crumb": "Marketing for plumbers",
 "title": "Marketing for Plumbers: Google Ads, Maps and SEO | Kamran Arshad",
 "desc": "Marketing for plumbing companies: Google Ads, Local Services Ads, Google Maps and service pages, tracked to the calls that become jobs. Free audit.",
 "svc_name": "Marketing for plumbing companies", "svc_type": "Google Ads and local SEO for plumbers",
 "h1": "Marketing for plumbers: more of the calls that turn into paid jobs",
 "body": f"""    <div class="answer">
      <p>Plumbing marketing comes down to being visible at the moment something leaks, and answering fast. Someone with a leak is unlikely to spend long comparing options.</p>
      <p>I run Google Ads, Local Services Ads, the Google Maps profile and service pages for a UK carpet cleaning company, with calls and forms tracked. That is the system I would bring to a plumbing company.</p>
    </div>
    <h2>Where I'd start for a plumbing company</h2>
    <div class="cause">
      <div class="cause-h"><span class="rank">01</span><h3>Google Ads for urgent and high-value work</h3></div>
      <p>Emergency call-outs, boiler or water heater work and bathroom installs behave very differently. Each gets its own ad groups, so you can bid hard on the jobs you want and leave out the ones you don't.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">02</span><h3>Local Services Ads where they're available</h3></div>
      <p>These charge per lead instead of per click and can appear prominently in Search. I have hands-on experience here: I set up the account and run Local Services Ads for a UK carpet cleaning company.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">03</span><h3>Google Maps and your Business Profile</h3></div>
      <p>Categories, services, service areas, photos and a steady flow of reviews decide how often you appear when someone nearby searches for a plumber.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">04</span><h3>A page for each service and area</h3></div>
      <p>One homepage can't rank for drain unblocking, leak repair and five nearby towns. Separate pages give Google and your customer an exact match.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">05</span><h3>Tracking down to the booked job</h3></div>
      <p>A tap on your phone number isn't a customer. Connected calls and forms are tracked, and booked jobs can be sent back to Google Ads so it learns which searches bring real work.</p>
    </div>
    <h2>What plumbing clicks cost</h2>
{market_table(["emergency plumber", "plumber near me", "blocked drain"])}
    <p>At the high end of those estimates, one missed emergency call can throw away an expensive click. That is why I would look at how calls get answered before raising any budget.</p>
    <h2>The system I run today</h2>
    {MR_EXPERT.format(text="I haven't run a plumbing account yet. What I do run is this system for a UK carpet cleaning company: the website, service and area pages, Google Ads, Local Services Ads, the Business Profile and server-side tracking, plus a custom plugin that sends booked job values back to Google Ads.")}
    <p>The customer journey is the same: a local search, a phone call or a form, then a job in the diary. The keywords and the cost per lead are different. Keyword Planner gives a first estimate, and only your own tracked results can give the real number.</p>
    <h2>Questions worth asking any plumbing marketing agency</h2>
    <ol class="steps">
      <li><b>Who owns the ad account?</b>It should be you, so your history stays with you if you ever leave.</li>
      <li><b>Are leads shared with other plumbers?</b>Some lead services sell one enquiry to several companies. Your own ads and pages only bring leads to you.</li>
      <li><b>What counts as a conversion?</b>Ask whether it means a connected call, or just a tap on a phone number.</li>
      <li><b>Can I see the search terms?</b>You should be able to see exactly what people searched before they called.</li>
    </ol>""",
 "faq": [
  ("Have you worked with plumbers before?", "Not yet. I run the same Google Ads, Maps, website and tracking system for a UK carpet cleaning company, which has the same call-led customer journey. I'm telling you that upfront so you can judge the fit for yourself."),
  ("Should a plumber use Google Ads or Local Services Ads?", "Often both. Local Services Ads charge per lead and need little setup, while Google Ads gives you more control over the jobs and areas you target. The audit will tell you what fits your area and budget."),
  ("How does working with you start?", "With a free audit of your ads, Maps listing and website. You get the findings in plain language before you decide anything."),
 ],
 "cta_h": "Where are your plumbing jobs really coming from?",
 "cta_p": "Send me your website and main service area. I'll check your ads, Maps listing and tracking, and tell you the first things I'd fix.",
 "cta_b": "Get my free plumbing marketing audit",
 "related": [
  ("blog/how-to-get-more-plumbing-leads.html", "How to get more plumbing leads", "Buying leads or generating your own, and how each one works."),
  ("blog/local-services-ads-vs-google-ads.html", "Local Services Ads vs Google Ads", "Billing, control and when to use each."),
  ("mr-expert-carpet-cleaning.html", "Mr Expert Carpet Cleaning case study", "Full digital build for a UK local service business."),
  ("local-seo-services.html", "Local SEO services", "Google Business Profile, service pages and indexing fixes."),
 ],
},
{
 "slug": "hvac-marketing", "crumb": "HVAC marketing",
 "title": "HVAC Marketing: Google Ads and Leads for Contractors | Kamran Arshad",
 "desc": "HVAC marketing for heating and cooling contractors: Google Ads, Local Services Ads and Maps, planned around peak season and tracked to booked jobs. Free audit.",
 "svc_name": "Marketing for HVAC contractors", "svc_type": "Google Ads and local SEO for heating and cooling companies",
 "h1": "HVAC marketing: your own leads, through the busy season and the quiet one",
 "body": f"""    <div class="answer">
      <p>HVAC demand swings with the weather. Marketing that runs the same all year overspends when you're fully booked and goes quiet when you most need the work.</p>
      <p>I run Google Ads, Local Services Ads, the Google Maps profile and service pages for a UK carpet cleaning company, with calls and forms tracked. An HVAC account would use the same system, planned around your seasons.</p>
    </div>
    <h2>How I'd plan the account around the seasons</h2>
    <div class="cause">
      <div class="cause-h"><span class="rank">01</span><h3>Budgets that follow the season</h3></div>
      <p>Repair demand tends to rise in very hot or very cold weather. Budgets and ad schedules can be adjusted around your capacity, so you aren't paying for calls your team can't take.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">02</span><h3>Repairs and replacements kept apart</h3></div>
      <p>A broken system needs someone quickly, while a replacement buyer may compare quotes for longer and the job is usually worth more. Separate campaigns let each get the right ad, page and bid.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">03</span><h3>Your own leads instead of shared ones</h3></div>
      <p>Bought HVAC leads can be useful for filling gaps, but they may also go to your competitors. Your own ads, Maps listing and pages bring enquiries to you alone.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">04</span><h3>Local Services Ads and Google Maps</h3></div>
      <p>Pay-per-lead ads and a strong Business Profile put you in front of people ready to call. I have hands-on experience with both, including setting up and running Local Services Ads for a UK carpet cleaning company.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">05</span><h3>Tracking down to the booked job</h3></div>
      <p>Connected calls and forms are tracked by source. Booked jobs and their value can go back to Google Ads, so it learns the difference between a quick repair and a full installation.</p>
    </div>
    <h2>Why waste matters more in HVAC</h2>
{market_table(["ac repair", "hvac repair", "furnace repair", "boiler repair"])}
    <p>US bids here are some of the highest in the 21 searches I checked for local businesses. Note the different words too: "boiler repair" and "ac repair" are very different markets in the UK and the US, so the keyword list has to follow your country.</p>
    <h2>The system I would bring</h2>
    {MR_EXPERT.format(text="There is no HVAC account in my case studies yet. The system I would bring is the one I run for a UK carpet cleaning company: the website, service and area pages, Google Ads, Local Services Ads, the Business Profile and server-side tracking, plus a custom plugin that sends booked job values back to Google Ads.")}
    <p>The structure carries over directly: local search, then a call or form, then a booked job. Seasonality and job value are what change most for HVAC, and they shape how the account is planned from the start.</p>
    <h2>What to check before hiring an HVAC marketing agency</h2>
    <ol class="steps">
      <li><b>Do you own the accounts?</b>Your ad account, website and call data should stay yours.</li>
      <li><b>Is the contract tied to results you can see?</b>Long contracts are hard to judge without tracking you can check yourself.</li>
      <li><b>Are repairs and installs reported separately?</b>A blended cost per lead hides which work actually pays.</li>
      <li><b>What happens in the quiet season?</b>Ask for a plan for slow months, not just the peak.</li>
    </ol>""",
 "faq": [
  ("Have you worked with HVAC companies before?", "Not yet. I run the same Google Ads, Maps, website and tracking system for a UK carpet cleaning company. The call-led customer journey is the same, and I'm telling you upfront so you can judge the fit."),
  ("Are HVAC leads better bought or generated?", "Bought leads are quick but may be shared with competitors, and you stop getting them when you stop paying. Your own ads and pages take longer to set up, but the leads are yours. Many companies use both while their own channels build up."),
  ("How does working with you start?", "With a free audit of your ads, Maps listing and website. You get the findings in plain language before you decide anything."),
 ],
 "cta_h": "Are you paying for calls you can't take?",
 "cta_p": "Send me your website and service area. I'll check your ads, Maps listing and tracking, and tell you the first things I'd fix.",
 "cta_b": "Get my free HVAC marketing audit",
 "related": [
  ("blog/local-services-ads-vs-google-ads.html", "Local Services Ads vs Google Ads", "Billing, control and when to use each."),
  ("mr-expert-carpet-cleaning.html", "Mr Expert Carpet Cleaning case study", "Full digital build for a UK local service business."),
  ("google-ads-management.html", "Google Ads management", "Search campaigns with call and form tracking."),
  ("blog/google-ads-call-tracking-local-business.html", "Google Ads Call Tracking for Local Service Businesses", "How to count the calls that turn into jobs."),
 ],
},
{
 "slug": "roofing-marketing", "crumb": "Roofing marketing",
 "title": "Roofing Marketing: Google Ads for Roofers | Kamran Arshad",
 "desc": "Roofing marketing that goes beyond bought leads: Google Ads, Local Services Ads, Maps, and tracking from the first call to the signed job. Free audit.",
 "svc_name": "Marketing for roofing companies", "svc_type": "Google Ads and local SEO for roofers",
 "h1": "Roofing marketing: fewer shared leads, more signed jobs from your own channels",
 "body": f"""    <div class="answer">
      <p>A roof is a big decision. Homeowners often compare several quotes and take time to choose, so a low cost per lead means little if those leads never sign.</p>
      <p>I run Google Ads, Local Services Ads, the Google Maps profile and service pages for a UK carpet cleaning company, with booked jobs sent back to Google Ads. A roofing account would use the same system.</p>
    </div>
    <h2>What I'd change first for a roofing company</h2>
    <div class="cause">
      <div class="cause-h"><span class="rank">01</span><h3>Repairs and replacements kept apart</h3></div>
      <p>A leak needs someone quickly, while a full replacement is a high-value job with a longer decision. Each gets its own campaign, landing page and budget so one can't quietly eat the other's money.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">02</span><h3>Your own enquiries, not shared lists</h3></div>
      <p>Bought roofing leads can be sold to several companies at once, which turns the job into a race on price. Your own ads and pages bring the homeowner to you first.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">03</span><h3>Trust on the page where they decide</h3></div>
      <p>Real photos of your jobs, reviews, accreditations and clear service areas matter for a purchase this size. A generic template page wastes the click you paid for.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">04</span><h3>Google Maps and Local Services Ads</h3></div>
      <p>A strong Business Profile and pay-per-lead ads put you in front of people ready to call. I have hands-on experience with both, including setting up and running Local Services Ads for a UK carpet cleaning company.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">05</span><h3>Tracking past the first call</h3></div>
      <p>Long sales cycles need more than a lead count. Signed jobs and their value can be sent back to Google Ads, so it learns which searches lead to real roofs and not just quote requests.</p>
    </div>
    <h2>What roofing clicks cost</h2>
{market_table(["roof repair", "roofer near me", "roof replacement"])}
    <p>When a single click can carry an estimate like these, judging the account on cost per lead alone isn't enough. What matters is what a signed job earns against what it cost to win.</p>
    <h2>What I can show you</h2>
    {MR_EXPERT.format(text="I don't have a roofing client to show you. I can show you the system I run for a UK carpet cleaning company: the website, service and area pages, Google Ads, Local Services Ads, the Business Profile and server-side tracking, plus a custom plugin that sends booked job values back to Google Ads.")}
    <p>The mechanics carry over directly. The difference with roofing is job value and decision time, so I'd judge the account on signed work and not on the number of leads.</p>
    <h2>What to ask a roofing marketing agency</h2>
    <ol class="steps">
      <li><b>Are these leads exclusive?</b>Ask directly whether any other roofer receives the same enquiry.</li>
      <li><b>Do you report on signed jobs?</b>A report that stops at leads can't tell you whether the ads are profitable.</li>
      <li><b>Who owns the ad account and website?</b>If you leave, your history and pages should stay with you.</li>
      <li><b>Will the page show my real work?</b>Stock photos and shared templates don't build trust for a job this size.</li>
    </ol>""",
 "faq": [
  ("Have you worked with roofers before?", "Not yet. I run the same Google Ads, Maps, website and tracking system for a UK carpet cleaning company. The call-led journey is the same, and I'm telling you upfront so you can judge the fit."),
  ("Should roofers buy leads?", "Bought leads can fill gaps quickly, but they may be shared and they stop when you stop paying. Your own ads and pages take longer to build, but the enquiries come to you alone. Many roofers use both at first."),
  ("How does working with you start?", "With a free audit of your ads, Maps listing and website. You get the findings in plain language before you decide anything."),
 ],
 "cta_h": "Are your leads turning into signed roofs?",
 "cta_p": "Send me your website and service area. I'll check your ads, Maps listing and tracking, and tell you the first things I'd fix.",
 "cta_b": "Get my free roofing marketing audit",
 "related": [
  ("blog/google-ads-offline-conversions-booked-jobs.html", "Google Ads Offline Conversions for Lead-Gen Businesses", "Telling Google Ads which leads became booked jobs."),
  ("blog/local-services-ads-vs-google-ads.html", "Local Services Ads vs Google Ads", "Billing, control and when to use each."),
  ("mr-expert-carpet-cleaning.html", "Mr Expert Carpet Cleaning case study", "Full digital build for a UK local service business."),
  ("local-seo-services.html", "Local SEO services", "Google Business Profile, service pages and indexing fixes."),
 ],
},
{
 "slug": "med-spa-marketing", "crumb": "Med spa marketing",
 "title": "Med Spa Marketing: Google and Meta Ads, Within the Rules | Kamran Arshad",
 "desc": "Med spa and aesthetic clinic marketing: Google Ads, Meta Ads and local SEO, planned around advertising policy and tracked to booked consultations. Free audit.",
 "svc_name": "Marketing for med spas and aesthetic clinics", "svc_type": "Google Ads and Meta Ads for med spas",
 "h1": "Med spa marketing: more booked consultations, inside Google's and Meta's rules",
 "body": f"""    <div class="answer">
      <p>Med spa advertising is different because the platforms restrict what you can say. A campaign written like any other can be disapproved, and repeated problems can put the whole account at risk.</p>
      <p>I build Google and Meta campaigns with tracking from enquiry onwards. For a clinic, I would plan them around those rules from the start.</p>
    </div>
    <h2>The rules that shape a med spa campaign</h2>
    <div class="note">
      <b class="l">Checked on Google's and Meta's policy pages, October 2026</b>
      <p>These rules change and depend on the country, so check them again before any campaign. This is practical guidance and not legal advice. Medical advertising also has its own local regulations.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">01</span><h3>Prescription drug terms on Google</h3></div>
      <p>Google restricts prescription drug terms in ads, landing pages and keywords. Campaigns targeting the US, Canada or New Zealand may use them promotionally under local law, but keyword-targeting them needs certification. Elsewhere, including the UK and Australia, promotional use isn't allowed. If a treatment uses a prescription drug, check its name against Google's list before using it in ads or on the landing page.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">02</span><h3>Age targeting and wording on Meta</h3></div>
      <p>Meta requires ads for cosmetic procedures to target people aged 18 or over. It also bars statements of inferiority about someone's appearance, so copy has to sell the outcome without attacking how the reader looks.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">03</span><h3>Before-and-after images</h3></div>
      <p>Meta's policy allows before-and-after images for general cosmetic procedures when the ad targets adults and avoids negative messaging. Check the current wording and your local medical advertising rules before using them.</p>
    </div>
    <h2>What I would set up for a clinic</h2>
    <ol class="steps">
      <li><b>Google Ads for treatment searches</b>People searching for a treatment near them are the closest to booking, so these campaigns are split by treatment and location.</li>
      <li><b>Meta Ads for local awareness</b>Facebook and Instagram are visual channels that suit consultations and seasonal offers, with creative written to meet the policy.</li>
      <li><b>A local presence on Maps</b>A complete Business Profile, reviews and a page for each treatment help you get found by people nearby.</li>
      <li><b>Tracking to the consultation</b>Calls, forms and booking requests are tracked by source, so you can see what each channel really brings.</li>
    </ol>
    <h2>What aesthetic searches look like</h2>
{market_table(["botox near me", "lip filler"])}
    <p>Search demand and a bid estimate don't mean you are allowed to advertise a term. Check the policy first, because the rules above still apply.</p>
    <h2>Experience this draws on</h2>
    <div class="proof">
      <span class="tag">Case study</span>
      <h3>Smile Line Dental</h3>
      <p>A clinic account rebuilt with local targeting, a negative keyword list and call and form tracking. For the first time, the clinic could see which ads and keywords were producing patient enquiries.</p>
      <p><a href="smile-line-dental.html">Read the Smile Line Dental case study &rarr;</a></p>
    </div>
    <div class="proof">
      <span class="tag">Case study</span>
      <h3>The Body Essential</h3>
      <p>Meta campaigns for a fashion store, where a pixel audit found about 100 reported orders against 55 to 70 real ones. Roughly 30 to 40% of the daily budget had been chasing conversions that didn't exist.</p>
      <p><a href="the-body-essential.html">Read The Body Essential case study &rarr;</a></p>
    </div>
    <p>I haven't run a med spa account yet. Clinic lead generation and clean Meta tracking are the parts I bring directly. The policy limits above are the part that's specific to your industry. {SAME_EVERYWHERE}</p>""",
 "faq": [
  ("Can a med spa advertise on Google Ads?", "Yes, but with limits. Prescription drug terms are restricted, and the rules depend on the countries you target. Campaigns need to be planned around Google's healthcare policy for your location."),
  ("Can med spas use before-and-after photos in Facebook ads?", "Meta's policy allows them for general cosmetic procedures when the ad targets people aged 18 or over and avoids negative messaging about appearance. Local medical advertising rules may be stricter, so check those too."),
  ("Have you worked with med spas before?", "Not yet. I have direct experience with clinic lead generation and Meta Ads, and I'm telling you upfront so you can judge the fit for yourself."),
  ("How does working with you start?", "With a free audit of your ads, website and tracking. You get the findings in plain language before you decide anything."),
 ],
 "cta_h": "Are your clinic's ads working, and within the rules?",
 "cta_p": "Send me your website. I'll review your ads, landing pages and tracking, and tell you the first things I'd fix.",
 "cta_b": "Get my free clinic ads audit",
 "related": [
  ("google-ads-for-dentists.html", "Google Ads for dentists", "Campaigns by treatment, tracked to patient enquiries."),
  ("meta-ads-management.html", "Meta Ads management", "Facebook and Instagram campaigns with clean tracking."),
  ("smile-line-dental.html", "Smile Line Dental case study", "A clinic's Google Ads rebuild and first-ever lead tracking."),
  ("the-body-essential.html", "The Body Essential case study", "A pixel audit that found phantom purchases."),
 ],
},
{
 "slug": "meta-ads-for-shopify-brands", "crumb": "Meta ads for Shopify",
 "title": "Meta Ads for Shopify Brands: Scale on Real Orders | Kamran Arshad",
 "desc": "Meta ads for Shopify brands, judged on real orders and not on reported ROAS. Pixel and Conversions API checks, then campaigns you can trust enough to scale.",
 "svc_name": "Meta ads for Shopify brands", "svc_type": "Facebook and Instagram ads for Shopify stores",
 "h1": "Meta ads for Shopify brands: scale on the orders you can actually count",
 "body": f"""    <div class="answer">
      <p>Before a Shopify brand spends more on Meta, it needs to know whether the numbers in Ads Manager match the orders in Shopify. Often they don't, and bigger budgets then flow to the wrong campaigns.</p>
      <p>I have run Facebook and Instagram ads for Shopify stores, and I start by checking reported purchases against real orders, so scaling decisions rest on numbers you can trust.</p>
    </div>
    <h2>Where I start with a Shopify brand</h2>
    <div class="cause">
      <div class="cause-h"><span class="rank">01</span><h3>Reconcile Meta against Shopify</h3></div>
      <p>I compare reported purchases with real orders. A gap isn't always a fault, because attribution windows differ, but you need to know how big it is and why.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">02</span><h3>Clean up the pixel and Conversions API</h3></div>
      <p>Duplicate pixels, app-installed tags and events sent twice all distort what Meta optimises towards. These get fixed before any budget moves.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">03</span><h3>Test products and creative on real margin</h3></div>
      <p>The best-looking ROAS can come from a product that loses money after costs and returns. I judge tests on the orders that actually get paid, not on what the platform reports about itself.</p>
    </div>
    <div class="cause">
      <div class="cause-h"><span class="rank">04</span><h3>Then scale what holds up</h3></div>
      <p>Budget moves to campaigns that still work once the data is clean. You get a short update every week.</p>
    </div>
    <h2>E-commerce experience behind this</h2>
    <div class="proof">
      <span class="tag">Case study</span>
      <h3>The Body Essential</h3>
      <p>A fashion brand on Shopify. Two pixels were installed, and one, added by a third-party app, was reporting purchases that never happened: about 100 orders in Meta against 55 to 70 real ones. Roughly 30 to 40% of the daily budget had been chasing them. I fixed the tracking, built the Shopify store and ran the Meta campaigns.</p>
      <p><a href="the-body-essential.html">Read The Body Essential case study &rarr;</a></p>
    </div>
    <div class="proof">
      <span class="tag">Case study</span>
      <h3>AlphaMart</h3>
      <p>A Shopify store I built and ran solo, with my own money on the line, advertising on Snapchat, Meta and TikTok. I traced every order from click to cash: the ad accounts reported 1,092 orders, and 523 became delivered, paid sales. That habit of checking past the dashboard is what I bring to your account.</p>
      <p><a href="alphamart.html">Read the AlphaMart case study &rarr;</a></p>
    </div>
    <p>{SAME_EVERYWHERE} The same is true of e-commerce: the ad platform, the pixel and the store work the same way, and reported numbers need checking everywhere.</p>""",
 "faq": [
  ("Why doesn't Meta match my Shopify orders?", "Some difference is normal, because Meta counts by its attribution window and Shopify counts orders when they happen. A large gap often points to a duplicate pixel, an app adding its own tracking or purchase events firing twice."),
  ("Do you work with stores on any platform?", "The e-commerce work in my case studies is on Shopify, so that is where I can help most directly."),
  ("Do you run Google Shopping as well?", "My e-commerce ad experience is on Meta and Snapchat, so that is what I offer. I run Google Ads for lead generation businesses, and I'd rather be clear about that than overclaim."),
  ("How does working with you start?", "With a free audit of your ad account, pixel and Conversions API setup. You get the findings in plain language before you decide anything."),
 ],
 "cta_h": "Does your Ads Manager match your Shopify orders?",
 "cta_p": "Send me your store URL. I'll check your pixel and tracking setup and tell you the first things I'd fix.",
 "cta_b": "Get my free Meta ads audit",
 "related": [
  ("blog/meta-ads-more-sales-than-shopify.html", "Meta Says 100 Orders. Shopify Says 62.", "Which one is lying, and how to find out."),
  ("blog/scaling-meta-campaigns-bad-data.html", "You Cannot Scale a Campaign You Cannot Trust", "What bad data does to your budget."),
  ("ecommerce-ppc-management.html", "Ecommerce PPC management", "Meta and Snapchat ads checked against real orders."),
  ("meta-ads-management.html", "Meta Ads management", "Facebook and Instagram campaigns with clean tracking."),
 ],
},
]

BLOG_PAGES = [
{
 "slug": "google-ads-cost-local-service-business", "section": "Google Ads", "crumb": "What Google Ads cost a local business", "read": 6,
 "title": "How Much Do Google Ads Cost a Local Service Business?",
 "desc": "Real Keyword Planner bids for plumbers, roofers, HVAC, dentists and cleaners in the UK and US, what a budget buys, and how to work out your cost per job.",
 "h1": "How much Google Ads cost a local service business, using real bid data",
 "body": f"""    <div class="answer">
      <p>There is no standard price. You set your own budget and pay per click, and the price of a click depends on your trade and country. In Google's estimates from October 2026, a top-of-page click for "plumber near me" ran from {UK_B['plumber near me'][6]} to {UK_B['plumber near me'][7]} in the UK and from {US_B['plumber near me'][6]} to {US_B['plumber near me'][7]} in the US.</p>
      <p>The useful number isn't the cost per click. It's the cost per booked job, and only your own tracking can tell you that.</p>
    </div>
    <p>Many of the cost guides I read while researching this came from agencies, with wide ranges and little data behind them. So I pulled figures from Google Ads Keyword Planner myself for 21 searches local businesses compete on. Twelve of them are below.</p>
    <h2>What clicks are estimated to cost, by trade</h2>
{market_table(['plumber near me', 'emergency plumber', 'roofer near me', 'roof repair', 'hvac repair', 'ac repair', 'boiler repair', 'electrician near me', 'pest control', 'carpet cleaning', 'dentist near me', 'dental implants'])}
    <p>Three things stand out. US bids are well above UK bids for most of these searches. Urgent searches can cost far more than general ones: compare "emergency plumber" with "plumber near me" on the high end. And some trades are much cheaper than others: "carpet cleaning" sits well below "roofer near me" in both countries.</p>
    <h2>What those bids mean for a budget</h2>
    <p>A monthly budget divided by the click price gives you a rough number of clicks. Using the estimates above, and only as a guide, £1,000 a month would buy roughly:</p>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th>Search</th><th>UK clicks for £1,000</th><th>US clicks for £1,000</th></tr></thead>
        <tbody>
          <tr><td>plumber near me</td><td>{clicks('plumber near me', UK_B)[0]:,} to {clicks('plumber near me', UK_B)[1]:,}</td><td>{clicks('plumber near me', US_B)[0]} to {clicks('plumber near me', US_B)[1]}</td></tr>
          <tr><td>roofer near me</td><td>{clicks('roofer near me', UK_B)[0]} to {clicks('roofer near me', UK_B)[1]}</td><td>{clicks('roofer near me', US_B)[0]} to {clicks('roofer near me', US_B)[1]}</td></tr>
          <tr><td>carpet cleaning</td><td>{clicks('carpet cleaning', UK_B)[0]:,} to {clicks('carpet cleaning', UK_B)[1]:,}</td><td>{clicks('carpet cleaning', US_B)[0]} to {clicks('carpet cleaning', US_B)[1]}</td></tr>
          <tr><td>dentist near me</td><td>{clicks('dentist near me', UK_B)[0]:,} to {clicks('dentist near me', UK_B)[1]:,}</td><td>{clicks('dentist near me', US_B)[0]} to {clicks('dentist near me', US_B)[1]}</td></tr>
        </tbody>
      </table>
    </div>
    <p>These ranges are wide because Google's estimates are wide. Actual prices depend on competition, your area, the time of day and your ad's quality, so your own account will tell you more within a few weeks.</p>
    <h2>How Google charges your budget</h2>
    <p>You set an average daily budget, and Google can spend above it on some days. According to Google's help pages, for most campaigns you won't pay more than twice your average daily budget on a given day, or more than 30.4 times it in a month. So a daily budget of £30 can spend up to £60 in one day, and up to £912 in a month.</p>
    <h2>Work out your own cost per job</h2>
    <ol class="steps">
      <li><b>Find your click price</b>Start with Keyword Planner for your own searches and area, then replace it with real data from your account.</li>
      <li><b>Measure how many clicks become enquiries</b>Count connected calls and forms, not taps on your phone number.</li>
      <li><b>Measure how many enquiries become jobs</b>Your own diary or CRM is the only source for this.</li>
      <li><b>Compare the cost per job with what a job earns</b>A costly lead can still be a bargain on a high-value job.</li>
    </ol>
    <div class="note">
      <b class="l">An example with made-up numbers</b>
      <p>Suppose clicks cost £5, one in ten clicks becomes an enquiry, and one in three enquiries becomes a job. That is £50 per enquiry and £150 per job. These numbers are only there to show the sum. They aren't a benchmark, so use your own.</p>
    </div>
    <h2>The costs on top of clicks</h2>
    <ul>
      <li><b>Management:</b> your own time, or a fee to a freelancer or agency. Ask exactly what's included each month.</li>
      <li><b>Tracking and landing pages:</b> often a one-off setup, and easy to overlook.</li>
      <li><b>Wasted clicks:</b> irrelevant searches cost real money until negative keywords remove them. On the <a href="../smile-line-dental.html">dental clinic account I rebuilt</a>, there were no negative keywords at all when I started.</li>
    </ul>
    <h2>Local Services Ads work differently</h2>
    <p>Where they're available, Local Services Ads charge per lead and not per click, so the table above doesn't apply to them. I compare the two in <a href="local-services-ads-vs-google-ads.html">Local Services Ads vs Google Ads</a>.</p>""",
 "faq": [
  ("How much should a small local business spend on Google Ads?", "There's no correct figure. Work backwards from your click price and what a job is worth, and set a budget that buys enough clicks to learn from. A budget that buys only a handful of clicks a month won't tell you much."),
  ("Why are Google Ads so expensive for plumbers and roofers?", "Advertisers bid against each other, and a single job can be worth a lot, so they're willing to pay more per click. Emergency searches in particular can carry high bids."),
  ("Is the top-of-page bid what I will pay per click?", "No. It's Google's estimate of what advertisers have paid to appear at the top of the page. Your actual cost per click depends on competition and your ad's quality."),
  ("Can Google spend more than my daily budget?", "Yes. Google says that for most campaigns it may spend up to twice your average daily budget on a given day, but no more than 30.4 times it in a month."),
 ],
 "cta_h": "Want to know what clicks cost in your own area?",
 "cta_p": "Send me your website and service area. I'll review your account and tracking, and tell you the first things I'd fix.",
 "cta_b": "Get a free Google Ads audit",
 "related": [
  ("local-services-ads-vs-google-ads.html", "Local Services Ads vs Google Ads", "Billing, control and when to use each."),
  ("google-ads-account-audit-lead-generation.html", "Google Ads Account Audit Checklist for Lead Generation", "Six checks for an account that lives on calls and forms."),
  ("google-ads-call-tracking-local-business.html", "Google Ads Call Tracking for Local Service Businesses", "How to count the calls that turn into jobs."),
  ("google-ads-freelancer-vs-agency.html", "Google Ads Freelancer vs Agency", "How to choose, and what to ask either one."),
 ],
},
{
 "slug": "local-services-ads-vs-google-ads", "section": "Local Service", "crumb": "Local Services Ads vs Google Ads", "read": 5,
 "title": "Local Services Ads vs Google Ads: Which Should You Use?",
 "desc": "Local Services Ads charge per lead and Google Ads per click. Billing, control, setup and the 2026 Performance Max move compared, from an account I run.",
 "h1": "Local Services Ads vs Google Ads: which one a local business should run",
 "body": """    <div class="answer">
      <p>Local Services Ads charge when a customer contacts you. Google Ads charge when someone clicks. Local Services Ads are simpler and focused on people ready to call, while Google Ads give you far more control over searches, areas and landing pages.</p>
      <p>For most eligible service businesses the useful question isn't which one, but which one to start with.</p>
    </div>
    <p>I've set up the account and I run Local Services Ads for a UK carpet cleaning company, alongside its Google Ads. The comparison below uses Google's own documentation for the facts and that hands-on work for the practical view.</p>
    <h2>The differences that matter</h2>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th>&nbsp;</th><th>Local Services Ads</th><th>Google Ads (Search)</th></tr></thead>
        <tbody>
          <tr><td>You pay for</td><td>Leads: a customer contacting you</td><td>Clicks on your ad</td></tr>
          <tr><td>Control</td><td>Less over audience and ad format</td><td>Extensive: budgets, keywords, targeting, format</td></tr>
          <tr><td>Website needed?</td><td>No, leads can be managed directly</td><td>Generally yes</td></tr>
          <tr><td>Who can use it</td><td>Certain categories and countries, with screening</td><td>Open to most businesses, subject to policy</td></tr>
          <tr><td>Trust badge</td><td>Can show a Google verification badge</td><td>No Google-backed badge</td></tr>
          <tr><td>Best for</td><td>People who need the service now</td><td>Reach, specific jobs and research-stage searches</td></tr>
        </tbody>
      </table>
    </div>
    <h2>When to start with Local Services Ads</h2>
    <p>They suit a business in an eligible category that wants phone calls and messages with little campaign management. They also work without a website, although I'd still want one: a customer who sees your ad will often check you out before calling.</p>
    <p>Eligibility is the first thing to check. Google limits these ads to certain service categories, and some features vary by country. Its help pages list categories such as plumbers, electricians and dentists, so look up your own category and country before planning around them.</p>
    <h2>When to start with Google Ads</h2>
    <p>Google Ads make more sense when you want to choose exactly which jobs you advertise, for example implants instead of check-ups, or boiler installs instead of small repairs. You also choose the landing page, which matters for high-value work where people compare before they call.</p>
    <p>The price of that control is management. Search terms need reviewing, negative keywords need adding and conversions need tracking. Without that upkeep, Google Ads can spend your budget on clicks that never become enquiries.</p>
    <h2>Why many businesses run both</h2>
    <p>The two aren't either-or. Google itself suggests combining them to increase visibility. A sensible order for many local businesses is this:</p>
    <ol class="steps">
      <li><b>Fix your Business Profile</b>Local Services Ads draw on your business information, and a complete profile helps your Maps visibility too.</li>
      <li><b>Start with whichever fits your goal</b>Choose Local Services Ads for fast, simple leads, or Google Ads if you need to target specific jobs.</li>
      <li><b>Track every lead by source</b>Otherwise you can't compare the two fairly.</li>
      <li><b>Add the second channel</b>Do this once the first is producing leads you can measure.</li>
    </ol>
    <h2>The change coming to Local Services Ads</h2>
    <div class="note">
      <b class="l">Moving into Google Ads</b>
      <p>Google is moving Local Services Ads into Google Ads as Performance Max campaigns with pay-per-lead goals. The first phase began in August 2026 for select US advertisers, and accounts outside the US follow in 2027. Google says you still pay per valid lead and ads stay on Search and Maps, but past performance reports won't carry over, so save them before migrating.</p>
    </div>
    <h2>What I'm not claiming</h2>
    <p>I'm not publishing lead costs or a verdict on which channel wins. Results vary by category, area and season, and one account isn't a benchmark. The honest way to decide is to run them side by side with tracking, then compare the cost of a booked job.</p>""",
 "faq": [
  ("Are Local Services Ads cheaper than Google Ads?", "Not automatically. They bill per lead instead of per click, so the two prices aren't directly comparable. Compare the cost per booked job from each channel in your own area."),
  ("Do I need a website for Local Services Ads?", "No. Google says leads can be managed directly without a website. A website still helps, because many customers check a business before calling."),
  ("Can I run Local Services Ads and Google Ads together?", "Yes. Google suggests combining them to increase visibility."),
  ("Are Local Services Ads available in my country?", "It depends on your country and category. Google limits them to certain service categories and some features vary by region, so check Google's help pages for your location."),
 ],
 "cta_h": "Not sure which one suits your business?",
 "cta_p": "Send me your website and service area. I'll look at your category and your current setup, and tell you where I'd start.",
 "cta_b": "Get a free local ads audit",
 "related": [
  ("how-to-get-more-plumbing-leads.html", "How to Get More Plumbing Leads", "Buying leads or generating your own."),
  ("google-ads-call-tracking-local-business.html", "Google Ads Call Tracking for Local Service Businesses", "How to count the calls that turn into jobs."),
  ("google-ads-offline-conversions-booked-jobs.html", "Google Ads Offline Conversions for Lead-Gen Businesses", "Telling Google Ads which leads became booked jobs."),
  ("local-seo-service-pages-service-business.html", "Local SEO Service Pages: One Page per Service and Area", "How to structure pages for Maps and organic search."),
 ],
},
{
 "slug": "how-to-get-more-plumbing-leads", "section": "Local Service", "crumb": "How to get more plumbing leads", "read": 5,
 "title": "How to Get More Plumbing Leads Without Relying on Bought Ones",
 "desc": "Six ways to get more plumbing leads, in the order I'd do them: Maps, reviews, service pages, Local Services Ads, Google Ads and call handling.",
 "h1": "How to get more plumbing leads, in the order I'd actually do it",
 "body": """    <div class="answer">
      <p>Plumbing leads come from being found at the moment of need and answering fast. Start with what you own: your Google Business Profile, reviews and service pages. Then add paid ads, and use bought leads only to fill gaps.</p>
    </div>
    <p>I haven't run a plumbing account yet. I do run this same setup for a UK carpet cleaning company, and the journey is the same: a local search, a call or a form, then a job in the diary. Your numbers will differ, but the order holds.</p>
    <h2>1. Fix your Google Business Profile</h2>
    <p>It costs nothing and it affects whether you appear on Maps. Check your primary category, list your actual services, set your service area accurately and add real photos of your work. Don't stuff keywords or town names into the business name, because that breaks Google's guidelines and risks suspension.</p>
    <h2>2. Ask for a review after every job</h2>
    <p>Reviews influence both your visibility and whether someone rings you or the next plumber. Make it a routine: send the review link by text or WhatsApp soon after the job, while the customer still remembers how relieved they were.</p>
    <h2>3. Build a page for each service and area</h2>
    <p>A single homepage can't match searches for drain unblocking, leak repair and water heaters in five nearby towns. Each main service, and each area you really cover, deserves its own useful page. Avoid copied pages with only the town name swapped, because those add little.</p>
    <h2>4. Consider Local Services Ads</h2>
    <p>Where your category and country qualify, these charge per lead and can appear prominently in Search. Google describes them as simpler to set up and needing less hands-on management, so they're a sensible first paid channel to look at. I compare them in detail in <a href="local-services-ads-vs-google-ads.html">Local Services Ads vs Google Ads</a>.</p>
    <h2>5. Run Google Ads for the jobs you most want</h2>
    <p>Google Ads let you pick your jobs, such as emergency call-outs or installs, and exclude the rest. Keep location targeting tight, add negative keywords for jobs, courses and DIY searches, and track connected calls and not just taps on your number.</p>
    <h2>6. Answer every enquiry fast</h2>
    <p>Someone with water on the floor will try the next number if you don't pick up. A missed call is a paid-for lead thrown away, so check how many you miss before you buy more traffic. A simple call-back rule or text reply can be worth more than extra ad budget.</p>
    <h2>What about buying plumbing leads?</h2>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th>&nbsp;</th><th>Bought leads</th><th>Your own channels</th></tr></thead>
        <tbody>
          <tr><td>Speed to start</td><td>Fast</td><td>Ads are fast, SEO is slower</td></tr>
          <tr><td>Exclusive to you?</td><td>Sometimes shared, so ask</td><td>Yes</td></tr>
          <tr><td>When you stop paying</td><td>Leads stop</td><td>Ads stop, but pages and reviews keep working</td></tr>
          <tr><td>Builds your brand?</td><td>Little</td><td>Yes</td></tr>
        </tbody>
      </table>
    </div>
    <p>Bought leads aren't bad. They're useful in a quiet week or while your own channels grow. The risk is depending on them, because you own nothing when they stop.</p>
    <h2>Measure before you spend more</h2>
    <p>Whichever you use, record where each job came from. A simple question on the phone is better than nothing, and proper call and form tracking is better still. Without it, you can't tell which channel to grow.</p>
    <p>I've written up how I set up that tracking in <a href="google-ads-call-tracking-local-business.html">Google Ads call tracking for local service businesses</a>.</p>""",
 "faq": [
  ("What is the fastest way to get plumbing leads?", "Paid channels are fastest: Local Services Ads where available, Google Ads, or bought leads. Your Business Profile and pages cost less over time but take longer to build up."),
  ("Are bought plumbing leads worth it?", "They can be useful for filling gaps, but check whether each lead is shared with other plumbers, and compare the cost per booked job with your other channels."),
  ("How many reviews does a plumber need?", "There's no fixed number. Look at the businesses at the top of Maps in your own area, and aim to keep adding recent reviews steadily."),
  ("Do plumbers need a website?", "Local Services Ads can run without one, but a website lets you rank for specific services and areas and gives customers somewhere to check you out."),
 ],
 "cta_h": "Want this order applied to your plumbing business?",
 "cta_p": "Send me your website and service area. I'll check your Maps listing, ads and tracking, and tell you the first things I'd fix.",
 "cta_b": "Get a free plumbing marketing audit",
 "related": [
  ("../marketing-for-plumbers.html", "Marketing for plumbers", "What I'd set up for a plumbing company."),
  ("local-services-ads-vs-google-ads.html", "Local Services Ads vs Google Ads", "Billing, control and when to use each."),
  ("local-seo-service-pages-service-business.html", "Local SEO Service Pages: One Page per Service and Area", "How to structure pages for Maps and organic search."),
  ("google-ads-account-audit-lead-generation.html", "Google Ads Account Audit Checklist for Lead Generation", "Six checks for an account that lives on calls and forms."),
 ],
},
{
 "slug": "google-ads-freelancer-vs-agency", "section": "Google Ads", "crumb": "Google Ads freelancer vs agency", "read": 5,
 "title": "Google Ads Freelancer vs Agency: How to Choose",
 "desc": "When a Google Ads freelancer beats an agency, when it doesn't, and the questions to ask either one. I sell this service myself, so weigh that bias.",
 "h1": "Google Ads freelancer vs agency: an honest way to choose",
 "body": """    <div class="answer">
      <p>A freelancer usually gives you direct access to the person doing the work, with less overhead. An agency usually gives you a team, more capacity and cover when someone is away. The right choice depends on your account's size and how much you need beyond ads.</p>
      <p>I sell Google Ads management myself, so I'm not neutral. I've tried to show where an agency really is the better choice.</p>
    </div>
    <h2>The trade-offs</h2>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th>&nbsp;</th><th>Freelancer</th><th>Agency</th></tr></thead>
        <tbody>
          <tr><td>Who does the work</td><td>The person you speak to</td><td>Often a team, and sometimes a junior</td></tr>
          <tr><td>Capacity</td><td>Limited to one person</td><td>Can add people as you grow</td></tr>
          <tr><td>Holiday or illness</td><td>A real risk, so ask about cover</td><td>Usually covered</td></tr>
          <tr><td>Range of skills</td><td>Varies by person</td><td>Often design, copy and analytics in-house</td></tr>
          <tr><td>Overhead in the fee</td><td>Usually lower</td><td>Usually higher</td></tr>
        </tbody>
      </table>
    </div>
    <h2>When a freelancer makes more sense</h2>
    <ul>
      <li>You run a single local business or a small set of campaigns.</li>
      <li>You want to speak directly to whoever is changing your account.</li>
      <li>You already have a website and just need ads and tracking done properly.</li>
    </ul>
    <h2>When an agency makes more sense</h2>
    <ul>
      <li>You advertise across many locations, or spend at a level that needs several specialists.</li>
      <li>You need creative, video, landing pages and ads produced under one roof.</li>
      <li>You can't accept any gap in cover, whatever happens to one person.</li>
    </ul>
    <h2>Be careful with marketplace pricing</h2>
    <p>Freelance marketplaces list ad management gigs at low starting prices. Some sellers may well be capable, but a low fixed price is unlikely to pay for ongoing search term reviews, conversion tracking and regular changes. Before comparing prices, compare what is actually included each month.</p>
    <h2>Questions to ask either one</h2>
    <ol class="steps">
      <li><b>Who owns the Google Ads account?</b>It should be you. Walk away if the account stays with them when you leave.</li>
      <li><b>Who will work on my account each week?</b>Get a name, and ask how much of the work is theirs.</li>
      <li><b>What counts as a conversion?</b>Ask for connected calls and real enquiries, not page views or taps.</li>
      <li><b>Can I see the search terms and the changes made?</b>Both are in your account, and you should be able to see them at any time.</li>
      <li><b>Can you show me a similar account?</b>Ask what they changed and what they can honestly show for it.</li>
      <li><b>What happens if I want to stop?</b>Check the notice period and how you get your data back.</li>
    </ol>
    <h2>Red flags, from either side</h2>
    <ul>
      <li>Guaranteed first position or a guaranteed number of leads.</li>
      <li>Reports showing only clicks and impressions.</li>
      <li>A refusal to give you access to your own account.</li>
      <li>A plan or quote made before anyone looks at your account and tracking.</li>
    </ul>
    <h2>Where my work fits</h2>
    <p>On Google Ads, you keep ownership of the account. My experience covers <a href="../smile-line-dental.html">a dental clinic</a>, <a href="../mr-expert-carpet-cleaning.html">a UK carpet cleaning company</a> and <a href="../the-body-essential.html">Shopify brands</a>. If you need creative, video and ads produced under one roof, an agency may suit you better, and I'll tell you that.</p>""",
 "faq": [
  ("Is a Google Ads freelancer cheaper than an agency?", "Often, because there's less overhead, but it isn't guaranteed. Compare what is included each month, not just the fee."),
  ("Should I hire a Google Ads freelancer from Upwork or Fiverr?", "You can find capable people there, but judge them the same way as anyone else: account ownership, tracking, reporting and proof of similar work. A very low fixed price is unlikely to cover ongoing management."),
  ("Who should own my Google Ads account?", "You should. Whoever you hire should work inside your account with access you can remove, so your history stays with you."),
  ("How do I know my Google Ads manager is doing a good job?", "Check whether conversions reflect real enquiries, whether search terms are being cleaned regularly, and whether you can see the changes they've made."),
 ],
 "cta_h": "Want a second opinion on your account first?",
 "cta_p": "Whether you end up hiring me, a freelancer or an agency, a free audit tells you what needs fixing, so you can compare quotes properly.",
 "cta_b": "Get a free Google Ads audit",
 "related": [
  ("../google-ads-management.html", "Google Ads management", "Search campaigns with call and form tracking."),
  ("google-ads-account-audit-lead-generation.html", "Google Ads Account Audit Checklist for Lead Generation", "Six checks for an account that lives on calls and forms."),
  ("local-services-ads-vs-google-ads.html", "Local Services Ads vs Google Ads", "Billing, control and when to use each."),
  ("google-ads-conversion-tracking-not-working.html", "Google Ads Conversion Tracking Not Working", "Why a working tag can still report nothing for weeks."),
 ],
},
]


def write(path, text):
    full = os.path.join(ROOT, path)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("wrote", path, len(re.sub(r"<[^>]+>", " ", text[text.index("<body>"):]).split()), "words")


if __name__ == "__main__":
    for p in SERVICE_PAGES:
        write(p["slug"] + ".html", service_page(p))
    for p in BLOG_PAGES:
        write("blog/" + p["slug"] + ".html", blog_page(p))

#!/usr/bin/env python3
"""Generates the site's HTML pages from shared header/footer + per-page content.

Usage:  python3 tools/build.py            -> writes *.html into the repo root
Edit the text below, run the script, and commit the regenerated pages.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHONE, TEL, EMAIL = "732.226.8111", "7322268111", "info@reliableos.com"

PHONE_SVG = '<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>'
MAIL_SVG = '<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M3 5h18v14H3z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M3 6l9 7 9-7" fill="none" stroke="currentColor" stroke-width="2"/></svg>'

NAV = [("index.html", "Home"), ("services.html", "Services"), ("about.html", "About Us"),
       ("faq.html", "FAQ"), ("contact.html", "Contact")]

SCHEMA = {
    "@context": "https://schema.org", "@type": "LocalBusiness",
    "name": "Reliable Office Services", "url": "https://reliableos.com/",
    "telephone": "+1-732-226-8111", "email": EMAIL,
    "logo": "https://reliableos.com/images/logo.png",
    "image": "https://reliableos.com/images/mascots/group.png",
    "address": {"@type": "PostalAddress", "addressLocality": "Lakewood", "addressRegion": "NJ", "addressCountry": "US"},
    "foundingDate": "2020", "founder": {"@type": "Person", "name": "Yitzi Fellner"},
}


def head(title, desc, path):
    url = "https://reliableos.com/" + ("" if path == "index.html" else path)
    schema = ('\n  <script type="application/ld+json">' + json.dumps(SCHEMA) + "</script>") if path == "index.html" else ""
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <link rel="icon" href="images/favicon.png">
  <meta name="theme-color" content="#2b3b90">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="https://reliableos.com/images/mascots/group.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/styles.css">
  <script>document.documentElement.classList.add('js');</script>{schema}
</head>
<body>
'''


def header(path):
    links = "\n".join(
        f'        <a href="{h}"{" class=\"active\" aria-current=\"page\"" if h == path else ""}>{t}</a>'
        for h, t in NAV if h != "contact.html")
    return f'''  <a class="skip-link" href="#main">Skip to content</a>
  <div class="progress" aria-hidden="true"><span></span></div>

  <header class="site-header" id="top">
    <div class="container header-inner">
      <a href="index.html" class="brand" aria-label="Reliable Office Services home">
        <img src="images/logo.png" alt="Reliable Office Services" width="490" height="169">
      </a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
        <span></span><span></span><span></span>
      </button>
      <nav class="site-nav" id="site-nav" aria-label="Main">
{links}
        <a href="tel:{TEL}" class="nav-phone">{PHONE_SVG} {PHONE}</a>
        <a href="contact.html" class="btn btn-lime btn-sm">Get Started</a>
      </nav>
    </div>
  </header>

  <main id="main">
'''


FOOTER = f'''  </main>

  <footer class="site-footer">
    <div class="container footer-inner">
      <div>
        <img src="images/logo.png" alt="Reliable Office Services" width="490" height="169" loading="lazy" class="footer-logo">
        <p class="footer-tag">Your business. Our support.<br>Based out of Lakewood, NJ.</p>
      </div>
      <nav aria-label="Footer">
        <a href="index.html">Home</a>
        <a href="services.html">Services</a>
        <a href="about.html">About Us</a>
        <a href="faq.html">FAQ</a>
        <a href="contact.html">Contact</a>
      </nav>
      <div class="footer-contact">
        <a href="tel:{TEL}">{PHONE}</a>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
        <span>Month to month. No commitment.</span>
      </div>
      <p class="copyright">© <span id="year">2026</span> Reliable Office Services. All rights reserved.</p>
    </div>
  </footer>

  <a href="tel:{TEL}" class="mobile-call" aria-label="Call Reliable Office Services">{PHONE_SVG} Call now</a>

  <script src="js/main.js" defer></script>
</body>
</html>
'''


def page_hero(eyebrow, title, sub, mascot, alt="", say="Hi there! 👋"):
    return f'''    <section class="page-hero">
      <div class="ring ring-a" aria-hidden="true"></div>
      <div class="container page-hero-grid">
        <div>
          <p class="eyebrow">{eyebrow}</p>
          <h1>{title}</h1>
          <p class="lead">{sub}</p>
        </div>
        <button class="mascot-btn page-hero-mascot" type="button" data-say="{say}" aria-label="Say hi to the mascot">
          <img src="images/mascots/{mascot}.png" alt="{alt}" width="560" height="560">
        </button>
      </div>
    </section>
'''


MARQUEE_ITEMS = ["Month to month", "No commitment required", "All staff in our Lakewood, NJ office",
                 "Nothing outsourced overseas", "A dedicated rep who knows your business", "We work in your software"]


def marquee():
    a = "".join(f"<span>{t}</span><i>✦</i>" for t in MARQUEE_ITEMS)
    b = "".join(f'<span aria-hidden="true">{t}</span><i>✦</i>' for t in MARQUEE_ITEMS)
    return f'''    <div class="marquee" aria-label="Why owners choose Reliable">
      <div class="marquee-track">{a}{b}</div>
    </div>
'''


SERVICES = [
    ("reception", "tint-cyan", "Reception", "A warm welcome. A clear next step.",
     "Answer calls, take messages, review voicemail and return calls.", "Ring ring! I’ve got it 📞", "Smiling desk-phone mascot"),
    ("scheduling", "tint-lav", "Scheduling", "An organized calendar. A smoother day.",
     "Book appointments, handle changes and cancellations, and confirm visits.", "Booked, confirmed, done ✅", "Smiling calendar mascot holding a pen"),
    ("customer-service", "tint-peach", "Customer Service", "Personal attention. Helpful follow-through.",
     "Answer questions, relay pricing, follow up and gather feedback.", "Happy to help! 😊", "Waving mascot wearing a headset"),
    ("data-entry", "tint-lime", "Data Entry", "Accurate records. Less unfinished admin.",
     "Update records and inboxes, send invoices and track payments.", "Records updated ⌨️", "Smiling computer mascot typing on a keyboard"),
]


def service_cards():
    out = '        <div class="service-grid">\n'
    for img, tint, tag, title, desc, say, alt in SERVICES:
        out += f'''          <article class="service-card {tint} reveal tilt">
            <button class="mascot-btn" type="button" data-say="{say}" aria-label="{tag} mascot says hello">
              <img src="images/mascots/{img}.png" alt="{alt}" width="560" height="560" loading="lazy">
            </button>
            <div>
              <span class="tag">{tag}</span>
              <h3>{title}</h3>
              <p>{desc}</p>
            </div>
          </article>
'''
    return out + "        </div>\n"


STATS = '''        <div class="stats">
          <div class="stat reveal tint-cyan">
            <p class="stat-label">In business since</p>
            <p class="stat-num" data-count="2020" data-from="2000">2020</p>
            <p>Helping owners stay organized and care for their customers.</p>
          </div>
          <div class="stat reveal tint-lime">
            <p class="stat-label">Businesses helped</p>
            <p class="stat-num" data-count="100" data-suffix="+">100+</p>
            <p>Support for your workload and ways of working.</p>
          </div>
          <div class="stat reveal tint-lav">
            <p class="stat-label">Industries served today</p>
            <p class="stat-num" data-count="10" data-suffix="+">10+</p>
            <p>Different industries. Different ways of working.</p>
          </div>
        </div>
'''

TESTIMONIAL = '''    <section class="testimonial">
      <div class="container narrow center reveal">
        <div class="stars" aria-label="5 out of 5 stars">★★★★★</div>
        <blockquote>
          <p>“I can’t say enough about this service. Being a small business in the COVID era, we had to look for more affordable ways to maintain an office staff. Reliable’s staff treated me as if they were ‘in-house.’ I was shocked at how smooth the transition was for my business!”</p>
          <footer><strong>Dr. Daniel Yousefzadeh</strong><span>Zada Rehab</span></footer>
        </blockquote>
      </div>
    </section>
'''

CTA = f'''    <section class="cta-band">
      <div class="ring ring-d" aria-hidden="true"></div>
      <div class="container cta-grid">
        <div class="reveal">
          <p class="eyebrow light">Let’s make room for what matters</p>
          <h2>What would you take off your plate first?</h2>
          <p>Month to month. No commitment. A local team that’s ready when you are.</p>
          <div class="hero-ctas static">
            <a href="contact.html" class="btn btn-lime">Get Started <span class="arrow" aria-hidden="true">→</span></a>
            <a href="tel:{TEL}" class="btn btn-outline-light">Call {PHONE}</a>
          </div>
        </div>
        <img src="images/mascots/group.png" alt="" class="cta-mascots reveal" width="1000" height="719" loading="lazy">
      </div>
    </section>
'''

PACKAGES = [
    ("p-cyan", "One service", "", "Start with the one thing you most want off your plate.", "pkg-1"),
    ("p-lime", "Two services", " featured", "Pair any two services, handled by the same team.", "pkg-2"),
    ("p-lav", "All four services", "", "Reception, scheduling, customer service and data entry in one package.", "pkg-4"),
]


def packages(heading_tag="h2"):
    cards = ""
    for cls, name, feat, desc, anchor in PACKAGES:
        btn = "btn-primary" if feat else "btn-ghost"
        cards += f'''          <article class="plan{feat} reveal tilt">
            <p class="plan-name {cls}">{name}</p>
            <p class="plan-desc">{desc}</p>
            <ul class="plan-list">
              <li>Customized to your business</li>
              <li>Dedicated local rep</li>
              <li>Works in your software</li>
              <li>Month to month</li>
            </ul>
            <a href="contact.html#{anchor}" class="btn {btn} btn-block">Get a Custom Quote</a>
          </article>
'''
    return f'''    <section class="pricing" id="packages">
      <div class="container">
        <div class="section-head center reveal">
          <p class="eyebrow">Three customized packages</p>
          <{heading_tag}>Support that fits your business</{heading_tag}>
          <p class="sub">Mix and match Reception, Scheduling, Customer Service and Data Entry. We tailor each package to how you work.</p>
        </div>
        <div class="no-commit reveal">
          <div class="nc-price"><span>Starting at</span><strong>$1,800</strong><span>a month</span></div>
          <div>
            <strong>Month to month. No commitment required.</strong>
            <span>No long-term contract. Tell us what you need and we’ll put together a quote for your business.</span>
          </div>
        </div>
        <div class="plans">
{cards}        </div>
      </div>
    </section>
'''


ROLES = '''        <div class="roles">
          <div class="role reveal">
            <div class="role-top r-cyan">Dedicated<br>account manager</div>
            <p>Your point of contact who knows your business.</p>
          </div>
          <div class="role reveal">
            <div class="role-top r-lime">Experienced<br>support team</div>
            <p>Trained staff who carry out your day-to-day work.</p>
          </div>
          <div class="role reveal">
            <div class="role-top r-lav">Supervisors<br>and managers</div>
            <p>Oversee quality, keep work on track and coordinate team coverage.</p>
          </div>
        </div>
'''

LOCAL_BADGE = '''          <div class="local-badge reveal" aria-hidden="true">
            <svg viewBox="0 0 200 200">
              <defs><path id="circ" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs>
              <text><textPath href="#circ" textLength="486" lengthAdjust="spacing">BASED OUT OF LAKEWOOD, NJ • NOTHING OVERSEAS •</textPath></text>
            </svg>
            <span class="pin">📍</span>
          </div>
'''

COMPARE = '''        <div class="compare reveal">
          <div class="compare-col them">
            <h3>An outsourced call center</h3>
            <ul>
              <li>Calls routed overseas</li>
              <li>A different voice every time</li>
              <li>Reading from a generic script</li>
              <li>Locked into a long contract</li>
            </ul>
          </div>
          <div class="compare-col us">
            <h3>Your Reliable team</h3>
            <ul>
              <li>Answered right here in Lakewood, NJ</li>
              <li>Your own dedicated rep who knows you</li>
              <li>Trained on your business and software</li>
              <li>Month to month, cancel anytime</li>
            </ul>
          </div>
        </div>
'''

FAQS = [
    ("Is Reliable Office Services a call center?", "Not at all! All our staff are in our Lakewood, NJ office, and we assign a personal rep to your account. We want you to build a personal relationship with the person you work with, and we’d love for you to come down and meet them!"),
    ("Is any of the work done overseas?", "No. Every member of our team works from our Lakewood, NJ office. Nothing is outsourced overseas."),
    ("Is there any commitment on my end?", "None at all! Every package is month to month. If the service isn’t working for you, you can cancel at any time. We just ask that you give us 30 days’ notice."),
    ("How much does it cost?", "Packages start at $1,800 a month. Because every business is different, we customize your package around the services you need. Get in touch and we’ll put together a quote."),
    ("What if my customer wants to speak with me directly?", "No problem! We collect their name, number and reason for the callback, so you’re fully informed and can make the most of your time."),
    ("Are you able to use my software?", "Absolutely! We learn your business and follow your preferences. We only provide our own systems if you don’t already have one you like."),
    ("Will customers lose the personal service they’re used to with me?", "In our experience, customers appreciate someone picking up their calls and are happier getting through to someone, even if it isn’t you. They can still reach you, but in a more organized way. Scheduling a call with the details ready makes the whole process more effective and efficient."),
    ("How will my receptionist know how to get the work done?", "We have an extensive onboarding process to learn your business. We document your preferences and former methods, then put them into practice on our end."),
]

# ---------------------------------------------------------------- pages

HOME = f'''    <section class="hero">
      <div class="ring ring-a" aria-hidden="true"></div>
      <div class="ring ring-b" aria-hidden="true"></div>
      <span class="bubble b1" aria-hidden="true"></span>
      <span class="bubble b2" aria-hidden="true"></span>
      <span class="bubble b3" aria-hidden="true"></span>
      <div class="container hero-grid">
        <div class="hero-copy">
          <h1><span class="line">Your business.</span> <span class="line accent">Our support.</span></h1>
          <p class="lead">Four services. One experienced <strong>local</strong> team. We answer your calls, manage your calendar, take care of your customers and handle the admin, so you get <strong>more time for what matters</strong>.</p>
          <div class="hero-ctas">
            <a href="contact.html" class="btn btn-primary">Let’s Talk <span class="arrow" aria-hidden="true">→</span></a>
            <a href="services.html" class="btn btn-ghost">See Our Services</a>
          </div>
          <ul class="promise">
            <li><span class="chk" aria-hidden="true"></span>Month to month</li>
            <li><span class="chk" aria-hidden="true"></span>No commitment</li>
            <li><span class="chk" aria-hidden="true"></span>100% local team</li>
          </ul>
        </div>
        <div class="hero-art">
          <div class="hero-blob" aria-hidden="true"></div>
          <button class="mascot-btn hero-mascots" type="button" data-say="Hi there! We’re the Reliable crew 👋" aria-label="Say hi to the Reliable mascots">
            <img src="images/mascots/group.png" alt="The Reliable mascots: a desk phone, a calendar, a headset and a computer, smiling and giving a thumbs up" width="1000" height="719">
          </button>
          <div class="float-card fc-1"><strong>Helping businesses</strong><span>since 2020</span></div>
          <div class="float-card fc-2"><span class="flag" aria-hidden="true">📍</span><div><span>Based out of</span><strong>Lakewood, NJ</strong></div></div>
        </div>
      </div>
    </section>

{marquee()}
    <section class="mission">
      <div class="container">
        <div class="mission-grid">
          <div class="mission-card reveal">
            <p class="eyebrow light">Small business. Big support.</p>
            <h2>Our mission is to help you run efficiently and keep your customers happy.</h2>
          </div>
          <ul class="benefits">
            <li class="reveal tint-cyan"><span class="b-dot"></span>More organized work</li>
            <li class="reveal tint-peach"><span class="b-dot"></span>Warm, personal service</li>
            <li class="reveal tint-lav"><span class="b-dot"></span>More peace of mind</li>
          </ul>
        </div>
{STATS}      </div>
    </section>

    <section class="services" id="services">
      <div class="container">
        <div class="section-head center reveal">
          <p class="eyebrow">Four services. One team to handle them.</p>
          <h2>Pick what you want off your plate</h2>
          <p class="sub">Tap a card to meet the mascot behind each service.</p>
        </div>
{service_cards()}        <p class="center more reveal"><a href="services.html" class="btn btn-ghost">How it works &amp; packages <span class="arrow" aria-hidden="true">→</span></a></p>
      </div>
    </section>

    <section class="team" id="team">
      <div class="ring ring-c" aria-hidden="true"></div>
      <div class="container">
        <div class="team-head">
          <div class="reveal">
            <p class="eyebrow light">A whole local team behind your business</p>
            <h2>Real people, based out of Lakewood, NJ. <span class="hl-lime">Nothing done overseas.</span></h2>
            <p class="team-lead">We’re not a call center. All of our staff work from our Lakewood, NJ office, and you get a personal rep assigned to your account.</p>
            <p class="team-cta"><a href="about.html" class="btn btn-lime">Meet the team <span class="arrow" aria-hidden="true">→</span></a></p>
          </div>
{LOCAL_BADGE}        </div>
      </div>
    </section>

    <section class="starting">
      <div class="container">
        <div class="starting-card reveal">
          <div>
            <p class="eyebrow">Three customized packages</p>
            <h2>Starting at $1,800 a month.</h2>
            <p><strong>Month to month. No commitment required.</strong> We build your package around the services your business needs.</p>
          </div>
          <div class="starting-actions">
            <a href="contact.html" class="btn btn-primary">Get a Custom Quote <span class="arrow" aria-hidden="true">→</span></a>
            <a href="services.html#packages" class="link-arrow">See the packages →</a>
          </div>
        </div>
      </div>
    </section>

{TESTIMONIAL}
{CTA}'''

SERVICES_PAGE = (
    page_hero("Our services", "Four services. One team to handle them.",
              "Reception, scheduling, customer service and data entry, all handled by a local team that learns how your business works.",
              "reception", "Smiling desk-phone mascot", "Ring ring! I’ve got it 📞")
    + f'''
    <section class="services">
      <div class="container">
{service_cards()}      </div>
    </section>

    <section class="how" id="how">
      <div class="container">
        <div class="section-head center reveal">
          <p class="eyebrow">How it works</p>
          <h2>We learn your business.<br>Then we keep the work moving.</h2>
        </div>
        <ol class="steps">
          <li class="reveal"><span class="num n-cyan">01</span><h3>Learn</h3><p>We learn your services, software, customers and preferences.</p></li>
          <li class="reveal"><span class="num n-lime">02</span><h3>Prepare</h3><p>We document workflows, call handling and handoffs so the team knows your way.</p></li>
          <li class="reveal"><span class="num n-lav">03</span><h3>Support</h3><p>The team handles the work. Supervisors check quality and coordinate coverage.</p></li>
        </ol>
        <p class="how-foot reveal">You focus on your business. <strong>We manage the staffing and daily support.</strong></p>
      </div>
    </section>

{packages()}
{CTA}''')

ABOUT_PAGE = (
    page_hero("About us", "A whole local team behind your business.",
              "Since 2020 we’ve helped small businesses stay organized and keep their customers happy, from our office in Lakewood, NJ.",
              "customer-service", "Waving mascot wearing a headset", "Nice to meet you! 😊")
    + f'''
    <section class="about" id="founder">
      <div class="container about-grid">
        <div class="about-photo reveal">
          <img src="images/yitzi.webp" alt="Yitzi Fellner, Founder and CEO of Reliable Office Services" width="720" height="882">
        </div>
        <div class="reveal">
          <p class="eyebrow">A message from our founder</p>
          <blockquote class="ceo-quote">
            <p>As a business owner, I know how hard it can be to give everyone your attention when you’re being pulled in every direction. Every call matters, every customer deserves a thoughtful response, and the everyday office work doesn’t stop just because you’re busy.</p>
            <p>I founded Reliable Office Services in 2020 to give business owners dependable support and the breathing room to focus on what they do best. Our team, based right here in Lakewood, New Jersey, takes the time to learn your business, understand your customers, and work alongside you—as if we’re sitting in the room next door.</p>
            <p>Whether we’re answering calls, managing schedules, or keeping up with the details behind the scenes, we take pride in representing your business with care. My goal is simple: to help you feel confident that your office is in good hands, so you have more time to grow your business and enjoy what matters most.</p>
            <footer><strong>Yitzi Fellner</strong><span>Founder &amp; CEO</span></footer>
          </blockquote>
        </div>
      </div>
    </section>

    <section class="mission">
      <div class="container">
        <div class="mission-grid">
          <div class="mission-card reveal">
            <p class="eyebrow light">Small business. Big support.</p>
            <h2>Our mission is to help you run efficiently and keep your customers happy.</h2>
          </div>
          <ul class="benefits">
            <li class="reveal tint-cyan"><span class="b-dot"></span>More organized work</li>
            <li class="reveal tint-peach"><span class="b-dot"></span>Warm, personal service</li>
            <li class="reveal tint-lav"><span class="b-dot"></span>More peace of mind</li>
          </ul>
        </div>
{STATS}      </div>
    </section>

    <section class="team" id="team">
      <div class="ring ring-c" aria-hidden="true"></div>
      <div class="container">
        <div class="team-head">
          <div class="reveal">
            <p class="eyebrow light">Who you’ll work with</p>
            <h2>Real people, based out of Lakewood, NJ. <span class="hl-lime">Nothing done overseas.</span></h2>
            <p class="team-lead">We’re not a call center. All of our staff work from our Lakewood, NJ office, and you get a personal rep assigned to your account. We’d love for you to come down and meet them.</p>
          </div>
{LOCAL_BADGE}        </div>
{ROLES}{COMPARE}      </div>
    </section>

{TESTIMONIAL}
{CTA}''')

FAQ_PAGE = (
    page_hero("FAQ", "Frequently asked questions",
              f"Quick answers about how we work. Don’t see yours? Call us at <a href=\"tel:{TEL}\">{PHONE}</a>.",
              "scheduling", "Smiling calendar mascot holding a pen", "Good question! ✅")
    + '''
    <section class="faq" id="faq">
      <div class="container narrow">
        <div class="faq-list">
'''
    + "".join(f'''          <details class="reveal"{" open" if i == 0 else ""}>
            <summary>{q}</summary>
            <div class="answer"><p>{a}</p></div>
          </details>
''' for i, (q, a) in enumerate(FAQS))
    + f'''        </div>
      </div>
    </section>

{CTA}''')

CONTACT_PAGE = f'''    <section class="contact" id="contact">
      <div class="ring ring-d" aria-hidden="true"></div>
      <div class="container contact-grid">
        <div class="contact-copy">
          <p class="eyebrow light">Let’s make room for what matters</p>
          <h1>What would you take off your plate first?</h1>
          <p>Tell us a little about your business. We’ll walk you through how it works and put together a custom quote, with no pressure and no commitment.</p>
          <div class="contact-lines">
            <a href="tel:{TEL}" class="c-line"><span class="c-ico">{PHONE_SVG}</span>{PHONE}</a>
            <a href="mailto:{EMAIL}" class="c-line"><span class="c-ico">{MAIL_SVG}</span>{EMAIL}</a>
          </div>
          <img src="images/mascots/group.png" alt="" class="contact-mascots" width="1000" height="719">
        </div>

        <form class="contact-form" id="contact-form" novalidate>
          <fieldset class="chips">
            <legend>I’d like help with…</legend>
            <label><input type="checkbox" name="service" value="Reception"><span>📞 Reception</span></label>
            <label><input type="checkbox" name="service" value="Scheduling"><span>📅 Scheduling</span></label>
            <label><input type="checkbox" name="service" value="Customer Service"><span>🎧 Customer Service</span></label>
            <label><input type="checkbox" name="service" value="Data Entry"><span>💻 Data Entry</span></label>
          </fieldset>
          <div class="field">
            <label for="full_name">Name <span aria-hidden="true">*</span></label>
            <input id="full_name" name="full_name" type="text" autocomplete="name" required>
          </div>
          <div class="field">
            <label for="email">Email address <span aria-hidden="true">*</span></label>
            <input id="email" name="email" type="email" autocomplete="email" required>
          </div>
          <div class="field">
            <label for="subject">Business name</label>
            <input id="subject" name="subject" type="text" placeholder="Optional">
          </div>
          <div class="field">
            <label for="message">Your message <span aria-hidden="true">*</span></label>
            <textarea id="message" name="message" rows="4" placeholder="Tell us about your business and what you need" required></textarea>
          </div>
          <button type="submit" class="btn btn-primary btn-block">Send Message <span class="arrow" aria-hidden="true">→</span></button>
          <p class="form-status" id="form-status" role="status" aria-live="polite"></p>
        </form>
      </div>
    </section>
'''

PAGES = {
    "index.html": ("Reliable Office Services | Your Business. Our Support.",
                   "Reception, scheduling, customer service and data entry from a local team in Lakewood, NJ. Nothing outsourced overseas. Starting at $1,800 a month, month to month, no commitment.", HOME),
    "services.html": ("Services & Packages | Reliable Office Services",
                      "Four services handled by one local team: reception, scheduling, customer service and data entry. Three customized packages starting at $1,800 a month.", SERVICES_PAGE),
    "about.html": ("About Us | Reliable Office Services",
                   "Meet the local team behind Reliable Office Services. All staff work from our Lakewood, NJ office. Nothing is done overseas.", ABOUT_PAGE),
    "faq.html": ("FAQ | Reliable Office Services",
                 "Answers to common questions about Reliable Office Services: commitment, pricing, software, and how our local team works.", FAQ_PAGE),
    "contact.html": ("Contact | Reliable Office Services",
                     "Get a custom quote from Reliable Office Services. Call 732.226.8111 or send us a message.", CONTACT_PAGE),
}

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else ROOT
    for path, (title, desc, body) in PAGES.items():
        with open(os.path.join(out, path), "w") as f:
            f.write(head(title, desc, path) + header(path) + body + FOOTER)
        print("wrote", path)

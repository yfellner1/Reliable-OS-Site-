# Reliable Office Services — reliableos.com

Static website (HTML + CSS + vanilla JS). No dependencies.

```
index.html, services.html, about.html, faq.html, contact.html   the pages (generated)
tools/build.py   page content + shared header/footer; regenerates the pages
css/styles.css   styles (brand colors are CSS variables at the top)
js/main.js       mobile nav, animations, mascot clicks, FAQ, contact form
images/          logo, mascots, founder photo, favicon
```

## Editing text
Edit the wording in `tools/build.py`, then run `python3 tools/build.py` to regenerate the pages.

## Preview locally
```
python3 -m http.server 8000   # then open http://localhost:8000
```

## Deploy
Upload the whole folder to any static host.

The contact form posts JSON (`full_name`, `email`, `subject`, `message`) to the same
endpoint the previous site used — see `ENDPOINT` in `js/main.js`.

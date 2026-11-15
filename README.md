# Reliable Office Services — reliableos.com

Static, dependency-free website (HTML + CSS + vanilla JS). No build step.

```
index.html      single-page site
css/styles.css  styles (brand colors are CSS variables at the top)
js/main.js      mobile nav, scroll effects, contact form
images/         logo, hero photo, CEO headshot, favicon
```

## Preview locally
```
python3 -m http.server 8000   # then open http://localhost:8000
```

## Deploy
Upload the whole folder to any static host (current host, Netlify, Vercel, GitHub Pages, S3).

The contact form posts JSON (`full_name`, `email`, `subject`, `message`) to the same
AWS endpoint the previous site used — see `ENDPOINT` in `js/main.js`.

(function () {
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  // Footer year
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Header shadow, scroll progress, mobile call bar
  var header = document.querySelector('.site-header');
  var bar = document.querySelector('.progress span');
  var mobileCall = document.querySelector('.mobile-call');
  var hero = document.querySelector('.hero');
  function onScroll() {
    var st = window.scrollY;
    header.classList.toggle('scrolled', st > 8);
    var max = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.transform = 'scaleX(' + (max > 0 ? st / max : 0) + ')';
    if (mobileCall) mobileCall.classList.toggle('show', st > hero.offsetHeight * 0.6);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile nav
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  function closeNav() {
    nav.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open menu');
  }
  toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });
  nav.addEventListener('click', function (e) { if (e.target.closest('a')) closeNav(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeNav(); });

  // Active nav link
  var links = Array.prototype.slice.call(nav.querySelectorAll('a[href^="#"]:not(.btn)'));
  if ('IntersectionObserver' in window) {
    var secObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (l) { l.classList.toggle('active', l.getAttribute('href') === '#' + en.target.id); });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    links.forEach(function (l) {
      var s = document.querySelector(l.getAttribute('href'));
      if (s) secObs.observe(s);
    });
  }

  // Reveal on scroll (staggered among siblings) + count-up numbers
  function countUp(el) {
    var end = parseInt(el.getAttribute('data-count'), 10);
    var start = parseInt(el.getAttribute('data-from') || '0', 10);
    var suffix = el.getAttribute('data-suffix') || '';
    // years (data-from) render plain; prices get thousands separators
    var fmt = el.hasAttribute('data-from') ? String : function (n) { return n.toLocaleString('en-US'); };
    if (reduceMotion) { el.textContent = fmt(end) + suffix; return; }
    var t0 = null, dur = 1400;
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(Math.round(start + (end - start) * eased)) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  var reveals = document.querySelectorAll('.reveal');
  reveals.forEach(function (el) {
    var sibs = Array.prototype.filter.call(el.parentElement.children, function (c) { return c.classList.contains('reveal'); });
    el.style.setProperty('--d', (sibs.indexOf(el) * 0.09) + 's');
  });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('in');
        en.target.querySelectorAll('[data-count]').forEach(countUp);
        io.unobserve(en.target);
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  // 3D tilt on cards (mouse only)
  if (finePointer && !reduceMotion) {
    document.querySelectorAll('.tilt').forEach(function (card) {
      card.addEventListener('mousemove', function (e) {
        var r = card.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5;
        var yy = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = 'perspective(900px) rotateX(' + (-yy * 6) + 'deg) rotateY(' + (x * 6) + 'deg) translateY(-6px)';
      });
      card.addEventListener('mouseleave', function () { card.style.transform = ''; });
    });
  }

  // Button ripple
  document.addEventListener('pointerdown', function (e) {
    var btn = e.target.closest('.btn');
    if (!btn || reduceMotion) return;
    var r = btn.getBoundingClientRect();
    var size = Math.max(r.width, r.height);
    var s = document.createElement('span');
    s.className = 'ripple';
    s.style.width = s.style.height = size + 'px';
    s.style.left = (e.clientX - r.left - size / 2) + 'px';
    s.style.top = (e.clientY - r.top - size / 2) + 'px';
    btn.appendChild(s);
    setTimeout(function () { s.remove(); }, 650);
  });

  // Click sparkles — the little "!" bursts from the mascots
  var sparkColors = ['#b9d63c', '#45c6eb', '#2b3b90', '#b9d63c'];
  document.addEventListener('click', function (e) {
    if (reduceMotion || e.detail === 0) return; // skip keyboard-triggered clicks
    if (e.target.closest('input, textarea, label')) return;
    for (var i = 0; i < 6; i++) {
      var sp = document.createElement('span');
      sp.className = 'spark';
      sp.style.left = e.clientX + 'px';
      sp.style.top = e.clientY + 'px';
      sp.style.background = sparkColors[i % sparkColors.length];
      sp.style.setProperty('--r', (i * 60 + Math.random() * 20 - 10) + 'deg');
      document.body.appendChild(sp);
      setTimeout(function (n) { n.remove(); }.bind(null, sp), 600);
    }
  });

  // Mascots: jump + speech bubble on click
  document.querySelectorAll('.mascot-btn').forEach(function (m) {
    m.addEventListener('click', function () {
      m.classList.remove('jump');
      void m.offsetWidth;
      m.classList.add('jump');
      var old = m.querySelector('.say');
      if (old) old.remove();
      var b = document.createElement('span');
      b.className = 'say';
      b.textContent = m.getAttribute('data-say');
      b.setAttribute('role', 'status');
      m.appendChild(b);
      setTimeout(function () { b.remove(); }, 2300);
    });
  });
  // Make whole service card clickable for the mascot
  document.querySelectorAll('.service-card').forEach(function (card) {
    card.addEventListener('click', function (e) {
      if (e.target.closest('.mascot-btn')) return;
      card.querySelector('.mascot-btn').click();
    });
  });

  // FAQ: smooth open/close, one open at a time
  var faqs = document.querySelectorAll('.faq details');
  faqs.forEach(function (d) {
    var summary = d.querySelector('summary');
    var answer = d.querySelector('.answer');
    summary.addEventListener('click', function (e) {
      if (reduceMotion || !answer.animate) return;
      e.preventDefault();
      if (d.open) {
        var h = answer.offsetHeight;
        answer.animate([{ height: h + 'px', opacity: 1 }, { height: '0px', opacity: 0 }], { duration: 280, easing: 'ease-in' })
          .onfinish = function () { d.open = false; };
      } else {
        faqs.forEach(function (o) { if (o !== d && o.open) o.querySelector('summary').click(); });
        d.open = true;
        var h2 = answer.offsetHeight;
        answer.animate([{ height: '0px', opacity: 0 }, { height: h2 + 'px', opacity: 1 }], { duration: 380, easing: 'cubic-bezier(.2,.8,.2,1)' });
      }
    });
  });

  // Plan buttons preselect services in the form
  var form = document.getElementById('contact-form');
  document.querySelectorAll('[data-plan]').forEach(function (a) {
    a.addEventListener('click', function () {
      var plan = a.getAttribute('data-plan');
      var msg = form.querySelector('#message');
      if (!msg.value.trim()) msg.value = 'I’m interested in the ' + plan + ' package.';
      if (/All 4/.test(plan)) form.querySelectorAll('input[name=service]').forEach(function (c) { c.checked = true; });
    });
  });

  // Contact form — posts to the same endpoint the previous site used
  var ENDPOINT = 'https://tpyd329og7.execute-api.us-east-1.amazonaws.com/production/submit';
  var status = document.getElementById('form-status');

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    status.className = 'form-status';
    var invalid = [];
    form.querySelectorAll('[required]').forEach(function (f) {
      var bad = !f.value.trim() || (f.type === 'email' && !/^\S+@\S+\.\S+$/.test(f.value));
      f.classList.remove('invalid');
      void f.offsetWidth;
      f.classList.toggle('invalid', bad);
      f.setAttribute('aria-invalid', bad);
      if (bad) invalid.push(f);
    });
    if (invalid.length) {
      status.textContent = 'Please fill in your name, a valid email and a message.';
      status.classList.add('error');
      invalid[0].focus();
      return;
    }

    var services = Array.prototype.map.call(form.querySelectorAll('input[name=service]:checked'), function (c) { return c.value; });
    var business = form.subject.value.trim();
    var data = {
      full_name: form.full_name.value.trim(),
      email: form.email.value.trim(),
      subject: [business, services.length ? 'Interested in: ' + services.join(', ') : ''].filter(Boolean).join(' | '),
      message: form.message.value.trim()
    };

    var btn = form.querySelector('button[type=submit]');
    btn.disabled = true;
    status.textContent = 'Sending…';

    fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(function (res) {
      if (!res.ok) throw new Error(res.status);
      form.reset();
      status.textContent = 'Thank you! A member of our local team will be in touch shortly. 🎉';
    }).catch(function () {
      status.textContent = 'Something went wrong. Please call us at 732.226.8111.';
      status.classList.add('error');
    }).finally(function () { btn.disabled = false; });
  });
})();

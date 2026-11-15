(function () {
  // Footer year
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Sticky header shadow
  var header = document.querySelector('.site-header');
  var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > 8); };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile nav
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });
  nav.addEventListener('click', function (e) {
    if (e.target.closest('a')) {
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });

  // Reveal on scroll
  var targets = document.querySelectorAll('.section-head, .card, .feature-list li, .steps li, .price-card, .about-grid > *, .testimonial blockquote, .intro .container');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    targets.forEach(function (el) { el.classList.add('reveal'); io.observe(el); });
  }

  // Contact form — posts to the same endpoint the previous site used
  var ENDPOINT = 'https://tpyd329og7.execute-api.us-east-1.amazonaws.com/production/submit';
  var form = document.getElementById('contact-form');
  var status = document.getElementById('form-status');

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    status.className = 'form-status';
    var invalid = [];
    form.querySelectorAll('[required]').forEach(function (f) {
      var bad = !f.value.trim() || (f.type === 'email' && !/^\S+@\S+\.\S+$/.test(f.value));
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

    var data = {};
    new FormData(form).forEach(function (v, k) { data[k] = v; });
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
      status.textContent = 'Thank you! A Reliable team member will be in touch shortly.';
    }).catch(function () {
      status.textContent = 'Something went wrong. Please call us at 732.226.8111.';
      status.classList.add('error');
    }).finally(function () { btn.disabled = false; });
  });
})();

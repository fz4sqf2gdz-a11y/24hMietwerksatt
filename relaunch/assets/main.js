/* ============================================================
   24h Mietwerkstatt – Redesign 2026 (v2)
   Navigation, Modals, Scroll-Reveal, Zeilen-Reveal,
   Scroll-Progress-Engine (Hebebühne, Wipes, Frost, Rad, Zähler),
   Count-up-Zahlen, exklusive Akkordeons,
   Google Analytics 4 (Konfiguration + Events)
   Event-Doku: siehe ANALYTICS.md
   ============================================================ */

/* ------------------------------------------------------------
   GOOGLE ANALYTICS 4 – KONFIGURATION
   Hier die echte Measurement-ID eintragen (z.B. "G-ABC123XYZ").
   Solange der Platzhalter drinsteht, wird GA4 NICHT geladen –
   die Seite funktioniert ganz normal ohne Tracking.
   ------------------------------------------------------------ */
const GA4_MEASUREMENT_ID = 'G-XXXXXXXXXX'; // <<< HIER GA4-ID EINTRAGEN

(function initGA4() {
  if (!GA4_MEASUREMENT_ID || GA4_MEASUREMENT_ID === 'G-XXXXXXXXXX') return;
  const s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4_MEASUREMENT_ID;
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', GA4_MEASUREMENT_ID, { anonymize_ip: true });
})();

function track(eventName, params) {
  if (typeof window.gtag === 'function') {
    window.gtag('event', eventName, params || {});
  }
}

/* ------------------------------------------------------------
   Modals
   ------------------------------------------------------------ */
function openModal(modalId) {
  const el = document.getElementById(modalId);
  if (!el) return;
  el.classList.add('open');
  el.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
  const closeBtn = el.querySelector('.modal-close');
  if (closeBtn) closeBtn.focus();
}

function closeModal(modalId) {
  const el = document.getElementById(modalId);
  if (!el) return;
  el.classList.remove('open');
  el.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
}

/* ------------------------------------------------------------
   WhatsApp-Formular (Wortlaut unverändert übernommen)
   ------------------------------------------------------------ */
function sendToWhatsapp(e, formId) {
  e.preventDefault();
  const form = document.getElementById(formId);
  if (!form) return;

  const nameInput = form.querySelector('[name="name"]');
  const msgInput = form.querySelector('[name="message"]');
  const name = nameInput ? nameInput.value : 'Kunde';
  const msg = msgInput ? msgInput.value : '';

  const text = `Hallo Werner, ich bin ${name}. ${msg}`;
  const url = `https://wa.me/436645171370?text=${encodeURIComponent(text)}`;

  track('cta_click', { cta: 'whatsapp_formular', form_id: formId });

  const btn = form.querySelector('button[type="submit"]');
  const oldText = btn ? btn.innerText : 'Senden';
  if (btn) btn.innerText = 'Wird geöffnet...';

  window.open(url, '_blank');

  setTimeout(() => {
    if (btn) btn.innerText = oldText;
    form.reset();
    document.querySelectorAll('.modal.open').forEach(m => closeModal(m.id));
  }, 1000);
}

/* ------------------------------------------------------------
   Hilfsfunktion: Zahl im deutschen Format
   ------------------------------------------------------------ */
function fmtNum(value, decimals) {
  return value.toFixed(decimals).replace('.', ',');
}

/* ------------------------------------------------------------
   DOM ready
   ------------------------------------------------------------ */
document.addEventListener('DOMContentLoaded', () => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --- Header: schrumpft/färbt sich beim Scrollen --- */
  const header = document.getElementById('siteHeader');
  if (header) {
    const onScrollHeader = () => {
      header.classList.toggle('scrolled', window.scrollY > 40);
    };
    window.addEventListener('scroll', onScrollHeader, { passive: true });
    onScrollHeader();
  }

  /* --- Mobile Navigation --- */
  const navToggle = document.getElementById('navToggle');
  const nav = document.getElementById('mainNavigation');

  if (navToggle && nav) {
    navToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = nav.classList.toggle('active');
      navToggle.setAttribute('aria-expanded', String(isOpen));
    });
    nav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        nav.classList.remove('active');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
    document.addEventListener('click', (e) => {
      if (nav.classList.contains('active') && !nav.contains(e.target) && !navToggle.contains(e.target)) {
        nav.classList.remove('active');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* --- Modals: Klick auf Overlay + Escape schließt --- */
  document.querySelectorAll('.modal').forEach(modal => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal(modal.id);
    });
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal.open').forEach(m => closeModal(m.id));
    }
  });

  /* --- Exklusive Akkordeons: ein offenes Element pro Gruppe --- */
  document.querySelectorAll('.faq-list, .tiles').forEach(group => {
    group.querySelectorAll(':scope > details').forEach(d => {
      d.addEventListener('toggle', () => {
        if (!d.open) return;
        group.querySelectorAll(':scope > details[open]').forEach(other => {
          if (other !== d) other.open = false;
        });
      });
    });
  });

  /* --- Scroll-Reveal + Zeilen-Reveal (dezent) --- */
  const revealEls = document.querySelectorAll('.reveal, .tr, .img-reveal');
  if (revealEls.length && !reducedMotion && 'IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });
    revealEls.forEach(el => revealObserver.observe(el));
    /* Hero-Headline sofort einblenden */
    const heroHeadline = document.getElementById('heroHeadline');
    if (heroHeadline) {
      requestAnimationFrame(() => heroHeadline.classList.add('is-visible'));
      revealObserver.unobserve(heroHeadline);
    }
  } else {
    revealEls.forEach(el => el.classList.add('is-visible'));
  }

  /* --- Count-up-Zahlen (Zahlen-Band) --- */
  const countEls = document.querySelectorAll('[data-count-to]');
  if (countEls.length && 'IntersectionObserver' in window && !reducedMotion) {
    const runCount = (el) => {
      const to = parseFloat(el.getAttribute('data-count-to'));
      const decimals = parseInt(el.getAttribute('data-count-decimals') || '0', 10);
      const duration = 1400;
      const start = performance.now();
      const tick = (now) => {
        const t = Math.min(1, (now - start) / duration);
        const eased = 1 - Math.pow(1 - t, 3);
        el.textContent = fmtNum(to * eased, decimals);
        if (t < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    };
    const countObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          runCount(entry.target);
          countObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    countEls.forEach(el => countObserver.observe(el));
  } else {
    countEls.forEach(el => {
      const decimals = parseInt(el.getAttribute('data-count-decimals') || '0', 10);
      el.textContent = fmtNum(parseFloat(el.getAttribute('data-count-to')), decimals);
    });
  }

  /* ------------------------------------------------------------
     Scroll-Progress-Engine
     Jedes Element mit [data-progress] bekommt eine CSS-Variable
     --p (0 → 1), während es durch den Viewport wandert.
     Damit laufen die Wipes (Vorher/Nachher), der Frost-Effekt,
     das rollende Rad und die Zähler – ohne Bibliotheken.
     ------------------------------------------------------------ */
  const progressEls = Array.from(document.querySelectorAll('[data-progress]'));
  const progressCounters = new Map();
  progressEls.forEach(el => {
    const counters = el.querySelectorAll('[data-progress-counter]');
    if (counters.length) progressCounters.set(el, Array.from(counters));
  });

  const updateProgressEls = () => {
    const vh = window.innerHeight;
    progressEls.forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.bottom < -80 || rect.top > vh + 80) return;
      /* 0 = Element betritt den Viewport unten, 1 = obere Hälfte erreicht */
      const raw = (vh * 0.92 - rect.top) / (vh * 0.62);
      const p = Math.max(0, Math.min(1, raw));
      el.style.setProperty('--p', p.toFixed(4));
      const counters = progressCounters.get(el);
      if (counters) {
        counters.forEach(c => {
          const from = parseFloat(c.getAttribute('data-from'));
          const to = parseFloat(c.getAttribute('data-to'));
          const decimals = parseInt(c.getAttribute('data-decimals') || '0', 10);
          const suffix = c.getAttribute('data-suffix') || '';
          c.textContent = fmtNum(from + (to - from) * p, decimals) + suffix;
        });
      }
    });
  };

  /* --- Hebebühnen-Scroll-Animation (Sticky Stage) --- */
  const liftWrap = document.getElementById('liftStageWrap');
  const liftCar = document.getElementById('liftCar');
  const liftArmL = document.getElementById('liftArmL');
  const liftArmR = document.getElementById('liftArmR');
  const liftHeight = document.getElementById('liftHeightValue');

  const MAX_LIFT_PX = 150;   /* Hub im SVG-Koordinatensystem */
  const MAX_HEIGHT_M = 1.8;  /* angezeigte Hubhöhe in Metern */
  const easeLift = t => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);

  const updateLift = () => {
    if (!liftWrap || !liftCar) return;
    const rect = liftWrap.getBoundingClientRect();
    const total = rect.height - window.innerHeight;
    if (total <= 0) return;
    let progress = -rect.top / total;
    progress = Math.max(0, Math.min(1, progress));
    const eased = easeLift(progress);
    const lift = eased * MAX_LIFT_PX;
    liftCar.style.transform = `translateY(${-lift}px)`;
    if (liftArmL) liftArmL.style.transform = `translateY(${-lift}px)`;
    if (liftArmR) liftArmR.style.transform = `translateY(${-lift}px)`;
    if (liftHeight) liftHeight.textContent = fmtNum(eased * MAX_HEIGHT_M, 2) + ' m';
  };

  if (!reducedMotion) {
    let ticking = false;
    const onScrollAnim = () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        ticking = false;
        updateLift();
        updateProgressEls();
      });
    };
    window.addEventListener('scroll', onScrollAnim, { passive: true });
    window.addEventListener('resize', onScrollAnim, { passive: true });
    updateLift();
    updateProgressEls();
  } else {
    /* Ohne Animation: Endzustände zeigen */
    if (liftCar) liftCar.style.transform = `translateY(${-MAX_LIFT_PX}px)`;
    if (liftArmL) liftArmL.style.transform = `translateY(${-MAX_LIFT_PX}px)`;
    if (liftArmR) liftArmR.style.transform = `translateY(${-MAX_LIFT_PX}px)`;
    if (liftHeight) liftHeight.textContent = fmtNum(MAX_HEIGHT_M, 2) + ' m';
    progressEls.forEach(el => {
      el.style.setProperty('--p', '1');
      const counters = progressCounters.get(el);
      if (counters) {
        counters.forEach(c => {
          const to = parseFloat(c.getAttribute('data-to'));
          const decimals = parseInt(c.getAttribute('data-decimals') || '0', 10);
          c.textContent = fmtNum(to, decimals) + (c.getAttribute('data-suffix') || '');
        });
      }
    });
  }

  /* ------------------------------------------------------------
     ANALYTICS-EVENTS (siehe ANALYTICS.md)
     ------------------------------------------------------------ */

  /* 1) CTA-Klicks */
  document.querySelectorAll('[data-ga-cta]').forEach(el => {
    el.addEventListener('click', () => {
      track('cta_click', {
        cta: el.getAttribute('data-ga-cta'),
        cta_location: el.getAttribute('data-ga-location') || 'unbekannt'
      });
    });
  });

  /* 2) Navigation: Klick auf Wohnwagen/Swift-Link */
  document.querySelectorAll('[data-ga-nav]').forEach(el => {
    el.addEventListener('click', () => {
      track('nav_click', { target: el.getAttribute('data-ga-nav') });
    });
  });

  /* 3) Section-Views (einmal pro Seitenaufruf) */
  if ('IntersectionObserver' in window) {
    const sectionObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          track('section_view', { section: entry.target.getAttribute('data-ga-section') });
          sectionObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.25 });
    document.querySelectorAll('[data-ga-section]').forEach(s => sectionObserver.observe(s));

    /* 4) Video-Sichtbarkeit */
    const videoObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const iframe = entry.target.querySelector('iframe');
          track('video_impression', { video_title: iframe ? iframe.title : 'unbekannt' });
          videoObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    document.querySelectorAll('.video-embed').forEach(v => videoObserver.observe(v));
  }

  /* 5) Scroll-Tiefe: 25 / 50 / 75 / 100 % (einmal pro Seitenaufruf) */
  const depthMarks = [25, 50, 75, 100];
  const firedDepths = new Set();
  let depthTicking = false;
  window.addEventListener('scroll', () => {
    if (depthTicking) return;
    depthTicking = true;
    requestAnimationFrame(() => {
      depthTicking = false;
      const scrollable = document.documentElement.scrollHeight - window.innerHeight;
      if (scrollable <= 0) return;
      const pct = Math.round((window.scrollY / scrollable) * 100);
      depthMarks.forEach(mark => {
        if (pct >= mark && !firedDepths.has(mark)) {
          firedDepths.add(mark);
          track('scroll_depth', { percent: mark });
        }
      });
    });
  }, { passive: true });
});

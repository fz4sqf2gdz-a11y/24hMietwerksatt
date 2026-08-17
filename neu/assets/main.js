/* ============================================================
   24h Mietwerkstatt – Redesign 2026
   Navigation, Modals, Scroll-Reveal, Hebebühnen-Animation,
   Google Analytics 4 (Konfiguration + Events)
   Event-Doku: siehe neu/ANALYTICS.md
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

/* Zentraler Event-Helfer – feuert nur, wenn GA4 aktiv ist. */
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
   DOM ready
   ------------------------------------------------------------ */
document.addEventListener('DOMContentLoaded', () => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

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

  /* --- Scroll-Reveal (dezent) --- */
  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length && !reducedMotion && 'IntersectionObserver' in window) {
    revealEls.forEach((el, i) => {
      el.style.transitionDelay = `${Math.min((i % 4) * 0.07, 0.28)}s`;
    });
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach(el => revealObserver.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('is-visible'));
  }

  /* --- Hebebühnen-Scroll-Animation ---
     Beim Scrollen durch die Sektion hebt die Bühne das Fahrzeug an.
     Reine Transform-Animation (GPU), respektiert prefers-reduced-motion. */
  const liftWrap = document.getElementById('liftStageWrap');
  const liftCar = document.getElementById('liftCar');
  const liftArmL = document.getElementById('liftArmL');
  const liftArmR = document.getElementById('liftArmR');
  const liftHeight = document.getElementById('liftHeightValue');

  if (liftWrap && liftCar && !reducedMotion) {
    const MAX_LIFT_PX = 150;   /* Hub im SVG-Koordinatensystem */
    const MAX_HEIGHT_M = 1.8;  /* angezeigte Hubhöhe in Metern */
    let ticking = false;

    const ease = t => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);

    const update = () => {
      ticking = false;
      const rect = liftWrap.getBoundingClientRect();
      const total = rect.height - window.innerHeight;
      if (total <= 0) return;
      let progress = -rect.top / total;
      progress = Math.max(0, Math.min(1, progress));
      const eased = ease(progress);
      const lift = eased * MAX_LIFT_PX;
      liftCar.style.transform = `translateY(${-lift}px)`;
      if (liftArmL) liftArmL.style.transform = `translateY(${-lift}px)`;
      if (liftArmR) liftArmR.style.transform = `translateY(${-lift}px)`;
      if (liftHeight) liftHeight.textContent = (eased * MAX_HEIGHT_M).toFixed(2).replace('.', ',') + ' m';
    };

    window.addEventListener('scroll', () => {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(update);
      }
    }, { passive: true });
    update();
  } else if (liftCar && reducedMotion) {
    /* Ohne Animation: Fahrzeug oben zeigen */
    liftCar.style.transform = 'translateY(-150px)';
    if (liftArmL) liftArmL.style.transform = 'translateY(-150px)';
    if (liftArmR) liftArmR.style.transform = 'translateY(-150px)';
    if (liftHeight) liftHeight.textContent = '1,80 m';
  }

  /* ------------------------------------------------------------
     ANALYTICS-EVENTS (siehe neu/ANALYTICS.md)
     ------------------------------------------------------------ */

  /* 1) CTA-Klicks: alle Elemente mit data-ga-cta="…" */
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

  /* 3) Section-Views: Sektionen mit data-ga-section="…" (einmal pro Seitenaufruf) */
  if ('IntersectionObserver' in window) {
    const sectionObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          track('section_view', { section: entry.target.getAttribute('data-ga-section') });
          sectionObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });
    document.querySelectorAll('[data-ga-section]').forEach(s => sectionObserver.observe(s));

    /* 4) Video-Sichtbarkeit: YouTube-Embeds, die in den Viewport scrollen */
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

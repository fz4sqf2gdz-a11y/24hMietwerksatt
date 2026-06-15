document.addEventListener('DOMContentLoaded', () => {

  // --- Navigation (Mobile) ---
  const navToggle = document.getElementById('navToggle');
  const nav = document.getElementById('mainNavigation') || document.querySelector('.nav');

  if (navToggle && nav) {
    navToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      nav.classList.toggle('active');
    });

    nav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => nav.classList.remove('active'));
    });

    document.addEventListener('click', (e) => {
      if (nav.classList.contains('active') &&
          !nav.contains(e.target) &&
          e.target !== navToggle) {
        nav.classList.remove('active');
      }
    });
  }

  // --- Modals ---
  const modalIds = ['whatsappModal', 'loginModal', 'sandstrahlModal'];

  modalIds.forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener('click', e => {
      if (e.target === el) closeModal(id);
    });
  });

  // --- Bild-Slider (Trockeneis) ---
  const track = document.getElementById('track');
  const nextBtn = document.getElementById('nextBtn');
  const prevBtn = document.getElementById('prevBtn');
  const slides = document.querySelectorAll('.slide');

  if (track && slides.length > 0) {
    let index = 0;
    const totalSlides = slides.length;
    let autoSlideInterval;

    const updateSlide = () => {
      track.style.transform = `translateX(-${index * 100}%)`;
    };

    const nextSlide = () => {
      index = (index + 1) % totalSlides;
      updateSlide();
    };

    const prevSlide = () => {
      index = (index - 1 + totalSlides) % totalSlides;
      updateSlide();
    };

    const startTimer = () => {
      if (autoSlideInterval) clearInterval(autoSlideInterval);
      autoSlideInterval = setInterval(nextSlide, 4000);
    };

    const resetTimer = () => {
      clearInterval(autoSlideInterval);
      startTimer();
    };

    nextBtn?.addEventListener('click', (e) => {
      e.preventDefault();
      nextSlide();
      resetTimer();
    });

    prevBtn?.addEventListener('click', (e) => {
      e.preventDefault();
      prevSlide();
      resetTimer();
    });

    startTimer();
  }

  // --- Scroll-Reveal (dezent, mit Stagger) ---
  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    revealEls.forEach((el, i) => {
      el.style.transitionDelay = `${Math.min(i * 0.06, 0.36)}s`;
    });

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    revealEls.forEach(el => observer.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('is-visible'));
  }

  // --- Sandstrahl-Hinweis (einmal pro Browser-Sitzung) ---
  const sandstrahlModal = document.getElementById('sandstrahlModal');
  const STORAGE_KEY = 'mws-sandstrahl-hinweis';

  if (sandstrahlModal && !sessionStorage.getItem(STORAGE_KEY)) {
    setTimeout(() => {
      if (typeof openModal === 'function') {
        openModal('sandstrahlModal');
        sessionStorage.setItem(STORAGE_KEY, '1');
      }
    }, 2200);
  }

});

function sendToWhatsapp(e, formId) {
  e.preventDefault();
  const form = document.getElementById(formId);
  if (!form) return;

  const nameInput = form.querySelector('[name="name"]');
  const msgInput = form.querySelector('[name="message"]');

  const name = nameInput ? nameInput.value : 'Kunde';
  const msg = msgInput ? msgInput.value : '';

  const text = `Hallo Werner, ich bin ${name}. ${msg}`;
  const encodedText = encodeURIComponent(text);
  const url = `https://wa.me/436645171370?text=${encodedText}`;

  const btn = form.querySelector('button');
  const oldText = btn ? btn.innerText : 'Senden';
  if (btn) btn.innerText = 'Wird geöffnet...';

  window.open(url, '_blank');

  setTimeout(() => {
    if (btn) btn.innerText = oldText;
    form.reset();
    ['whatsappModal', 'sandstrahlModal'].forEach(id => {
      const modal = document.getElementById(id);
      if (modal) modal.style.display = 'none';
    });
    document.body.style.overflow = '';
  }, 1000);
}

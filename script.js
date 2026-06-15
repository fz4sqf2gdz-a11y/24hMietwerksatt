document.addEventListener('DOMContentLoaded', () => {
  
  const navToggle = document.getElementById('navToggle');
  const nav = document.querySelector('.nav');
  
  if(navToggle && nav) {
    navToggle.addEventListener('click', () => {
      nav.classList.toggle('open');
    });

    nav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        nav.classList.remove('open');
      });
    });
  }

  const modal = document.getElementById('modal');
  const loginModal = document.getElementById('loginModal');
  const dryIceModal = document.getElementById('dryIceModal');

  const open = (el) => { if(el) { el.style.display='flex'; el.setAttribute('aria-hidden','false'); }};
  const close = (el) => { if(el) { el.style.display='none'; el.setAttribute('aria-hidden','true'); }};

  document.getElementById('openModal')?.addEventListener('click', () => open(modal));
  document.getElementById('closeModal')?.addEventListener('click', () => close(modal));
  document.getElementById('loginBtn')?.addEventListener('click', () => open(loginModal));
  document.getElementById('closeLogin')?.addEventListener('click', () => close(loginModal));

  [modal, loginModal, dryIceModal].forEach(m => {
    if(m) m.addEventListener('click', e => { if(e.target === m) close(m); });
  });


  const track = document.getElementById('track');
  const nextBtn = document.getElementById('nextBtn');
  const prevBtn = document.getElementById('prevBtn');
  const slides = document.querySelectorAll('.slide');

  if (track && slides.length > 0) {
    console.log("Slider gefunden, starte Logik..."); // Debug Info
    
    let index = 0;
    const totalSlides = slides.length;
    let autoSlideInterval;

    const updateSlide = () => {
      track.style.transform = `translateX(-${index * 100}%)`;
    };

    const nextSlide = () => {
      index = (index + 1) % totalSlides; // 0 -> 1 -> 2 -> 0
      updateSlide();
    };

    const prevSlide = () => {
      index = (index - 1 + totalSlides) % totalSlides; // 0 -> 2 -> 1 -> 0
      updateSlide();
    };

    const startTimer = () => {
      if(autoSlideInterval) clearInterval(autoSlideInterval);
      autoSlideInterval = setInterval(nextSlide, 4000);
    };

    const resetTimer = () => {
      clearInterval(autoSlideInterval);
      startTimer();
    };

    if(nextBtn) nextBtn.addEventListener('click', (e) => {
      e.preventDefault();
      nextSlide();
      resetTimer();
    });

    if(prevBtn) prevBtn.addEventListener('click', (e) => {
      e.preventDefault();
      prevSlide();
      resetTimer();
    });

    startTimer();
  } else {
    console.log("Kein Slider auf dieser Seite gefunden.");
  }

}); 

function sendToWhatsapp(e, formId) {
  e.preventDefault();
  const form = document.getElementById(formId);
  if(!form) return;

  const nameInput = form.querySelector('[name="name"]');
  const msgInput = form.querySelector('[name="message"]');
  
  const name = nameInput ? nameInput.value : "Kunde";
  const msg = msgInput ? msgInput.value : "";
  
  const text = `Hallo Werner, ich bin ${name}. ${msg}`;
  const encodedText = encodeURIComponent(text);
  
  const url = `https://wa.me/436645171370?text=${encodedText}`;
  
  const btn = form.querySelector('button');
  const oldText = btn ? btn.innerText : "Senden";
  if(btn) btn.innerText = "Wird geöffnet...";
  
  window.open(url, '_blank');
  
  setTimeout(() => {
    if(btn) btn.innerText = oldText;
    form.reset();
    const modal = document.getElementById('modal');
    if(modal) modal.style.display = 'none';
  }, 1000);
}
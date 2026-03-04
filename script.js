// Theme
const html = document.documentElement;
const saved = localStorage.getItem('theme') || 'dark';
html.setAttribute('data-theme', saved);

document.getElementById('themeToggle').addEventListener('click', () => {
  const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
});

// Mobile menu
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');

hamburger.addEventListener('click', () => mobileMenu.classList.toggle('active'));
mobileMenu.querySelectorAll('a').forEach(a =>
  a.addEventListener('click', () => mobileMenu.classList.remove('active'))
);

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    e.preventDefault();
    const t = document.querySelector(a.getAttribute('href'));
    if (t) t.scrollIntoView({ behavior: 'smooth' });
  });
});

// Active nav highlighting
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-links a');

function updateActiveNav() {
  let current = '';
  sections.forEach(s => {
    if (window.scrollY >= s.offsetTop - 120) current = s.id;
  });
  navLinks.forEach(l => {
    l.classList.toggle('active', l.getAttribute('href') === `#${current}`);
  });
}
window.addEventListener('scroll', updateActiveNav, { passive: true });

// Scroll animations with stagger
const observer = new IntersectionObserver(
  entries => entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      observer.unobserve(e.target);
    }
  }),
  { threshold: 0.06, rootMargin: '0px 0px -30px 0px' }
);

function addStagger(selector, animClass) {
  const els = document.querySelectorAll(selector);
  els.forEach((el, i) => {
    el.classList.add(animClass);
    if (animClass === 'fade-in') {
      el.classList.add('stagger-' + Math.min(i, 5));
    }
    observer.observe(el);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  // Timeline cards slide from left, staggered
  document.querySelectorAll('.exp-card').forEach((el, i) => {
    el.classList.add('fade-in-left');
    el.style.transitionDelay = (i * 0.12) + 's';
    observer.observe(el);
  });

  // Info cards slide from right, staggered
  document.querySelectorAll('.info-card').forEach((el, i) => {
    el.classList.add('fade-in-right');
    el.style.transitionDelay = (i * 0.1) + 's';
    observer.observe(el);
  });

  // Project cards scale up, staggered
  document.querySelectorAll('.project-card').forEach((el, i) => {
    el.classList.add('fade-in-scale');
    el.style.transitionDelay = (i * 0.1) + 's';
    observer.observe(el);
  });

  // Featured project
  document.querySelectorAll('.project-featured').forEach(el => {
    el.classList.add('fade-in');
    observer.observe(el);
  });

  // Achievement cards stagger
  document.querySelectorAll('.ach-card').forEach((el, i) => {
    el.classList.add('fade-in-scale');
    el.style.transitionDelay = (i * 0.1) + 's';
    observer.observe(el);
  });

  // Cert cards stagger
  document.querySelectorAll('.cert-card').forEach((el, i) => {
    el.classList.add('fade-in');
    el.style.transitionDelay = (i * 0.08) + 's';
    observer.observe(el);
  });

  // Skill groups stagger
  document.querySelectorAll('.skill-group').forEach((el, i) => {
    el.classList.add('fade-in');
    el.style.transitionDelay = (i * 0.1) + 's';
    observer.observe(el);
  });

  // Contact circles stagger
  document.querySelectorAll('.contact-circle').forEach((el, i) => {
    el.classList.add('fade-in-scale');
    el.style.transitionDelay = (i * 0.12) + 's';
    observer.observe(el);
  });

  // Portfolio other items
  document.querySelectorAll('.po-item').forEach((el, i) => {
    el.classList.add('fade-in');
    el.style.transitionDelay = (i * 0.1) + 's';
    observer.observe(el);
  });

  // Hero stats
  document.querySelectorAll('.hero-quick-stats .qs').forEach((el, i) => {
    el.classList.add('fade-in');
    el.style.transitionDelay = (i * 0.15) + 's';
    observer.observe(el);
  });
});

// Nav shadow on scroll + experience card stacking
const nav = document.getElementById('nav');
const expItems = document.querySelectorAll('.exp-item');
let ticking = false;

window.addEventListener('scroll', () => {
  if (!ticking) {
    requestAnimationFrame(() => {
      nav.style.boxShadow = window.scrollY > 60 ? 'var(--shadow)' : 'none';

      // Experience stacking: gradual fade/shrink as next card covers
      if (window.innerWidth > 768) {
        expItems.forEach((item, i) => {
          const nextItem = expItems[i + 1];
          if (!nextItem) {
            item.style.transform = '';
            item.style.opacity = '';
            return;
          }
          const rect = item.getBoundingClientRect();
          const nextRect = nextItem.getBoundingClientRect();
          const overlap = (rect.top + rect.height) - nextRect.top;
          const progress = Math.max(0, Math.min(1, overlap / rect.height));

          const scale = 1 - (progress * 0.05);
          const opacity = 1 - (progress * 0.6);

          item.style.transform = `scale3d(${scale},${scale},1)`;
          item.style.opacity = opacity;
        });
      }
      ticking = false;
    });
    ticking = true;
  }
}, { passive: true });

// Lightbox for images
const lightbox = document.getElementById('lightbox');
const lbImg = document.getElementById('lbImg');
const lbClose = document.getElementById('lbClose');

document.querySelectorAll('.clickable-img').forEach(el => {
  el.addEventListener('click', e => {
    e.stopPropagation();
    const src = el.dataset.full || el.src;
    if (!src) return;
    lbImg.src = src;
    lbImg.alt = el.alt || '';
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
  });
});

function closeLightbox() {
  lightbox.classList.remove('active');
  document.body.style.overflow = '';
  lbImg.src = '';
}
lbClose.addEventListener('click', closeLightbox);
lbImg.addEventListener('click', closeLightbox);
lightbox.addEventListener('click', e => {
  if (e.target === lightbox) closeLightbox();
});

// Close modals on Escape key
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    if (lightbox.classList.contains('active')) closeLightbox();
  }
});

// Contact form — AJAX submit via Formspree
const contactForm = document.getElementById('contactForm');
const formSuccess = document.getElementById('formSuccess');

if (contactForm) {
  contactForm.addEventListener('submit', async e => {
    e.preventDefault();
    const btn = contactForm.querySelector('.form-submit');
    btn.textContent = 'Sending...';
    btn.disabled = true;

    try {
      const res = await fetch(contactForm.action, {
        method: 'POST',
        body: new FormData(contactForm),
        headers: { 'Accept': 'application/json' }
      });

      if (res.ok) {
        contactForm.reset();
        formSuccess.style.display = 'block';
        btn.textContent = 'Send Message';
        btn.disabled = false;
      } else {
        btn.textContent = 'Failed. Try again.';
        btn.disabled = false;
      }
    } catch {
      btn.textContent = 'Failed. Try again.';
      btn.disabled = false;
    }
  });
}

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

// ── Case Studies Switcher ──────────────────────────────────────────────────
const CS_DATA = [
  {
    badge: 'Case Study',
    sub: 'Prop Trading · 2026',
    title: 'Retention Intelligence — Alametria',
    desc: '581,000 users. One retention label hiding 10 behaviors. $10.2M combined impact — from the existing user base alone.',
    slides: 'case-studies/alametria/retention-intelligence-slides.html',
    thumbGradient: 'linear-gradient(135deg, #0d1f35 0%, #1a3a5c 100%)',
    thumbLabel: 'Retention Intelligence',
    thumbStat: '$10.2M',
    thumbStatLabel: 'Identified Impact',
    doc: {
      title: "What's Inside",
      desc: 'Full methodology, framework, and results. 21 pages covering the complete analytical process from raw transaction data to $10.2M in measurable impact.',
      checklist: [
        'Behavioral Lifecycle Framework',
        '10-Segment Classification Model',
        'Results & $10.2M Impact Analysis',
        'SQL Methodology & Data Sources',
      ],
      readUrl: 'case-studies/alametria/retention-intelligence-casestudy.html',
      pdfUrl: 'case-studies/alametria/retention-intelligence-casestudy.pdf',
      pdfName: 'Retention-Intelligence-Alametria.pdf',
    }
  },
  {
    badge: 'Case Study',
    sub: 'Prop Trading · 2026',
    title: 'Project Boomerang — Alametria',
    desc: '1 in 3 customers who drop off come back. We built the system to predict, track, and act on every cycle — turning accidental returns into a $8.3M opportunity.',
    slides: 'case-studies/alametria-boomerang/boomerang-slides.html',
    thumbGradient: 'linear-gradient(135deg, #0d2a1a 0%, #1a4530 100%)',
    thumbLabel: 'Project Boomerang',
    thumbStat: '$8.3M',
    thumbStatLabel: 'Annual Opportunity',
    doc: {
      title: "What's Inside",
      desc: 'Full lifecycle framework, methodology, and opportunity analysis. Covers 500,000 customers across 5 drop-return cycles with $8.3M in estimated annual impact.',
      checklist: [
        'Drop + Return + Escape Framework',
        '5-Cycle Behavioral Tracking',
        'The 45-Day Critical Window',
        '$8.3M Opportunity Analysis',
      ],
      readUrl: 'case-studies/alametria-boomerang/boomerang-casestudy.html',
      pdfUrl: 'case-studies/alametria-boomerang/boomerang-casestudy.pdf',
      pdfName: 'Project-Boomerang-Alametria.pdf',
    }
  },
  // Add future case studies here — the switcher will handle them automatically
];

(function initCaseSwitcher() {
  let current = 0;

  const iframe    = document.getElementById('csIframe');
  const badge     = document.getElementById('csBadge');
  const badgeSub  = document.getElementById('csBadgeSub');
  const title     = document.getElementById('csTitle');
  const desc      = document.getElementById('csDesc');
  const csMore    = document.getElementById('csMore');
  const btnPrev   = document.getElementById('csPrev');
  const btnNext   = document.getElementById('csNext');
  const docTitle  = document.getElementById('csDocTitle');
  const docDesc   = document.getElementById('csDocDesc');
  const checklist = document.getElementById('csChecklist');
  const readBtn   = document.getElementById('csReadBtn');

  if (!iframe) return;

  const checkIcon = `<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13l4 4L19 7"/></svg>`;

  function renderMore() {
    if (!csMore) return;

    // Hide section entirely when only one case study
    const others = CS_DATA.filter((_, i) => i !== current);
    if (others.length === 0) { csMore.innerHTML = ''; return; }

    csMore.innerHTML = `
      <div class="cs-more-header">
        <h3>More <span>Case Studies</span></h3>
      </div>
      <div class="cs-more-grid">
        ${CS_DATA.map((cs, i) => `
          <button class="cs-more-card${i === current ? ' cs-more-active' : ''}" data-index="${i}">
            <div class="cs-more-thumb" style="background:${cs.thumbGradient}">
              <div class="cs-more-stat">
                <span class="cs-more-stat-num">${cs.thumbStat || ''}</span>
                <span class="cs-more-stat-lbl">${cs.thumbStatLabel || ''}</span>
              </div>
              <div class="cs-more-hover">
                <div class="cs-more-arrow">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                </div>
              </div>
            </div>
            <div class="cs-more-info">
              <span class="cs-more-tag">${cs.sub}</span>
              <h4>${cs.thumbLabel}</h4>
            </div>
          </button>
        `).join('')}
      </div>
    `;

    csMore.querySelectorAll('.cs-more-card').forEach(btn => {
      btn.addEventListener('click', () => goTo(+btn.dataset.index));
    });
  }

  function goTo(index) {
    if (index < 0 || index >= CS_DATA.length) return;
    current = index;
    const cs = CS_DATA[current];

    iframe.src   = cs.slides;
    badge.textContent    = cs.badge;
    badgeSub.textContent = cs.sub;
    title.textContent    = cs.title;
    desc.textContent     = cs.desc;

    docTitle.textContent = cs.doc.title;
    docDesc.textContent  = cs.doc.desc;
    checklist.innerHTML  = cs.doc.checklist.map(item => `
      <li><span class="cs-check">${checkIcon}</span>${item}</li>
    `).join('');

    readBtn.href = cs.doc.readUrl;

    btnPrev.disabled = current === 0;
    btnNext.disabled = current === CS_DATA.length - 1;

    renderMore();
  }

  btnPrev.addEventListener('click', () => goTo(current - 1));
  btnNext.addEventListener('click', () => goTo(current + 1));

  // Init
  goTo(0);
})();

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

// ── Case Study Share ──────────────────────────────────────────────────────────
(function initShareMenu() {
  const btn     = document.getElementById('csShareBtn');
  const menu    = document.getElementById('csShareMenu');
  const liLink  = document.getElementById('csShareLinkedIn');
  const waLink  = document.getElementById('csShareWhatsApp');

  if (!btn || !menu) return;

  const PORTFOLIO_BASE = 'https://saidulalam01.github.io';

  function getShareUrl() {
    const readBtn = document.getElementById('csReadBtn');
    const relUrl  = readBtn ? readBtn.getAttribute('href') : '';
    return PORTFOLIO_BASE + '/' + relUrl;
  }

  function updateLinks() {
    const url   = getShareUrl();
    const title = (document.getElementById('csTitle') || {}).textContent || 'Case Study';
    liLink.href = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`;
    waLink.href = `https://wa.me/?text=${encodeURIComponent(title + ' — ' + url)}`;
  }

  btn.addEventListener('click', e => {
    e.stopPropagation();
    const isOpen = !menu.classList.contains('open');
    if (isOpen) {
      updateLinks();
      const r = btn.getBoundingClientRect();
      menu.style.right  = (window.innerWidth - r.right) + 'px';
      menu.style.top    = (r.bottom + 8) + 'px';
      menu.style.bottom = '';
      menu.classList.add('open');
    } else {
      menu.classList.remove('open');
    }
  });

  document.addEventListener('click', e => {
    if (!btn.contains(e.target) && !menu.contains(e.target)) {
      menu.classList.remove('open');
    }
  });
})();

function csCopyLink() {
  const readBtn = document.getElementById('csReadBtn');
  const relUrl  = readBtn ? readBtn.getAttribute('href') : '';
  const fullUrl = 'https://saidulalam01.github.io/' + relUrl;
  const textEl  = document.getElementById('csCopyText');

  navigator.clipboard.writeText(fullUrl).then(() => {
    textEl.textContent = 'Copied!';
    setTimeout(() => { textEl.textContent = 'Copy Link'; }, 2000);
  }).catch(() => {
    textEl.textContent = 'Copy failed';
    setTimeout(() => { textEl.textContent = 'Copy Link'; }, 2000);
  });

  document.getElementById('csShareMenu').classList.remove('open');
}

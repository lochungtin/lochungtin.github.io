// ── Hamburger menu (same logic as main.js) ───────────────────────────
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');

hamburger.addEventListener('click', () => {
  const isOpen = hamburger.classList.toggle('open');
  mobileMenu.classList.toggle('open', isOpen);
  document.body.style.overflow = isOpen ? 'hidden' : '';
});

mobileMenu.querySelectorAll('.mobile-menu-item').forEach(link => {
  link.addEventListener('click', () => {
    hamburger.classList.remove('open');
    mobileMenu.classList.remove('open');
    document.body.style.overflow = '';
  });
});

// ── TOC dropdown toggle (mobile) ─────────────────────────────────────
const tocToggle = document.getElementById('tocToggle');
const tocLinks  = document.getElementById('tocLinks');

if (tocToggle && tocLinks) {
  tocToggle.addEventListener('click', () => {
    const isOpen = tocToggle.classList.toggle('open');
    tocLinks.classList.toggle('open', isOpen);
  });

  // Close TOC when a section link is tapped
  tocLinks.querySelectorAll('.proj-toc-item').forEach(link => {
    link.addEventListener('click', () => {
      tocToggle.classList.remove('open');
      tocLinks.classList.remove('open');
    });
  });
}

// ── Sidebar active section highlight ────────────────────────────────
const sidebarLinks = document.querySelectorAll('.proj-sidebar-link');
const sections = document.querySelectorAll('.proj-section[id]');

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.id;
      sidebarLinks.forEach(link => {
        link.classList.toggle('active', link.dataset.section === id);
      });
    }
  });
}, {
  rootMargin: '-64px 0px -60% 0px',
  threshold: 0
});

sections.forEach(s => observer.observe(s));

// ── Number the "What's Next" list items ─────────────────────────────
document.querySelectorAll('.proj-next-list li').forEach((li, i) => {
  li.setAttribute('data-n', String(i + 1).padStart(2, '0'));
});

// ── Stagger dot cluster opacity on load ─────────────────────────────
document.querySelectorAll('.proj-dot-cluster span').forEach((dot, i) => {
  dot.style.opacity = 0;
  dot.style.transition = `opacity .4s ease ${i * 0.05}s`;
  setTimeout(() => { dot.style.opacity = 0.25; }, 80);
});

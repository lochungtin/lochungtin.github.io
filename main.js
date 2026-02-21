// Hamburger menu toggle
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');

hamburger.addEventListener('click', () => {
  const isOpen = hamburger.classList.toggle('open');
  mobileMenu.classList.toggle('open', isOpen);
  document.body.style.overflow = isOpen ? 'hidden' : '';
});

// Close menu when a link is tapped
mobileMenu.querySelectorAll('.mobile-menu-item').forEach(link => {
  link.addEventListener('click', () => {
    hamburger.classList.remove('open');
    mobileMenu.classList.remove('open');
    document.body.style.overflow = '';
  });
});

// Fade in on scroll + trigger skill bar animations
const fadeEls = document.querySelectorAll('.fade-in');
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      e.target.querySelectorAll('.skill-bar-fill').forEach((bar, i) => {
        bar.style.transitionDelay = `${i * 0.06}s`;
      });
    }
  });
}, { threshold: 0.08 });
fadeEls.forEach(el => io.observe(el));

// Stagger hero dots on load
const dots = document.querySelectorAll('.hero-dot-grid span');
dots.forEach((d, i) => {
  d.style.opacity = 0;
  d.style.transition = `opacity .4s ease ${i * 0.03}s`;
  setTimeout(() => { d.style.opacity = 1; }, 100);
});

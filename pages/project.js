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

// ── Horizontal galleries: prev/next buttons + counter ───────────────
document.querySelectorAll('.proj-gallery').forEach(gallery => {
  const track = gallery.querySelector('.proj-gallery-track');
  const items = [...track.querySelectorAll('.proj-gallery-item')];
  const current = gallery.querySelector('.proj-gallery-current');
  const [prev, next] = gallery.querySelectorAll('.proj-gallery-btn');

  const index = () => {
    const left = track.scrollLeft;
    let best = 0;
    items.forEach((item, i) => {
      if (Math.abs(item.offsetLeft - track.offsetLeft - left) <
          Math.abs(items[best].offsetLeft - track.offsetLeft - left)) best = i;
    });
    return best;
  };

  const update = () => {
    const i = index();
    current.textContent = String(i + 1).padStart(2, '0');
    const atEnd = track.scrollLeft + track.clientWidth >= track.scrollWidth - 2;
    prev.disabled = i === 0 && track.scrollLeft <= 2;
    next.disabled = atEnd;
  };

  const go = dir => {
    const target = items[Math.max(0, Math.min(items.length - 1, index() + dir))];
    track.scrollTo({ left: target.offsetLeft - track.offsetLeft, behavior: 'smooth' });
  };

  prev.addEventListener('click', () => go(-1));
  next.addEventListener('click', () => go(1));
  track.addEventListener('keydown', ev => {
    if (ev.key === 'ArrowLeft')  { ev.preventDefault(); go(-1); }
    if (ev.key === 'ArrowRight') { ev.preventDefault(); go(1); }
  });
  track.addEventListener('scroll', () => requestAnimationFrame(update), { passive: true });
  window.addEventListener('resize', update);
  update();
});

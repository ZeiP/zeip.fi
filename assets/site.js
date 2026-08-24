document.addEventListener('DOMContentLoaded', () => {
  const menuButton = document.querySelector('.mobile-menu');
  const mobileNav = document.querySelector('#mobile-nav');
  if (menuButton && mobileNav) {
    menuButton.addEventListener('click', () => {
      const expanded = menuButton.getAttribute('aria-expanded') === 'true';
      menuButton.setAttribute('aria-expanded', String(!expanded));
      mobileNav.hidden = expanded;
    });
  }

  const articleImages = document.querySelectorAll('.article-body p > img:only-child');
  if (!articleImages.length) {
    return;
  }

  const lightbox = document.createElement('div');
  lightbox.className = 'lightbox';
  lightbox.hidden = true;
  lightbox.innerHTML = [
    '<button class="lightbox-close" type="button" aria-label="Close image view">x</button>',
    '<button class="lightbox-nav lightbox-prev" type="button" aria-label="Previous image">‹</button>',
    '<img class="lightbox-image" alt="">',
    '<button class="lightbox-nav lightbox-next" type="button" aria-label="Next image">›</button>',
    '<div class="lightbox-caption"></div>',
  ].join('');
  document.body.appendChild(lightbox);

  const lightboxImage = lightbox.querySelector('.lightbox-image');
  const lightboxCaption = lightbox.querySelector('.lightbox-caption');
  const closeButton = lightbox.querySelector('.lightbox-close');
  const prevButton = lightbox.querySelector('.lightbox-prev');
  const nextButton = lightbox.querySelector('.lightbox-next');
  const gallery = [];
  let currentIndex = -1;

  const closeLightbox = () => {
    lightbox.hidden = true;
    document.body.classList.remove('lightbox-open');
    lightboxImage.removeAttribute('src');
    lightboxImage.alt = '';
    lightboxCaption.textContent = '';
    currentIndex = -1;
  };

  const showImage = (index) => {
    currentIndex = (index + gallery.length) % gallery.length;
    const item = gallery[currentIndex];
    const position = gallery.length > 1 ? ` (${currentIndex + 1}/${gallery.length})` : '';

    lightboxImage.src = item.src;
    lightboxImage.alt = item.alt || item.caption;
    lightboxCaption.textContent = item.caption ? `${item.caption}${position}` : position.trim();
    prevButton.hidden = gallery.length < 2;
    nextButton.hidden = gallery.length < 2;
  };

  const openLightbox = (index) => {
    showImage(index);
    lightbox.hidden = false;
    document.body.classList.add('lightbox-open');
    closeButton.focus();
  };

  articleImages.forEach((image, index) => {
    const paragraph = image.parentElement;
    const caption = image.getAttribute('title') || image.alt || '';
    const figure = document.createElement('figure');
    const link = document.createElement('a');
    const src = image.currentSrc || image.src;

    gallery.push({
      src,
      alt: image.alt || '',
      caption,
    });

    figure.className = 'article-image';
    link.className = 'article-image-link';
    link.href = src;
    link.setAttribute('aria-label', caption ? `Open full-size image: ${caption}` : 'Open full-size image');

    paragraph.replaceWith(figure);
    figure.appendChild(link);
    link.appendChild(image);

    if (caption) {
      const figcaption = document.createElement('figcaption');
      figcaption.textContent = caption;
      figure.appendChild(figcaption);
    }

    link.addEventListener('click', (event) => {
      event.preventDefault();
      openLightbox(index);
    });
  });

  closeButton.addEventListener('click', closeLightbox);
  prevButton.addEventListener('click', () => showImage(currentIndex - 1));
  nextButton.addEventListener('click', () => showImage(currentIndex + 1));
  lightbox.addEventListener('click', (event) => {
    if (event.target === lightbox) {
      closeLightbox();
    }
  });
  document.addEventListener('keydown', (event) => {
    if (lightbox.hidden) {
      return;
    }
    if (event.key === 'Escape') {
      closeLightbox();
    } else if (event.key === 'ArrowLeft' && gallery.length > 1) {
      showImage(currentIndex - 1);
    } else if (event.key === 'ArrowRight' && gallery.length > 1) {
      showImage(currentIndex + 1);
    }
  });
});

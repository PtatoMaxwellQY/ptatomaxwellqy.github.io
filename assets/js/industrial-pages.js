(function () {
    var root = document.documentElement;
    var toggle = document.getElementById('theme-toggle');
    var storageKey = 'optihk-theme';
    var storedTheme = null;

    try {
        storedTheme = localStorage.getItem(storageKey);
    } catch (error) {
        storedTheme = null;
    }

    function setTheme(choice, persist) {
        root.setAttribute('data-theme', choice);
        if (toggle) toggle.setAttribute('data-theme', choice);
        document.querySelectorAll('.theme-logo').forEach(function (logo) {
            var nextSource = choice === 'bright' ? logo.getAttribute('data-logo-bright') : logo.getAttribute('data-logo-dark');
            if (nextSource && logo.getAttribute('src') !== nextSource) {
                logo.setAttribute('src', nextSource);
            }
        });
        if (persist) {
            try {
                localStorage.setItem('optihk-theme', choice);
            } catch (error) {
                return;
            }
        }
    }

    if (toggle) {
        toggle.addEventListener('click', function () {
            var current = root.getAttribute('data-theme');
            setTheme(current === 'bright' ? 'dark' : 'bright', true);
        });
    }

    setTheme(storedTheme || root.getAttribute('data-theme') || 'bright', false);
})();

(function () {
    var menu = document.getElementById('mobile-menu');
    var openButton = document.querySelector('.menu-toggle');
    var closeButton = document.querySelector('.menu-close');
    if (!menu || !openButton || !closeButton) return;

    function setMenu(open) {
        menu.classList.toggle('is-open', open);
        menu.setAttribute('aria-hidden', String(!open));
        openButton.setAttribute('aria-expanded', String(open));
        document.body.style.overflow = open ? 'hidden' : '';
    }

    openButton.addEventListener('click', function () { setMenu(true); });
    closeButton.addEventListener('click', function () { setMenu(false); });
    menu.addEventListener('click', function (event) {
        if (event.target === menu || event.target.tagName === 'A') setMenu(false);
    });
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') setMenu(false);
    });
})();

(function () {
    var groups = document.querySelectorAll('[data-filter-group]');
    groups.forEach(function (group) {
        var buttons = group.querySelectorAll('[data-filter-target]');
        var items = document.querySelectorAll('[data-filter-item]');
        if (!buttons.length || !items.length) return;

        function setFilter(target) {
            buttons.forEach(function (button) {
                button.setAttribute('aria-pressed', String(button.getAttribute('data-filter-target') === target));
            });
            items.forEach(function (item) {
                var match = target === 'all' || item.getAttribute('data-filter-item') === target;
                item.classList.toggle('is-filtered-out', !match);
            });
        }

        buttons.forEach(function (button) {
            button.addEventListener('click', function () {
                setFilter(button.getAttribute('data-filter-target'));
            });
        });
    });
})();

(function () {
    var details = document.querySelectorAll('details.job-card');
    details.forEach(function (item) {
        function sync() {
            item.classList.toggle('is-open', item.open);
        }
        item.addEventListener('toggle', sync);
        sync();
    });
})();

(function () {
    var reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var revealSelectors = [
        '.section-head',
        '.why-card',
        '.pathway',
        '.product-lane',
        '.precision-card',
        '.process-band',
        '.job-card',
        '.inquiry-panel',
        '.team-card',
        '.featured-news',
        '.news-card'
    ];

    revealSelectors.forEach(function (selector) {
        document.querySelectorAll(selector).forEach(function (item) {
            item.classList.add('reveal-on-scroll');
        });
    });

    document.querySelectorAll('.team-grid, .product-wrap, .precision-grid, .jobs-wrap, .news-grid, .pathway-grid, .why-grid').forEach(function (group) {
        group.querySelectorAll('.reveal-on-scroll').forEach(function (item, index) {
            item.style.setProperty('--reveal-delay', Math.min(index, 5) * 90 + 'ms');
        });
    });

    document.querySelectorAll('.reveal-on-scroll').forEach(function (item, index) {
        if (!item.style.getPropertyValue('--reveal-delay')) {
            item.style.setProperty('--reveal-delay', (index % 3) * 80 + 'ms');
        }
        if (!item.hasAttribute('data-reveal-style')) {
            var style = 'lift';
            if (item.matches('.product-lane, .pathway, .featured-news')) {
                style = index % 2 === 0 ? 'slide-left' : 'slide-right';
            } else if (item.matches('.team-card, .news-card, .why-card')) {
                style = 'zoom';
            } else if (item.matches('.job-card, .precision-card')) {
                style = index % 2 === 0 ? 'slide-left' : 'slide-right';
            }
            item.setAttribute('data-reveal-style', style);
        }
    });

    var revealItems = document.querySelectorAll('.reveal-on-scroll');
    if (reducedMotion || !('IntersectionObserver' in window)) {
        revealItems.forEach(function (item) { item.classList.add('is-visible'); });
        return;
    }

    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.14, rootMargin: '0px 0px -8% 0px' });

    revealItems.forEach(function (item) {
        observer.observe(item);
    });
})();

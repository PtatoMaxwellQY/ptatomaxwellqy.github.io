(function () {
    var root = document.documentElement;
    var buttons = document.querySelectorAll('[data-theme-choice]');
    var storageKey = 'optihk-theme';
    var storedTheme = null;

    try {
        storedTheme = localStorage.getItem(storageKey);
    } catch (error) {
        storedTheme = null;
    }

    function setTheme(choice, persist) {
        root.setAttribute('data-theme', choice);
        buttons.forEach(function (button) {
            button.setAttribute('aria-pressed', String(button.getAttribute('data-theme-choice') === choice));
        });
        if (persist) {
            try {
                localStorage.setItem('optihk-theme', choice);
            } catch (error) {
                return;
            }
        }
    }

    buttons.forEach(function (button) {
        button.addEventListener('click', function () {
            setTheme(button.getAttribute('data-theme-choice'), true);
        });
    });

    setTheme(storedTheme || root.getAttribute('data-theme') || 'dark', false);
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
    }, { threshold: 0.16 });

    revealItems.forEach(function (item, index) {
        item.style.transitionDelay = (index % 3) * 80 + 'ms';
        observer.observe(item);
    });
})();

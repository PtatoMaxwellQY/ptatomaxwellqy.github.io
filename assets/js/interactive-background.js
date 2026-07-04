(function () {
    var canvas = document.getElementById('bg-canvas');
    if (!canvas || !canvas.getContext) return;

    var ctx = canvas.getContext('2d');
    if (!ctx) return;

    var root = document.documentElement;
    var reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var variant = canvas.getAttribute('data-bg-variant') || 'product';
    var width = 0;
    var height = 0;
    var particles = [];
    var pointerX = -1000;
    var pointerY = -1000;
    var pointerPresent = false;
    var resizeTimer = null;
    var frameInterval = reducedMotion ? 1000 / 24 : 0;
    var lastFrameTime = 0;

    var variants = {
        home: {
            count: 118,
            distance: 156,
            forceDistance: 190,
            force: 1.9,
            drift: 0.035,
            speed: 0.36,
            lineWidth: 1,
            dotSize: 2.1,
            dark: { line: [168, 218, 220], glow: '#A8DADC', dot: '#E63946' },
            bright: { line: [0, 109, 119], glow: '#457B9D', dot: '#E63946' }
        },
        product: {
            count: 168,
            distance: 172,
            forceDistance: 180,
            force: 1.8,
            drift: 0.06,
            speed: 0.5,
            lineWidth: 1.2,
            dotSize: 2.8,
            dark: { line: [102, 167, 173], glow: '#A8DADC', dot: '#E8687F' },
            bright: { line: [69, 123, 157], glow: '#006D77', dot: '#D90429' }
        },
        technology: {
            count: 150,
            distance: 166,
            forceDistance: 190,
            force: 1.95,
            drift: 0.045,
            speed: 0.44,
            lineWidth: 1.1,
            dotSize: 2.35,
            dark: { line: [143, 176, 196], glow: '#8FB0C4', dot: '#A8DADC' },
            bright: { line: [88, 108, 122], glow: '#457B9D', dot: '#006D77' }
        },
        careers: {
            count: 130,
            distance: 158,
            forceDistance: 184,
            force: 1.85,
            drift: 0.04,
            speed: 0.38,
            lineWidth: 1,
            dotSize: 2.25,
            dark: { line: [235, 97, 107], glow: '#E63946', dot: '#F1FAEE' },
            bright: { line: [174, 3, 33], glow: '#006D77', dot: '#457B9D' }
        },
        news: {
            count: 118,
            distance: 150,
            forceDistance: 176,
            force: 1.7,
            drift: 0.034,
            speed: 0.34,
            lineWidth: 0.95,
            dotSize: 2.05,
            dark: { line: [125, 211, 252], glow: '#7DD3FC', dot: '#38BDF8' },
            bright: { line: [14, 165, 233], glow: '#38BDF8', dot: '#0284C7' }
        },
        team: {
            count: 136,
            distance: 160,
            forceDistance: 184,
            force: 1.85,
            drift: 0.038,
            speed: 0.4,
            lineWidth: 1,
            dotSize: 2.2,
            dark: { line: [51, 138, 146], glow: '#66A7AD', dot: '#66A7AD' },
            bright: { line: [51, 138, 146], glow: '#006D77', dot: '#66A7AD' }
        }
    };

    function currentTheme() {
        return root.getAttribute('data-theme') === 'bright' ? 'bright' : 'dark';
    }

    function themeBackground() {
        var fallback = currentTheme() === 'bright' ? '#F1FAEE' : '#09090D';
        if (!window.getComputedStyle) return fallback;

        var value = window.getComputedStyle(root).getPropertyValue('--opti-bg').trim();
        return value || fallback;
    }

    function settings() {
        var config = variants[variant] || variants.product;
        var colors = config[currentTheme()] || config.dark;
        return {
            bg: themeBackground(),
            line: colors.line,
            glow: colors.glow,
            dot: colors.dot,
            count: config.count,
            distance: config.distance,
            forceDistance: config.forceDistance,
            force: config.force,
            drift: config.drift,
            speed: config.speed,
            lineWidth: config.lineWidth,
            dotSize: config.dotSize
        };
    }

    function particleCount(baseCount) {
        if (width <= 480) return Math.max(38, Math.round(baseCount * 0.46));
        if (width <= 800) return Math.max(58, Math.round(baseCount * 0.72));
        return baseCount;
    }

    function initParticles() {
        var config = settings();
        var count = reducedMotion ? Math.max(48, Math.round(particleCount(config.count) * 0.82)) : particleCount(config.count);
        var margin = 30;

        particles = [];
        for (var i = 0; i < count; i += 1) {
            particles.push({
                x: Math.random() * Math.max(1, width - 2 * margin) + margin,
                y: Math.random() * Math.max(1, height - 2 * margin) + margin,
                vx: (Math.random() - 0.5) * config.speed,
                vy: (Math.random() - 0.5) * config.speed,
                phase: Math.random() * Math.PI * 2,
                sway: 0.55 + Math.random() * 0.75
            });
        }
    }

    function resizeCanvas() {
        var pixelRatio = Math.min(window.devicePixelRatio || 1, 2);
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = Math.ceil(width * pixelRatio);
        canvas.height = Math.ceil(height * pixelRatio);
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
        initParticles();
        draw();
    }

    function onPointerMove(event) {
        if (typeof event.clientX !== 'number' || typeof event.clientY !== 'number') return;
        pointerX = event.clientX;
        pointerY = event.clientY;
        pointerPresent = true;
        if (reducedMotion && width && height) {
            updateParticles();
            draw();
        }
    }

    function resetPointer() {
        pointerX = -1000;
        pointerY = -1000;
        pointerPresent = false;
    }

    function updateParticles() {
        var config = settings();
        var margin = 30;
        var time = performance.now() * 0.001;
        var idleFlow = reducedMotion ? 0.018 : 0.026;

        particles.forEach(function (particle) {
            if (pointerPresent) {
                var dx = particle.x - pointerX;
                var dy = particle.y - pointerY;
                var dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < config.forceDistance && dist > 0.5) {
                    var intensity = 1 - dist / config.forceDistance;
                    var force = (intensity * intensity + intensity * 0.35) * config.force;
                    particle.vx += (dx / dist) * force;
                    particle.vy += (dy / dist) * force;
                }
            }

            particle.vx += Math.cos(time * 0.72 + particle.phase) * idleFlow * particle.sway;
            particle.vy += Math.sin(time * 0.58 + particle.phase) * idleFlow * particle.sway;
            particle.vx += (Math.random() - 0.5) * config.drift;
            particle.vy += (Math.random() - 0.5) * config.drift;
            particle.vx *= 0.96;
            particle.vy *= 0.96;
            particle.x += particle.vx;
            particle.y += particle.vy;

            if (particle.x < margin || particle.x > width - margin) particle.vx *= -0.9;
            if (particle.y < margin || particle.y > height - margin) particle.vy *= -0.9;

            particle.x = Math.min(width - margin, Math.max(margin, particle.x));
            particle.y = Math.min(height - margin, Math.max(margin, particle.y));
        });
    }

    function draw() {
        var config = settings();

        ctx.clearRect(0, 0, width, height);
        ctx.fillStyle = config.bg;
        ctx.fillRect(0, 0, width, height);
        ctx.lineWidth = config.lineWidth;
        ctx.shadowColor = config.glow;
        ctx.shadowBlur = 6;

        for (var i = 0; i < particles.length; i += 1) {
            for (var j = i + 1; j < particles.length; j += 1) {
                var p1 = particles[i];
                var p2 = particles[j];
                var dx = p1.x - p2.x;
                var dy = p1.y - p2.y;
                var dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < config.distance) {
                    var alpha = 1 - dist / config.distance * 0.5;
                    ctx.strokeStyle = 'rgba(' + config.line[0] + ', ' + config.line[1] + ', ' + config.line[2] + ', ' + alpha + ')';
                    ctx.beginPath();
                    ctx.moveTo(p1.x, p1.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.stroke();
                }
            }
        }

        ctx.shadowBlur = 8;
        ctx.shadowColor = config.dot;
        ctx.fillStyle = config.dot;
        particles.forEach(function (particle) {
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, config.dotSize, 0, Math.PI * 2);
            ctx.fill();
        });
        ctx.shadowBlur = 0;
    }

    function animate(timestamp) {
        var now = timestamp || performance.now();
        if (frameInterval && now - lastFrameTime < frameInterval) {
            requestAnimationFrame(animate);
            return;
        }
        lastFrameTime = now;
        updateParticles();
        draw();
        requestAnimationFrame(animate);
    }

    window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(resizeCanvas, 80);
    });
    document.addEventListener('pointermove', onPointerMove, { passive: true });
    canvas.addEventListener('pointermove', onPointerMove, { passive: true });
    document.addEventListener('pointerleave', resetPointer);
    window.addEventListener('mousemove', onPointerMove, { passive: true });
    window.addEventListener('mouseleave', resetPointer);
    window.addEventListener('blur', resetPointer);

    if ('MutationObserver' in window) {
        new MutationObserver(function () {
            draw();
        }).observe(root, { attributes: true, attributeFilter: ['data-theme'] });
    }

    resizeCanvas();
    animate();
})();

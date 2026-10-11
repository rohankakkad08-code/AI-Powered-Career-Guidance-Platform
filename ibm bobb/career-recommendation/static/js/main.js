/* ============================================================
   CAREERAI MAIN.JS
   - Animated background particles
   - Navbar scroll effect
   - Typed text animation
   - Counter animation
   - Scroll-reveal (fade-in-up / fade-in-right)
   - Multi-step form with sidebar updates
   - Enhanced range sliders
   - Results page bar animations
   ============================================================ */

// ============================================================
// 1. BACKGROUND PARTICLES
// ============================================================
(function createParticles() {
    const container = document.getElementById('bgParticles');
    if (!container) return;

    const colors = ['#4f46e5', '#7c3aed', '#0ea5e9', '#22c55e', '#f97316', '#a855f7'];
    const count = 18;

    for (let i = 0; i < count; i++) {
        const p = document.createElement('div');
        p.className = 'particle';
        const size = Math.random() * 120 + 40;
        p.style.cssText = `
            width: ${size}px;
            height: ${size}px;
            left: ${Math.random() * 100}%;
            bottom: -${size}px;
            background: ${colors[Math.floor(Math.random() * colors.length)]};
            animation-duration: ${Math.random() * 20 + 15}s;
            animation-delay: ${Math.random() * 15}s;
            filter: blur(${Math.random() * 20 + 10}px);
            opacity: 0.07;
        `;
        container.appendChild(p);
    }
})();

// ============================================================
// 2. NAVBAR SCROLL EFFECT
// ============================================================
const navbar = document.getElementById('navbar');
if (navbar) {
    window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 20);
    });
}

// ============================================================
// 3. SCROLL REVEAL OBSERVER
// ============================================================
const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.fade-in-up, .fade-in-right').forEach(el => {
    revealObserver.observe(el);
});

// ============================================================
// 4. TYPED TEXT ANIMATION (hero)
// ============================================================
(function typedText() {
    const el = document.getElementById('typedText');
    if (!el) return;

    const phrases = [
        'Perfect Career',
        'Dream Path',
        'Ideal Future',
        'True Calling'
    ];

    // Add cursor element
    const cursor = document.createElement('span');
    cursor.className = 'typed-cursor';
    el.parentNode.insertBefore(cursor, el.nextSibling);

    let phraseIdx = 0, charIdx = 0, deleting = false;

    function type() {
        const currentPhrase = phrases[phraseIdx];
        if (!deleting) {
            el.textContent = currentPhrase.slice(0, ++charIdx);
            if (charIdx === currentPhrase.length) {
                deleting = true;
                setTimeout(type, 1800);
                return;
            }
        } else {
            el.textContent = currentPhrase.slice(0, --charIdx);
            if (charIdx === 0) {
                deleting = false;
                phraseIdx = (phraseIdx + 1) % phrases.length;
                setTimeout(type, 400);
                return;
            }
        }
        setTimeout(type, deleting ? 60 : 90);
    }

    setTimeout(type, 600);
})();

// ============================================================
// 5. COUNTER ANIMATION (hero stats)
// ============================================================
(function counterAnimation() {
    const nums = document.querySelectorAll('.stat-num');
    if (!nums.length) return;

    const obs = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            const el = entry.target;
            const target = parseInt(el.dataset.target || '0', 10);
            let current = 0;
            const step = Math.ceil(target / 40);
            const interval = setInterval(() => {
                current = Math.min(current + step, target);
                el.textContent = current;
                if (current >= target) clearInterval(interval);
            }, 35);
            obs.unobserve(el);
        });
    }, { threshold: 0.5 });

    nums.forEach(el => obs.observe(el));
})();

// ============================================================
// 6. MULTI-STEP FORM
// ============================================================
const STEP_TIPS = [
    'Be honest — there are no right or wrong answers!',
    'Rate yourself fairly — overrating won\'t help your results.',
    'Choose what truly motivates you, not what sounds impressive.'
];

function goToStep(step) {
    const currentActive = document.querySelector('.form-step.active');
    const currentNum = currentActive ? parseInt(currentActive.id.replace('step', '')) : 1;

    // Validate required fields on forward navigation
    if (step > currentNum) {
        const required = document.querySelectorAll(`#step${currentNum} [required]`);
        for (const input of required) {
            if (!input.value) {
                input.focus();
                input.classList.add('input-error');
                input.style.borderColor = '#ef4444';
                input.style.boxShadow = '0 0 0 4px rgba(239,68,68,0.12)';
                setTimeout(() => {
                    input.classList.remove('input-error');
                    input.style.borderColor = '';
                    input.style.boxShadow = '';
                }, 2500);
                shakeElement(input);
                return;
            }
        }
        // Mark current step as done in sidebar
        const sb = document.getElementById(`sb${currentNum}`);
        if (sb) {
            sb.classList.remove('active');
            sb.classList.add('done');
        }
    }

    // Hide all steps
    document.querySelectorAll('.form-step').forEach(s => s.classList.remove('active'));

    // Show target step
    const target = document.getElementById('step' + step);
    if (target) target.classList.add('active');

    // Update sidebar
    const sbNew = document.getElementById(`sb${step}`);
    if (sbNew) {
        sbNew.classList.remove('done');
        sbNew.classList.add('active');
    }

    // Update progress bar
    const pct = Math.round((step / 3) * 100);
    const bar = document.getElementById('progressBar');
    const pctEl = document.getElementById('stepPct');
    const labelEl = document.getElementById('stepLabel');

    if (bar) bar.style.width = pct + '%';
    if (pctEl) pctEl.textContent = pct + '%';
    if (labelEl) labelEl.textContent = `Step ${step} of 3`;

    // Update tip
    const tipEl = document.getElementById('tipText');
    if (tipEl) {
        tipEl.style.opacity = '0';
        setTimeout(() => {
            tipEl.textContent = STEP_TIPS[step - 1];
            tipEl.style.opacity = '1';
        }, 200);
    }

    // If going back, un-mark done
    if (step > 1 && step <= currentNum) {
        for (let i = step; i <= currentNum; i++) {
            const sb = document.getElementById(`sb${i}`);
            if (sb) {
                sb.classList.remove('done');
                if (i === step) sb.classList.add('active');
            }
        }
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function shakeElement(el) {
    el.animate([
        { transform: 'translateX(0)' },
        { transform: 'translateX(-6px)' },
        { transform: 'translateX(6px)' },
        { transform: 'translateX(-4px)' },
        { transform: 'translateX(4px)' },
        { transform: 'translateX(0)' }
    ], { duration: 350, easing: 'ease-out' });
}

// ============================================================
// 7. RANGE SLIDERS — live value + fill
// ============================================================
const sliders = [
    { rangeId: 'analyticalRange', valId: 'analyticalVal', fillId: 'analyticalFill' },
    { rangeId: 'codingRange',     valId: 'codingVal',     fillId: 'codingFill' },
    { rangeId: 'commRange',       valId: 'commVal',       fillId: 'commFill' },
    { rangeId: 'creativeRange',   valId: 'creativeVal',   fillId: 'creativeFill' },
    { rangeId: 'psRange',         valId: 'psVal',         fillId: 'psFill' },
    { rangeId: 'resRange',        valId: 'resVal',        fillId: 'resFill' },
];

sliders.forEach(({ rangeId, valId, fillId }) => {
    const range = document.getElementById(rangeId);
    const val   = document.getElementById(valId);
    const fill  = document.getElementById(fillId);
    if (!range) return;

    function update() {
        const pct = ((range.value - range.min) / (range.max - range.min)) * 100;
        if (val) val.textContent = range.value;
        if (fill) fill.style.width = pct + '%';
    }

    range.addEventListener('input', update);
    update();
});

// ============================================================
// 8. FORM SUBMIT LOADING STATE
// ============================================================
const form = document.getElementById('assessmentForm');
if (form) {
    form.addEventListener('submit', function () {
        const btn    = document.getElementById('submitBtn');
        const text   = document.getElementById('submitText');
        const loader = document.getElementById('btnLoader');
        if (btn && text && loader) {
            text.textContent = 'Analysing your profile…';
            loader.style.display = 'block';
            btn.disabled = true;
        }
    });
}

// ============================================================
// 9. RESULTS PAGE — animate bars on load
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
    // Skill bars (data-width attribute)
    const skillFills = document.querySelectorAll('.skill-bar-fill');
    skillFills.forEach(el => {
        const target = el.dataset.width || '0%';
        el.style.width = '0%';
        setTimeout(() => { el.style.width = target; }, 300);
    });

    // Match bars (data-width attribute)
    const matchFills = document.querySelectorAll('.rc-match-bar');
    matchFills.forEach((el, i) => {
        const target = el.dataset.width || '0%';
        el.style.width = '0%';
        setTimeout(() => { el.style.width = target; }, 500 + i * 120);
    });
});

// ============================================================
// 10. HAMBURGER MENU (mobile)
// ============================================================
const hamburger = document.getElementById('hamburger');
if (hamburger) {
    hamburger.addEventListener('click', () => {
        const navLinks = document.querySelector('.nav-links');
        if (!navLinks) return;

        if (navLinks.style.display === 'flex') {
            navLinks.style.display = '';
        } else {
            Object.assign(navLinks.style, {
                display: 'flex',
                flexDirection: 'column',
                position: 'absolute',
                top: '68px',
                left: '0',
                right: '0',
                background: 'rgba(15,23,42,0.98)',
                padding: '1rem 2rem',
                borderBottom: '1px solid rgba(255,255,255,0.08)',
                zIndex: '999'
            });
        }
    });
}

// ============================================================
// 11. MARQUEE PAUSE ON HOVER
// ============================================================
const track = document.querySelector('.marquee-track');
if (track) {
    track.addEventListener('mouseenter', () => track.style.animationPlayState = 'paused');
    track.addEventListener('mouseleave', () => track.style.animationPlayState = 'running');
}

// ============================================================
// 12. CONFETTI BURST (results page)
// ============================================================
(function confettiBurst() {
    const canvas = document.getElementById('confettiCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;

    const colors = ['#4f46e5','#7c3aed','#22c55e','#f97316','#0ea5e9','#a855f7','#ec4899','#fbbf24'];
    const pieces = [];
    const TOTAL  = 140;
    let running  = true;

    function rand(min, max) { return Math.random() * (max - min) + min; }

    for (let i = 0; i < TOTAL; i++) {
        pieces.push({
            x: rand(0, canvas.width),
            y: rand(-canvas.height, 0),
            w: rand(8, 18),
            h: rand(4, 10),
            color: colors[Math.floor(rand(0, colors.length))],
            rot: rand(0, Math.PI * 2),
            rotSpeed: rand(-0.08, 0.08),
            vx: rand(-2, 2),
            vy: rand(2, 6),
            opacity: rand(0.7, 1)
        });
    }

    function draw() {
        if (!running) return;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        let allOut = true;

        pieces.forEach(p => {
            p.x  += p.vx;
            p.y  += p.vy;
            p.vy += 0.05; // gravity
            p.rot += p.rotSpeed;

            if (p.y < canvas.height + 30) allOut = false;

            ctx.save();
            ctx.globalAlpha = p.opacity;
            ctx.translate(p.x, p.y);
            ctx.rotate(p.rot);
            ctx.fillStyle = p.color;
            ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
            ctx.restore();

            // fade out as it falls
            if (p.y > canvas.height * 0.7) {
                p.opacity = Math.max(0, p.opacity - 0.008);
            }
        });

        if (allOut) {
            running = false;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            return;
        }
        requestAnimationFrame(draw);
    }

    // Start with a short delay so the page loads first
    setTimeout(draw, 600);

    window.addEventListener('resize', () => {
        canvas.width  = window.innerWidth;
        canvas.height = window.innerHeight;
    });
})();

// ============================================================
// 13. 3D TILT EFFECT on cards
// ============================================================
(function tiltEffect() {
    function addTilt(selector, intensity) {
        document.querySelectorAll(selector).forEach(card => {
            card.addEventListener('mousemove', e => {
                const rect   = card.getBoundingClientRect();
                const cx     = rect.left + rect.width  / 2;
                const cy     = rect.top  + rect.height / 2;
                const dx     = (e.clientX - cx) / (rect.width  / 2);
                const dy     = (e.clientY - cy) / (rect.height / 2);
                const rotX   = (-dy * intensity).toFixed(2);
                const rotY   = ( dx * intensity).toFixed(2);
                card.style.transform = `perspective(800px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateY(-6px)`;
                card.style.transition = 'none';
            });

            card.addEventListener('mouseleave', () => {
                card.style.transition = 'transform 0.4s ease';
                card.style.transform  = '';
            });
        });
    }

    addTilt('.step-card',    8);
    addTilt('.showcase-card', 6);
    addTilt('.result-card',  5);
    addTilt('.about-card',   7);
    addTilt('.formula-box',  10);
})();

// ============================================================
// 14. RIPPLE EFFECT on buttons
// ============================================================
document.querySelectorAll('.ripple-btn, .btn-primary, .btn-next-step, .btn-submit-final').forEach(btn => {
    btn.addEventListener('click', function (e) {
        const rect   = this.getBoundingClientRect();
        const size   = Math.max(rect.width, rect.height) * 2;
        const x      = e.clientX - rect.left  - size / 2;
        const y      = e.clientY - rect.top   - size / 2;
        const wave   = document.createElement('span');
        wave.className = 'ripple-wave';
        wave.style.cssText = `width:${size}px;height:${size}px;left:${x}px;top:${y}px`;
        this.style.position = 'relative';
        this.style.overflow = 'hidden';
        this.appendChild(wave);
        setTimeout(() => wave.remove(), 700);
    });
});

// ============================================================
// 15. MOUSE PARALLAX — aurora blobs follow cursor gently
// ============================================================
(function parallaxBlobs() {
    const blobs = document.querySelectorAll('.hero-blob');
    if (!blobs.length) return;

    document.addEventListener('mousemove', e => {
        const mx = (e.clientX / window.innerWidth  - 0.5) * 2; // -1 to 1
        const my = (e.clientY / window.innerHeight - 0.5) * 2;

        blobs.forEach((blob, i) => {
            const factor = (i + 1) * 12;
            blob.style.transform = `translate(${mx * factor}px, ${my * factor}px)`;
        });
    });
})();

// ============================================================
// 16. NAVBAR LINK HOVER — underline slide animation
// ============================================================
document.querySelectorAll('.nav-links a').forEach(link => {
    link.style.position = 'relative';
    const underline = document.createElement('span');
    underline.style.cssText = `
        position:absolute; bottom:2px; left:10px; right:10px;
        height:2px; background:linear-gradient(90deg,#818cf8,#c084fc);
        border-radius:2px; transform:scaleX(0); transform-origin:left;
        transition:transform 0.25s ease;
    `;
    link.appendChild(underline);
    link.addEventListener('mouseenter', () => underline.style.transform = 'scaleX(1)');
    link.addEventListener('mouseleave', () => underline.style.transform = 'scaleX(0)');
});

// ============================================================
// 17. CARD ENTRANCE — staggered pop-in on scroll
// ============================================================
(function staggerCards() {
    const cards = document.querySelectorAll('.showcase-card, .about-card, .tech-item');
    cards.forEach((card, i) => {
        card.style.transitionDelay = `${i * 0.08}s`;
    });
})();

// ============================================================
// 18. SMOOTH NUMBER TICKER on results skill scores
// ============================================================
(function tickScores() {
    const scoreNums = document.querySelectorAll('.skill-score');
    scoreNums.forEach(el => {
        const text = el.textContent;   // e.g. "8/10"
        const val  = parseInt(text);
        if (isNaN(val)) return;
        el.textContent = '0/10';

        const obs = new IntersectionObserver(entries => {
            if (!entries[0].isIntersecting) return;
            let cur = 0;
            const iv = setInterval(() => {
                cur++;
                el.textContent = `${cur}/10`;
                if (cur >= val) clearInterval(iv);
            }, 60);
            obs.unobserve(el);
        }, { threshold: 0.5 });

        obs.observe(el);
    });
})();

// ============================================================
// 19. CLICK-TO-PLAY YOUTUBE VIDEOS
// ============================================================
(function videoClickPlay() {
    document.querySelectorAll('.video-card').forEach(card => {
        const thumbWrap = card.querySelector('.video-thumb-wrap');
        const overlay   = card.querySelector('.video-play-overlay');
        const iframe    = card.querySelector('.video-iframe');
        const thumb     = card.querySelector('.video-thumb');
        if (!iframe || !overlay) return;

        function activate() {
            // Load the iframe src
            if (!iframe.src && iframe.dataset.src) {
                iframe.src = iframe.dataset.src;
            }
            // Show iframe, hide thumbnail + overlay
            iframe.style.display = 'block';
            if (thumb) thumb.style.display = 'none';
            overlay.style.display = 'none';
        }

        // Click on thumbnail or play button activates the video
        thumbWrap.addEventListener('click', activate);
    });
})();

// ============================================================
// 20. COMPARISON CHART + SALARY SECTION BAR ANIMATIONS
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
    // Comparison chart bars
    const cmpFills = document.querySelectorAll('.cmp-bar-fill');
    cmpFills.forEach((el, i) => {
        const target = el.dataset.width || '0%';
        el.style.width = '0%';
        const obs = new IntersectionObserver(entries => {
            if (!entries[0].isIntersecting) return;
            setTimeout(() => { el.style.width = target; }, i * 120);
            obs.unobserve(el);
        }, { threshold: 0.3 });
        obs.observe(el);
    });

    // Roadmap steps — stagger animate in
    document.querySelectorAll('.roadmap-step').forEach((el, i) => {
        el.style.opacity = '0';
        el.style.transform = 'translateX(-20px)';
        const obs = new IntersectionObserver(entries => {
            if (!entries[0].isIntersecting) return;
            setTimeout(() => {
                el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                el.style.opacity = '1';
                el.style.transform = 'translateX(0)';
            }, i * 150);
            obs.unobserve(el);
        }, { threshold: 0.2 });
        obs.observe(el);
    });

    // Quote card — fade + scale in
    const quote = document.querySelector('.quote-card');
    if (quote) {
        quote.style.opacity = '0';
        quote.style.transform = 'scale(0.96)';
        const obs = new IntersectionObserver(entries => {
            if (!entries[0].isIntersecting) return;
            quote.style.transition = 'opacity 0.7s ease, transform 0.7s ease';
            quote.style.opacity = '1';
            quote.style.transform = 'scale(1)';
            obs.unobserve(quote);
        }, { threshold: 0.3 });
        obs.observe(quote);
    }
});

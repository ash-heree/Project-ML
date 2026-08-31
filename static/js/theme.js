document.addEventListener('DOMContentLoaded', () => {
    // ==========================================
    // 1. GLOBAL CURSOR AMBIENT LIGHT
    // ==========================================
    const globalLight = document.createElement('div');
    globalLight.id = 'global-cursor-light';
    document.body.appendChild(globalLight);

    let globalMouseX = window.innerWidth / 2;
    let globalMouseY = window.innerHeight / 2;
    let globalLightFrame;

    function updateGlobalLight() {
        globalLight.style.transform = `translate(${globalMouseX}px, ${globalMouseY}px)`;
    }

    document.addEventListener('mousemove', (e) => {
        globalMouseX = e.clientX;
        globalMouseY = e.clientY;
        if (globalLightFrame) cancelAnimationFrame(globalLightFrame);
        globalLightFrame = requestAnimationFrame(updateGlobalLight);
    });

    // ==========================================
    // 2. PREMIUM CARD EFFECTS (Hover Glow & Tracking)
    // ==========================================
    const targetCards = document.querySelectorAll('.glass-card, .card, .feature-card, .info-card, .chart-card, .recent-transactions, .details-card, .meter-card');

    targetCards.forEach((card, index) => {
        // Cascaded organic animation delays
        const entranceDelay = 0.2 + (index * 0.1);
        const floatDelay = index * 0.4;
        card.style.animationDelay = `${entranceDelay}s, ${floatDelay}s`;

        // Inject inner cursor glow
        if (!card.querySelector('.cursor-glow')) {
            const glow = document.createElement('div');
            glow.classList.add('cursor-glow');
            card.appendChild(glow);
        }

        // Inject inner complex background
        if (!card.querySelector('.card-bg-gradient')) {
            const bg = document.createElement('div');
            bg.classList.add('card-bg-gradient');
            
            // Look for specific background artwork theme
            const bgTheme = card.getAttribute('data-bg-theme');
            if (bgTheme) {
                bg.classList.add(bgTheme);
            }
            
            card.appendChild(bg);
        }

        // Hardware acceleration
        card.style.transformStyle = 'preserve-3d';
        card.style.backfaceVisibility = 'hidden';

        const glowElement = card.querySelector('.cursor-glow');
        let bounds;
        let isHovering = false;
        let animationFrameId;

        function updateCardState(e) {
            if (!isHovering) return;
            const leftX = e.clientX - bounds.left;
            const topY = e.clientY - bounds.top;
            
            if (glowElement) {
                glowElement.style.transform = `translate(${leftX}px, ${topY}px)`;
                glowElement.style.opacity = '1';
            }
        }

        card.addEventListener('mouseenter', () => {
            isHovering = true;
            bounds = card.getBoundingClientRect();
            card.classList.add('is-hovered');
            
            if (glowElement) {
                glowElement.style.transition = 'opacity 0.3s ease';
                glowElement.style.opacity = '1';
            }
        });

        card.addEventListener('mousemove', (e) => {
            if (animationFrameId) cancelAnimationFrame(animationFrameId);
            animationFrameId = requestAnimationFrame(() => updateCardState(e));
        });

        card.addEventListener('mouseleave', () => {
            isHovering = false;
            if (animationFrameId) cancelAnimationFrame(animationFrameId);
            card.classList.remove('is-hovered');
            if (glowElement) {
                glowElement.style.opacity = '0';
            }
        });
    });

    // ==========================================
    // 3. TABLE ROW STAGGER ENTRANCE
    // ==========================================
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach((row, index) => {
        row.style.animationDelay = `${0.6 + (index * 0.05)}s`;
        row.classList.add('table-row-entrance');
    });

    // ==========================================
    // 4. BUTTON RIPPLE EFFECT
    // ==========================================
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach((btn, index) => {
        // Entrance stagger for buttons
        btn.style.animationDelay = `${0.5 + (index * 0.1)}s`;
        btn.classList.add('btn-entrance');

        btn.addEventListener('click', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const ripple = document.createElement('span');
            ripple.classList.add('ripple-effect');
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;

            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });

});

import React, { useEffect, useRef } from 'react';

const TELUGU_GLYPHS = ['అ', 'ఆ', 'క', 'మ', 'త', 'న', 'ర', 'ల', 'వ', 'శ', 'హ', 'ఙ', 'ఞ', 'కృ', 'క్ష', 'జ్ఞ'];

export default function ParticlesBackground({ theme }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let animationFrameId;

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    // Track user accessibility preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', handleResize);

    const particles = [];
    const glyphs = [];
    const beams = [];

    const isDark = theme === 'dark';
    const densityRatio = prefersReducedMotion ? 0.2 : 1.0;

    // Initialize regular particles
    const particleCount = Math.min(50, Math.floor((width * height) / 30000)) * densityRatio;
    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: prefersReducedMotion ? 0 : (Math.random() - 0.5) * 0.3,
        vy: prefersReducedMotion ? 0 : (Math.random() - 0.5) * 0.3,
        radius: Math.random() * 2 + 0.5,
        alpha: Math.random() * 0.3 + 0.1,
      });
    }

    // Initialize floating Telugu glyphs (2-3% opacity)
    const glyphCount = Math.min(12, Math.floor((width * height) / 100000)) * densityRatio;
    for (let i = 0; i < glyphCount; i++) {
      glyphs.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: prefersReducedMotion ? 0 : (Math.random() - 0.5) * 0.15,
        vy: prefersReducedMotion ? 0 : (Math.random() - 0.5) * 0.15,
        char: TELUGU_GLYPHS[Math.floor(Math.random() * TELUGU_GLYPHS.length)],
        size: Math.floor(Math.random() * 32) + 24,
        angle: Math.random() * Math.PI * 2,
        angularVelocity: prefersReducedMotion ? 0 : (Math.random() - 0.5) * 0.002,
        alpha: Math.random() * 0.015 + 0.015, // 1.5% - 3.0% opacity
      });
    }

    // Initialize light beams
    const beamCount = prefersReducedMotion ? 1 : 3;
    for (let i = 0; i < beamCount; i++) {
      beams.push({
        x: Math.random() * width,
        width: Math.random() * 150 + 100,
        opacity: Math.random() * 0.05 + 0.02,
        speed: prefersReducedMotion ? 0 : (Math.random() * 0.2 + 0.1) * (Math.random() > 0.5 ? 1 : -1),
      });
    }

    let mouseX = null;
    let mouseY = null;

    const handleMouseMove = (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    };
    const handleMouseLeave = () => {
      mouseX = null;
      mouseY = null;
    };
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseleave', handleMouseLeave);

    // Game loop
    const animate = () => {
      // Background base clear
      ctx.clearRect(0, 0, width, height);

      // Draw light beams
      beams.forEach((b) => {
        if (!prefersReducedMotion) {
          b.x += b.speed;
          if (b.x < -b.width) b.x = width + b.width;
          if (b.x > width + b.width) b.x = -b.width;
        }

        const gradient = ctx.createLinearGradient(b.x, 0, b.x + b.width, 0);
        const col = isDark ? '99, 102, 241' : '59, 130, 246';
        gradient.addColorStop(0, `rgba(${col}, 0)`);
        gradient.addColorStop(0.5, `rgba(${col}, ${b.opacity})`);
        gradient.addColorStop(1, `rgba(${col}, 0)`);

        ctx.fillStyle = gradient;
        ctx.fillRect(b.x, 0, b.width, height);
      });

      // Draw and update glyphs (subtle Telugu characters)
      ctx.font = 'normal 700 1px Inter, sans-serif';
      glyphs.forEach((g) => {
        if (!prefersReducedMotion) {
          g.x += g.vx;
          g.y += g.vy;
          g.angle += g.angularVelocity;

          if (g.x < -50) g.x = width + 50;
          if (g.x > width + 50) g.x = -50;
          if (g.y < -50) g.y = height + 50;
          if (g.y > height + 50) g.y = -50;
        }

        ctx.save();
        ctx.translate(g.x, g.y);
        ctx.rotate(g.angle);
        ctx.font = `${g.size}px 'Inter', sans-serif`;
        ctx.fillStyle = isDark ? `rgba(255, 255, 255, ${g.alpha})` : `rgba(15, 23, 42, ${g.alpha})`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(g.char, 0, 0);
        ctx.restore();
      });

      // Draw and update regular particles
      particles.forEach((p) => {
        if (!prefersReducedMotion) {
          p.x += p.vx;
          p.y += p.vy;

          if (p.x < 0 || p.x > width) p.vx = -p.vx;
          if (p.y < 0 || p.y > height) p.vy = -p.vy;
        }

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = isDark ? `rgba(255, 255, 255, ${p.alpha})` : `rgba(15, 23, 42, ${p.alpha})`;
        ctx.fill();
      });

      // Draw constellation connections
      const maxDistance = 120;
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < maxDistance) {
            const alpha = (1 - dist / maxDistance) * 0.08;
            ctx.strokeStyle = isDark ? `rgba(99, 102, 241, ${alpha})` : `rgba(59, 130, 246, ${alpha})`;
            ctx.lineWidth = 0.5;
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.stroke();
          }
        }

        // Connect to mouse interaction
        if (mouseX !== null && mouseY !== null && !prefersReducedMotion) {
          const dx = particles[i].x - mouseX;
          const dy = particles[i].y - mouseY;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 150) {
            const alpha = (1 - dist / 150) * 0.15;
            ctx.strokeStyle = isDark ? `rgba(147, 51, 234, ${alpha})` : `rgba(99, 102, 241, ${alpha})`;
            ctx.lineWidth = 0.8;
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(mouseX, mouseY);
            ctx.stroke();
          }
        }
      }

      animationFrameId = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseleave', handleMouseLeave);
      cancelAnimationFrame(animationFrameId);
    };
  }, [theme]);

  return (
    <div className="fixed inset-0 pointer-events-none -z-20 w-full h-full">
      {/* Animated Aurora Blobs */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-[600px] overflow-hidden pointer-events-none select-none">
        <div className="absolute -top-24 left-[10%] w-96 h-96 rounded-full bg-blue-500/20 dark:bg-blue-600/10 blur-[130px] animate-blob-1" />
        <div className="absolute -top-12 right-[10%] w-[450px] h-[450px] rounded-full bg-cyan-400/15 dark:bg-indigo-600/10 blur-[140px] animate-blob-2" />
        <div className="absolute top-[200px] left-[30%] w-[500px] h-[500px] rounded-full bg-sky-400/20 dark:bg-purple-600/10 blur-[150px] animate-blob-3" />
      </div>
      <canvas ref={canvasRef} className="w-full h-full" />
    </div>
  );
}

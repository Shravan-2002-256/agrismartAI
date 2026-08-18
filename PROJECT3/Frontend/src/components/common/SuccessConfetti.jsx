// Success Confetti Animation
// Lightweight custom confetti effect for successful actions
// Triggers on disease detection completion

import React, { useEffect, useState } from 'react';

const SuccessConfetti = ({ active, duration = 3000, onComplete }) => {
  const [particles, setParticles] = useState([]);
  
  useEffect(() => {
    if (!active) return;
    
    // Generate confetti particles with varied properties for natural look
    const colors = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];
    const newParticles = Array.from({ length: 50 }, (_, i) => ({
      id: i,
      x: Math.random() * 100,
      y: -10,
      color: colors[Math.floor(Math.random() * colors.length)],
      size: Math.random() * 8 + 4,
      rotation: Math.random() * 360,
      speedX: (Math.random() - 0.5) * 2,
      speedY: Math.random() * 2 + 1,
      delay: Math.random() * 200,
    }));
    
    setParticles(newParticles);
    
    // Auto cleanup
    const timer = setTimeout(() => {
      setParticles([]);
      if (onComplete) onComplete();
    }, duration);
    
    return () => clearTimeout(timer);
  }, [active, duration, onComplete]);
  
  if (particles.length === 0) return null;
  
  return (
    <div className="fixed inset-0 pointer-events-none z-50 overflow-hidden">
      {particles.map((particle) => (
        <div
          key={particle.id}
          className="absolute animate-confetti"
          style={{
            left: `${particle.x}%`,
            top: `${particle.y}%`,
            width: `${particle.size}px`,
            height: `${particle.size}px`,
            backgroundColor: particle.color,
            transform: `rotate(${particle.rotation}deg)`,
            animationDelay: `${particle.delay}ms`,
            animationDuration: `${duration}ms`,
            '--speed-x': particle.speedX,
            '--speed-y': particle.speedY,
          }}
        />
      ))}
    </div>
  );
};

export default SuccessConfetti;

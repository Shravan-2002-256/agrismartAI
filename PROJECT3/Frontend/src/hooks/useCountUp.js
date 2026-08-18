// Counter Hook - Custom implementation for animated counting
// Created for AgriSmart AI Dashboard
// Provides smooth number animations when stats load

import { useEffect, useState } from 'react';

export const useCountUp = (end, duration = 1500, startOnMount = true) => {
  const [count, setCount] = useState(0);
  const [started, setStarted] = useState(false);

  useEffect(() => {
    if (!startOnMount || started) return;
    
    setStarted(true);
    let startTime = null;
    const startValue = 0;
    
    const animate = (currentTime) => {
      if (!startTime) startTime = currentTime;
      const progress = Math.min((currentTime - startTime) / duration, 1);
      
      // Easing function for smooth deceleration
      const easeOutQuart = 1 - Math.pow(1 - progress, 4);
      const currentCount = Math.floor(easeOutQuart * (end - startValue) + startValue);
      
      setCount(currentCount);
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        setCount(end); // Ensure we hit the exact number
      }
    };
    
    requestAnimationFrame(animate);
  }, [end, duration, startOnMount, started]);

  return count;
};

export default useCountUp;

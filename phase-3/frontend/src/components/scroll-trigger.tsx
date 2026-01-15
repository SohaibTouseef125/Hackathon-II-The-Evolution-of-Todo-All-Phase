'use client';

import { useEffect, useRef, useState } from 'react';
import { motion, useAnimation } from 'framer-motion';

interface ScrollTriggerProps {
  children: React.ReactNode;
  offset?: number;
  once?: boolean;
  triggerOnce?: boolean;
  threshold?: number;
  variants?: {
    hidden: any;
    visible: any;
  };
  className?: string;
}

export default function ScrollTrigger({
  children,
  offset = 100,
  once = false,
  triggerOnce = false,
  threshold = 0.1,
  variants,
  className
}: ScrollTriggerProps) {
  const controls = useAnimation();
  const elementRef = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const element = elementRef.current;
    if (!element) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          controls.start('visible');
          setIsVisible(true);

          if (once || triggerOnce) {
            observer.unobserve(element);
          }
        } else if (!once && !triggerOnce) {
          controls.start('hidden');
        }
      },
      {
        root: null,
        rootMargin: `-${offset}px`,
        threshold,
      }
    );

    observer.observe(element);

    return () => {
      observer.disconnect();
    };
  }, [controls, offset, once, triggerOnce, threshold]);

  const defaultVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: 'easeOut' } },
  };

  const mergedVariants = variants ? { ...defaultVariants, ...variants } : defaultVariants;

  return (
    <motion.div
      ref={elementRef}
      className={className}
      initial="hidden"
      animate={controls}
      variants={mergedVariants}
    >
      {children}
    </motion.div>
  );
}
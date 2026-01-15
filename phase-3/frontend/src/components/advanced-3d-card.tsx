'use client';

import { useState, useRef } from 'react';
import { motion, useMotionValue, useSpring, useTransform } from 'framer-motion';

interface Advanced3DCardProps {
  children: React.ReactNode;
  className?: string;
  perspective?: number;
  rotateIntensity?: number;
  scaleOnHover?: boolean;
  tiltEffect?: boolean;
}

export default function Advanced3DCard({
  children,
  className = '',
  perspective = 1000,
  rotateIntensity = 15,
  scaleOnHover = true,
  tiltEffect = true
}: Advanced3DCardProps) {
  const ref = useRef<HTMLDivElement>(null);

  const x = useMotionValue(0);
  const y = useMotionValue(0);

  const xSpring = useSpring(x);
  const ySpring = useSpring(y);

  const rotateX = useTransform(ySpring, [-100, 100], [rotateIntensity, -rotateIntensity]);
  const rotateY = useTransform(xSpring, [-100, 100], [-rotateIntensity, rotateIntensity]);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!ref.current) return;

    const rect = ref.current.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;

    const mouseX = e.clientX - centerX;
    const mouseY = e.clientY - centerY;

    x.set(mouseX);
    y.set(mouseY);
  };

  const handleMouseLeave = () => {
    x.set(0);
    y.set(0);
  };

  const springConfig = { stiffness: 300, damping: 30 };

  return (
    <motion.div
      ref={ref}
      className={`relative cursor-pointer ${className}`}
      onMouseMove={tiltEffect ? handleMouseMove : undefined}
      onMouseLeave={tiltEffect ? handleMouseLeave : undefined}
      style={{
        perspective: `${perspective}px`,
      }}
    >
      <motion.div
        style={
          tiltEffect
            ? {
                rotateX,
                rotateY,
                transformStyle: "preserve-3d",
              }
            : {}
        }
        animate={
          scaleOnHover
            ? {
                scale: [1, 1.03],
              }
            : {}
        }
        whileHover={scaleOnHover ? { scale: 1.03 } : {}}
        transition={springConfig}
        className="bg-white dark:bg-neutral-800 rounded-2xl shadow-xl border border-neutral-200 dark:border-neutral-700 overflow-hidden"
      >
        <div className="relative">{children}</div>

        {/* Reflective surface effect */}
        <motion.div
          className="absolute inset-0 pointer-events-none rounded-2xl overflow-hidden"
          style={{
            background: "radial-gradient(circle at 100px 100px, rgba(255,255,255,0.2) 0%, transparent 70%)",
          }}
          initial={{ opacity: 0 }}
          whileHover={{ opacity: 0.6 }}
          transition={{ duration: 0.3 }}
        />

        {/* Glow effect on hover */}
        <motion.div
          className="absolute -inset-2 rounded-2xl bg-gradient-to-r from-primary-500/20 to-secondary-500/20 blur-xl opacity-0 -z-10"
          animate={{
            opacity: [0, 0.3, 0],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            repeatType: "reverse",
          }}
        />
      </motion.div>
    </motion.div>
  );
}
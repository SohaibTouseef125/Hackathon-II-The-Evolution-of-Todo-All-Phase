import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

function Skeleton({
  className,
  ...props
}: React.ComponentProps<typeof motion.div>) {
  return (
    <motion.div
      className={cn(
        'animate-pulse rounded-md bg-neutral-300 dark:bg-neutral-700',
        className
      )}
      animate={{ opacity: [0.5, 1, 0.5] }}
      transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut' }}
      {...props}
    />
  );
}

export { Skeleton };
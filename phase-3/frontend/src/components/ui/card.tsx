import * as React from 'react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

const Card = React.forwardRef<
  HTMLDivElement,
  React.ComponentProps<typeof motion.div>
>(({ className, ...props }, ref) => (
  <motion.div
    ref={ref}
    className={cn(
      'rounded-2xl border bg-card text-card-foreground shadow-lg',
      'bg-white dark:bg-neutral-800/50',
      'border-neutral-200 dark:border-neutral-700',
      'transition-all duration-300 hover:shadow-xl hover:-translate-y-1',
      'motion-reduce:hover:shadow-lg motion-reduce:hover:-translate-y-0',
      className
    )}
    whileHover={{ y: -5 }}
    transition={{ type: 'spring', stiffness: 300, damping: 30 }}
    {...props}
  />
));
Card.displayName = 'Card';

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('flex flex-col space-y-1.5 p-6', className)}
    {...props}
  />
));
CardHeader.displayName = 'CardHeader';

const CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      'text-2xl font-semibold leading-none tracking-tight',
      'text-neutral-900 dark:text-white',
      className
    )}
    {...props}
  />
));
CardTitle.displayName = 'CardTitle';

const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn(
      'text-sm text-muted-foreground',
      'text-neutral-600 dark:text-neutral-300',
      className
    )}
    {...props}
  />
));
CardDescription.displayName = 'CardDescription';

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('p-6 pt-0', className)} {...props} />
));
CardContent.displayName = 'CardContent';

const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('flex items-center p-6 pt-0', className)}
    {...props}
  />
));
CardFooter.displayName = 'CardFooter';

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent };
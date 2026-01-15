import { cva, type VariantProps } from 'class-variance-authority';
import { X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';

const toastVariants = cva(
  'flex items-center justify-between p-4 rounded-xl shadow-lg border',
  {
    variants: {
      variant: {
        default: 'bg-white dark:bg-neutral-800 border-neutral-200 dark:border-neutral-700 text-neutral-900 dark:text-white',
        success: 'bg-green-50 dark:bg-green-950/30 border-green-200 dark:border-green-800 text-green-800 dark:text-green-200',
        error: 'bg-red-50 dark:bg-red-950/30 border-red-200 dark:border-red-800 text-red-800 dark:text-red-200',
        warning: 'bg-yellow-50 dark:bg-yellow-950/30 border-yellow-200 dark:border-yellow-800 text-yellow-800 dark:text-yellow-200',
        info: 'bg-blue-50 dark:bg-blue-950/30 border-blue-200 dark:border-blue-800 text-blue-800 dark:text-blue-200',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

interface ToastProps {
  id: string;
  title: string;
  description?: string;
  variant?: VariantProps<typeof toastVariants>['variant'];
  onDismiss?: (id: string) => void;
  duration?: number;
}

export function Toast({ id, title, description, variant = 'default', onDismiss, duration = 4000 }: ToastProps) {
  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, x: 300, scale: 0.8 }}
        animate={{ opacity: 1, x: 0, scale: 1 }}
        exit={{ opacity: 0, x: 300, scale: 0.8 }}
        transition={{ type: 'spring', damping: 25, stiffness: 200 }}
        className={cn(toastVariants({ variant }))}
      >
        <div className="flex-1">
          <h4 className="font-medium">{title}</h4>
          {description && <p className="text-sm mt-1 opacity-80">{description}</p>}
        </div>
        <button
          onClick={() => onDismiss?.(id)}
          className="ml-4 p-1 rounded-full hover:bg-neutral-200 dark:hover:bg-neutral-700 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </motion.div>
    </AnimatePresence>
  );
}

interface ToastProviderProps {
  children: React.ReactNode;
}

export function ToastProvider({ children }: ToastProviderProps) {
  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {children}
    </div>
  );
}
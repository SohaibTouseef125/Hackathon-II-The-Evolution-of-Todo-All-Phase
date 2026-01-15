'use client';

import React from 'react';
import { Toaster, toast } from 'sonner';

// Toast context and provider component
export interface Toast {
  id: string;
  title: string;
  description?: string;
  type: 'success' | 'error' | 'info' | 'warning';
}

export interface ToastContextProps {
  showToast: (toastData: Omit<Toast, 'id'>) => void;
  dismissToast: (id: string) => void;
}

const ToastContext = React.createContext<ToastContextProps>({
  showToast: () => {},
  dismissToast: () => {},
});

export const useToast = () => React.useContext(ToastContext);

export interface ToastProviderProps {
  children: React.ReactNode;
}

export default function ToastProvider({ children }: ToastProviderProps) {
  const showToast = ({ title, description, type }: Omit<Toast, 'id'>) => {
    switch (type) {
      case 'success':
        toast.success(title, { description });
        break;
      case 'error':
        toast.error(title, { description });
        break;
      case 'warning':
        toast.warning(title, { description });
        break;
      case 'info':
      default:
        toast.info(title, { description });
        break;
    }
  };

  const dismissToast = (id: string) => {
    // In sonner, toasts are dismissed automatically or by user interaction
    // We don't need to manually dismiss by ID in this implementation
  };

  return (
    <ToastContext.Provider value={{ showToast, dismissToast }}>
      {children}
      <Toaster
        position="top-right"
        toastOptions={{
          className: 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg',
          style: {
            background: '#fff',
            color: '#000',
          },
        }}
      />
    </ToastContext.Provider>
  );
}
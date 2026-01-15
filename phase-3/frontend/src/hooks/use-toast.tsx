import { toast } from 'sonner';

interface ToastOptions {
  description?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
  cancel?: {
    label: string;
    onClick: () => void;
  };
  duration?: number;
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
}

export interface ToastHook {
  toast: (options: {
    title: string;
    description?: string;
    variant?: 'default' | 'destructive' | 'success' | 'warning' | 'info' | 'error';
  }) => void;
  success: (title: string, options?: ToastOptions) => void;
  error: (title: string, options?: ToastOptions) => void;
  info: (title: string, options?: ToastOptions) => void;
  warning: (title: string, options?: ToastOptions) => void;
  dismiss: (id?: string) => void;
  loading: (title: string, options?: ToastOptions) => string | number;
}

/**
 * Hook to display toast notifications.
 * 
 * @returns A hook with functions to display toast notifications.
 * The hook returns an object with the following functions:
 * - `toast`: Displays a toast notification with a title and optional description.
 * - `success`: Displays a success toast notification with a title and optional description.
 * - `error`: Displays an error toast notification with a title and optional description.
 * - `info`: Displays an info toast notification with a title and optional description.
 * - `warning`: Displays a warning toast notification with a title and optional description.
 * - `dismiss`: Dismisses a toast notification by its ID.
 * - `loading`: Displays a loading toast notification with a title and optional description.
 */
export function useToast(): ToastHook {
  const showToast = ({
    title,
    description,
    variant = 'default',
  }: {
    title: string;
    description?: string;
    variant?: 'default' | 'destructive' | 'success' | 'warning' | 'info' | 'error';
  }): void => {
    const toastContent = description ? (
      <div>
        <div className="font-medium">{title}</div>
        <div className="text-sm opacity-80">{description}</div>
      </div>
    ) : (
      title 
    );
    switch (variant) {
      case 'success':
        toast.success(toastContent);
        break;
      case 'error':
        toast.error(toastContent);
        break;
      case 'warning':
        toast.warning(toastContent);
        break;
      case 'info':
        toast.info(toastContent);
        break;
      case 'default':
      default:
        toast(toastContent);
        break;
    }
  };

  const toastHook: ToastHook = {
    toast: showToast,
    success: (title: string, options?: ToastOptions) => {
      toast.success(title, options);
    },
    error: (title: string, options?: ToastOptions) => {
      toast.error(title, options);
    },
    info: (title: string, options?: ToastOptions) => {
      toast.info(title, options);
    },
    warning: (title: string, options?: ToastOptions) => {
      toast.warning(title, options);
    },
    dismiss: (id?: string) => {
      if (id) {
        toast.dismiss(id);
      } else {
        toast.dismiss();
      }
    },
    loading: (title: string, options?: ToastOptions) => {
      return toast.loading(title, options);
    },
  };

  return toastHook;
}

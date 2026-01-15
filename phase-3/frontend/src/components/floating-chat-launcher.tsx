'use client';

import { useState, useEffect } from 'react';
import { MessageCircle, X } from 'lucide-react';
import { useAuth } from '@/hooks/use-auth';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

const FLOATING_LAUNCHER_KEY = 'floating_launcher_hidden';

export default function FloatingChatLauncher() {
  const { user, isAuthenticated } = useAuth();
  const router = useRouter();
  const [isVisible, setIsVisible] = useState(false);
  const [isHidden, setIsHidden] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const hidden = localStorage.getItem(FLOATING_LAUNCHER_KEY) === 'true';
      setIsHidden(hidden);
    }
  }, []);

  useEffect(() => {
    if (isAuthenticated && user) {
      setIsVisible(true);
    } else {
      setIsVisible(false);
    }
  }, [isAuthenticated, user]);

  if (!isVisible || isHidden) {
    return null;
  }

  const handleClose = () => {
    setIsHidden(true);
    localStorage.setItem(FLOATING_LAUNCHER_KEY, 'true');
  };

  const handleOpenChat = () => {
    router.push('/chat');
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <div className="relative">
        <button
          type="button"
          onClick={handleOpenChat}
          className="flex items-center justify-center w-14 h-14 rounded-full bg-blue-600 text-white shadow-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200"
          aria-label="Open chat"
        >
          <MessageCircle className="h-6 w-6" aria-hidden="true" />
          <span className="sr-only">Open chat</span>
        </button>

        <button
          type="button"
          onClick={handleClose}
          className="absolute -top-2 -right-2 flex items-center justify-center w-6 h-6 rounded-full bg-red-500 text-white text-xs hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
          aria-label="Hide chat launcher"
        >
          <X className="h-3 w-3" aria-hidden="true" />
          <span className="sr-only">Hide chat launcher</span>
        </button>
      </div>
    </div>
  );
}
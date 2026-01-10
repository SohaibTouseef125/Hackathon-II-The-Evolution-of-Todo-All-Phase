'use client';

import { ReactNode, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';

interface AuthLayoutProps {
  children: ReactNode;
  requireAuth?: boolean; // If true, redirects to login if not authenticated
  redirectIfAuth?: boolean; // If true, redirects to dashboard if authenticated
}

export default function AuthLayout({
  children,
  requireAuth = false,
  redirectIfAuth = false
}: AuthLayoutProps) {
  const router = useRouter();
  const { user, loading } = useAuth();

  useEffect(() => {
    if (!loading) {
      if (requireAuth && !user) {
        router.push('/login');
      } else if (redirectIfAuth && user) {
        router.push('/dashboard');
      }
    }
  }, [user, loading, requireAuth, redirectIfAuth, router]);

  // Show loading state while checking authentication
  if (loading && requireAuth) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // If redirecting, don't render children
  if ((requireAuth && !user) || (redirectIfAuth && user)) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <main className="py-12">
        <div className="max-w-md mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white shadow rounded-lg p-6 sm:p-8">
            {children}
          </div>
        </div>
      </main>
    </div>
  );
}
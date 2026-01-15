import './globals.css';
import type { Metadata } from 'next';
import { AuthProvider } from '@/hooks/use-auth';
import ToastProvider from '@/components/toast-provider';
import FloatingChatLauncher from '@/components/floating-chat-launcher';

export const metadata: Metadata = {
  title: 'Todo Web Application',
  description: 'A multi-user todo application with authentication',
  icons: {
    icon: '/favicon.svg',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="hydrated" data-scroll-behavior="smooth">
      <body>
        <AuthProvider>
          <ToastProvider>
            <main>{children}</main>
            <FloatingChatLauncher />
          </ToastProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
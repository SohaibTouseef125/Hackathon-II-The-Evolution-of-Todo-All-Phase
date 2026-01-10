import './globals.css';
import type { Metadata } from 'next';
import { AuthProvider } from '@/hooks/use-auth';

export const metadata: Metadata = {
  title: 'Todo Web Application',
  description: 'A multi-user todo application with authentication',
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
          <main>{children}</main>
        </AuthProvider>
      </body>
    </html>
  );
}
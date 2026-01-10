import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { AuthProvider, useAuth } from '@/hooks/use-auth';
import AuthLayout from '@/components/auth-layout';
import { useRouter } from 'next/navigation';

// Mock the router
vi.mock('next/navigation', () => ({
  useRouter: vi.fn(),
}));

// Mock the useAuth hook
vi.mock('@/hooks/use-auth', () => {
  const actual = vi.importActual('@/hooks/use-auth');
  return {
    ...actual,
    useAuth: vi.fn(),
  };
});

describe('AuthLayout', () => {
  const mockPush = vi.fn();
  const mockUser = { id: 'user1', email: 'test@example.com' };

  beforeEach(() => {
    vi.clearAllMocks();
    (useRouter as vi.Mock).mockReturnValue({ push: mockPush });
  });

  it('renders children when no auth requirements are specified', () => {
    (useAuth as vi.Mock).mockReturnValue({
      user: null,
      loading: false,
      isAuthenticated: false,
    });

    render(
      <AuthProvider>
        <AuthLayout>
          <div>Test Content</div>
        </AuthLayout>
      </AuthProvider>
    );

    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });

  it('redirects to login when requireAuth is true and user is not authenticated', () => {
    (useAuth as vi.Mock).mockReturnValue({
      user: null,
      loading: false,
      isAuthenticated: false,
    });

    render(
      <AuthProvider>
        <AuthLayout requireAuth={true}>
          <div>Protected Content</div>
        </AuthLayout>
      </AuthProvider>
    );

    expect(mockPush).toHaveBeenCalledWith('/login');
  });

  it('does not redirect when requireAuth is true and user is authenticated', () => {
    (useAuth as vi.Mock).mockReturnValue({
      user: mockUser,
      loading: false,
      isAuthenticated: true,
    });

    render(
      <AuthProvider>
        <AuthLayout requireAuth={true}>
          <div>Protected Content</div>
        </AuthLayout>
      </AuthProvider>
    );

    expect(screen.getByText('Protected Content')).toBeInTheDocument();
    expect(mockPush).not.toHaveBeenCalled();
  });

  it('redirects to dashboard when redirectIfAuth is true and user is authenticated', () => {
    (useAuth as vi.Mock).mockReturnValue({
      user: mockUser,
      loading: false,
      isAuthenticated: true,
    });

    render(
      <AuthProvider>
        <AuthLayout redirectIfAuth={true}>
          <div>Public Content</div>
        </AuthLayout>
      </AuthProvider>
    );

    expect(mockPush).toHaveBeenCalledWith('/dashboard');
  });

  it('does not redirect when redirectIfAuth is true and user is not authenticated', () => {
    (useAuth as vi.Mock).mockReturnValue({
      user: null,
      loading: false,
      isAuthenticated: false,
    });

    render(
      <AuthProvider>
        <AuthLayout redirectIfAuth={true}>
          <div>Public Content</div>
        </AuthLayout>
      </AuthProvider>
    );

    expect(screen.getByText('Public Content')).toBeInTheDocument();
    expect(mockPush).not.toHaveBeenCalled();
  });

  it('shows loading state when loading and requireAuth is true', () => {
    (useAuth as vi.Mock).mockReturnValue({
      user: null,
      loading: true,
      isAuthenticated: false,
    });

    render(
      <AuthProvider>
        <AuthLayout requireAuth={true}>
          <div>Protected Content</div>
        </AuthLayout>
      </AuthProvider>
    );

    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });
});
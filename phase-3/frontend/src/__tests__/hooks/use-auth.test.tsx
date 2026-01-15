import { renderHook, act, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { AuthProvider, useAuth } from '@/hooks/use-auth';
import { apiClient } from '@/lib/api';

// Mock the apiClient
vi.mock('@/lib/api', () => ({
  apiClient: {
    login: vi.fn(),
    register: vi.fn(),
    logout: vi.fn(),
  },
}));

// Mock localStorage
const mockLocalStorage = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
};

Object.defineProperty(window, 'localStorage', {
  value: mockLocalStorage,
});

describe('useAuth', () => {
  const mockUser = {
    id: 'user1',
    email: 'test@example.com',
    name: 'Test User',
    created_at: '2023-01-01T00:00:00Z',
    updated_at: '2023-01-01T00:00:00Z',
  };

  beforeEach(() => {
    vi.clearAllMocks();
    mockLocalStorage.getItem.mockClear();
    mockLocalStorage.setItem.mockClear();
    mockLocalStorage.removeItem.mockClear();
  });

  it('provides auth context with initial state', () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <AuthProvider>{children}</AuthProvider>
    );
    const { result } = renderHook(() => useAuth(), { wrapper });

    expect(result.current.user).toBeNull();
    expect(result.current.loading).toBe(true);
    expect(result.current.isAuthenticated).toBe(false);
  });

  it('handles login successfully', async () => {
    const mockLoginResponse = {
      access_token: 'mock-token',
      user: mockUser,
    };

    (apiClient.login as vi.Mock).mockResolvedValue(mockLoginResponse);
    mockLocalStorage.getItem.mockReturnValue(null);

    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <AuthProvider>{children}</AuthProvider>
    );
    const { result } = renderHook(() => useAuth(), { wrapper });

    // Wait for initial loading to complete
    await waitFor(() => expect(result.current.loading).toBe(false));

    await act(async () => {
      await result.current.login('test@example.com', 'password123');
    });

    expect(apiClient.login).toHaveBeenCalledWith('test@example.com', 'password123');
    expect(mockLocalStorage.setItem).toHaveBeenCalledWith('access_token', 'mock-token');
    expect(mockLocalStorage.setItem).toHaveBeenCalledWith('user', JSON.stringify(mockUser));
    expect(result.current.user).toEqual(mockUser);
    expect(result.current.isAuthenticated).toBe(true);
  });

  it('handles registration successfully', async () => {
    const mockRegisterResponse = {
      access_token: 'mock-token',
      user: mockUser,
    };

    (apiClient.register as vi.Mock).mockResolvedValue(mockRegisterResponse);
    mockLocalStorage.getItem.mockReturnValue(null);

    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <AuthProvider>{children}</AuthProvider>
    );
    const { result } = renderHook(() => useAuth(), { wrapper });

    // Wait for initial loading to complete
    await waitFor(() => expect(result.current.loading).toBe(false));

    await act(async () => {
      await result.current.register('test@example.com', 'password123', 'Test User');
    });

    expect(apiClient.register).toHaveBeenCalledWith('test@example.com', 'password123', 'Test User');
    expect(mockLocalStorage.setItem).toHaveBeenCalledWith('access_token', 'mock-token');
    expect(mockLocalStorage.setItem).toHaveBeenCalledWith('user', JSON.stringify(mockUser));
    expect(result.current.user).toEqual(mockUser);
    expect(result.current.isAuthenticated).toBe(true);
  });

  it('handles logout successfully', async () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <AuthProvider>{children}</AuthProvider>
    );
    const { result } = renderHook(() => useAuth(), { wrapper });

    // Wait for initial loading to complete
    await waitFor(() => expect(result.current.loading).toBe(false));

    // Set a user to log out from
    await act(async () => {
      mockLocalStorage.getItem.mockReturnValue(JSON.stringify(mockUser));
    });

    await act(async () => {
      await result.current.logout();
    });

    expect(apiClient.logout).toHaveBeenCalled();
    expect(mockLocalStorage.removeItem).toHaveBeenCalledWith('access_token');
    expect(mockLocalStorage.removeItem).toHaveBeenCalledWith('user');
    expect(result.current.user).toBeNull();
    expect(result.current.isAuthenticated).toBe(false);
  });

  it('handles login error', async () => {
    const mockError = new Error('Invalid credentials');
    (apiClient.login as vi.Mock).mockRejectedValue(mockError);
    mockLocalStorage.getItem.mockReturnValue(null);

    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <AuthProvider>{children}</AuthProvider>
    );
    const { result } = renderHook(() => useAuth(), { wrapper });

    // Wait for initial loading to complete
    await waitFor(() => expect(result.current.loading).toBe(false));

    await expect(async () => {
      await act(async () => {
        await result.current.login('test@example.com', 'wrongpassword');
      });
    }).rejects.toThrow('Invalid credentials');

    expect(result.current.user).toBeNull();
  });

  it('handles registration error', async () => {
    const mockError = new Error('Registration failed');
    (apiClient.register as vi.Mock).mockRejectedValue(mockError);
    mockLocalStorage.getItem.mockReturnValue(null);

    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <AuthProvider>{children}</AuthProvider>
    );
    const { result } = renderHook(() => useAuth(), { wrapper });

    // Wait for initial loading to complete
    await waitFor(() => expect(result.current.loading).toBe(false));

    await expect(async () => {
      await act(async () => {
        await result.current.register('test@example.com', 'password123', 'Test User');
      });
    }).rejects.toThrow('Registration failed');

    expect(result.current.user).toBeNull();
  });
});
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { apiClient } from '@/lib/api';

// Mock the fetch API
const mockFetch = vi.fn();
global.fetch = mockFetch;

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

describe('apiClient', () => {
  const mockUser = {
    id: 'user1',
    email: 'test@example.com',
    name: 'Test User',
    created_at: '2023-01-01T00:00:00Z',
    updated_at: '2023-01-01T00:00:00Z',
  };

  const mockTask = {
    id: 1,
    title: 'Test Task',
    description: 'Test Description',
    completed: false,
    user_id: 'user1',
    created_at: '2023-01-01T00:00:00Z',
    updated_at: '2023-01-01T00:00:00Z',
  };

  beforeEach(() => {
    vi.clearAllMocks();
    mockLocalStorage.getItem.mockClear();
    mockLocalStorage.setItem.mockClear();
    mockLocalStorage.removeItem.mockClear();
  });

  describe('authentication methods', () => {
    it('login makes correct API call and returns response', async () => {
      const mockResponse = {
        access_token: 'mock-token',
        user: mockUser,
      };

      mockFetch.mockResolvedValue({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await apiClient.login('test@example.com', 'password123');

      expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: 'test@example.com', password: 'password123' }),
      });

      expect(result).toEqual(mockResponse);
    });

    it('register makes correct API call and returns response', async () => {
      const mockResponse = {
        access_token: 'mock-token',
        user: mockUser,
      };

      mockFetch.mockResolvedValue({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await apiClient.register('test@example.com', 'password123', 'Test User');

      expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: 'test@example.com', password: 'password123', name: 'Test User' }),
      });

      expect(result).toEqual(mockResponse);
    });

    it('logout removes tokens from localStorage', async () => {
      const result = await apiClient.logout();

      expect(mockLocalStorage.removeItem).toHaveBeenCalledWith('access_token');
      expect(mockLocalStorage.removeItem).toHaveBeenCalledWith('user');
      expect(result).toEqual({ message: 'Successfully logged out' });
    });

    it('request adds authorization header when token is present', async () => {
      mockLocalStorage.getItem.mockReturnValue('mock-token');
      const mockResponse = { data: 'success' };

      mockFetch.mockResolvedValue({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await apiClient.request('/test-endpoint');

      expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/test-endpoint', {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer mock-token',
        },
      });

      expect(result).toEqual(mockResponse);
    });

    it('request does not add authorization header when token is absent', async () => {
      mockLocalStorage.getItem.mockReturnValue(null);
      const mockResponse = { data: 'success' };

      mockFetch.mockResolvedValue({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await apiClient.request('/test-endpoint');

      expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/test-endpoint', {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      expect(result).toEqual(mockResponse);
    });

    it('throws error when API request fails', async () => {
      mockFetch.mockResolvedValue({
        ok: false,
        status: 400,
        json: async () => ({ error: { message: 'Bad Request' } }),
      });

      await expect(apiClient.request('/test-endpoint')).rejects.toThrow('Bad Request');

      // Test with generic error message
      mockFetch.mockResolvedValue({
        ok: false,
        status: 500,
        json: async () => ({}),
      });

      await expect(apiClient.request('/test-endpoint')).rejects.toThrow('API request failed: 500');
    });
  });

  describe('task methods', () => {
    beforeEach(() => {
      mockLocalStorage.getItem.mockReturnValue('mock-token');
    });

    it('getTasks makes correct API call', async () => {
      const mockResponse = {
        tasks: [mockTask],
        total_count: 1,
        completed_count: 0,
        pending_count: 1,
      };

      mockFetch.mockResolvedValue({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await apiClient.getTasks('user1');

      expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/user1/tasks?status=all&sort=created', {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer mock-token',
        },
      });

      expect(result).toEqual(mockResponse);
    });

    it('createTask makes correct API call', async () => {
      const mockTaskData = { title: 'New Task', description: 'New Description' };
      const mockCreatedTask = { ...mockTask, id: 2, title: 'New Task', description: 'New Description' };

      mockFetch.mockResolvedValue({
        ok: true,
        json: async () => mockCreatedTask,
      });

      const result = await apiClient.createTask('user1', mockTaskData);

      expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/user1/tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer mock-token',
        },
        body: JSON.stringify(mockTaskData),
      });

      expect(result).toEqual(mockCreatedTask);
    });

    it('getTask makes correct API call', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        json: async () => mockTask,
      });

      const result = await apiClient.getTask('user1', 1);

      expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/user1/tasks/1', {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer mock-token',
        },
      });

      expect(result).toEqual(mockTask);
    });

    it('updateTask makes correct API call', async () => {
      const mockUpdateData = { title: 'Updated Task' };
      const mockUpdatedTask = { ...mockTask, title: 'Updated Task' };

      mockFetch.mockResolvedValue({
        ok: true,
        json: async () => mockUpdatedTask,
      });

      const result = await apiClient.updateTask('user1', 1, mockUpdateData);

      expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/user1/tasks/1', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer mock-token',
        },
        body: JSON.stringify(mockUpdateData),
      });

      expect(result).toEqual(mockUpdatedTask);
    });

    it('deleteTask makes correct API call', async () => {
      const mockResponse = { message: 'Task deleted successfully' };

      mockFetch.mockResolvedValue({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await apiClient.deleteTask('user1', 1);

      expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/user1/tasks/1', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer mock-token',
        },
      });

      expect(result).toEqual(mockResponse);
    });

    it('toggleTaskCompletion makes correct API call', async () => {
      const mockToggledTask = { ...mockTask, completed: true };

      mockFetch.mockResolvedValue({
        ok: true,
        json: async () => mockToggledTask,
      });

      const result = await apiClient.toggleTaskCompletion('user1', 1, true);

      expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/user1/tasks/1/complete', {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer mock-token',
        },
        body: JSON.stringify({ completed: true }),
      });

      expect(result).toEqual(mockToggledTask);
    });
  });
});
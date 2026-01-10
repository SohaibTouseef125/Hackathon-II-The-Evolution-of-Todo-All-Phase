// API client for the Todo Web Application
import {
  AuthResponse,
  Task,
  TaskListResponse,
  TaskCreateData,
  TaskUpdateData,
  TaskToggleCompleteData
} from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const token = localStorage.getItem('access_token');

    const headers = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    };

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      console.log("respone",response);
      
      const errorData = await response.json().catch(() => ({}));
      console.log("error",errorData);
      
      throw new Error(errorData.error?.message || `API request failed: ${response}`);
    }

    return response.json();
  }

  // Authentication methods
  async login(email: string, password: string): Promise<AuthResponse> {
    const token = localStorage.getItem('access_token');

    const formData = new URLSearchParams();
    formData.append('email', email);
    formData.append('password', password);

    const headers: HeadersInit = {
      'Content-Type': 'application/x-www-form-urlencoded',
      ...(token && { 'Authorization': `Bearer ${token}` }),
    };

    const response = await fetch(`${this.baseUrl}/auth/login`, {
      method: 'POST',
      headers,
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Login failed');
    }

    return response.json();
  }

  async register(email: string, password: string, name: string): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password, name }),
    });
  }

  async logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    return { message: 'Successfully logged out' };
  }

  // Task methods
  // Note: User is identified by JWT token, not URL path
  async getTasks(statusFilter: string = 'all', sort: string = 'created'): Promise<Task[]> {
    // Backend returns List[TaskRead], statusFilter and sort are currently not supported by backend
    return this.request<Task[]>('/tasks');
  }

  async createTask(taskData: TaskCreateData): Promise<Task> {
    return this.request<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async getTask(taskId: string): Promise<Task> {
    return this.request<Task>(`/tasks/${taskId}`);
  }

  async updateTask(taskId: string, taskData: TaskUpdateData): Promise<Task> {
    return this.request<Task>(`/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(taskId: string): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskCompletion(taskId: string, completed: boolean): Promise<Task> {
    return this.request<Task>(`/tasks/${taskId}/complete`, {
      method: 'PATCH',
    });
  }
}

export const apiClient = new ApiClient();
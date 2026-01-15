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

  async request<T>(endpoint: string, options: RequestInit = {}, showToast: boolean = true): Promise<T> {
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
      const errorData = await response.json().catch(() => ({}));
      const errorMessage = errorData.detail || errorData.message || `API request failed: ${response.status}`;

      if (showToast) {
        // Dynamically import toast to avoid circular dependencies
        const { useToast } = await import('@/hooks/use-toast');
        const { toast } = useToast();
        toast({
          title: 'Error',
          description: errorMessage,
          variant: 'destructive'
        });
      }

      console.error(errorMessage); // Log for debugging
      throw new Error(errorMessage); // Still throw for backward compatibility
    }

    return response.json();
  }

  // Authentication methods
  async login(email: string, password: string, showToast: boolean = true): Promise<AuthResponse> {
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
      const errorMessage = errorData.detail || 'Login failed';

      if (showToast) {
        // Dynamically import toast to avoid circular dependencies
        const { useToast } = await import('@/hooks/use-toast');
        const { toast } = useToast();
        toast({
          title: 'Error',
          description: errorMessage,
          variant: 'destructive'
        });
      }

      console.error(errorMessage); // Log for debugging
      throw new Error(errorMessage);
    }

    return response.json();
  }

  async register(email: string, password: string, name: string, showToast: boolean = true): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password, name }),
    }, showToast);
  }

  async logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    return { message: 'Successfully logged out' };
  }

  // Task methods
  // Note: User is identified by JWT token, not URL path
  async getTasks(statusFilter: string = 'all', sort: string = 'created', showToast: boolean = true): Promise<Task[]> {
    // Backend returns List[TaskRead], statusFilter and sort are currently not supported by backend
    return this.request<Task[]>('/tasks', {}, showToast);
  }

  async createTask(taskData: TaskCreateData, showToast: boolean = true): Promise<Task> {
    return this.request<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    }, showToast);
  }

  async getTask(taskId: string, showToast: boolean = true): Promise<Task> {
    return this.request<Task>(`/tasks/${taskId}`, {}, showToast);
  }

  async updateTask(taskId: string, taskData: TaskUpdateData, showToast: boolean = true): Promise<Task> {
    return this.request<Task>(`/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    }, showToast);
  }

  async deleteTask(taskId: string, showToast: boolean = true): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/tasks/${taskId}`, {
      method: 'DELETE',
    }, showToast);
  }

  async toggleTaskCompletion(taskId: string, completed: boolean, showToast: boolean = true): Promise<Task> {
    return this.request<Task>(`/tasks/${taskId}/complete`, {
      method: 'PATCH',
    }, showToast);
  }
}

// Chat interface types
import type { ChatMessageRecord, ChatResponse, Conversation } from '@/types';

interface ChatRequest {
  message: string;
  conversation_id?: string;
}

class ChatApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}, showToast: boolean = true): Promise<T> {
    const token = localStorage.getItem('access_token');

    const headers = {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    };

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const contentType = response.headers.get('content-type');

      if (contentType && contentType.includes('application/json')) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.detail || errorData.message || 'Chat request failed';

        if (showToast) {
          // Dynamically import toast to avoid circular dependencies
          const { useToast } = await import('@/hooks/use-toast');
          const { toast } = useToast();
          toast({
            title: 'Error',
            description: errorMessage,
            variant: 'destructive'
          });
        }

        console.error(errorMessage); // Log for debugging
        throw new Error(errorMessage); // Still throw for backward compatibility
      }

      const errorText = await response.text().catch(() => '');
      const errorStatusMessage = `Chat request failed: ${response.status}`;

      if (showToast) {
        // Dynamically import toast to avoid circular dependencies
        const { useToast } = await import('@/hooks/use-toast');
        const { toast } = useToast();
        toast({
          title: 'Error',
          description: errorStatusMessage,
          variant: 'destructive'
        });
      }

      console.error('Non-JSON response:', errorText);
      throw new Error(errorStatusMessage);
    }

    // Some endpoints may return 204 in the future; handle gracefully
    if (response.status === 204) {
      return undefined as T;
    }

    return response.json();
  }

  async sendMessage(userId: string, message: string, conversationId?: string, showToast: boolean = true): Promise<ChatResponse> {
    return this.request<ChatResponse>(`/${userId}/chat`, {
      method: 'POST',
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
      } satisfies ChatRequest),
    }, showToast);
  }

  async listConversations(userId: string, showToast: boolean = true): Promise<Conversation[]> {
    return this.request<Conversation[]>(`/${userId}/conversations`, { method: 'GET' }, showToast);
  }

  async createConversation(userId: string, showToast: boolean = true): Promise<Conversation> {
    return this.request<Conversation>(`/${userId}/conversations`, { method: 'POST' }, showToast);
  }

  async getLatestConversation(userId: string, showToast: boolean = true): Promise<Conversation | null> {
    return this.request<Conversation | null>(`/${userId}/conversations/latest`, { method: 'GET' }, showToast);
  }

  async getConversationMessages(
    userId: string,
    conversationId: string,
    limit?: number,
    showToast: boolean = true,
  ): Promise<ChatMessageRecord[]> {
    const query = typeof limit === 'number' ? `?limit=${encodeURIComponent(limit)}` : '';
    return this.request<ChatMessageRecord[]>(
      `/${userId}/conversations/${conversationId}/messages${query}`,
      { method: 'GET' },
      showToast
    );
  }

  async clearConversationMessages(userId: string, conversationId: string, showToast: boolean = true): Promise<{ message: string; deleted: number }> {
    return this.request<{ message: string; deleted: number }>(
      `/${userId}/conversations/${conversationId}/messages`,
      { method: 'DELETE' },
      showToast
    );
  }

  async deleteConversation(userId: string, conversationId: string, showToast: boolean = true): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/${userId}/conversations/${conversationId}`, {
      method: 'DELETE',
    }, showToast);
  }

  async deleteMessage(
    userId: string,
    conversationId: string,
    messageId: string,
    showToast: boolean = true,
  ): Promise<{ message: string }> {
    return this.request<{ message: string }>(
      `/${userId}/conversations/${conversationId}/messages/${messageId}`,
      { method: 'DELETE' },
      showToast
    );
  }
}

export const apiClient = new ApiClient();
export const chatApiClient = new ChatApiClient();
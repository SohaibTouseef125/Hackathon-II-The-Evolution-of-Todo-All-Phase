import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { AuthProvider } from '@/hooks/use-auth';
import DashboardPage from '@/app/dashboard/page';
import { apiClient } from '@/lib/api';

// Mock the apiClient
vi.mock('@/lib/api', () => ({
  apiClient: {
    getTasks: vi.fn(),
    createTask: vi.fn(),
    toggleTaskCompletion: vi.fn(),
    deleteTask: vi.fn(),
    logout: vi.fn(),
  },
}));

// Mock the router
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
  usePathname: () => '/dashboard',
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

describe('Dashboard Page Integration', () => {
  const mockUser = {
    id: 'user1',
    email: 'test@example.com',
    name: 'Test User',
    created_at: '2023-01-01T00:00:00Z',
    updated_at: '2023-01-01T00:00:00Z',
  };

  const mockTasks = [
    {
      id: 1,
      title: 'Test Task 1',
      description: 'Test Description 1',
      completed: false,
      user_id: 'user1',
      created_at: '2023-01-01T00:00:00Z',
      updated_at: '2023-01-01T00:00:00Z',
    },
    {
      id: 2,
      title: 'Test Task 2',
      description: undefined,
      completed: true,
      user_id: 'user1',
      created_at: '2023-01-01T00:00:00Z',
      updated_at: '2023-01-01T00:00:00Z',
    }
  ];

  beforeEach(() => {
    vi.clearAllMocks();
    mockLocalStorage.getItem.mockReturnValue(JSON.stringify(mockUser));
    (apiClient.getTasks as vi.Mock).mockResolvedValue({ tasks: mockTasks, total_count: 2, completed_count: 1, pending_count: 1 });
    (apiClient.createTask as vi.Mock).mockResolvedValue({ ...mockTasks[0], id: 3, title: 'New Task', completed: false });
    (apiClient.toggleTaskCompletion as vi.Mock).mockResolvedValue({ ...mockTasks[0], completed: true });
    (apiClient.deleteTask as vi.Mock).mockResolvedValue({ message: 'Task deleted successfully' });
  });

  it('loads tasks and displays them on initial render', async () => {
    render(
      <AuthProvider>
        <DashboardPage />
      </AuthProvider>
    );

    // Should show loading initially
    expect(screen.getByText('Loading...')).toBeInTheDocument();

    // Wait for tasks to load
    await waitFor(() => {
      expect(screen.getByText('Test Task 1')).toBeInTheDocument();
      expect(screen.getByText('Test Task 2')).toBeInTheDocument();
    });

    // Verify tasks are displayed
    expect(screen.getByText('Test Task 1')).toBeInTheDocument();
    expect(screen.getByText('Test Task 2')).toBeInTheDocument();
    expect(screen.getByText('Test Description 1')).toBeInTheDocument();
    expect(screen.getByRole('checkbox', { checked: false })).toBeInTheDocument();
    expect(screen.getByRole('checkbox', { checked: true })).toBeInTheDocument();
  });

  it('allows creating a new task', async () => {
    render(
      <AuthProvider>
        <DashboardPage />
      </AuthProvider>
    );

    // Wait for initial load
    await waitFor(() => {
      expect(screen.getByText('Test Task 1')).toBeInTheDocument();
    });

    // Fill in the new task form
    const titleInput = screen.getByPlaceholderText(/what needs to be done/i);
    const descriptionInput = screen.getByPlaceholderText(/add details/i);
    const form = screen.getByRole('form');

    fireEvent.change(titleInput, { target: { value: 'New Task' } });
    fireEvent.change(descriptionInput, { target: { value: 'New Task Description' } });

    fireEvent.submit(form);

    // Wait for the task to be created
    await waitFor(() => {
      expect(apiClient.createTask).toHaveBeenCalledWith('user1', {
        title: 'New Task',
        description: 'New Task Description'
      });
    });

    // Verify the new task appears in the list
    expect(screen.getByText('New Task')).toBeInTheDocument();
  });

  it('allows toggling task completion', async () => {
    render(
      <AuthProvider>
        <DashboardPage />
      </AuthProvider>
    );

    // Wait for initial load
    await waitFor(() => {
      expect(screen.getByText('Test Task 1')).toBeInTheDocument();
    });

    // Find the checkbox for the first task and click it
    const checkbox = screen.getByRole('checkbox', { checked: false });
    fireEvent.click(checkbox);

    // Wait for the API call to complete
    await waitFor(() => {
      expect(apiClient.toggleTaskCompletion).toHaveBeenCalledWith('user1', 1, true);
    });

    // Verify the task is now marked as completed (with strikethrough)
    const completedTask = screen.getByText('Test Task 1');
    expect(completedTask).toHaveClass('line-through');
  });

  it('allows deleting a task', async () => {
    // Mock confirm dialog
    window.confirm = vi.fn(() => true);

    render(
      <AuthProvider>
        <DashboardPage />
      </AuthProvider>
    );

    // Wait for initial load
    await waitFor(() => {
      expect(screen.getByText('Test Task 1')).toBeInTheDocument();
    });

    // Find the delete button for the first task and click it
    const deleteButton = screen.getAllByText('Delete')[0]; // Get the first delete button
    fireEvent.click(deleteButton);

    // Wait for the API call to complete
    await waitFor(() => {
      expect(apiClient.deleteTask).toHaveBeenCalledWith('user1', 1);
    });

    // Verify the task is no longer in the list
    expect(screen.queryByText('Test Task 1')).not.toBeInTheDocument();
  });

  it('handles API errors gracefully', async () => {
    // Mock an error when fetching tasks
    (apiClient.getTasks as vi.Mock).mockRejectedValue(new Error('Network error'));

    render(
      <AuthProvider>
        <DashboardPage />
      </AuthProvider>
    );

    // Wait to see if an error message appears
    await waitFor(() => {
      expect(screen.queryByText(/error fetching tasks/i)).toBeInTheDocument();
    });
  });
});
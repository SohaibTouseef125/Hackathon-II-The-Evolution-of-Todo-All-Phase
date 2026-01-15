import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import TaskList from '@/components/task-list';
import { Task } from '@/types';

describe('TaskList', () => {
  const mockTasks: Task[] = [
    {
      id: '1',
      title: 'Test Task 1',
      description: 'Test Description 1',
      completed: false,
      user_id: 'user1',
      created_at: '2023-01-01T00:00:00Z',
      updated_at: '2023-01-01T00:00:00Z'
    },
    {
      id: '2',
      title: 'Test Task 2',
      description: undefined,
      completed: true,
      user_id: 'user1',
      created_at: '2023-01-01T00:00:00Z',
      updated_at: '2023-01-01T00:00:00Z'
    }
  ];

  const mockOnToggleComplete = vi.fn();
  const mockOnDelete = vi.fn();

  beforeEach(() => {
    mockOnToggleComplete.mockClear();
    mockOnDelete.mockClear();
  });

  it('renders correctly when tasks are provided', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onToggleComplete={mockOnToggleComplete}
        onDelete={mockOnDelete}
      />
    );

    expect(screen.getByText('Test Task 1')).toBeInTheDocument();
    expect(screen.getByText('Test Task 2')).toBeInTheDocument();
    expect(screen.getByText('- Test Description 1')).toBeInTheDocument();
    expect(screen.getByRole('checkbox', { checked: false })).toBeInTheDocument();
    expect(screen.getByRole('checkbox', { checked: true })).toBeInTheDocument();
  });

  it('renders empty state when no tasks are provided', () => {
    render(
      <TaskList
        tasks={[]}
        onToggleComplete={mockOnToggleComplete}
        onDelete={mockOnDelete}
      />
    );

    expect(screen.getByText(/no tasks yet/i)).toBeInTheDocument();
  });

  it('calls onToggleComplete when checkbox is clicked', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onToggleComplete={mockOnToggleComplete}
        onDelete={mockOnDelete}
      />
    );

    const checkbox = screen.getByRole('checkbox', { checked: false });
    fireEvent.click(checkbox);

    expect(mockOnToggleComplete).toHaveBeenCalledWith('1', false);
  });

  it('calls onDelete when delete button is clicked', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onToggleComplete={mockOnToggleComplete}
        onDelete={mockOnDelete}
      />
    );

    const deleteButton = screen.getByText('Delete');
    fireEvent.click(deleteButton);

    expect(mockOnDelete).toHaveBeenCalledWith('1');
  });

  it('displays completed tasks with strikethrough', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onToggleComplete={mockOnToggleComplete}
        onDelete={mockOnDelete}
      />
    );

    const completedTask = screen.getByText('Test Task 2');
    expect(completedTask).toHaveClass('line-through');
  });

  it('displays pending tasks without strikethrough', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onToggleComplete={mockOnToggleComplete}
        onDelete={mockOnDelete}
      />
    );

    const pendingTask = screen.getByText('Test Task 1');
    expect(pendingTask).not.toHaveClass('line-through');
  });
});
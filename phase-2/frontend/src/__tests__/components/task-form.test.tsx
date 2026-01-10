import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import TaskForm from '@/components/task-form';

describe('TaskForm', () => {
  const mockOnSubmit = vi.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  it('renders correctly with default props', () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    expect(screen.getByLabelText(/task title/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/what needs to be done/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/add details/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /add task/i })).toBeInTheDocument();
  });

  it('renders with custom submit button text', () => {
    render(<TaskForm onSubmit={mockOnSubmit} submitButtonText="Update Task" />);

    expect(screen.getByRole('button', { name: /update task/i })).toBeInTheDocument();
  });

  it('allows user to input title and description', () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByPlaceholderText(/what needs to be done/i);
    const descriptionInput = screen.getByPlaceholderText(/add details/i);

    fireEvent.change(titleInput, { target: { value: 'Test Title' } });
    fireEvent.change(descriptionInput, { target: { value: 'Test Description' } });

    expect(titleInput).toHaveValue('Test Title');
    expect(descriptionInput).toHaveValue('Test Description');
  });

  it('submits form data when submitted', () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByPlaceholderText(/what needs to be done/i);
    const descriptionInput = screen.getByPlaceholderText(/add details/i);
    const form = screen.getByRole('form');

    fireEvent.change(titleInput, { target: { value: 'Test Title' } });
    fireEvent.change(descriptionInput, { target: { value: 'Test Description' } });
    fireEvent.submit(form);

    expect(mockOnSubmit).toHaveBeenCalledWith({
      title: 'Test Title',
      description: 'Test Description'
    });
  });

  it('resets form after submission when not in edit mode', () => {
    render(<TaskForm onSubmit={mockOnSubmit} />);

    const titleInput = screen.getByPlaceholderText(/what needs to be done/i);
    const descriptionInput = screen.getByPlaceholderText(/add details/i);

    fireEvent.change(titleInput, { target: { value: 'Test Title' } });
    fireEvent.change(descriptionInput, { target: { value: 'Test Description' } });

    expect(titleInput).toHaveValue('Test Title');
    expect(descriptionInput).toHaveValue('Test Description');

    fireEvent.submit(screen.getByRole('form'));

    // After submission, the form should reset for add mode
    expect(titleInput).toHaveValue('');
    expect(descriptionInput).toHaveValue('');
  });

  it('does not reset form after submission when in edit mode', () => {
    render(<TaskForm onSubmit={mockOnSubmit} isEditing={true} initialData={{ title: 'Initial Title', description: 'Initial Description' }} />);

    const titleInput = screen.getByDisplayValue('Initial Title');
    const descriptionInput = screen.getByDisplayValue('Initial Description');

    fireEvent.change(titleInput, { target: { value: 'Updated Title' } });
    fireEvent.change(descriptionInput, { target: { value: 'Updated Description' } });

    fireEvent.submit(screen.getByRole('form'));

    // In edit mode, the form should not reset after submission
    expect(titleInput).toHaveValue('Updated Title');
    expect(descriptionInput).toHaveValue('Updated Description');
  });
});
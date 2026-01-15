import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { MockedProvider } from '@apollo/client/testing';
import ChatPage from '../src/app/chat/page';
import { useAuth } from '../src/hooks/use-auth';
import { useChat } from 'ai/react';

// Mock the useAuth hook
jest.mock('../src/hooks/use-auth', () => ({
  useAuth: jest.fn(),
}));

// Mock the useChat hook
jest.mock('ai/react', () => ({
  useChat: jest.fn(),
}));

// Mock the ChatWidget
jest.mock('@openai/chat-widget', () => ({
  ChatWidget: ({ messages, input, handleInputChange, handleSubmit }: any) => (
    <div data-testid="chat-widget">
      <div data-testid="messages">
        {messages?.map((msg: any, index: number) => (
          <div key={index} data-testid={`message-${index}`}>
            {msg.content}
          </div>
        ))}
      </div>
      <input
        data-testid="chat-input"
        value={input}
        onChange={handleInputChange}
        placeholder="Ask me to add, view, update, or manage your tasks..."
      />
      <button data-testid="send-button" onClick={handleSubmit}>Send</button>
    </div>
  ),
}));

// Mock the ChatWidgetRuntime
jest.mock('@openai/chat-widget/types', () => ({
  ChatWidgetRuntime: {},
}));

describe('ChatPage', () => {
  beforeEach(() => {
    (useAuth as jest.Mock).mockReturnValue({
      user: { id: 'test-user-id', email: 'test@example.com', name: 'Test User' },
      loading: false,
      isAuthenticated: true,
    });

    (useChat as jest.Mock).mockReturnValue({
      messages: [
        { id: '1', role: 'user', content: 'Hello' },
        { id: '2', role: 'assistant', content: 'Hi there!' },
      ],
      input: '',
      handleInputChange: jest.fn(),
      handleSubmit: jest.fn(),
      isLoading: false,
      error: null,
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders the chat page when authenticated', () => {
    render(
      <MockedProvider>
        <ChatPage />
      </MockedProvider>
    );

    expect(screen.getByText('Todo AI Assistant')).toBeInTheDocument();
    expect(screen.getByText('Welcome, Test User')).toBeInTheDocument();
    expect(screen.getByTestId('chat-widget')).toBeInTheDocument();
    expect(screen.getByTestId('message-0')).toHaveTextContent('Hello');
    expect(screen.getByTestId('message-1')).toHaveTextContent('Hi there!');
  });

  it('shows loading state while authenticating', () => {
    (useAuth as jest.Mock).mockReturnValue({
      user: null,
      loading: true,
      isAuthenticated: false,
    });

    render(
      <MockedProvider>
        <ChatPage />
      </MockedProvider>
    );

    expect(screen.getByRole('status')).toBeInTheDocument(); // Loading spinner
  });

  it('shows access denied message when not authenticated', () => {
    (useAuth as jest.Mock).mockReturnValue({
      user: null,
      loading: false,
      isAuthenticated: false,
    });

    render(
      <MockedProvider>
        <ChatPage />
      </MockedProvider>
    );

    expect(screen.getByText('Access Denied')).toBeInTheDocument();
    expect(screen.getByText('Please log in to access the chat interface.')).toBeInTheDocument();
  });

  it('displays user input and handles changes', async () => {
    const mockHandleInputChange = jest.fn();
    (useChat as jest.Mock).mockReturnValue({
      messages: [],
      input: 'Buy groceries',
      handleInputChange: mockHandleInputChange,
      handleSubmit: jest.fn(),
      isLoading: false,
      error: null,
    });

    render(
      <MockedProvider>
        <ChatPage />
      </MockedProvider>
    );

    const inputElement = screen.getByTestId('chat-input');
    expect(inputElement).toHaveValue('Buy groceries');

    fireEvent.change(inputElement, { target: { value: 'Call mom' } });
    expect(mockHandleInputChange).toHaveBeenCalled();
  });

  it('handles form submission', async () => {
    const mockHandleSubmit = jest.fn((e) => e.preventDefault());
    (useChat as jest.Mock).mockReturnValue({
      messages: [],
      input: 'Buy groceries',
      handleInputChange: jest.fn(),
      handleSubmit: mockHandleSubmit,
      isLoading: false,
      error: null,
    });

    render(
      <MockedProvider>
        <ChatPage />
      </MockedProvider>
    );

    const form = screen.getByRole('form');
    fireEvent.submit(form);

    await waitFor(() => {
      expect(mockHandleSubmit).toHaveBeenCalled();
    });
  });

  it('disables send button when input is empty', () => {
    (useChat as jest.Mock).mockReturnValue({
      messages: [],
      input: '',
      handleInputChange: jest.fn(),
      handleSubmit: jest.fn(),
      isLoading: false,
      error: null,
    });

    render(
      <MockedProvider>
        <ChatPage />
      </MockedProvider>
    );

    const sendButton = screen.getByTestId('send-button');
    expect(sendButton).toBeDisabled();
  });

  it('enables send button when input has content', () => {
    (useChat as jest.Mock).mockReturnValue({
      messages: [],
      input: 'Buy groceries',
      handleInputChange: jest.fn(),
      handleSubmit: jest.fn(),
      isLoading: false,
      error: null,
    });

    render(
      <MockedProvider>
        <ChatPage />
      </MockedProvider>
    );

    const sendButton = screen.getByTestId('send-button');
    expect(sendButton).not.toBeDisabled();
  });

  it('shows loading indicator when chat is loading', () => {
    (useChat as jest.Mock).mockReturnValue({
      messages: [],
      input: '',
      handleInputChange: jest.fn(),
      handleSubmit: jest.fn(),
      isLoading: true,
      error: null,
    });

    render(
      <MockedProvider>
        <ChatPage />
      </MockedProvider>
    );

    // Check for loading indicator elements
    const loadingElements = screen.queryAllByRole('status');
    expect(loadingElements.length).toBeGreaterThan(0);
  });

  it('displays error message when there is an error', () => {
    const mockError = { message: 'Test error' };
    (useChat as jest.Mock).mockReturnValue({
      messages: [],
      input: '',
      handleInputChange: jest.fn(),
      handleSubmit: jest.fn(),
      isLoading: false,
      error: mockError,
    });

    render(
      <MockedProvider>
        <ChatPage />
      </MockedProvider>
    );

    expect(screen.getByText('Error: Test error')).toBeInTheDocument();
  });
});
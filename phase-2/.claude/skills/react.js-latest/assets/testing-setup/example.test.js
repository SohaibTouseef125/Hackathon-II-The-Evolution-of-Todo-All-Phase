// Example React Component Test
// example.test.js
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ExampleComponent } from '../src/components/ExampleComponent';

describe('ExampleComponent', () => {
  test('renders with initial count', () => {
    render(<ExampleComponent initialCount={5} />);
    expect(screen.getByText(/Count: 5/i)).toBeInTheDocument();
  });

  test('increments count when button is clicked', async () => {
    render(<ExampleComponent initialCount={0} />);

    const incrementButton = screen.getByRole('button', { name: /increment/i });
    fireEvent.click(incrementButton);

    expect(await screen.findByText(/Count: 1/i)).toBeInTheDocument();
  });

  test('decrements count when button is clicked', async () => {
    render(<ExampleComponent initialCount={5} />);

    const decrementButton = screen.getByRole('button', { name: /decrement/i });
    fireEvent.click(decrementButton);

    expect(await screen.findByText(/Count: 4/i)).toBeInTheDocument();
  });

  test('handles async operations', async () => {
    // Mock fetch API
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({ data: 'test' }),
      })
    );

    render(<ExampleComponent />);

    // Wait for async operation to complete
    await waitFor(() => {
      expect(screen.getByText(/Data loaded/i)).toBeInTheDocument();
    });
  });
});
// Error Boundary Component Template
import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // You can also log the error to an error reporting service
    console.error('Error caught by boundary:', error, errorInfo);
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
  }

  render() {
    if (this.state.hasError) {
      // You can render any custom fallback UI
      return (
        <div className="error-boundary">
          <h2>Something went wrong.</h2>
          <details style={{ whiteSpace: 'pre-wrap' }}>
            {this.state.error && this.state.error.toString()}
            <br />
            {this.state.errorInfo.componentStack}
          </details>
        </div>
      );
    }

    return this.props.children;
  }
}

// Example usage with functional component and hooks (React 18+)
import { useState, useEffect } from 'react';

const withErrorBoundary = (Component) => {
  return ({ fallback = <div>Something went wrong</div>, ...props }) => {
    const [hasError, setHasError] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
      const errorHandler = (error) => {
        setError(error);
        setHasError(true);
      };

      window.addEventListener('error', errorHandler);
      window.addEventListener('unhandledrejection', (event) => {
        setError(event.reason);
        setHasError(true);
      });

      return () => {
        window.removeEventListener('error', errorHandler);
        window.removeEventListener('unhandledrejection', errorHandler);
      };
    }, []);

    if (hasError) {
      return fallback;
    }

    return <Component {...props} />;
  };
};

export { ErrorBoundary, withErrorBoundary };
---
name: react.js-latest
description: Comprehensive expert guidance for React.js development covering latest features, hooks, state management, component patterns, performance optimization, testing, and best practices for modern React applications. Use this skill when working with React 18+ projects, implementing new React features, creating performant components, or following modern React development patterns and practices.
---

# React.js Latest Development Skill

## Overview

This skill provides comprehensive guidance for React.js development with the latest features and best practices. It covers React 18+ concurrent features, hooks, state management, component architecture, performance optimization, testing strategies, and integration with modern tooling ecosystems. Use this skill when working with React applications to implement modern patterns, optimize performance, handle complex state management, and follow React best practices.

## Core Capabilities

### 1. React 18+ Features and Concurrent Rendering
- Automatic batching and Suspense with transitions
- useId, useSyncExternalStore, useTransition, useDeferredValue hooks
- Strict mode enhancements and effect handling
- Server components and client components integration

### 2. Advanced Hooks and State Management
- Custom hooks for reusable logic
- Complex state management with useReducer
- Performance optimization with useMemo and useCallback
- Ref management and imperative handles

### 3. Component Architecture and Patterns
- Functional components with hooks
- Compound components and render props
- Higher-order components and custom hooks
- Error boundaries and debugging tools

### 4. Performance Optimization
- Code splitting with React.lazy and Suspense
- Memoization strategies with React.memo
- Virtualization for large lists
- Bundle optimization and tree shaking

### 5. Modern Tooling and Ecosystem
- Vite and Webpack configuration
- Next.js integration and server-side rendering
- React Router patterns
- TypeScript integration with React

### 6. Testing and Quality Assurance
- React Testing Library patterns
- Component testing strategies
- Integration and end-to-end testing
- Performance testing and monitoring

## React Fundamentals

### Component Patterns
React components can be implemented as functional components with hooks or class components. Functional components are preferred for their simplicity and better performance characteristics:

```jsx
import { useState, useEffect } from 'react';

const UserProfile = ({ userId }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await fetch(`/api/users/${userId}`);
        const userData = await response.json();
        setUser(userData);
      } catch (error) {
        console.error('Error fetching user:', error);
      } finally {
        setLoading(false);
      }
    };

    if (userId) {
      fetchUser();
    }
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  if (!user) return <div>User not found</div>;

  return (
    <div className="user-profile">
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  );
};
```

### State Management Approaches
React provides multiple approaches for state management depending on complexity:

1. **Local State**: useState and useReducer for component-level state
2. **Context**: useContext for cross-component state sharing
3. **External Libraries**: Redux Toolkit, Zustand, or React Query for complex state

## Hooks Deep Dive

### Core Hooks
- `useState`: For managing local component state
- `useEffect`: For handling side effects and lifecycle events
- `useContext`: For accessing React Context values
- `useReducer`: For complex state logic with actions

### Advanced Hooks
- `useRef`: For accessing DOM elements and storing mutable values
- `useMemo`: For memoizing expensive computations
- `useCallback`: For memoizing callback functions
- `useLayoutEffect`: For synchronous side effects after DOM mutations

### Custom Hooks
Create custom hooks to extract component logic into reusable functions:

```javascript
import { useState, useEffect, useCallback } from 'react';

// Custom hook for managing local storage
export const useLocalStorage = (key, initialValue) => {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  const setValue = useCallback((value) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error);
    }
  }, [key, storedValue]);

  return [storedValue, setValue];
};
```

## Server Components and Data Fetching

React Server Components enable server-side rendering and data fetching with better performance:

```javascript
// Server Component (runs only on server)
async function ProductList() {
  const products = await fetch('https://api.example.com/products').then(r => r.json());
  return (
    <div>
      {products.map(product => (
        <ProductItem key={product.id} product={product} />
      ))}
    </div>
  );
}

// Client Component (runs on client)
'use client';
import { useState } from 'react';

function ProductItem({ product }) {
  const [isFavorite, setIsFavorite] = useState(false);

  return (
    <div className="product-item">
      <h3>{product.name}</h3>
      <button onClick={() => setIsFavorite(!isFavorite)}>
        {isFavorite ? '★' : '☆'}
      </button>
    </div>
  );
}
```

## Performance Optimization

### Memoization Strategies
Use React.memo for component memoization:

```jsx
import { memo, useMemo } from 'react';

const ExpensiveComponent = memo(({ items, filter }) => {
  const filteredItems = useMemo(() => {
    return items.filter(item => item.category === filter);
  }, [items, filter]);

  return (
    <div>
      {filteredItems.map(item => (
        <ItemComponent key={item.id} item={item} />
      ))}
    </div>
  );
});
```

### Code Splitting
Implement code splitting with React.lazy:

```jsx
import { Suspense, lazy } from 'react';

const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));

function App() {
  return (
    <div>
      <nav>
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/settings">Settings</Link>
      </nav>
      <Suspense fallback={<div>Loading...</div>}>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Suspense>
    </div>
  );
}
```

## TypeScript Integration

TypeScript provides excellent type safety for React applications:

```tsx
import { useState } from 'react';

interface User {
  id: number;
  name: string;
  email: string;
}

interface UserListProps {
  users: User[];
  onUserSelect: (user: User) => void;
}

const UserList: React.FC<UserListProps> = ({ users, onUserSelect }) => {
  return (
    <div className="user-list">
      {users.map(user => (
        <div
          key={user.id}
          onClick={() => onUserSelect(user)}
          className="user-item"
        >
          <span>{user.name}</span>
          <span>{user.email}</span>
        </div>
      ))}
    </div>
  );
};
```

## Testing Strategies

### React Testing Library
Use React Testing Library for component testing:

```jsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import UserProfile from './UserProfile';

test('displays user information when user is loaded', async () => {
  // Mock API response
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve({ id: 1, name: 'John Doe', email: 'john@example.com' })
    })
  );

  render(<UserProfile userId={1} />);

  // Check loading state
  expect(screen.getByText('Loading...')).toBeInTheDocument();

  // Wait for user data to load
  await waitFor(() => {
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });
});
```

## Error Handling and Debugging

### Error Boundaries
Implement error boundaries to gracefully handle component errors:

```jsx
import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
    // Log error to monitoring service
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
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
```

## Accessibility Implementation

Ensure your React applications are accessible:

```jsx
import { useState, useRef, useEffect } from 'react';

const AccessibleModal = ({ isOpen, onClose, children }) => {
  const modalRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      // Focus modal when opened
      modalRef.current?.focus();

      // Trap focus within modal
      const handleKeyDown = (e) => {
        if (e.key === 'Escape') {
          onClose();
        }
      };

      document.addEventListener('keydown', handleKeyDown);
      return () => document.removeEventListener('keydown', handleKeyDown);
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        className="modal-content"
        onClick={(e) => e.stopPropagation()}
        tabIndex={-1}
      >
        <button
          onClick={onClose}
          aria-label="Close modal"
          className="close-button"
        >
          ×
        </button>
        {children}
      </div>
    </div>
  );
};
```

## Modern Tooling

### Vite Configuration
Configure Vite for React development:

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true
  },
  build: {
    outDir: './dist',
    sourcemap: true
  }
});
```

### ESLint Configuration
Use ESLint with React-specific rules:

```javascript
// eslint.config.js
import js from '@eslint/js';
import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';

export default [
  {
    files: ['**/*.{js,jsx}'],
    languageOptions: {
      ecmaVersion: 2020,
      sourceType: 'module',
    },
    plugins: {
      react,
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
    },
    rules: {
      ...js.configs.recommended.rules,
      ...react.configs.recommended.rules,
      ...react.configs['jsx-runtime'].rules,
      ...reactHooks.configs.recommended.rules,
      'react/jsx-no-target-blank': 'off',
      'react-refresh/only-export-components': [
        'warn',
        { allowConstantExport: true },
      ],
    }
  }
];
```

## Best Practices

### Component Composition
Favor composition over inheritance for building flexible and reusable components:

```jsx
// Instead of inheritance, use composition
const Modal = ({ isOpen, onClose, children, title }) => (
  <div className={`modal ${isOpen ? 'open' : ''}`}>
    <div className="modal-header">
      <h2>{title}</h2>
      <button onClick={onClose}>×</button>
    </div>
    <div className="modal-body">
      {children}
    </div>
  </div>
);

// Usage
const UserProfileModal = ({ user, isOpen, onClose }) => (
  <Modal isOpen={isOpen} onClose={onClose} title="User Profile">
    <div>
      <p>Name: {user.name}</p>
      <p>Email: {user.email}</p>
    </div>
  </Modal>
);
```

### State Colocation
Keep state as close to where it's needed as possible:

```jsx
// Good: State is colocated with the component that needs it
const SearchableList = ({ items }) => {
  const [filter, setFilter] = useState('');

  const filteredItems = items.filter(item =>
    item.name.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <input
        type="text"
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        placeholder="Search items..."
      />
      <ItemList items={filteredItems} />
    </div>
  );
};
```

## Resources

This skill includes comprehensive resources for React.js development:

### scripts/
Python and JavaScript utilities for React development tasks, including component generators, code analyzers, and project setup tools.

### references/
Complete React.js API documentation, best practices guides, and detailed examples for all React features and patterns.

### assets/
Template files for React components, hooks, contexts, and project configurations including Vite, Next.js, and Create React App setups.
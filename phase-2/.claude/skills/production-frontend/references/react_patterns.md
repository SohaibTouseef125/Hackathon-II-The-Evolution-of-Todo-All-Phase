# React Best Practices and Patterns

## Component Design Patterns

### Presentational vs Container Components
- **Presentational Components**: Focus on how things look
  - Receive data and callbacks exclusively through props
  - Rarely have their own state
  - Know about Redux only if they're a container themselves

- **Container Components**: Focus on how things work
  - Provide data and behavior to presentational components
  - Subscribe to Redux state
  - Call Redux actions
  - Are often generated using higher-order components

### Compound Components Pattern
```tsx
// Example of compound components
interface TabsProps {
  children: React.ReactNode;
  activeTab?: string;
  onChange?: (tabId: string) => void;
}

const Tabs = ({ children, activeTab, onChange }: TabsProps) => {
  return (
    <div className="tabs">
      {React.Children.map(children, child =>
        React.cloneElement(child, { activeTab, onChange })
      )}
    </div>
  );
};

const TabList = ({ children, activeTab, onChange }: TabsProps) => {
  return <div className="tab-list">{children}</div>;
};

const Tab = ({ id, children, activeTab, onChange }: { id: string } & React.PropsWithChildren) => {
  return (
    <button
      className={`tab ${activeTab === id ? 'active' : ''}`}
      onClick={() => onChange?.(id)}
    >
      {children}
    </button>
  );
};
```

### Higher-Order Components (HOCs)
```tsx
// Example HOC for authentication
function withAuth<T extends object>(
  Component: React.ComponentType<T>
) {
  return function AuthenticatedComponent(props: T) {
    const { user, loading } = useAuth();

    if (loading) return <div>Loading...</div>;
    if (!user) return <div>Please log in</div>;

    return <Component {...props} />;
  };
}
```

## Performance Optimization Patterns

### React.memo for Component Memoization
```tsx
interface UserProfileProps {
  user: {
    id: string;
    name: string;
    email: string;
  };
}

const UserProfile = React.memo<UserProfileProps>(({ user }) => {
  return (
    <div>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  );
});

// With custom comparison function
const UserProfileWithCustomCompare = React.memo<UserProfileProps>(
  ({ user }) => {
    return (
      <div>
        <h2>{user.name}</h2>
        <p>{user.email}</p>
      </div>
    );
  },
  (prevProps, nextProps) => {
    // Only re-render if user id changes
    return prevProps.user.id === nextProps.user.id;
  }
);
```

### useCallback and useMemo
```tsx
// useCallback for functions passed to child components
const MyComponent = ({ userId }: { userId: string }) => {
  const [data, setData] = useState<any[]>([]);

  const handleUpdate = useCallback(async () => {
    const result = await fetchData(userId);
    setData(result);
  }, [userId]);

  return <ChildComponent onUpdate={handleUpdate} />;
};

// useMemo for expensive calculations
const ExpensiveComponent = ({ items }: { items: number[] }) => {
  const expensiveValue = useMemo(() => {
    return items.reduce((sum, num) => {
      // Expensive calculation
      for (let i = 0; i < 1000; i++) {
        sum += num * i;
      }
      return sum;
    }, 0);
  }, [items]);

  return <div>{expensiveValue}</div>;
};
```

## Custom Hooks

### Data Fetching Hook
```tsx
// Custom hook for data fetching
function useApi<T>(url: string, options?: RequestInit) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await fetch(url, options);

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url]);

  return { data, loading, error };
}
```

### Form State Hook
```tsx
interface FormState<T> {
  values: T;
  errors: Partial<Record<keyof T, string>>;
  touched: Partial<Record<keyof T, boolean>>;
  isSubmitting: boolean;
  isValid: boolean;
}

function useForm<T extends Record<string, any>>(
  initialValues: T,
  validationSchema?: any
) {
  const [state, setState] = useState<FormState<T>>({
    values: initialValues,
    errors: {},
    touched: {},
    isSubmitting: false,
    isValid: true,
  });

  const handleChange = useCallback((name: keyof T, value: any) => {
    setState(prev => ({
      ...prev,
      values: { ...prev.values, [name]: value },
      touched: { ...prev.touched, [name]: true },
    }));
  }, []);

  const handleSubmit = useCallback(async (onSubmit: (values: T) => Promise<void>) => {
    setState(prev => ({ ...prev, isSubmitting: true }));

    try {
      await onSubmit(state.values);
    } finally {
      setState(prev => ({ ...prev, isSubmitting: false }));
    }
  }, [state.values]);

  return {
    ...state,
    handleChange,
    handleSubmit,
  };
}
```

## Error Handling Patterns

### Error Boundary Component
```tsx
class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean; error: Error | null }
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // Log error to an error reporting service
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <h2>Something went wrong.</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => this.setState({ hasError: false, error: null })}>
            Try again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

### Try-Catch Wrapper Hook
```tsx
function useAsyncCallback<T, A extends any[]>(
  callback: (...args: A) => Promise<T>,
  deps: React.DependencyList
) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = useCallback(async (...args: A): Promise<T | undefined> => {
    setLoading(true);
    setError(null);

    try {
      const result = await callback(...args);
      return result;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'An error occurred';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, deps);

  return { execute, loading, error };
}
```

## Context Pattern Best Practices

### Context Provider Pattern
```tsx
interface AppContextType {
  user: User | null;
  theme: string;
  updateUser: (user: User) => void;
  toggleTheme: () => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [theme, setTheme] = useState('light');

  const updateUser = useCallback((newUser: User) => {
    setUser(newUser);
  }, []);

  const toggleTheme = useCallback(() => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  }, []);

  const value = useMemo(() => ({
    user,
    theme,
    updateUser,
    toggleTheme,
  }), [user, theme, updateUser, toggleTheme]);

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};
```

## Testing Patterns

### Component Testing with Mock Data
```tsx
// Example test for a component
describe('UserProfile', () => {
  const mockUser = {
    id: '1',
    name: 'John Doe',
    email: 'john@example.com',
  };

  it('renders user information correctly', () => {
    render(<UserProfile user={mockUser} />);

    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('handles loading state', () => {
    const { rerender } = render(<UserProfile user={null} />);

    expect(screen.getByText('Loading...')).toBeInTheDocument();

    rerender(<UserProfile user={mockUser} />);
    expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
  });
});
```

These patterns help ensure consistent, maintainable, and performant React applications. Always consider the specific use case when applying these patterns, as not all patterns are suitable for every situation.
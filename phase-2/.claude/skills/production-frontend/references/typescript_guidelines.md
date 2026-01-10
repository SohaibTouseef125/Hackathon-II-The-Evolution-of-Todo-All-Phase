# TypeScript Configuration and Patterns

## Project Configuration

### Strict TypeScript Configuration
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

### ESLint Configuration for TypeScript
```json
{
  "extends": [
    "next/core-web-vitals",
    "@typescript-eslint/recommended",
    "@typescript-eslint/recommended-requiring-type-checking",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "parserOptions": {
    "project": "./tsconfig.json"
  },
  "rules": {
    "@typescript-eslint/strict-boolean-expressions": [
      "error",
      {
        "allowString": false,
        "allowNumber": false,
        "allowNullableObject": false
      }
    ],
    "@typescript-eslint/prefer-nullish-coalescing": "error",
    "@typescript-eslint/prefer-optional-chain": "error",
    "@typescript-eslint/no-unused-vars": [
      "error",
      {
        "argsIgnorePattern": "^_",
        "varsIgnorePattern": "^_",
        "caughtErrorsIgnorePattern": "^_"
      }
    ],
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-non-null-assertion": "error",
    "@typescript-eslint/no-unnecessary-type-assertion": "error",
    "@typescript-eslint/no-unsafe-assignment": "error",
    "@typescript-eslint/no-unsafe-call": "error",
    "@typescript-eslint/no-unsafe-member-access": "error",
    "@typescript-eslint/no-unsafe-return": "error",
    "@typescript-eslint/restrict-template-expressions": [
      "error",
      {
        "allowNumber": true,
        "allowBoolean": true
      }
    ]
  }
}
```

## Type Definitions and Interfaces

### Basic Interface Patterns
```typescript
// Use interfaces for objects that will be implemented by classes
interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
  updatedAt?: Date;
}

// Use types for union types and complex compositions
type UserRole = 'admin' | 'user' | 'moderator';
type Status = 'active' | 'inactive' | 'pending';

// Use generics for reusable components
interface ApiResponse<T> {
  data: T;
  message: string;
  status: number;
  success: boolean;
}

// Discriminated unions for handling different types
interface LoadingState {
  status: 'loading';
}

interface SuccessState<T> {
  status: 'success';
  data: T;
}

interface ErrorState {
  status: 'error';
  error: string;
}

type RemoteData<T> = LoadingState | SuccessState<T> | ErrorState;
```

### Advanced Type Patterns

#### Utility Types
```typescript
// Pick - select specific properties from a type
interface User {
  id: string;
  name: string;
  email: string;
  password: string;
}

type UserSummary = Pick<User, 'id' | 'name' | 'email'>;

// Omit - exclude specific properties from a type
type CreateUserInput = Omit<User, 'id'>;

// Partial - make all properties optional
type UpdateUserInput = Partial<User>;

// Required - make all properties required (opposite of Partial)
interface UserWithOptionalProfile {
  id: string;
  name?: string;
  email?: string;
}

type CompleteUser = Required<UserWithOptionalProfile>;

// Record - create an object type with keys of type K and values of type T
type UserPreferences = Record<'theme' | 'language' | 'notifications', string>;

// Extract - extract types from a union that are assignable to another type
type Status = 'active' | 'inactive' | 'pending' | 1 | 2 | 3;
type StringStatus = Extract<Status, string>; // 'active' | 'inactive' | 'pending'
type NumberStatus = Extract<Status, number>; // 1 | 2 | 3

// Exclude - exclude types from a union that are assignable to another type
type AvailableStatus = Exclude<Status, 1>; // 'active' | 'inactive' | 'pending' | 2 | 3
```

#### Conditional Types
```typescript
// Conditional types for different API responses
type ApiResponse<T> = T extends { error: any }
  ? { success: false; error: T['error'] }
  : { success: true; data: T };

// Function return type based on input
type AsyncReturnType<T extends (...args: any) => Promise<any>> =
  T extends (...args: any) => Promise<infer R> ? R : never;

// Example usage
async function getUser(id: string): Promise<User> {
  // Implementation
  return {} as User;
}

type GetUserResult = AsyncReturnType<typeof getUser>; // User
```

## React-Specific TypeScript Patterns

### Component Type Definitions
```tsx
// Functional component with props interface
interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  onClick?: () => void;
  disabled?: boolean;
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  onClick,
  disabled = false
}) => {
  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

// Alternative with explicit typing
const ButtonWithExplicitType: React.FC<ButtonProps> = (props) => {
  const { children, variant = 'primary', size = 'md', onClick, disabled = false } = props;

  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};
```

### Generic Components
```tsx
// Generic list component
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T, index: number) => string | number;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={keyExtractor(item, index)}>
          {renderItem(item, index)}
        </li>
      ))}
    </ul>
  );
}

// Usage
const users: User[] = [
  { id: '1', name: 'John', email: 'john@example.com' },
  { id: '2', name: 'Jane', email: 'jane@example.com' }
];

<List
  items={users}
  renderItem={(user) => <div>{user.name}</div>}
  keyExtractor={(user) => user.id}
/>;
```

### Context with TypeScript
```tsx
// Define context type
interface AppContextType {
  user: User | null;
  theme: 'light' | 'dark';
  setUser: (user: User | null) => void;
  toggleTheme: () => void;
}

// Create context with initial value
const AppContext = React.createContext<AppContextType | undefined>(undefined);

// Provider component
export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = React.useState<User | null>(null);
  const [theme, setTheme] = React.useState<'light' | 'dark'>('light');

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  const value = React.useMemo(() => ({
    user,
    theme,
    setUser,
    toggleTheme
  }), [user, theme]);

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

// Custom hook for type-safe context usage
export const useApp = () => {
  const context = React.useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};
```

### Hook Type Definitions
```tsx
// Custom hook with return type
interface UseApiResult<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

function useApi<T>(url: string): UseApiResult<T> {
  const [data, setData] = React.useState<T | null>(null);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  const fetchData = React.useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(url);
      if (!response.ok) throw new Error('Network response was not ok');
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }, [url]);

  React.useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}

// Async hook with proper typing
type AsyncState<T> =
  | { status: 'idle'; data?: null; error?: null }
  | { status: 'loading'; data?: null; error?: null }
  | { status: 'success'; data: T; error?: null }
  | { status: 'error'; data?: null; error: Error };

function useAsync<T>(asyncFunction: () => Promise<T>, deps: React.DependencyList = []): AsyncState<T> {
  const [state, setState] = React.useState<AsyncState<T>>({ status: 'idle' });

  React.useEffect(() => {
    setState({ status: 'loading' });

    asyncFunction()
      .then(data => setState({ status: 'success', data }))
      .catch(error => setState({ status: 'error', error }));
  }, deps);

  return state;
}
```

## Advanced TypeScript Patterns

### Mapped Types
```typescript
// Create readonly version of an interface
interface MutableUser {
  id: string;
  name: string;
  email: string;
}

type ReadonlyUser = {
  readonly [K in keyof MutableUser]: MutableUser[K];
};

// Transform all string properties to optional
type OptionalStringProperties<T> = {
  [K in keyof T]: T[K] extends string ? T[K] | undefined : T[K];
};

type UserWithOptionalStrings = OptionalStringProperties<User>;

// Create a type with only required properties (remove optional ones)
type RequiredProperties<T> = {
  [K in keyof T as T[K] extends Required<T>[K] ? K : never]: T[K]
};
```

### Template Literal Types
```typescript
// Create event handler type names
type EventHandlers<T extends string> = {
  [K in `on${Capitalize<T>}`]: (event: Event) => void;
};

type ClickHandlers = EventHandlers<'click' | 'hover'>;
// Results in: { onClick: (event: Event) => void; onHover: (event: Event) => void; }

// Create CSS class names
type BEM<B extends string, E extends string[], M extends string[]> =
  | `${B}--${M[number]}`
  | `${B}__${E[number]}`
  | `${B}__${E[number]}--${M[number]}`;

type ButtonClasses = BEM<'button', ['icon', 'text'], ['primary', 'secondary']>;
// Results in: 'button--primary' | 'button--secondary' | 'button__icon' | 'button__text' | 'button__icon--primary' | ...
```

### Type Guards
```typescript
// Type guard function
function isUser(obj: any): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.id === 'string' &&
    typeof obj.name === 'string' &&
    typeof obj.email === 'string'
  );
}

// Usage
function processUser(data: unknown) {
  if (isUser(data)) {
    // TypeScript knows data is User here
    console.log(data.name);
  }
}

// Array type guard
function isArrayOf<T>(predicate: (item: any) => item is T) {
  return (array: any): array is T[] => {
    return Array.isArray(array) && array.every(predicate);
  };
}

const isUserArray = isArrayOf(isUser);

// Async type guard
async function isValidUser(id: string): Promise<User | null> {
  try {
    const response = await fetch(`/api/users/${id}`);
    const user = await response.json();

    if (isUser(user)) {
      return user;
    }

    return null;
  } catch {
    return null;
  }
}
```

## API Response Typing

### API Response Patterns
```typescript
// Generic API response
interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
  errors?: string[];
}

// Error response
interface ApiError {
  message: string;
  code: string;
  details?: Record<string, any>;
}

// Paginated response
interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    pageSize: number;
    total: number;
    totalPages: number;
  };
}

// Async API call with proper typing
async function apiCall<T>(url: string): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(url);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || 'API call failed');
    }

    return {
      data,
      success: true
    };
  } catch (error) {
    return {
      data: null as any,
      success: false,
      message: error instanceof Error ? error.message : 'Unknown error'
    };
  }
}

// Specific API call with typing
interface GetUserResponse {
  id: string;
  name: string;
  email: string;
  createdAt: string;
}

async function getUser(id: string): Promise<ApiResponse<GetUserResponse>> {
  return apiCall<GetUserResponse>(`/api/users/${id}`);
}
```

## Testing with TypeScript

### Type-Safe Testing Utilities
```typescript
// Type-safe mock factory
interface UserFactoryOptions {
  id?: string;
  name?: string;
  email?: string;
}

const createUser = (options: UserFactoryOptions = {}): User => ({
  id: options.id || '1',
  name: options.name || 'Test User',
  email: options.email || 'test@example.com',
  ...options
});

// Type-safe testing utilities
type TestComponentProps<T> = {
  children: (props: T) => React.ReactElement;
};

function TestComponent<T>({ children }: TestComponentProps<T>) {
  return children({} as T);
}

// Type-safe mock functions
type MockFn<T extends (...args: any[]) => any> = jest.Mock<ReturnType<T>, Parameters<T>>;

function createMockFn<T extends (...args: any[]) => any>(fn?: T): MockFn<T> {
  return jest.fn(fn) as MockFn<T>;
}
```

These patterns ensure type safety, maintainability, and proper tooling support in your TypeScript projects. Always consider the specific use case when applying these patterns, as not all patterns are suitable for every situation.
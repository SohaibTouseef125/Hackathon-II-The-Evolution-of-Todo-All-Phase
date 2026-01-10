# React.js Latest API Reference Guide

## Core React Hooks

### useState
```javascript
const [state, setState] = useState(initialState);
```

**Purpose:** Manages local component state that can trigger re-renders when updated.

**Usage patterns:**
- For primitive values (strings, numbers, booleans)
- For objects and arrays
- For functions as initial state

**Best practices:**
- Use functional updates when new state depends on previous state
- Don't mutate state directly; create new objects/arrays

### useEffect
```javascript
useEffect(() => {
  // Side effect logic
  return () => {
    // Cleanup logic
  };
}, [dependencyArray]);
```

**Purpose:** Handles side effects like data fetching, subscriptions, and DOM manipulation.

**Dependency array options:**
- Empty array `[]` - Runs once after initial render
- With dependencies `[prop, state]` - Runs when dependencies change
- No array - Runs after every render

### useContext
```javascript
const contextValue = useContext(MyContext);
```

**Purpose:** Accesses values from React Context without prop drilling.

### useReducer
```javascript
const [state, dispatch] = useReducer(reducer, initialState, initFunction);
```

**Purpose:** Alternative to useState for complex state logic.

**When to use:**
- Complex state logic
- Multiple sub-values in state object
- State transitions depend on previous state

### useCallback
```javascript
const memoizedCallback = useCallback(
  () => {
    // Function logic
  },
  [dependencyArray]
);
```

**Purpose:** Memoizes callback functions to prevent unnecessary re-renders.

### useMemo
```javascript
const memoizedValue = useMemo(() => {
  // Expensive computation
  return computedValue;
}, [dependencyArray]);
```

**Purpose:** Memoizes expensive computations to optimize performance.

## Advanced React Hooks

### useRef
```javascript
const refContainer = useRef(initialValue);
```

**Purpose:** Accesses DOM elements or stores mutable values that don't trigger re-renders.

### useImperativeHandle
```javascript
useImperativeHandle(ref, () => ({
  // Methods and properties to expose
}), [dependencyArray]);
```

**Purpose:** Customizes instance value exposed to parent component via ref.

### useLayoutEffect
```javascript
useLayoutEffect(() => {
  // Synchronous side effect
}, [dependencyArray]);
```

**Purpose:** Similar to useEffect but fires synchronously after DOM mutations.

### useDebugValue
```javascript
useDebugValue(value, formatFunction);
```

**Purpose:** Displays custom labels for custom hooks in React DevTools.

## React 18+ New Hooks

### useId
```javascript
const id = useId();
```

**Purpose:** Generates unique IDs that are stable across server and client.

### useSyncExternalStore
```javascript
const state = useSyncExternalStore(
  subscribe,
  getSnapshot,
  getServerSnapshot
);
```

**Purpose:** Reads from external stores and updates when they change.

### useTransition
```javascript
const [isPending, startTransition] = useTransition();
```

**Purpose:** Allows updating state without blocking UI updates.

### useDeferredValue
```javascript
const deferredValue = useDeferredValue(value);
```

**Purpose:** Defers re-rendering of a value to avoid blocking UI updates.

## Component API

### React.memo
```javascript
const MyComponent = React.memo(Component, areEqual);
```

**Purpose:** Prevents re-rendering when props haven't changed.

### forwardRef
```javascript
const MyComponent = forwardRef((props, ref) => {
  return <div ref={ref}>...</div>;
});
```

**Purpose:** Passes refs to child components.

### React.lazy
```javascript
const Component = React.lazy(() => import('./Component'));
```

**Purpose:** Enables code splitting by lazy loading components.

### Suspense
```javascript
<Suspense fallback={<div>Loading...</div>}>
  <LazyComponent />
</Suspense>
```

**Purpose:** Specifies loading UI while components load.

## Context API

### createContext
```javascript
const MyContext = createContext(defaultValue);
```

**Purpose:** Creates a context object for sharing values between components.

### Context.Provider
```javascript
<MyContext.Provider value={value}>
  {children}
</MyContext.Provider>
```

**Purpose:** Provides context values to child components.

## Error Handling

### Error Boundary Pattern
```javascript
class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // Log error
  }

  render() {
    if (this.state.hasError) {
      return <div>Something went wrong.</div>;
    }

    return this.props.children;
  }
}
```

## React Testing

### React Testing Library API
```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';

// Rendering
render(<Component />);

// Queries
screen.getByText('text');
screen.getByRole('button');
screen.getByLabelText('label');

// Events
fireEvent.click(button);
fireEvent.change(input, { target: { value: 'text' } });

// Async helpers
await waitFor(() => expect(element).toBeInTheDocument());
```

## Performance Optimization

### React.PureComponent
```javascript
class MyComponent extends React.PureComponent {
  // Shallow comparison of props and state
}
```

### React.Suspense for data
```javascript
// With React Query or SWR
const Component = () => {
  const { data } = useQuery('key', fetcher);
  return <div>{data}</div>;
};

<Suspense fallback={<div>Loading...</div>}>
  <Component />
</Suspense>;
```

## Server Components (React Server Components)

### Server Component Example
```javascript
// Server component (runs only on server)
async function ServerComponent() {
  const data = await fetch('https://api.example.com/data').then(r => r.json());
  return <div>{data}</div>;
}

// Client component (runs on client)
'use client';
import { useState } from 'react';

function ClientComponent() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

## React Router API

### Basic Routing
```javascript
import { Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <div>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </div>
  );
}
```

### Route Parameters
```javascript
<Route path="/users/:id" element={<UserProfile />} />

// In component
import { useParams } from 'react-router-dom';
const { id } = useParams();
```

## State Management Libraries

### Redux Toolkit
```javascript
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async action
export const fetchUserById = createAsyncThunk(
  'users/fetchById',
  async (userId) => {
    const response = await fetch(`https://api.example.com/users/${userId}`);
    return response.json();
  }
);

// Slice
const userSlice = createSlice({
  name: 'users',
  initialState: { entities: [], loading: 'idle' },
  reducers: {
    // Synchronous reducers
  },
  extraReducers: (builder) => {
    builder.addCase(fetchUserById.fulfilled, (state, action) => {
      state.entities.push(action.payload);
    });
  }
});
```

### Zustand
```javascript
import { create } from 'zustand';

const useStore = create((set) => ({
  count: 1,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
}));
```

### React Query
```javascript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Query
const { data, isLoading, error } = useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers,
});

// Mutation
const mutation = useMutation({
  mutationFn: updateUser,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['users'] });
  },
});
```

## TypeScript React Patterns

### Component Props
```tsx
interface Props {
  name: string;
  age?: number;
  onClick: (event: React.MouseEvent) => void;
}

const Component: React.FC<Props> = ({ name, age, onClick }) => {
  return <div onClick={onClick}>{name} is {age} years old</div>;
};
```

### Generic Components
```tsx
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

function List<T>({ items, renderItem }: ListProps<T>) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={index}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}
```

## Performance Monitoring

### Profiler Component
```javascript
import { Profiler } from 'react';

function onRenderCallback(id, phase, actualDuration) {
  console.log({ id, phase, actualDuration });
}

<Profiler id="App" onRender={onRenderCallback}>
  <App />
</Profiler>
```

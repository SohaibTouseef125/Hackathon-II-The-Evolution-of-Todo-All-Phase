// Context Provider Component Template
import React, { createContext, useContext, useReducer } from 'react';

// Create contexts for different parts of the application
const AppContext = createContext();
const UserContext = createContext();
const ThemeContext = createContext();

// Reducer for complex state management
const appReducer = (state, action) => {
  switch (action.type) {
    case 'SET_USER':
      return {
        ...state,
        user: action.payload
      };
    case 'SET_THEME':
      return {
        ...state,
        theme: action.payload
      };
    case 'SET_LOADING':
      return {
        ...state,
        loading: action.payload
      };
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload
      };
    default:
      return state;
  }
};

// Initial state
const initialState = {
  user: null,
  theme: 'light',
  loading: false,
  error: null
};

// Provider component
const AppProvider = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  // Actions that can be dispatched
  const setUser = (user) => dispatch({ type: 'SET_USER', payload: user });
  const setTheme = (theme) => dispatch({ type: 'SET_THEME', payload: theme });
  const setLoading = (loading) => dispatch({ type: 'SET_LOADING', payload: loading });
  const setError = (error) => dispatch({ type: 'SET_ERROR', payload: error });

  const value = {
    ...state,
    setUser,
    setTheme,
    setLoading,
    setError
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

// Custom hooks to access context
const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};

const useUserContext = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUserContext must be used within a UserProvider');
  }
  return context;
};

const useThemeContext = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useThemeContext must be used within a ThemeProvider');
  }
  return context;
};

// Theme provider with default value
const ThemeProvider = ({ children, initialTheme = 'light' }) => {
  const [theme, setTheme] = React.useState(initialTheme);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  const value = { theme, toggleTheme, setTheme };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

// User provider example
const UserProvider = ({ children }) => {
  const [user, setUser] = React.useState(null);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    // Simulate fetching user data
    const fetchUser = async () => {
      try {
        setLoading(true);
        // Simulate API call
        const userData = { id: 1, name: 'John Doe', email: 'john@example.com' };
        setUser(userData);
      } catch (error) {
        console.error('Error fetching user:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  const value = { user, setUser, loading, setLoading };

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
};

// Combined provider wrapper
const CombinedProviders = ({ children }) => {
  return (
    <ThemeProvider>
      <UserProvider>
        <AppProvider>
          {children}
        </AppProvider>
      </UserProvider>
    </ThemeProvider>
  );
};

// Example usage in app
const AppWithProviders = ({ children }) => {
  return (
    <CombinedProviders>
      {children}
    </CombinedProviders>
  );
};

export {
  AppProvider,
  UserProvider,
  ThemeProvider,
  CombinedProviders,
  AppWithProviders,
  useAppContext,
  useUserContext,
  useThemeContext
};

// Example of using the context in a component
/*
const UserProfile = () => {
  const { user, loading } = useUserContext();
  const { theme, toggleTheme } = useThemeContext();

  if (loading) return <div>Loading...</div>;

  return (
    <div className={`profile ${theme}`}>
      <h2>Welcome, {user?.name}</h2>
      <button onClick={toggleTheme}>
        Switch to {theme === 'light' ? 'dark' : 'light'} mode
      </button>
    </div>
  );
};
*/
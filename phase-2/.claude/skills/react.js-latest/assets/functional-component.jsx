// Functional Component Template
import { useState, useEffect } from 'react';

const FunctionalComponent = ({ initialCount = 0 }) => {
  const [count, setCount] = useState(initialCount);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Component did mount logic
    console.log('Component mounted');

    // Cleanup function
    return () => {
      console.log('Component unmounted');
    };
  }, []);

  const handleIncrement = () => {
    setCount(count + 1);
  };

  const handleDecrement = () => {
    setCount(count - 1);
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="component-container">
      <h2>Functional Component</h2>
      <p>Count: {count}</p>
      <button onClick={handleIncrement}>Increment</button>
      <button onClick={handleDecrement}>Decrement</button>
    </div>
  );
};

export default FunctionalComponent;
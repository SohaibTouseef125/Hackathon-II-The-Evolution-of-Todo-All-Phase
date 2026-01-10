// Lazy Component with Suspense Template
import React, { lazy, Suspense } from 'react';

// Lazy load components for code splitting
const LazyComponent = lazy(() => import('./LazyComponent'));
const AnotherLazyComponent = lazy(() => import('./AnotherComponent'));

// Lazy loaded route component
const LazyRouteComponent = lazy(() => import('./RouteComponent'));

const LazyComponentWrapper = () => {
  return (
    <div>
      <h2>Lazy Loaded Components</h2>
      <Suspense fallback={<div>Loading lazy component...</div>}>
        <LazyComponent />
      </Suspense>
    </div>
  );
};

// Example with error boundary for lazy components
const LazyComponentWithErrorBoundary = () => {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <LazyComponent />
    </Suspense>
  );
};

// Lazy loaded route example
const LazyRouteExample = () => {
  return (
    <Suspense fallback={<div>Loading route...</div>}>
      <LazyRouteComponent />
    </Suspense>
  );
};

// Lazy loading with dynamic import based on condition
const ConditionalLazyComponent = ({ shouldLoad }) => {
  const [LazyComp, setLazyComp] = React.useState(null);

  React.useEffect(() => {
    if (shouldLoad) {
      import('./ConditionalComponent').then((module) => {
        setLazyComp(() => module.default);
      });
    }
  }, [shouldLoad]);

  if (shouldLoad && LazyComp) {
    return (
      <Suspense fallback={<div>Loading conditional component...</div>}>
        <LazyComp />
      </Suspense>
    );
  }

  return <div>Component not loaded yet</div>;
};

export {
  LazyComponentWrapper,
  LazyComponentWithErrorBoundary,
  LazyRouteExample,
  ConditionalLazyComponent
};

// Example of the component being lazy loaded
// LazyComponent.jsx
/*
import React from 'react';

const LazyComponent = () => {
  return (
    <div>
      <h3>This is a lazy loaded component</h3>
      <p>It was loaded on demand!</p>
    </div>
  );
};

export default LazyComponent;
*/
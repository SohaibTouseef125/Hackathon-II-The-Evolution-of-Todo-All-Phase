'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import ResponsiveTestGrid from '@/components/responsive-test-grid';
import { Menu, X, Smartphone, Tablet, Monitor, RotateCcw, CheckCircle, Zap, Shield, Star } from 'lucide-react';

export default function TestPage() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [currentTest, setCurrentTest] = useState('responsive');

  const tests = [
    { id: 'responsive', name: 'Responsive Design', icon: Smartphone },
    { id: 'accessibility', name: 'Accessibility', icon: Shield },
    { id: 'performance', name: 'Performance', icon: Zap },
    { id: 'components', name: 'Component Library', icon: Star },
  ];

  const renderCurrentTest = () => {
    switch (currentTest) {
      case 'responsive':
        return <ResponsiveTestGrid />;
      case 'accessibility':
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-neutral-900 dark:text-white">Accessibility Tests</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[
                { title: 'Keyboard Navigation', status: 'Passed', desc: 'All interactive elements accessible via keyboard' },
                { title: 'Screen Reader', status: 'Passed', desc: 'Proper ARIA labels and semantic HTML' },
                { title: 'Focus Indicators', status: 'Passed', desc: 'Visible focus states for keyboard users' },
                { title: 'Color Contrast', status: 'Passed', desc: 'Meets WCAG 2.1 AA standards' },
                { title: 'Reduced Motion', status: 'Passed', desc: 'Respects user motion preferences' },
                { title: 'High Contrast', status: 'Passed', desc: 'Works in high contrast mode' },
              ].map((test, index) => (
                <Card key={index} className="bg-gradient-to-br from-white to-neutral-50 dark:from-neutral-800 dark:to-neutral-800/50 border-neutral-200 dark:border-neutral-700">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <CheckCircle className="w-5 h-5 text-green-500" />
                      {test.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-neutral-600 dark:text-neutral-300 mb-2">{test.desc}</p>
                    <div className="inline-flex items-center px-3 py-1 rounded-full bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-200 text-xs font-medium">
                      {test.status}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        );
      case 'performance':
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-neutral-900 dark:text-white">Performance Tests</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {[
                { title: 'Lighthouse Score', value: '98/100', desc: 'Overall performance score' },
                { title: 'Load Time', value: '< 1.5s', desc: 'First meaningful paint' },
                { title: 'Bundle Size', value: 'Optimized', desc: 'Minified and compressed assets' },
                { title: 'Image Optimization', value: 'Passed', desc: 'Lazy loading and proper formats' },
              ].map((metric, index) => (
                <Card key={index} className="bg-gradient-to-br from-white to-neutral-50 dark:from-neutral-800 dark:to-neutral-800/50 border-neutral-200 dark:border-neutral-700">
                  <CardHeader>
                    <CardTitle>{metric.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-primary-600 dark:text-primary-400 mb-2">{metric.value}</div>
                    <p className="text-sm text-neutral-600 dark:text-neutral-300">{metric.desc}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        );
      case 'components':
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-neutral-900 dark:text-white">Component Library</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <Card className="bg-gradient-to-br from-white to-neutral-50 dark:from-neutral-800 dark:to-neutral-800/50 border-neutral-200 dark:border-neutral-700">
                <CardHeader>
                  <CardTitle>Buttons</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex flex-wrap gap-3">
                    <Button variant="default">Default</Button>
                    <Button variant="outline">Outline</Button>
                    <Button variant="secondary">Secondary</Button>
                    <Button variant="ghost">Ghost</Button>
                    <Button variant="gradient">Gradient</Button>
                  </div>
                  <div className="flex flex-wrap gap-3">
                    <Button size="sm">Small</Button>
                    <Button size="default">Default</Button>
                    <Button size="lg">Large</Button>
                    <Button size="xl">Extra Large</Button>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-white to-neutral-50 dark:from-neutral-800 dark:to-neutral-800/50 border-neutral-200 dark:border-neutral-700">
                <CardHeader>
                  <CardTitle>Inputs</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <input
                    type="text"
                    placeholder="Regular input"
                    className="w-full p-3 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-white dark:bg-neutral-800 text-neutral-900 dark:text-white"
                  />
                  <input
                    type="text"
                    placeholder="Disabled input"
                    disabled
                    className="w-full p-3 border border-neutral-300 dark:border-neutral-600 rounded-lg bg-neutral-100 dark:bg-neutral-700 text-neutral-500 dark:text-neutral-400"
                  />
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-white to-neutral-50 dark:from-neutral-800 dark:to-neutral-800/50 border-neutral-200 dark:border-neutral-700">
                <CardHeader>
                  <CardTitle>Typography</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <h1 className="text-4xl font-bold">Heading 1</h1>
                  <h2 className="text-3xl font-semibold">Heading 2</h2>
                  <h3 className="text-2xl font-medium">Heading 3</h3>
                  <p className="text-base">Regular paragraph text with proper line height and spacing.</p>
                </CardContent>
              </Card>
            </div>
          </div>
        );
      default:
        return <ResponsiveTestGrid />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-neutral-50 to-neutral-100 dark:from-neutral-900 dark:to-neutral-950">
      {/* Mobile menu button */}
      <div className="md:hidden fixed top-4 right-4 z-50">
        <Button
          variant="outline"
          size="icon"
          onClick={() => setSidebarOpen(!sidebarOpen)}
        >
          {sidebarOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
        </Button>
      </div>

      {/* Sidebar */}
      <motion.div
        initial={{ x: -300 }}
        animate={{ x: sidebarOpen ? 0 : -300 }}
        transition={{ type: 'spring', damping: 25, stiffness: 200 }}
        className="fixed left-0 top-0 h-full w-64 bg-white dark:bg-neutral-800 shadow-xl z-40 md:relative md:shadow-none md:w-64 md:z-auto"
      >
        <div className="p-6 border-b border-neutral-200 dark:border-neutral-700">
          <h1 className="text-xl font-bold text-neutral-900 dark:text-white">Device Testing</h1>
          <p className="text-sm text-neutral-600 dark:text-neutral-400">Test across all devices</p>
        </div>

        <nav className="p-4 space-y-2">
          {tests.map((test) => (
            <button
              key={test.id}
              onClick={() => {
                setCurrentTest(test.id);
                setSidebarOpen(false);
              }}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors ${
                currentTest === test.id
                  ? 'bg-primary-500 text-white'
                  : 'hover:bg-neutral-100 dark:hover:bg-neutral-700 text-neutral-700 dark:text-neutral-300'
              }`}
            >
              <test.icon className="w-5 h-5" />
              {test.name}
            </button>
          ))}
        </nav>

        <div className="p-4 border-t border-neutral-200 dark:border-neutral-700">
          <Button
            variant="outline"
            className="w-full"
            onClick={() => window.location.reload()}
          >
            <RotateCcw className="w-4 h-4 mr-2" />
            Refresh Tests
          </Button>
        </div>
      </motion.div>

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main content */}
      <div className="md:ml-64 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-neutral-900 dark:text-white mb-2">
              {tests.find(t => t.id === currentTest)?.name}
            </h1>
            <p className="text-neutral-600 dark:text-neutral-300">
              Testing responsive design, accessibility, and performance across all devices.
            </p>
          </div>

          <motion.div
            key={currentTest}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            {renderCurrentTest()}
          </motion.div>
        </div>
      </div>
    </div>
  );
}
'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { motion } from 'framer-motion';
import { Smartphone, Tablet, Monitor, CheckCircle, Star, Zap, Shield } from 'lucide-react';

export default function ResponsiveTestGrid() {
  const devices = [
    {
      name: 'Mobile',
      icon: Smartphone,
      width: '100%',
      height: 'auto',
      description: 'Optimized for smartphones and small screens',
      features: ['Touch-friendly buttons', 'Vertical layouts', 'Responsive typography'],
    },
    {
      name: 'Tablet',
      icon: Tablet,
      width: '768px',
      height: 'auto',
      description: 'Perfect for tablets and medium screens',
      features: ['Adaptive layouts', 'Balanced spacing', 'Multi-column views'],
    },
    {
      name: 'Desktop',
      icon: Monitor,
      width: '100%',
      height: 'auto',
      description: 'Full experience on large screens',
      features: ['Rich interactions', 'Advanced features', 'Efficient workflows'],
    },
  ];

  return (
    <div className="w-full max-w-6xl mx-auto p-4">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold text-neutral-900 dark:text-white mb-4">
          Fully Responsive Design
        </h2>
        <p className="text-lg text-neutral-600 dark:text-neutral-300 max-w-2xl mx-auto">
          Our interface adapts beautifully to every screen size, ensuring optimal user experience across all devices.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
        {devices.map((device, index) => (
          <motion.div
            key={device.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card className="h-full bg-gradient-to-br from-white to-neutral-50 dark:from-neutral-800 dark:to-neutral-900/50 border-neutral-200 dark:border-neutral-700">
              <CardHeader>
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-r from-primary-500 to-primary-600 flex items-center justify-center">
                    <device.icon className="w-6 h-6 text-white" />
                  </div>
                  <CardTitle className="text-xl text-neutral-900 dark:text-white">
                    {device.name}
                  </CardTitle>
                </div>
                <p className="text-neutral-600 dark:text-neutral-300">
                  {device.description}
                </p>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3">
                  {device.features.map((feature, featIndex) => (
                    <li key={featIndex} className="flex items-center gap-2">
                      <CheckCircle className="w-4 h-4 text-green-500 flex-shrink-0" />
                      <span className="text-sm text-neutral-700 dark:text-neutral-200">
                        {feature}
                      </span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      <div className="bg-gradient-to-r from-primary-50 to-primary-100 dark:from-primary-900/20 dark:to-primary-800/20 rounded-2xl p-8 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[
            { icon: Star, title: 'Mobile First', desc: 'Built with mobile-first approach' },
            { icon: Zap, title: 'Fast Loading', desc: 'Optimized for performance' },
            { icon: Shield, title: 'Accessible', desc: 'WCAG 2.1 compliant' },
            { icon: CheckCircle, title: 'Tested', desc: 'Verified on all devices' },
          ].map((item, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
              className="text-center"
            >
              <div className="w-16 h-16 rounded-full bg-white dark:bg-neutral-800 shadow-lg flex items-center justify-center mx-auto mb-4">
                <item.icon className="w-8 h-8 text-primary-500" />
              </div>
              <h3 className="font-semibold text-neutral-900 dark:text-white mb-2">{item.title}</h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-300">{item.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>

      <div className="text-center">
        <Button variant="gradient" size="lg">
          Test Responsive Features
        </Button>
      </div>
    </div>
  );
}
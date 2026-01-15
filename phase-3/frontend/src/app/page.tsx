'use client';

import { useState, useEffect } from 'react';
import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';
import { motion } from 'framer-motion';
import ScrollTrigger from '@/components/scroll-trigger';
import { Menu, X, CheckCircle, Calendar, BarChart3, User, Lock, Mail, ChevronRight, Star, ArrowRight, Play, Zap, Globe, Shield } from 'lucide-react';

export default function HomePage() {
  const router = useRouter();
  const { isAuthenticated, loading } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  // Redirect authenticated users to dashboard
  useEffect(() => {
    if (!loading && isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, loading, router]);

  // Handle scroll effect for navbar
  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleGetStarted = () => {
    router.push('/signup');
  };

  const handleLogin = () => {
    router.push('/login');
  };

  // Animation variants
  const fadeInUp = {
    initial: { opacity: 0, y: 60 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6, ease: 'easeOut' }
  };

  const staggerContainer = {
    animate: {
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const featureIcons = [
    { icon: CheckCircle, gradient: 'from-green-400 to-emerald-500' },
    { icon: Calendar, gradient: 'from-blue-400 to-cyan-500' },
    { icon: BarChart3, gradient: 'from-purple-400 to-pink-500' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-neutral-50 to-neutral-100 dark:from-neutral-900 dark:to-neutral-950 text-neutral-900 dark:text-neutral-100">
      {/* Navigation */}
      <motion.nav
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
          scrolled
            ? 'bg-white/90 dark:bg-neutral-900/90 backdrop-blur-xl border-b border-neutral-200 dark:border-neutral-800 shadow-lg'
            : 'bg-transparent backdrop-blur-none'
        }`}
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Link href="/" className="flex items-center space-x-2 group">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-r from-primary-500 to-primary-600 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                  <CheckCircle className="w-6 h-6 text-white" />
                </div>
                <span className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-primary-600 bg-clip-text text-transparent">
                  TaskFlow
                </span>
              </Link>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-8">
              <Link href="/#features" className="text-neutral-600 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 px-3 py-2 rounded-md text-sm font-medium transition-all duration-300 relative group">
                Features
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-primary-500 group-hover:w-full transition-all duration-300"></span>
              </Link>
              <Link href="/#how-it-works" className="text-neutral-600 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 px-3 py-2 rounded-md text-sm font-medium transition-all duration-300 relative group">
                How It Works
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-primary-500 group-hover:w-full transition-all duration-300"></span>
              </Link>
              <Link href="/#testimonials" className="text-neutral-600 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 px-3 py-2 rounded-md text-sm font-medium transition-all duration-300 relative group">
                Testimonials
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-primary-500 group-hover:w-full transition-all duration-300"></span>
              </Link>
              <button
                onClick={handleLogin}
                className="text-neutral-600 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 px-3 py-2 rounded-md text-sm font-medium transition-all duration-300 relative group"
              >
                Login
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-primary-500 group-hover:w-full transition-all duration-300"></span>
              </button>
              <button
                onClick={handleGetStarted}
                className="bg-gradient-to-r from-primary-500 to-primary-600 text-white px-6 py-2.5 rounded-lg text-sm font-medium hover:from-primary-600 hover:to-primary-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
              >
                Get Started
              </button>
            </div>

            {/* Mobile menu button */}
            <div className="md:hidden">
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="inline-flex items-center justify-center p-2 rounded-md text-neutral-600 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-neutral-100 dark:hover:bg-neutral-800 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
              >
                {isMenuOpen ? (
                  <X className="h-6 w-6" />
                ) : (
                  <Menu className="h-6 w-6" />
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <motion.div
            className="md:hidden"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white dark:bg-neutral-800 border-t border-neutral-200 dark:border-neutral-700">
              <Link href="/#features" className="block text-neutral-600 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 px-3 py-2 rounded-md text-base font-medium transition-colors">
                Features
              </Link>
              <Link href="/#how-it-works" className="block text-neutral-600 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 px-3 py-2 rounded-md text-base font-medium transition-colors">
                How It Works
              </Link>
              <Link href="/#testimonials" className="block text-neutral-600 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 px-3 py-2 rounded-md text-base font-medium transition-colors">
                Testimonials
              </Link>
              <button
                onClick={handleLogin}
                className="block text-neutral-600 dark:text-neutral-300 hover:text-primary-600 dark:hover:text-primary-400 px-3 py-2 rounded-md text-base font-medium w-full text-left transition-colors"
              >
                Login
              </button>
              <button
                onClick={handleGetStarted}
                className="w-full bg-gradient-to-r from-primary-500 to-primary-600 text-white px-3 py-2.5 rounded-md text-base font-medium hover:from-primary-600 hover:to-primary-700 transition-all duration-300"
              >
                Get Started
              </button>
            </div>
          </motion.div>
        )}
      </motion.nav>

      {/* Hero Section */}
      <motion.section
        className="relative min-h-screen flex items-center justify-center overflow-hidden pt-16"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
      >
        <div className="absolute inset-0 bg-pattern-light dark:bg-pattern-dark"></div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 relative z-10">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-center lg:text-left"
            >
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.3 }}
                className="inline-flex items-center px-4 py-2 rounded-full bg-primary-50 dark:bg-primary-950/30 text-primary-700 dark:text-primary-300 text-sm font-medium mb-6"
              >
                <Zap className="w-4 h-4 mr-2" />
                AI-Powered Task Management
              </motion.div>

              <motion.h1
                {...fadeInUp}
                transition={{ delay: 0.4 }}
                className="text-4xl sm:text-5xl lg:text-6xl font-bold leading-tight mb-6"
              >
                Streamline Your Tasks,{' '}
                <span className="bg-gradient-to-r from-primary-600 to-primary-600 bg-clip-text text-transparent">
                  Boost Productivity
                </span>
              </motion.h1>

              <motion.p
                {...fadeInUp}
                transition={{ delay: 0.5 }}
                className="text-xl text-neutral-600 dark:text-neutral-300 mb-8 max-w-2xl"
              >
                The ultimate AI-powered task management solution designed to help you organize, prioritize, and accomplish more with less stress. Experience seamless workflow automation.
              </motion.p>

              <motion.div
                {...fadeInUp}
                transition={{ delay: 0.6 }}
                className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start"
              >
                <button
                  onClick={handleGetStarted}
                  className="group relative bg-gradient-to-r from-primary-500 to-primary-600 text-white px-8 py-4 rounded-xl text-lg font-semibold hover:from-primary-600 hover:to-primary-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1 inline-flex items-center justify-center"
                >
                  Get Started Free
                  <ArrowRight className="ml-2 w-5 h-5 transition-transform group-hover:translate-x-1" />
                </button>
                <button
                  onClick={handleLogin}
                  className="border-2 border-neutral-300 dark:border-neutral-700 text-neutral-700 dark:text-neutral-200 px-8 py-4 rounded-xl text-lg font-semibold hover:bg-neutral-50 dark:hover:bg-neutral-800 transition-all duration-300 flex items-center justify-center"
                >
                  Sign In
                  <Play className="ml-2 w-4 h-4" />
                </button>
              </motion.div>

              <motion.div
                {...fadeInUp}
                transition={{ delay: 0.7 }}
                className="mt-8 flex flex-wrap justify-center lg:justify-start items-center gap-6 text-sm text-neutral-500 dark:text-neutral-400"
              >
                <div className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  Free Forever
                </div>
                <div className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  No Credit Card
                </div>
                <div className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  24/7 Support
                </div>
              </motion.div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="relative"
            >
              <div className="relative bg-gradient-to-br from-white/80 to-neutral-100/80 dark:from-neutral-800/80 dark:to-neutral-900/80 backdrop-blur-xl rounded-3xl p-8 shadow-2xl border border-neutral-200/50 dark:border-neutral-700/50">
                <div className="absolute -top-4 -right-4 w-24 h-24 bg-gradient-to-r from-primary-400 to-primary-500 rounded-full opacity-20 blur-xl"></div>
                <div className="absolute -bottom-4 -left-4 w-32 h-32 bg-gradient-to-r from-secondary-400 to-secondary-500 rounded-full opacity-20 blur-xl"></div>

                <div className="relative z-10">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-lg font-semibold">Today's Tasks</h3>
                    <div className="flex space-x-2">
                      <div className="w-3 h-3 bg-red-400 rounded-full"></div>
                      <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
                      <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                    </div>
                  </div>

                  <div className="space-y-4">
                    {[
                      { title: 'Complete project proposal', completed: false, priority: 'high' },
                      { title: 'Team meeting prep', completed: true, priority: 'medium' },
                      { title: 'Research new features', completed: false, priority: 'low' },
                      { title: 'Update documentation', completed: false, priority: 'medium' }
                    ].map((task, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.1 * index }}
                        className={`flex items-center p-4 rounded-xl border ${
                          task.completed
                            ? 'bg-green-50 dark:bg-green-950/20 border-green-200 dark:border-green-800'
                            : 'bg-white dark:bg-neutral-700 border-neutral-200 dark:border-neutral-600 hover:shadow-md transition-shadow'
                        }`}
                      >
                        <input

                          type="checkbox"
                          checked={task.completed}
                          readOnly
                          className="w-5 h-5 text-primary-600 rounded focus:ring-primary-500 border-neutral-300 dark:border-neutral-600"
                        />
                        <span className={`ml-3 ${task.completed ? 'line-through text-neutral-500 dark:text-neutral-400' : 'text-neutral-700 dark:text-neutral-200'}`}>
                          {task.title}
                        </span>
                        <span className={`ml-auto text-xs px-2 py-1 rounded-full ${
                          task.priority === 'high' ? 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300' :
                          task.priority === 'medium' ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300' :
                          'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300'
                        }`}>
                          {task.priority}
                        </span>
                      </motion.div>
                    ))}
                  </div>

                  <div className="mt-6 flex space-x-3">
                    <button className="flex-1 bg-primary-500 text-white py-3 rounded-lg font-medium hover:bg-primary-600 transition-colors">
                      Add Task
                    </button>
                    <button className="px-4 py-3 rounded-lg border border-neutral-300 dark:border-neutral-600 hover:bg-neutral-50 dark:hover:bg-neutral-800 transition-colors">
                      <ChevronRight className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </motion.section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white dark:bg-neutral-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <ScrollTrigger
            offset={100}
            once={true}
            variants={{
              hidden: { opacity: 0, y: 30 },
              visible: { opacity: 1, y: 0, transition: { duration: 0.6 } }
            }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-neutral-900 dark:text-white mb-4">
              Powerful Features for Maximum Productivity
            </h2>
            <p className="text-xl text-neutral-600 dark:text-neutral-300 max-w-2xl mx-auto">
              Everything you need to manage your tasks efficiently and achieve your goals.
            </p>
          </ScrollTrigger>

          <ScrollTrigger
            offset={100}
            once={true}
            variants={{
              hidden: { opacity: 0 },
              visible: {
                opacity: 1,
                transition: {
                  staggerChildren: 0.2,
                  delayChildren: 0.1
                }
              }
            }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8"
          >
            {[
              {
                title: 'AI-Powered Organization',
                description: 'Intelligent task prioritization and smart categorization powered by advanced algorithms.',
                iconIndex: 0
              },
              {
                title: 'Real-time Collaboration',
                description: 'Work together seamlessly with team members in real-time with instant updates and notifications.',
                iconIndex: 1
              },
              {
                title: 'Advanced Analytics',
                description: 'Detailed insights and productivity reports to help you optimize your workflow.',
                iconIndex: 2
              }
            ].map((feature, index) => (
              <ScrollTrigger
                key={index}
                offset={100}
                once={true}
                variants={{
                  hidden: { opacity: 0, y: 20 },
                  visible: { opacity: 1, y: 0, transition: { duration: 0.5, delay: index * 0.1 } }
                }}
                className="group relative bg-gradient-to-br from-white to-neutral-50 dark:from-neutral-800 dark:to-neutral-800/50 p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 border border-neutral-200 dark:border-neutral-700 hover:-translate-y-2"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-primary-500/5 to-secondary-500/5 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                <div className="relative z-10">
                  <div className={`w-16 h-16 rounded-2xl bg-gradient-to-r ${feature.iconIndex === 0 ? 'from-green-400 to-emerald-500' : feature.iconIndex === 1 ? 'from-blue-400 to-cyan-500' : 'from-purple-400 to-pink-500'} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                    {React.createElement(featureIcons[feature.iconIndex].icon, { className: 'w-8 h-8 text-white' })}
                  </div>
                  <h3 className="text-xl font-semibold text-neutral-900 dark:text-white mb-3">{feature.title}</h3>
                  <p className="text-neutral-600 dark:text-neutral-300">{feature.description}</p>
                </div>
              </ScrollTrigger>
            ))}
          </ScrollTrigger>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 bg-gradient-to-br from-neutral-50 to-neutral-100 dark:from-neutral-900 dark:to-neutral-950">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <ScrollTrigger
            offset={100}
            once={true}
            variants={{
              hidden: { opacity: 0, y: 30 },
              visible: { opacity: 1, y: 0, transition: { duration: 0.6 } }
            }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-neutral-900 dark:text-white mb-4">
              How TaskFlow Works
            </h2>
            <p className="text-xl text-neutral-600 dark:text-neutral-300 max-w-2xl mx-auto">
              Get started in just a few simple steps and transform your productivity.
            </p>
          </ScrollTrigger>

          <ScrollTrigger
            offset={100}
            once={true}
            variants={{
              hidden: { opacity: 0 },
              visible: {
                opacity: 1,
                transition: {
                  staggerChildren: 0.2,
                  delayChildren: 0.1
                }
              }
            }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8"
          >
            {[
              {
                step: 1,
                title: 'Sign Up',
                description: 'Create your free account in seconds and customize your workspace.'
              },
              {
                step: 2,
                title: 'Add Tasks',
                description: 'Create and organize your tasks with AI-powered suggestions and smart templates.'
              },
              {
                step: 3,
                title: 'Achieve Goals',
                description: 'Track progress, collaborate with teams, and accomplish more than ever before.'
              }
            ].map((step, index) => (
              <ScrollTrigger
                key={index}
                offset={100}
                once={true}
                variants={{
                  hidden: { opacity: 0, y: 20 },
                  visible: { opacity: 1, y: 0, transition: { duration: 0.5, delay: index * 0.1 } }
                }}
                className="text-center group"
              >
                <div className={`w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-r ${
                  step.step === 1 ? 'from-green-400 to-emerald-500' :
                  step.step === 2 ? 'from-blue-400 to-cyan-500' :
                  'from-purple-400 to-pink-500'
                } flex items-center justify-center text-white text-2xl font-bold group-hover:scale-110 transition-transform duration-300`}>
                  {step.step}
                </div>
                <h3 className="text-xl font-semibold text-neutral-900 dark:text-white mb-3">{step.title}</h3>
                <p className="text-neutral-600 dark:text-neutral-300">{step.description}</p>
              </ScrollTrigger>
            ))}
          </ScrollTrigger>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="py-20 bg-white dark:bg-neutral-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <ScrollTrigger
            offset={100}
            once={true}
            variants={{
              hidden: { opacity: 0, y: 30 },
              visible: { opacity: 1, y: 0, transition: { duration: 0.6 } }
            }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-neutral-900 dark:text-white mb-4">
              Loved by Thousands of Users
            </h2>
            <p className="text-xl text-neutral-600 dark:text-neutral-300 max-w-2xl mx-auto">
              Join our community of satisfied customers who have transformed their productivity.
            </p>
          </ScrollTrigger>

          <ScrollTrigger
            offset={100}
            once={true}
            variants={{
              hidden: { opacity: 0 },
              visible: {
                opacity: 1,
                transition: {
                  staggerChildren: 0.2,
                  delayChildren: 0.1
                }
              }
            }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8"
          >
            {[
              {
                quote: 'TaskFlow has completely revolutionized how our team manages projects. The AI features save us hours every week.',
                author: 'Sarah Johnson',
                role: 'Product Manager'
              },
              {
                quote: 'I love how intuitive and beautiful the interface is. It makes managing my personal tasks so enjoyable.',
                author: 'Mike Chen',
                role: 'Freelancer'
              },
              {
                quote: 'The analytics helped me identify my most productive hours and optimize my workflow significantly.',
                author: 'Emma Davis',
                role: 'CEO, Tech Startup'
              }
            ].map((testimonial, index) => (
              <ScrollTrigger
                key={index}
                offset={100}
                once={true}
                variants={{
                  hidden: { opacity: 0, y: 20 },
                  visible: { opacity: 1, y: 0, transition: { duration: 0.5, delay: index * 0.1 } }
                }}
                className="bg-gradient-to-br from-white to-neutral-50 dark:from-neutral-800 dark:to-neutral-800/50 p-8 rounded-2xl shadow-lg border border-neutral-200 dark:border-neutral-700"
              >
                <div className="flex mb-4">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                <p className="text-neutral-600 dark:text-neutral-300 mb-6 italic">"{testimonial.quote}"</p>
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-gradient-to-r from-primary-500 to-primary-600 rounded-full flex items-center justify-center text-white font-bold text-sm">
                    {testimonial.author.split(' ').map(n => n[0]).join('')}
                  </div>
                  <div className="ml-4">
                    <div className="font-semibold text-neutral-900 dark:text-white">{testimonial.author}</div>
                    <div className="text-neutral-500 dark:text-neutral-400 text-sm">{testimonial.role}</div>
                  </div>
                </div>
              </ScrollTrigger>
            ))}
          </ScrollTrigger>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-primary-500 to-primary-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <ScrollTrigger
            offset={100}
            once={true}
            variants={{
              hidden: { opacity: 0, y: 30 },
              visible: {
                opacity: 1,
                y: 0,
                transition: {
                  duration: 0.6,
                  ease: "easeOut"
                }
              }
            }}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
              Ready to Transform Your Productivity?
            </h2>
            <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
              Join thousands of users who have already transformed their workflow with TaskFlow.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={handleGetStarted}
                className="bg-white text-primary-600 px-8 py-4 rounded-xl text-lg font-semibold hover:bg-neutral-50 transition-all duration-300 transform hover:-translate-y-1 shadow-lg hover:shadow-xl"
              >
                Start Free Trial
              </button>
              <button
                onClick={handleLogin}
                className="border-2 border-white text-white px-8 py-4 rounded-xl text-lg font-semibold hover:bg-white hover:text-primary-600 transition-all duration-300"
              >
                Sign In
              </button>
            </div>
          </ScrollTrigger>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-neutral-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <ScrollTrigger
            offset={100}
            once={true}
            variants={{
              hidden: { opacity: 0 },
              visible: {
                opacity: 1,
                transition: {
                  staggerChildren: 0.1,
                  delayChildren: 0.1
                }
              }
            }}
            className="grid grid-cols-1 md:grid-cols-4 gap-8"
          >
            <ScrollTrigger
              offset={100}
              once={true}
              variants={{
                hidden: { opacity: 0, y: 20 },
                visible: { opacity: 1, y: 0, transition: { duration: 0.5, delay: 0.1 } }
              }}
            >
              <div>
                <div className="flex items-center space-x-2 mb-6">
                  <div className="w-8 h-8 rounded-lg bg-gradient-to-r from-primary-500 to-primary-600 flex items-center justify-center">
                    <CheckCircle className="w-5 h-5 text-white" />
                  </div>
                  <span className="text-xl font-bold">TaskFlow</span>
                </div>
                <p className="text-neutral-400 mb-6">
                  The ultimate AI-powered task management solution for individuals and teams.
                </p>
                <div className="flex space-x-4">
                  <a href="#" className="text-neutral-400 hover:text-white transition-colors">
                    <Globe className="w-5 h-5" />
                  </a>
                  <a href="#" className="text-neutral-400 hover:text-white transition-colors">
                    <Shield className="w-5 h-5" />
                  </a>
                </div>
              </div>
            </ScrollTrigger>

            <ScrollTrigger
              offset={100}
              once={true}
              variants={{
                hidden: { opacity: 0, y: 20 },
                visible: { opacity: 1, y: 0, transition: { duration: 0.5, delay: 0.2 } }
              }}
            >
              <div>
                <h4 className="text-lg font-semibold mb-6">Product</h4>
                <ul className="space-y-3">
                  <li><Link href="/#features" className="text-neutral-400 hover:text-white transition-colors">Features</Link></li>
                  <li><Link href="/pricing" className="text-neutral-400 hover:text-white transition-colors">Pricing</Link></li>
                  <li><Link href="/#how-it-works" className="text-neutral-400 hover:text-white transition-colors">How It Works</Link></li>
                  <li><Link href="/integrations" className="text-neutral-400 hover:text-white transition-colors">Integrations</Link></li>
                </ul>
              </div>
            </ScrollTrigger>

            <ScrollTrigger
              offset={100}
              once={true}
              variants={{
                hidden: { opacity: 0, y: 20 },
                visible: { opacity: 1, y: 0, transition: { duration: 0.5, delay: 0.3 } }
              }}
            >
              <div>
                <h4 className="text-lg font-semibold mb-6">Company</h4>
                <ul className="space-y-3">
                  <li><Link href="/about" className="text-neutral-400 hover:text-white transition-colors">About</Link></li>
                  <li><Link href="/contact" className="text-neutral-400 hover:text-white transition-colors">Contact</Link></li>
                  <li><Link href="/blog" className="text-neutral-400 hover:text-white transition-colors">Blog</Link></li>
                  <li><Link href="/careers" className="text-neutral-400 hover:text-white transition-colors">Careers</Link></li>
                </ul>
              </div>
            </ScrollTrigger>

            <ScrollTrigger
              offset={100}
              once={true}
              variants={{
                hidden: { opacity: 0, y: 20 },
                visible: { opacity: 1, y: 0, transition: { duration: 0.5, delay: 0.4 } }
              }}
            >
              <div>
                <h4 className="text-lg font-semibold mb-6">Legal</h4>
                <ul className="space-y-3">
                  <li><Link href="/privacy" className="text-neutral-400 hover:text-white transition-colors">Privacy</Link></li>
                  <li><Link href="/terms" className="text-neutral-400 hover:text-white transition-colors">Terms</Link></li>
                  <li><Link href="/security" className="text-neutral-400 hover:text-white transition-colors">Security</Link></li>
                  <li><Link href="/cookies" className="text-neutral-400 hover:text-white transition-colors">Cookies</Link></li>
                </ul>
              </div>
            </ScrollTrigger>
          </ScrollTrigger>

          <ScrollTrigger
            offset={100}
            once={true}
            variants={{
              hidden: { opacity: 0, y: 20 },
              visible: { opacity: 1, y: 0, transition: { duration: 0.5, delay: 0.5 } }
            }}
            className="border-t border-neutral-800 mt-12 pt-8 text-center text-neutral-400"
          >
            <p>&copy; 2026 TaskFlow. All rights reserved.</p>
          </ScrollTrigger>
        </div>
      </footer>
    </div>
  );
}
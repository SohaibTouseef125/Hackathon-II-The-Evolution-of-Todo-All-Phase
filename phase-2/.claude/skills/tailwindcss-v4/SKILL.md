---
name: tailwindcss-v4
description: Comprehensive Tailwind CSS v4 development with utility-first styling, responsive design, dark mode, custom components, and modern styling techniques. Use when Claude needs to work with Tailwind CSS v4 projects for creating responsive web interfaces, implementing design systems, customizing themes, optimizing performance, or following best practices for utility-first styling.
---

# Tailwind CSS v4

## Overview

This skill enables Claude to work effectively with Tailwind CSS v4 for creating responsive, accessible, and maintainable web interfaces. It covers the latest features in Tailwind CSS v4, utility-first styling principles, responsive design patterns, dark mode implementation, custom component creation, performance optimization, and integration with modern frameworks like React, Vue, and Next.js.

## Core Capabilities

### 1. Tailwind CSS v4 Fundamentals

**Utility-First Approach:**
- Understanding the utility-first philosophy and its benefits
- Mastering the core utility classes and their naming conventions
- Building complex UIs using composable utility classes
- Avoiding common anti-patterns in utility-first styling

**Configuration & Setup:**
- Setting up `tailwind.config.js` for v4 with proper configuration
- Understanding the new v4 features and changes from v3
- Configuring themes, breakpoints, and custom properties
- Setting up PostCSS and build tools for optimal performance

### 2. Responsive Design & Breakpoints

**Responsive Utilities:**
- Using responsive prefixes (sm:, md:, lg:, xl:, 2xl:)
- Implementing mobile-first and desktop-first approaches
- Creating fluid, adaptive layouts with modern CSS
- Understanding container queries and their usage with Tailwind

**Breakpoint Management:**
- Customizing default breakpoints in configuration
- Creating custom breakpoints for specific needs
- Using arbitrary values for precise control
- Managing responsive behavior across different screen sizes

### 3. Dark Mode & Color Schemes

**Dark Mode Implementation:**
- Setting up dark mode using class and media strategies
- Creating accessible color palettes for both light and dark modes
- Managing state for dark mode toggle functionality
- Using `dark:` variant for dark mode styling

**Color System:**
- Understanding Tailwind's color palette system
- Creating custom color scales and gradients
- Ensuring proper color contrast for accessibility
- Using dynamic color systems with CSS variables

### 4. Custom Components & Reusability

**Component Creation:**
- Building reusable component classes with `@apply`
- Creating component libraries using Tailwind utilities
- Managing component-specific styles and variants
- Using arbitrary values for one-off styling needs

**Plugin System:**
- Creating custom plugins for project-specific utilities
- Extending Tailwind with custom functionality
- Using community plugins effectively
- Managing plugin compatibility with v4

### 5. Performance & Optimization

**Build Optimization:**
- Purge configuration for production builds
- Tree-shaking unused utilities
- Optimizing for critical CSS
- Managing CSS bundle size effectively

**Performance Patterns:**
- Using the JIT compiler for dynamic class generation
- Optimizing for CSS-in-JS integration
- Managing complex layouts efficiently
- Avoiding performance bottlenecks in large projects

## Tailwind CSS v4 Specific Features

### 1. New Features in v4

**CSS Nesting Support:**
- Leveraging native CSS nesting with Tailwind
- Understanding how nesting affects utility generation
- Best practices for combining nesting with utility classes
- Migration patterns from v3 to v4

**Improved JIT Compiler:**
- Enhanced arbitrary value support
- Better performance and caching mechanisms
- New arbitrary variants and features
- Optimized build times and output

**Enhanced Custom Properties:**
- Better CSS variable integration
- Dynamic theme switching capabilities
- Improved custom property handling
- Advanced theming techniques

### 2. Migration from v3 to v4

**Breaking Changes:**
- Understanding deprecated features and alternatives
- Updating configuration files for v4 compatibility
- Migrating custom plugins and utilities
- Handling changed class names and behaviors

**Upgrade Strategies:**
- Step-by-step migration approach
- Testing strategies for migration validation
- Maintaining backward compatibility during transition
- Performance considerations during migration

## Design System Implementation

### 1. Theme Configuration

**Customizing Themes:**
- Extending default theme with project-specific values
- Creating design tokens for consistent styling
- Managing theme variants and states
- Using theme functions and callbacks

**Theme Best Practices:**
- Organizing theme configuration for maintainability
- Creating scalable spacing and typography systems
- Managing component-specific theme extensions
- Documenting theme decisions and usage

### 2. Component Libraries

**Building Component Systems:**
- Creating consistent component APIs
- Managing component variants and states
- Using composition patterns with Tailwind
- Ensuring accessibility in component design

**Reusable Patterns:**
- Button, form, and navigation component patterns
- Card, modal, and layout component templates
- Animation and transition utility patterns
- Responsive component design patterns

## Integration Patterns

### 1. Framework Integration

**React Integration:**
- Using Tailwind with React component patterns
- Managing dynamic class names and conditional styling
- Creating reusable React components with Tailwind
- Performance optimization in React/Tailwind projects

**Vue Integration:**
- Leveraging Vue's class binding with Tailwind
- Creating Vue component libraries with Tailwind
- Managing scoped styles with Tailwind utilities
- Using Vue directives with Tailwind classes

**Next.js Integration:**
- Setting up Tailwind in Next.js projects
- Optimizing for Next.js production builds
- Using CSS Modules alongside Tailwind
- Implementing Next.js-specific styling patterns

### 2. Third-Party Libraries

**UI Libraries:**
- Combining Headless UI, Radix UI with Tailwind
- Customizing library components with Tailwind
- Managing conflicts between libraries
- Creating cohesive design systems

**Animation Libraries:**
- Integrating Framer Motion, GSAP with Tailwind
- Combining utility classes with animation libraries
- Performance considerations for animations
- Creating smooth, accessible animations

## Accessibility & Best Practices

### 1. Accessibility Guidelines

**WCAG Compliance:**
- Ensuring proper color contrast ratios
- Managing focus states and keyboard navigation
- Using semantic HTML with Tailwind utilities
- Creating accessible forms and interactive elements

**Screen Reader Support:**
- Using ARIA attributes with Tailwind
- Managing landmark regions and navigation
- Creating accessible modal and dropdown patterns
- Testing accessibility with automated tools

### 2. Code Quality & Maintenance

**Code Organization:**
- Structuring Tailwind projects for maintainability
- Managing complex layouts and component hierarchies
- Using comments and documentation effectively
- Establishing team conventions for Tailwind usage

**Performance Monitoring:**
- Identifying and fixing CSS bloat
- Optimizing for critical rendering path
- Managing CSS specificity issues
- Using Tailwind's debugging utilities

## Common Patterns & Examples

### 1. Layout Patterns

**Grid Systems:**
```html
<!-- Responsive grid with different column counts -->
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
  <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">Item 1</div>
  <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">Item 2</div>
  <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">Item 3</div>
  <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">Item 4</div>
</div>
```

**Flexbox Layouts:**
```html
<!-- Centered card layout -->
<div class="flex min-h-screen items-center justify-center bg-gray-50 dark:bg-gray-900 p-4">
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 max-w-md w-full">
    <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Card Title</h2>
    <p class="text-gray-600 dark:text-gray-300">Card content goes here.</p>
  </div>
</div>
```

### 2. Component Patterns

**Button Component:**
```html
<!-- Primary button with hover, focus, and disabled states -->
<button class="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 focus:outline-none text-white font-medium rounded-lg transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
  Submit
</button>
```

**Card Component:**
```html
<!-- Responsive card with image and content -->
<article class="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
  <img class="w-full h-48 object-cover" src="image.jpg" alt="Card image">
  <div class="p-6">
    <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">Card Title</h3>
    <p class="text-gray-600 dark:text-gray-300 mb-4">Card description text.</p>
    <a href="#" class="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 font-medium">Read more</a>
  </div>
</article>
```

## Troubleshooting & Debugging

### 1. Common Issues

**Class Conflicts:**
- Understanding CSS specificity with Tailwind
- Resolving conflicting utility classes
- Using `!important` appropriately with Tailwind
- Managing third-party CSS conflicts

**Performance Issues:**
- Identifying CSS bloat and unused utilities
- Optimizing purge configuration
- Managing complex responsive designs
- Debugging slow build times

### 2. Debugging Tools

**Development Tools:**
- Using Tailwind's debug utilities
- Browser dev tools for Tailwind debugging
- VS Code extensions for Tailwind development
- Testing responsive designs across devices

## When to Use This Skill

Use this skill when working with:
- New Tailwind CSS v4 projects and configurations
- Migration from Tailwind v3 to v4
- Creating responsive, accessible web interfaces
- Building design systems and component libraries
- Performance optimization for Tailwind projects
- Integration with React, Vue, Next.js, or other frameworks
- Custom theme and plugin development
- Troubleshooting complex Tailwind implementations
- Accessibility compliance for Tailwind projects

## Resources

This skill includes comprehensive resources for Tailwind CSS v4 development:

### scripts/
Helper scripts for Tailwind development tasks:
- Configuration validation and setup
- Migration tools from v3 to v4
- Performance optimization utilities
- Component generation tools
- Theme management utilities

### references/
Detailed documentation and reference materials:
- Tailwind CSS v4 API reference
- Migration guide from v3 to v4
- Accessibility guidelines and patterns
- Performance optimization techniques
- Framework integration patterns

### assets/
Template files and boilerplate code:
- Tailwind configuration templates
- Component boilerplate files
- Project starter templates
- Design system examples
- Responsive layout templates

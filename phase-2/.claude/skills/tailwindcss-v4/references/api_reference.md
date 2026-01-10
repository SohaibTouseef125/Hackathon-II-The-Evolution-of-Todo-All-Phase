# Tailwind CSS v4 Complete Reference Guide

## Configuration Reference

### Tailwind Config File Options

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Custom colors
        brand: {
          50: '#eff6ff',
          500: '#3b82f6',
          900: '#1e3a8a',
        }
      },
      spacing: {
        // Custom spacing
        '18': '4.5rem',
        '88': '22rem',
      },
      fontFamily: {
        // Custom fonts
        sans: ['Inter', 'sans-serif'],
      },
      screens: {
        // Custom breakpoints
        '3xl': '1600px',
        '4xl': '2000px',
      },
    },
  },
  plugins: [
    // Custom plugins
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

### Core Configuration Options

**Important changes in v4:**
- CSS Nesting is now supported natively
- JIT compiler is enabled by default
- Improved arbitrary value support
- Enhanced CSS variable handling

## Utility Class Reference

### Layout Utilities

**Container & Box Alignment:**
- `container` - Max-width container with horizontal padding
- `box-border`, `box-content` - Box sizing options
- `block`, `inline-block`, `inline` - Display properties
- `flex`, `inline-flex` - Flexbox display
- `grid`, `inline-grid` - Grid display
- `table`, `inline-table` - Table display

**Flexbox & Grid:**
- `flex-row`, `flex-col` - Flex direction
- `flex-wrap`, `flex-nowrap` - Flex wrapping
- `items-start`, `items-center`, `items-end` - Align items
- `justify-start`, `justify-center`, `justify-end` - Justify content
- `gap-1`, `gap-2`, `gap-4` - Gap utilities
- `grid-cols-1`, `grid-cols-2`, etc. - Grid columns
- `grid-rows-1`, `grid-rows-2`, etc. - Grid rows

**Spacing:**
- `p-4`, `px-4`, `py-4` - Padding
- `m-4`, `mx-4`, `my-4` - Margin
- `space-x-4`, `space-y-4` - Space between children
- `divide-x`, `divide-y` - Divide between children

### Typography Utilities

**Font & Text:**
- `font-sans`, `font-serif`, `font-mono` - Font families
- `text-xs`, `text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl`, etc. - Font sizes
- `font-thin`, `font-normal`, `font-bold`, `font-extrabold` - Font weights
- `text-left`, `text-center`, `text-right`, `text-justify` - Text alignment
- `uppercase`, `lowercase`, `capitalize`, `normal-case` - Text case
- `italic`, `not-italic` - Font style
- `underline`, `line-through`, `no-underline` - Text decoration
- `antialiased`, `subpixel-antialiased` - Font smoothing

**Leading & Tracking:**
- `leading-4`, `leading-5`, `leading-6`, etc. - Line height
- `tracking-tight`, `tracking-normal`, `tracking-wide` - Letter spacing

### Background & Borders

**Backgrounds:**
- `bg-white`, `bg-blue-500`, etc. - Background colors
- `bg-gradient-to-r`, `bg-gradient-to-l`, etc. - Gradient direction
- `bg-gradient-to-tr`, `bg-gradient-to-br`, etc. - Diagonal gradients
- `bg-cover`, `bg-contain`, `bg-auto` - Background size
- `bg-center`, `bg-top`, `bg-bottom`, etc. - Background position

**Borders:**
- `border`, `border-2`, `border-4` - Border width
- `border-t`, `border-r`, `border-b`, `border-l` - Side borders
- `border-blue-500`, `border-red-500`, etc. - Border colors
- `rounded`, `rounded-md`, `rounded-lg`, `rounded-full` - Border radius
- `divide-x`, `divide-y` - Divider between elements

### Effects & Transitions

**Shadows & Transparency:**
- `shadow-sm`, `shadow`, `shadow-md`, `shadow-lg`, `shadow-xl`, `shadow-2xl` - Shadows
- `shadow-inner`, `shadow-none` - Special shadow types
- `opacity-0`, `opacity-25`, `opacity-50`, etc. - Opacity
- `bg-opacity-25`, `bg-opacity-50`, etc. - Background opacity

**Transitions & Animation:**
- `transition`, `transition-all`, `transition-colors` - Transition properties
- `duration-100`, `duration-300`, `duration-500` - Transition duration
- `ease-linear`, `ease-in`, `ease-out`, `ease-in-out` - Transition timing
- `animate-spin`, `animate-ping`, `animate-pulse` - Built-in animations

## Responsive Design Reference

### Breakpoint Prefixes

- `sm:` - (640px and up)
- `md:` - (768px and up)
- `lg:` - (1024px and up)
- `xl:` - (1280px and up)
- `2xl:` - (1536px and up)

**Example:**
```html
<div class="text-base sm:text-lg md:text-xl lg:text-2xl xl:text-3xl">
  Responsive text that grows with screen size
</div>
```

### Container Queries (New in v4)

- `@container` - Container query support
- `@container (min-width: 400px)` - Custom container queries

## Dark Mode Reference

### Dark Mode Strategies

**Class Strategy (Default):**
```html
<html class="dark">
  <div class="bg-white dark:bg-gray-800">Content</div>
</html>
```

**Media Strategy:**
```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'media', // Use media query instead of class
}
```

**Example:**
```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  This adapts to dark mode
</div>
```

## Arbitrary Values Reference

### Using Arbitrary Values

**Syntax:**
- `w-[200px]` - Fixed width
- `h-[50vh]` - Viewport height
- `text-[2.5rem]` - Custom font size
- `bg-[#ff0000]` - Custom hex color
- `rotate-[30deg]` - Custom rotation

**Examples:**
```html
<!-- Custom sizes -->
<div class="w-[300px] h-[200px]">Fixed size box</div>

<!-- Custom colors -->
<div class="bg-[#123456] text-[rgba(255,255,255,0.8)]">Custom colors</div>

<!-- Custom spacing -->
<div class="p-[2.5rem] m-[calc(100vh-4rem)]">Custom spacing</div>
```

## Plugin Development Reference

### Creating Custom Plugins

```javascript
// tailwind.config.js
const plugin = require('tailwindcss/plugin')

module.exports = {
  plugins: [
    plugin(function({ addUtilities, addComponents, e, theme }) {
      // Add custom utilities
      addUtilities({
        '.skew-10deg': {
          transform: 'skewY(-10deg)',
        },
        '.skew-20deg': {
          transform: 'skewY(-20deg)',
        },
      })

      // Add custom components
      addComponents({
        '.btn': {
          padding: '.5rem 1rem',
          borderRadius: '.25rem',
          fontWeight: '600',
        }
      })
    })
  ]
}
```

## Performance Optimization Reference

### Purge Configuration

```javascript
// tailwind.config.js
module.exports = {
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
    './public/**/*.html',
  ],
  safelist: [
    // Keep these classes even if they appear to be unused
    'bg-red-500',
    'text-white',
  ],
  blocklist: [
    // Remove these classes from production build
    'bg-black',
  ]
}
```

### Build Performance Tips

1. **Optimize Content Paths:**
   - Use specific paths instead of broad glob patterns
   - Exclude node_modules and build directories

2. **Use JIT Mode:**
   - JIT compiler is faster and more efficient
   - Only generates used classes

3. **Configure Safelist:**
   - Add dynamically generated class names to safelist
   - Prevents them from being purged

## Migration Guide: v3 to v4

### Breaking Changes

1. **CSS Nesting Support:**
   - Native CSS nesting is now supported
   - May affect how styles are processed

2. **Plugin API Changes:**
   - Some plugin APIs may have changed
   - Review custom plugins for compatibility

3. **Configuration Changes:**
   - Check for deprecated configuration options
   - Update custom configuration accordingly

### Migration Steps

1. **Update Dependencies:**
   ```bash
   npm install -D tailwindcss@latest
   ```

2. **Update Configuration:**
   - Review tailwind.config.js for compatibility
   - Update any deprecated options

3. **Test Components:**
   - Verify existing components render correctly
   - Update any that rely on removed features

## Common Patterns & Recipes

### Responsive Design Patterns

**Mobile-First Grid:**
```html
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
  <!-- Grid items -->
</div>
```

**Card with Hover Effect:**
```html
<div class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
  <div class="p-6">
    <h3 class="text-lg font-medium text-gray-900">Card Title</h3>
    <p class="mt-2 text-gray-600">Card content goes here.</p>
  </div>
</div>
```

### Form Styling

**Styled Input:**
```html
<input
  type="text"
  class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
>
```

### Button Variants

**Primary Button:**
```html
<button class="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
  Button Text
</button>
```

**Secondary Button:**
```html
<button class="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
  Button Text
</button>
```

## Troubleshooting Reference

### Common Issues

**Classes Not Working:**
- Verify the class name is spelled correctly
- Check that content paths in config include your files
- Ensure Tailwind is properly configured

**Build Performance:**
- Optimize content paths in configuration
- Use specific glob patterns instead of broad ones
- Consider using safelist for dynamically generated classes

**Dark Mode Not Working:**
- Verify dark mode strategy in configuration
- Check HTML class/attribute for dark mode
- Ensure all dark variants are properly applied

**CSS Output Too Large:**
- Review purge configuration
- Check for unused utility classes
- Consider using safelist/blocklist appropriately

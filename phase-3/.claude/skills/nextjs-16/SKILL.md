---
name: nextjs-16
description: Comprehensive Next.js 16 development with App Router, Server Components, and modern patterns. Use when Claude needs to work with Next.js 16 projects for creating new pages and components with App Router, implementing Server Components and Server Functions, handling data fetching and API routes, optimizing performance with streaming and Suspense, configuring routing, middleware, and deployment, or any other Next.js 16 development tasks.
---

# Next.js 16 Development

## Overview

This skill provides comprehensive guidance for Next.js 16 development, focusing on the App Router architecture, Server Components, and modern React patterns. It enables Claude to create production-ready Next.js applications following best practices and current conventions.

## Core Capabilities

### 1. App Router Implementation
- Creating nested routes with the `app` directory structure
- Implementing layout and template components
- Handling dynamic routes and route groups
- Using loading, error, and not-found boundaries

### 2. Server and Client Components
- Distinguishing between server and client components
- Using 'use client' directive appropriately
- Leveraging Server Components for data fetching
- Managing state and interactivity in Client Components

### 3. Data Fetching and Caching
- Implementing server-side data fetching with async components
- Using Server Functions for server-side operations
- Configuring caching strategies (static and dynamic)
- Handling loading states with Suspense

### 4. API Routes and Integration
- Creating API routes with the App Router
- Implementing authentication flows
- Connecting to databases and external services
- Handling form submissions and mutations

## Quick Start: New Page Creation

When creating a new page in a Next.js 16 app:

1. **Create the route directory** in `app/` (e.g., `app/products/[id]/page.tsx`)
2. **Implement as a Server Component** by default (no 'use client' needed)
3. **Use async/await** for data fetching directly in the component
4. **Add error boundaries** and loading states as needed

Example page structure:
```tsx
// app/products/[id]/page.tsx
import { getProduct } from '@/lib/products'

export default async function ProductPage({
  params
}: {
  params: { id: string }
}) {
  const product = await getProduct(params.id)

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
    </div>
  )
}
```

## Routing Patterns

### Static Routes
- Create directories under `app/` (e.g., `app/about/page.tsx`)
- Use `layout.tsx` for shared UI in route segments
- Use `template.tsx` for unique UI per route in segment

### Dynamic Routes
- Use bracket syntax: `[id]`, `[slug]`, `[...param]`
- Access via `params` prop in page components
- Example: `app/products/[id]/page.tsx`

### Route Groups
- Use parentheses: `(auth)` to organize routes without affecting URL structure
- Useful for grouping admin, dashboard, or auth routes
- Example: `app/(auth)/login/page.tsx` → `/login`

## Server Components Best Practices

### Data Fetching
- Perform data fetching directly in Server Components
- Use async/await in component functions
- Leverage automatic request memoization
- Cache data appropriately with `fetch` options

```tsx
// Server Component with data fetching
import { unstable_cache } from 'next/cache'

const getCachedData = unstable_cache(
  async () => {
    const res = await fetch('https://api.example.com/data')
    return res.json()
  },
  ['data-key'],
  { revalidate: 3600 } // Cache for 1 hour
)

export default async function DataComponent() {
  const data = await getCachedData()
  return <div>{JSON.stringify(data)}</div>
}
```

### Streaming and Suspense
- Use Suspense boundaries for granular loading states
- Implement streaming for faster perceived performance
- Wrap independent data fetching with Suspense

```tsx
// layout.tsx
import { Suspense } from 'react'
import Header from './header'
import Loading from './loading'

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <Suspense fallback={<Loading />}>
          <Header />
        </Suspense>
        <main>{children}</main>
      </body>
    </html>
  )
}
```

## Client Components Guidelines

### When to Use Client Components
- For interactive elements (buttons, forms)
- When using React state (`useState`, `useEffect`)
- For browser APIs (localStorage, geolocation)
- When using third-party libraries that require client-side execution

### Client Component Syntax
```tsx
'use client'

import { useState } from 'react'

export default function InteractiveComponent() {
  const [count, setCount] = useState(0)

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  )
}
```

## API Routes with App Router

### Basic API Route
```ts
// app/api/users/route.ts
import { NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const id = searchParams.get('id')

  // Return JSON response
  return Response.json({ message: 'Hello World' })
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  // Process the request body
  return Response.json({ success: true })
}
```

## Environment Configuration

### Environment Variables
- Use `.env.local` for sensitive variables
- Use `.env` for non-sensitive defaults
- Access with `process.env.VARIABLE_NAME`

### Next.js Configuration
```js
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverActions: true, // Enable Server Actions
  },
  images: {
    domains: ['example.com'], // Configure image optimization
  },
}

module.exports = nextConfig
```

## Deployment Considerations

### Static Export
- Use `output: 'export'` in next.config.js for static sites
- All routes must be prerenderable
- No server-side data fetching allowed

### Vercel Deployment
- Zero configuration deployment
- Automatic environment detection
- Edge and Node.js runtime options

### Build Optimization
- Leverage Next.js automatic code splitting
- Use `next/image` for optimized images
- Implement proper error boundaries
- Use `next/link` for client-side navigation

## Common Patterns and Examples

### Form Handling with Server Actions
```tsx
'use server'

import { revalidatePath } from 'next/cache'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  // Create the post in database
  await createPostInDB({ title, content })

  // Revalidate the path to show the new post
  revalidatePath('/posts')
}
```

```tsx
// In your component
'use client'

export default function CreatePostForm() {
  return (
    <form action={createPost}>
      <input name="title" placeholder="Title" required />
      <textarea name="content" placeholder="Content" required />
      <button type="submit">Create Post</button>
    </form>
  )
}
```

### Middleware Implementation
```ts
// middleware.ts
import { NextRequest, NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
  // Add custom headers
  const response = NextResponse.next()
  response.headers.set('X-Custom-Header', 'custom-value')

  return response
}

// Apply to specific paths
export const config = {
  matcher: ['/admin/:path*', '/api/:path*'],
}
```

## Resources

### references/
- `app_router_patterns.md` - Detailed routing examples and patterns
- `server_components_guide.md` - In-depth Server Components documentation
- `data_fetching_strategies.md` - Caching and data fetching best practices
- `performance_optimization.md` - Performance tips and techniques

### assets/
- `component_templates/` - Reusable component boilerplates
- `page_templates/` - Common page structure templates
- `config_templates/` - Configuration file templates

# Next.js 16 Server Components Guide

## Understanding Server Components

Server Components run on the server and can access server-side resources like databases, file systems, and environment variables. They are the default component type in Next.js 16 App Router.

### Key Benefits
- **Security**: Sensitive data and API keys stay on the server
- **Performance**: Server-rendered HTML is sent to the client faster
- **Bundle Size**: Server-only code doesn't increase client bundle size
- **Direct Data Access**: Access to databases and file systems without API routes

## Data Fetching in Server Components

### Direct Data Fetching
Server Components can fetch data directly without API routes:

```tsx
// app/products/page.tsx
import { getProducts } from '@/lib/products'

export default async function ProductsPage() {
  const products = await getProducts()

  return (
    <div>
      {products.map(product => (
        <div key={product.id}>{product.name}</div>
      ))}
    </div>
  )
}
```

### Using fetch() with Caching
Next.js automatically caches `fetch()` calls:

```tsx
// Server Component with automatic caching
export default async function DataComponent() {
  // This fetch is automatically cached
  const res = await fetch('https://api.example.com/data')
  const data = await res.json()

  return <div>{JSON.stringify(data)}</div>
}
```

### Manual Caching with unstable_cache
For more control over caching:

```tsx
import { unstable_cache } from 'next/cache'

const getCachedUsers = unstable_cache(
  async () => {
    const res = await fetch('https://api.example.com/users')
    return res.json()
  },
  ['users'], // Cache key
  { revalidate: 3600 } // Revalidate every hour
)

export default async function UsersPage() {
  const users = await getCachedUsers()
  return <div>{/* render users */}</div>
}
```

## Server Actions

Server Actions allow you to execute server-side code from client components:

```tsx
'use server'

import { revalidatePath } from 'next/cache'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  await createPostInDB({ title, content })

  // Revalidate the path to show the new post
  revalidatePath('/posts')
}
```

```tsx
// Client Component using Server Action
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

## When to Use Server Components

### Use Server Components for:
- **Data fetching** - Access databases, APIs, file systems
- **Environment variables** - Access sensitive data without exposing to client
- **Server-side libraries** - Use Node.js APIs and server-side packages
- **Initial render** - Most pages should start as Server Components
- **SEO content** - Content that needs to be indexed by search engines

### Example: Product Page
```tsx
// app/products/[id]/page.tsx
import { getProduct, getRelatedProducts } from '@/lib/products'
import { AddToCartButton } from '@/components/add-to-cart-button'

export default async function ProductPage({
  params
}: {
  params: { id: string }
}) {
  // Server Component can fetch data directly
  const product = await getProduct(params.id)
  const relatedProducts = await getRelatedProducts(params.id)

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <AddToCartButton productId={product.id} />

      <div>
        <h2>Related Products</h2>
        {relatedProducts.map(product => (
          <div key={product.id}>{product.name}</div>
        ))}
      </div>
    </div>
  )
}
```

## Server Components vs Client Components

### Server Components
```tsx
// Server Component - no 'use client' directive
import { getServerData } from '@/lib/data'

export default async function ServerComponent() {
  const data = await getServerData() // Direct server access

  return <div>{data.content}</div>
}
```

### Client Components
```tsx
// Client Component - has 'use client' directive
'use client'

import { useState } from 'react'

export default function ClientComponent() {
  const [count, setCount] = useState(0) // Client-side state

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  )
}
```

## Streaming and Progressive Rendering

### Using Suspense for Streaming
```tsx
// layout.tsx
import { Suspense } from 'react'
import Header from './header'
import Sidebar from './sidebar'
import Loading from './loading'

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <header>
          <Suspense fallback={<Loading />}>
            <Header />
          </Suspense>
        </header>
        <aside>
          <Suspense fallback={<div>Loading sidebar...</div>}>
            <Sidebar />
          </Suspense>
        </aside>
        <main>{children}</main>
      </body>
    </html>
  )
}
```

### Streaming Data Components
```tsx
// components/product-list.tsx
import { getProducts } from '@/lib/products'

export default async function ProductList() {
  const products = await getProducts()

  return (
    <div>
      {products.map(product => (
        <div key={product.id}>
          <h3>{product.name}</h3>
          <p>{product.description}</p>
        </div>
      ))}
    </div>
  )
}
```

## Security Best Practices

### Environment Variables
Server Components can safely access environment variables:

```tsx
// Server Component - safe to access environment variables
export default async function AdminDashboard() {
  const API_KEY = process.env.INTERNAL_API_KEY
  const adminData = await fetchAdminData(API_KEY)

  return <div>{/* render admin data */}</div>
}
```

### Input Validation
Always validate input in Server Actions:

```tsx
'use server'

import { z } from 'zod'

const PostSchema = z.object({
  title: z.string().min(1).max(100),
  content: z.string().min(10),
})

export async function createPost(formData: FormData) {
  const rawData = {
    title: formData.get('title'),
    content: formData.get('content'),
  }

  const validatedData = PostSchema.parse(rawData)

  await createPostInDB(validatedData)
  revalidatePath('/posts')
}
```

## Performance Optimization

### Selective Hydration
Only hydrate components that need client-side interactivity:

```tsx
// Server Component with selective hydration
import { ProductCard } from './product-card' // Client Component

export default async function ProductList() {
  const products = await getProducts()

  return (
    <div>
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  )
}
```

### Caching Strategies
- Use automatic `fetch()` caching for frequently accessed data
- Use `unstable_cache` for complex server-side operations
- Use `revalidatePath` in Server Actions to invalidate cache when data changes

```tsx
// Cache expensive operations
const getExpensiveData = unstable_cache(
  async () => {
    // Expensive operation
    return await performExpensiveOperation()
  },
  ['expensive-data'],
  { revalidate: 3600 }
)
```
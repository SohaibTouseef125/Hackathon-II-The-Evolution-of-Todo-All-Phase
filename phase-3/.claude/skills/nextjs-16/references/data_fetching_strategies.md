# Next.js 16 Data Fetching Strategies

## Overview

Next.js 16 provides multiple data fetching strategies optimized for different use cases. Understanding when to use each strategy is crucial for performance and user experience.

## Server Component Data Fetching (Default)

### Direct Data Fetching in Server Components
Server Components can fetch data directly without API routes:

```tsx
// app/products/[id]/page.tsx
import { getProduct } from '@/lib/products'

export default async function ProductPage({
  params
}: {
  params: { id: string }
}) {
  const product = await getProduct(params.id) // Server-side fetch

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
    </div>
  )
}
```

### Automatic Caching with fetch()
Next.js automatically caches `fetch()` calls in Server Components:

```tsx
// Server Component with automatic caching
export default async function DataComponent() {
  // This request is automatically cached
  const res = await fetch('https://api.example.com/data', {
    // Optional: Configure caching behavior
    next: { revalidate: 3600 } // Revalidate every hour
  })

  const data = await res.json()
  return <div>{JSON.stringify(data)}</div>
}
```

### Manual Caching with unstable_cache
For more granular control over caching:

```tsx
import { unstable_cache } from 'next/cache'

const getCachedUsers = unstable_cache(
  async () => {
    const res = await fetch('https://api.example.com/users')
    return res.json()
  },
  ['users-list'], // Cache key
  {
    revalidate: 3600, // Revalidate every hour
    tags: ['users']   // Cache tags for selective invalidation
  }
)

export default async function UsersPage() {
  const users = await getCachedUsers()
  return <div>{/* render users */}</div>
}
```

## Streaming and Progressive Loading

### Using Suspense for Granular Loading
```tsx
// app/products/page.tsx
import { Suspense } from 'react'
import { ProductList } from './product-list'
import { FeaturedProducts } from './featured-products'

export default function ProductsPage() {
  return (
    <div>
      <h1>All Products</h1>

      {/* Featured products load first */}
      <Suspense fallback={<div>Loading featured products...</div>}>
        <FeaturedProducts />
      </Suspense>

      {/* All products stream in after */}
      <Suspense fallback={<div>Loading all products...</div>}>
        <ProductList />
      </Suspense>
    </div>
  )
}
```

### Streaming Component Implementation
```tsx
// components/featured-products.tsx
import { getFeaturedProducts } from '@/lib/products'

export default async function FeaturedProducts() {
  const products = await getFeaturedProducts()

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

## Client-Side Data Fetching

### When to Use Client-Side Fetching
- Interactive UI that depends on user actions
- Data that changes frequently
- User-specific data (after authentication)
- Real-time updates

### Using SWR for Client Components
```tsx
// components/user-profile.tsx
'use client'

import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(r => r.json())

export default function UserProfile({ userId }: { userId: string }) {
  const { data, error, isLoading } = useSWR(
    `/api/users/${userId}`,
    fetcher
  )

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error loading profile</div>
  if (!data) return <div>No user found</div>

  return (
    <div>
      <h1>{data.name}</h1>
      <p>{data.email}</p>
    </div>
  )
}
```

### React Query Example
```tsx
// components/product-details.tsx
'use client'

import { useQuery } from '@tanstack/react-query'

export default function ProductDetails({ productId }: { productId: string }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['product', productId],
    queryFn: () => fetchProduct(productId),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <div>
      <h1>{data.name}</h1>
      <p>{data.description}</p>
    </div>
  )
}
```

## Server Actions for Mutations

### Basic Server Action
```tsx
'use server'

import { revalidatePath } from 'next/cache'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  await createPostInDB({ title, content })

  // Revalidate to show the new post
  revalidatePath('/posts')
}
```

### Server Action with Validation
```tsx
'use server'

import { z } from 'zod'
import { revalidateTag } from 'next/cache'

const PostSchema = z.object({
  title: z.string().min(1).max(100),
  content: z.string().min(10),
})

export async function createPost(formData: FormData) {
  try {
    const validatedData = PostSchema.parse({
      title: formData.get('title'),
      content: formData.get('content'),
    })

    await createPostInDB(validatedData)

    // Revalidate using tags
    revalidateTag('posts')

    return { success: true }
  } catch (error) {
    if (error instanceof z.ZodError) {
      return {
        success: false,
        errors: error.errors.map(e => e.message)
      }
    }
    return { success: false, errors: ['An unexpected error occurred'] }
  }
}
```

## Caching Strategies

### Static Data (Fully Pre-rendered)
For data that rarely changes:

```tsx
// app/static-page/page.tsx
export const revalidate = 0 // Static generation - never revalidates

export default async function StaticPage() {
  const staticData = await getStaticData()
  return <div>{JSON.stringify(staticData)}</div>
}
```

### Dynamic Data (On-demand Revalidation)
For data that changes frequently:

```tsx
// app/dynamic-page/page.tsx
export const revalidate = 60 // Revalidate every 60 seconds

export default async function DynamicPage() {
  const dynamicData = await getDynamicData()
  return <div>{JSON.stringify(dynamicData)}</div>
}
```

### Conditional Caching
```tsx
// app/user-dashboard/page.tsx
export default async function UserDashboard() {
  // For logged-in users, don't cache
  if (await getCurrentUser()) {
    return await getUserDashboardData()
  }

  // For public data, use caching
  const publicData = await getPublicData()
  return <div>{JSON.stringify(publicData)}</div>
}
```

## Error Handling

### Error Boundaries with Data Fetching
```tsx
// app/products/error.tsx
'use client'

export default function ProductsError({
  error,
  reset,
}: {
  error: Error
  reset: () => void
}) {
  return (
    <div>
      <h2>Failed to load products</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}
```

### Graceful Degradation
```tsx
// components/product-list.tsx
export default async function ProductList() {
  try {
    const products = await getProducts()
    return (
      <div>
        {products.map(product => (
          <div key={product.id}>{product.name}</div>
        ))}
      </div>
    )
  } catch (error) {
    console.error('Failed to fetch products:', error)
    return <div>Failed to load products. Please try again later.</div>
  }
}
```

## Performance Considerations

### Minimize Waterfalls
Instead of sequential data fetching:

```tsx
// ❌ Waterfall - slow
export default async function UserProfile({ userId }: { userId: string }) {
  const user = await getUser(userId)
  const posts = await getPostsByUser(user.id)  // Waits for user fetch
  const comments = await getCommentsByUser(user.id)  // Waits for posts fetch

  return <div>{/* render */}</div>
}
```

Use Promise.all for parallel fetching:

```tsx
// ✅ Parallel - fast
export default async function UserProfile({ userId }: { userId: string }) {
  const [user, posts, comments] = await Promise.all([
    getUser(userId),
    getPostsByUser(userId),
    getCommentsByUser(userId),
  ])

  return <div>{/* render */}</div>
}
```

### Cache Invalidation
Use cache tags for selective invalidation:

```tsx
// In your data fetching function
export async function getProduct(id: string) {
  const res = await fetch(`https://api.example.com/products/${id}`, {
    next: { tags: [`product-${id}`] }
  })
  return res.json()
}

// In your Server Action
'use server'
import { revalidateTag } from 'next/cache'

export async function updateProduct(id: string, data: any) {
  await updateProductInDB(id, data)
  revalidateTag(`product-${id}`) // Only invalidate this product
}
```
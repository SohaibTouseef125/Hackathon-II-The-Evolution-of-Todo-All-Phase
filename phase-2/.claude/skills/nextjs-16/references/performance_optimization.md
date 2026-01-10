# Next.js 16 Performance Optimization

## Core Performance Principles

### Client-Server Component Strategy
- **Server Components by default**: Use for initial render and data fetching
- **Client Components sparingly**: Only when interactivity is needed
- **Minimize client bundle**: Keep server-only code from increasing bundle size

### Component Hydration Strategy
```tsx
// ❌ Bad: Everything is client-side
'use client'
import { useState, useEffect } from 'react'

export default function ProductPage() {
  const [product, setProduct] = useState(null)

  useEffect(() => {
    fetch('/api/product').then(res => res.json()).then(setProduct)
  }, [])

  return <div>{product?.name}</div>
}
```

```tsx
// ✅ Good: Server Component for initial render
// app/products/[id]/page.tsx
export default async function ProductPage({ params }) {
  const product = await getProduct(params.id)

  return (
    <div>
      <h1>{product.name}</h1>
      <InteractiveComponent productId={product.id} />
    </div>
  )
}

// Only interactive part is client component
// components/interactive-component.tsx
'use client'
export default function InteractiveComponent({ productId }) {
  const [isFavorite, setIsFavorite] = useState(false)

  return (
    <button onClick={() => toggleFavorite(productId)}>
      {isFavorite ? '★' : '☆'}
    </button>
  )
}
```

## Image Optimization

### Using next/image
```tsx
import Image from 'next/image'

export default function ProductImage({ src, alt, width, height }) {
  return (
    <Image
      src={src}
      alt={alt}
      width={width}
      height={height}
      // Optional: different loading strategies
      priority={false} // Use priority for above-the-fold images
      placeholder="blur" // Use blur placeholder for better UX
      blurDataURL="data:image/jpeg;base64..." // Precomputed blur placeholder
    />
  )
}
```

### Responsive Images
```tsx
// For responsive images with different sizes
export default function ResponsiveImage() {
  return (
    <Image
      src="/hero.jpg"
      alt="Hero image"
      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
      fill={false}
      style={{
        width: '100%',
        height: 'auto',
      }}
    />
  )
}
```

## Font Optimization

### Using next/font
```tsx
// lib/fonts.ts
import { Inter } from 'next/font/google'

export const inter = Inter({
  subsets: ['latin'],
  display: 'swap', // Optimize loading
  variable: '--font-inter',
})

// In your layout
// app/layout.tsx
import { inter } from '@/lib/fonts'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.variable}>
      <body>{children}</body>
    </html>
  )
}
```

## Code Splitting and Dynamic Imports

### Dynamic Imports for Client Components
```tsx
// components/heavy-chart.tsx
'use client'
import dynamic from 'next/dynamic'

// Dynamically import without SSR
const HeavyChart = dynamic(() => import('./chart'), {
  loading: () => <p>Loading chart...</p>,
  ssr: false, // Don't render on server
})

// With named exports
const { ChartComponent } = dynamic(() => import('./charts'), {
  loading: () => <p>Loading...</p>,
  ssr: true,
})
```

### Conditional Dynamic Imports
```tsx
'use client'

import { useState, useEffect } from 'react'
import dynamic from 'next/dynamic'

export default function ConditionalComponent() {
  const [showAdvanced, setShowAdvanced] = useState(false)

  const AdvancedFeature = showAdvanced
    ? dynamic(() => import('./advanced-feature'))
    : () => null

  return (
    <div>
      <button onClick={() => setShowAdvanced(!showAdvanced)}>
        Toggle Advanced Feature
      </button>
      {showAdvanced && <AdvancedFeature />}
    </div>
  )
}
```

## Route-based Code Splitting

### Automatic Splitting
Next.js automatically splits code by route:
```
app/
├── layout.tsx           // Shared across all routes
├── page.tsx             // Home page bundle
├── products/
│   ├── layout.tsx       // Products section shared
│   ├── page.tsx         // Products page bundle
│   └── [id]/page.tsx    // Product detail bundle
└── dashboard/
    ├── layout.tsx       // Dashboard shared
    └── page.tsx         // Dashboard bundle
```

### Parallel Route Optimization
```tsx
// app/layout.tsx
export default function Layout({
  children,
  sidebar,
  modal,
}: {
  children: React.ReactNode
  sidebar: React.ReactNode
  modal: React.ReactNode
}) {
  return (
    <div className="flex">
      {children}
      {sidebar && <aside>{sidebar}</aside>}
      {modal && <div className="modal">{modal}</div>}
    </div>
  )
}
```

## Caching Strategies

### Request Memoization
Server Components automatically memoize identical requests:

```tsx
// These will be cached automatically
async function getData() {
  // First call: executes
  const res = await fetch('https://api.example.com/data')
  return res.json()
}

// In your component
export default async function MyPage() {
  // Multiple calls with same URL will use cached result
  const [data1, data2] = await Promise.all([
    getData(),
    getData() // Uses cached result
  ])

  return <div>{/* render data */}</div>
}
```

### Selective Revalidation
```tsx
// Revalidate specific paths after mutations
'use server'
import { revalidatePath, revalidateTag } from 'next/cache'

export async function updateProduct(productId: string) {
  await updateProductInDB(productId)

  // Revalidate specific path
  revalidatePath(`/products/${productId}`)

  // Or use tags for more flexible invalidation
  revalidateTag('products')
}
```

## Streaming and Progressive Rendering

### Granular Suspense Boundaries
```tsx
// app/products/page.tsx
import { Suspense } from 'react'
import ProductGrid from './product-grid'
import FilterSidebar from './filter-sidebar'
import ProductHero from './product-hero'

export default function ProductsPage() {
  return (
    <div>
      {/* Hero section loads first */}
      <Suspense fallback={<HeroSkeleton />}>
        <ProductHero />
      </Suspense>

      <div className="flex">
        {/* Sidebar loads independently */}
        <aside>
          <Suspense fallback={<FilterSkeleton />}>
            <FilterSidebar />
          </Suspense>
        </aside>

        {/* Main content loads independently */}
        <main>
          <Suspense fallback={<ProductGridSkeleton />}>
            <ProductGrid />
          </Suspense>
        </main>
      </div>
    </div>
  )
}
```

### Streaming Server Components
```tsx
// components/product-grid.tsx
import { getProducts } from '@/lib/products'

export default async function ProductGrid({
  searchParams
}: {
  searchParams: { category?: string }
}) {
  const products = await getProducts(searchParams.category)

  return (
    <div className="grid">
      {products.map(product => (
        <div key={product.id} className="product-card">
          <h3>{product.name}</h3>
          <p>{product.description}</p>
        </div>
      ))}
    </div>
  )
}
```

## Bundle Optimization

### Tree Shaking
```tsx
// ❌ Bad: Importing entire libraries
import * as _ from 'lodash' // Imports everything

// ✅ Good: Import only what you need
import { debounce } from 'lodash-es'

// ✅ Even better: Use native JavaScript when possible
const debounce = (fn, delay) => {
  let timeoutId
  return (...args) => {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => fn(...args), delay)
  }
}
```

### Optimize Third-Party Libraries
```tsx
// For heavy libraries, use dynamic imports
'use client'
import { useState } from 'react'
import dynamic from 'next/dynamic'

// Dynamically import heavy chart library
const Chart = dynamic(() => import('react-chartjs-2'), {
  loading: () => <div>Loading chart...</div>,
  ssr: false
})

// For date libraries, import specific functions
import format from 'date-fns/format'
import parseISO from 'date-fns/parseISO'
// Instead of: import * as dateFns from 'date-fns'
```

## Network Optimization

### Preloading and Prefetching
```tsx
// In your components
'use client'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function ProductCard({ productId }) {
  const router = useRouter()

  // Prefetch on hover for better UX
  const onMouseEnter = () => {
    router.prefetch(`/products/${productId}`)
  }

  return (
    <div onMouseEnter={onMouseEnter}>
      <a href={`/products/${productId}`}>View Product</a>
    </div>
  )
}
```

### Optimize API Routes
```ts
// app/api/optimized/route.ts
import { NextRequest } from 'next/server'

export const dynamic = 'force-dynamic' // or 'auto', 'error', 'force-static'

export async function GET(request: NextRequest) {
  // Use search params for caching
  const { searchParams } = new URL(request.url)
  const category = searchParams.get('category')

  // Cache based on request params
  const data = await fetch(
    `https://api.example.com/data?category=${category}`,
    {
      next: {
        revalidate: 300, // Cache for 5 minutes
        tags: [`products-${category}`]
      }
    }
  )

  return Response.json(await data.json())
}
```

## Performance Monitoring

### Core Web Vitals
Focus on the three Core Web Vitals metrics:

1. **Largest Contentful Paint (LCP)**: Load main content quickly
2. **First Input Delay (FID)**: Keep page responsive
3. **Cumulative Layout Shift (CLS)**: Prevent unexpected layout shifts

```tsx
// Prevent layout shift with size placeholders
export default function ImageWithPlaceholder({ src, width, height }) {
  return (
    <div style={{ width, height }}>
      <Image
        src={src}
        width={width}
        height={height}
        placeholder="blur" // Reduces CLS
        blurDataURL="data:..." // Precomputed blur placeholder
      />
    </div>
  )
}
```

### Performance Budgets
```js
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config, { isServer }) => {
    if (!isServer) {
      // Analyze bundle size
      config.performance = {
        maxAssetSize: 250000, // 250 KB
        maxEntrypointSize: 250000, // 250 KB
        hints: 'warning'
      }
    }
    return config
  }
}

module.exports = nextConfig
```
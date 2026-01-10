// Next.js App Router Example
// app/page.js
import { Suspense } from 'react'
import { Card } from './components/Card'

export default function HomePage() {
  return (
    <main>
      <h1>Next.js 14 App</h1>
      <Suspense fallback={<div>Loading cards...</div>}>
        <Card title="Welcome" content="This is a Next.js 14 app with App Router" />
      </Suspense>
    </main>
  )
}
// app/[route]/page.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description for SEO',
}

export default async function PageName() {
  // Server Component - can perform server-side operations
  // const data = await getData()

  return (
    <div className="container">
      <h1>Page Title</h1>
      <p>Page content goes here</p>
    </div>
  )
}
// app/[route]/layout.tsx
import { ReactNode } from 'react'
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Section Title',
  description: 'Section description',
}

export default function SectionLayout({
  children,
}: {
  children: ReactNode
}) {
  return (
    <section>
      <nav>
        {/* Navigation for this section */}
      </nav>
      <main>{children}</main>
    </section>
  )
}
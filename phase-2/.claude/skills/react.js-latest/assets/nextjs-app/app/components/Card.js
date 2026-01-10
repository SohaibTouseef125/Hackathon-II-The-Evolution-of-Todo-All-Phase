// Card Component for Next.js App
'use client'

import { useState } from 'react'

export function Card({ title, content }) {
  const [isExpanded, setIsExpanded] = useState(false)

  return (
    <div className={`card ${isExpanded ? 'expanded' : ''}`}>
      <h2 onClick={() => setIsExpanded(!isExpanded)} style={{ cursor: 'pointer' }}>
        {title}
      </h2>
      {isExpanded && <p>{content}</p>}
    </div>
  )
}
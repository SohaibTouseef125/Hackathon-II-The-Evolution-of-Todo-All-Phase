---
name: openai-chatkit
description: OpenAI ChatKit UI framework for building conversational interfaces. Use when building chatbot frontends with OpenAI's ChatKit, including message bubbles, typing indicators, and integration with backend chat APIs.
---

# OpenAI ChatKit

ChatKit is OpenAI's conversational UI framework for building modern chat interfaces.

## Quick Start

```tsx
import ChatKit from '@openai/chatkit'

function ChatInterface() {
  return (
    <ChatKit
      apiUrl="http://localhost:8000/api/{user_id}/chat"
      domainKey={process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY}
    />
  )
}
```

## ChatKit Configuration

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| apiUrl | string | Yes | Backend chat endpoint |
| domainKey | string | Yes | OpenAI domain allowlist key |
| title | string | No | Chat window title |
| welcomeMessage | string | No | Initial bot message |
| placeholder | string | No | Input placeholder text |

## Domain Allowlist Setup

1. Deploy frontend to get production URL (Vercel/GitHub Pages)
2. Go to [OpenAI Security Domain Allowlist](https://platform.openai.com/settings/organization/security/domain-allowlist)
3. Add your domain (e.g., `https://your-app.vercel.app`)
4. Copy the domain key and set in environment:

```bash
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key
```

## Styling

ChatKit uses CSS variables for customization:

```css
:root {
  --chatkit-primary: #10a37f;
  --chatkit-background: #ffffff;
  --chatkit-text: #1a1a1a;
  --chatkit-border-radius: 12px;
}
```

## Integration with Next.js App Router

```tsx
// app/chat/page.tsx
'use client'

import ChatKit from '@openai/chatkit'

export default function ChatPage({ params }: { params: { userId: string } }) {
  return (
    <div className="h-screen">
      <ChatKit
        apiUrl={`http://localhost:8000/api/${params.userId}/chat`}
        domainKey={process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY}
        title="Todo Assistant"
        welcomeMessage="Hi! I can help you manage your tasks. What would you like to do?"
      />
    </div>
  )
}
```

## Error Handling

```tsx
<ChatKit
  apiUrl="..."
  domainKey="..."
  onError={(error) => {
    console.error('Chat error:', error)
    // Show user-friendly error message
  }}
/>
```

## See Also

- [Phase 3 Todo Chatbot Skill](../phase3-todo-chatbot/SKILL.md) - Complete chatbot integration
- [OpenAI Agents SDK Skill](../openai-agents-sdk/SKILL.md) - Backend AI agent logic

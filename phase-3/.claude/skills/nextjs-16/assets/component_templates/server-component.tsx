// components/{ComponentName}.tsx
// This is a Server Component - no 'use client' directive needed

interface {ComponentName}Props {
  // Define your props here
}

export default async function {ComponentName}({ }: {ComponentName}Props) {
  // You can perform server-side operations here
  // const data = await fetchData()

  return (
    <div className="{ComponentName | lower}">
      {/* Your component content here */}
    </div>
  )
}
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverActions: true, // Enable Server Actions
    serverComponentsExternalPackages: [], // Add external packages if needed
  },
  images: {
    domains: ['example.com'], // Add image domains for next/image
    formats: ['image/webp'], // Enable WebP format
  },
  // Enable compression
  compress: true,
  // Optimize page loading
  reactStrictMode: true,
  // Configure redirects, rewrites, headers
  async redirects() {
    return [
      // Example redirect
      // {
      //   source: '/old-page',
      //   destination: '/new-page',
      //   permanent: true,
      // },
    ]
  },
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
        ],
      },
    ]
  },
}

module.exports = nextConfig
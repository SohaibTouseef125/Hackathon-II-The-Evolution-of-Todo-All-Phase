/** @type {import('next').NextConfig} */
const nextConfig = {

  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api',
    NEXT_PUBLIC_BETTER_AUTH_URL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:3000',
  },
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "**"
      },
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
      },
      {
        protocol: 'https',
        hostname: 'placehold.co',
      },
    ]
  },
  experimental: {
    scrollRestoration: true,
    // reactCompiler: true, // Temporarily disabled until babel-plugin-react-compiler is installed
  },
};

module.exports = nextConfig;
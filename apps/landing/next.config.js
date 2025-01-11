/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ['tailwindcss'],
  experimental: {
    externalDir: true
  }
}

module.exports = nextConfig 
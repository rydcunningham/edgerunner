/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ['tailwindcss'],
  experimental: {
    externalDir: true,
    serverComponentsExternalPackages: ['tailwindcss']
  }
}

module.exports = nextConfig 
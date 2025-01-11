/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ['tailwindcss'],
  experimental: {
    externalDir: true,
    serverComponentsExternalPackages: ['tailwindcss']
  },
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@/lib': './lib'
    }
    return config
  }
}

module.exports = nextConfig 
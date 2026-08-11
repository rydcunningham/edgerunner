/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ['@edgerunner/brand'],
  async redirects() {
    // Order matters: /blog/research must match before /blog/:slug.
    return [
      { source: '/blog/research', destination: '/research', permanent: true },
      { source: '/blog', destination: '/writing', permanent: true },
      { source: '/blog/:slug', destination: '/writing/:slug', permanent: true },
      { source: '/bio', destination: '/about', permanent: true },
    ]
  },
}

module.exports = nextConfig

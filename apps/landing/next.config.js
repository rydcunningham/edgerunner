/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  experimental: {
    outputFileTracingRoot: __dirname,
    outputFileTracingIncludes: {
      '/**': ['./lib/**/*']
    }
  }
}

module.exports = nextConfig 
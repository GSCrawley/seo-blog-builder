/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['localhost'],
    unoptimized: true, // For static export support
  },
  trailingSlash: true, // Better for SEO and static export
  exportPathMap: async function (defaultPathMap) {
    return defaultPathMap;
  },
}

module.exports = nextConfig

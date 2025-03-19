/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  trailingSlash: true, // Append trailing slashes to URLs
  images: {
    domains: ['images.unsplash.com'], // Allow images from Unsplash
    unoptimized: process.env.NODE_ENV === 'development' ? false : true, // Optimize images in development, not in static exports
  },
  output: 'export', // Generate static HTML export
  // Add any other custom configuration here
};

module.exports = nextConfig;

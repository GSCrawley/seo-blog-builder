/**
 * Site configuration
 * This file will be dynamically updated during site generation
 */
const siteConfig = {
  // Basic info
  title: 'SITE_TITLE',
  description: 'SITE_DESCRIPTION',
  siteUrl: 'SITE_URL',
  
  // Author info
  author: {
    name: 'DEFAULT_AUTHOR',
    bio: 'Content Creator',
    social: {
      twitter: '',
      facebook: '',
      instagram: '',
      linkedin: '',
    },
  },
  
  // SEO and analytics
  googleAnalyticsId: 'GOOGLE_ANALYTICS_ID',
  
  // Design
  colors: {
    primary: 'PRIMARY_COLOR',
    secondary: 'SECONDARY_COLOR',
    background: '#ffffff',
    text: '#333333',
    accent: '#f39c12',
  },
  
  // Navigation
  navigation: [
    { name: 'Home', path: '/' },
    { name: 'Blog', path: '/blog/' },
    { name: 'Categories', path: '/categories/' },
    { name: 'About', path: '/about/' },
  ],
  
  // Content
  postsPerPage: 10,
  showRelatedPosts: true,
  showTableOfContents: true,
  
  // Features
  enableSearch: true,
  enableNewsletter: false,
  
  // Affiliate/monetization
  affiliateDisclosure: 'This site contains affiliate links. If you purchase through these links, we may earn a commission at no additional cost to you.',
};

module.exports = siteConfig;

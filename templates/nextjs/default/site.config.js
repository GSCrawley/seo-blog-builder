/**
 * Site configuration
 * This will be updated by the site generation service
 */
const siteConfig = {
  // Site info
  title: 'SITE_TITLE',
  description: 'SITE_DESCRIPTION',
  siteUrl: 'SITE_URL',
  defaultAuthor: 'DEFAULT_AUTHOR',
  
  // Styling
  primaryColor: 'PRIMARY_COLOR',
  secondaryColor: 'SECONDARY_COLOR',
  
  // Social media
  twitterHandle: '',
  facebookPage: '',
  
  // Analytics
  googleAnalyticsId: 'GOOGLE_ANALYTICS_ID',
  
  // Navigation
  mainNav: [
    { label: 'Home', path: '/' },
    { label: 'Blog', path: '/blog/' },
    { label: 'About', path: '/about/' },
  ],
  
  // Footer
  footerLinks: [
    { label: 'Privacy Policy', path: '/privacy-policy/' },
    { label: 'Terms of Service', path: '/terms-of-service/' },
    { label: 'Contact', path: '/contact/' },
  ],
  
  // Affiliate disclosure
  affiliateDisclosure: 'This site contains affiliate links. If you click and make a purchase, I may receive a commission at no additional cost to you.',
  
  // Date format
  dateFormat: 'MMMM d, yyyy',
  
  // Pagination
  postsPerPage: 10,
};

module.exports = siteConfig;

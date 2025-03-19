import '../styles/globals.css';
import siteConfig from '../site.config';
import Layout from '../components/Layout';
import { useEffect } from 'react';

// Google Analytics initialization
const initGA = () => {
  if (typeof window === 'undefined' || !siteConfig.googleAnalyticsId) return;
  
  // Add Google Analytics script
  const script = document.createElement('script');
  script.src = `https://www.googletagmanager.com/gtag/js?id=${siteConfig.googleAnalyticsId}`;
  script.async = true;
  document.head.appendChild(script);
  
  // Configure Google Analytics
  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }
  gtag('js', new Date());
  gtag('config', siteConfig.googleAnalyticsId);
};

function MyApp({ Component, pageProps }) {
  // Initialize Google Analytics
  useEffect(() => {
    initGA();
  }, []);
  
  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  );
}

export default MyApp;

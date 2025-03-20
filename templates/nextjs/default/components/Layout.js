import Head from 'next/head';
import Header from './Header';
import Footer from './Footer';
import { useEffect } from 'react';
import siteConfig from '../site.config';

export default function Layout({ children }) {
  // Google Analytics setup
  useEffect(() => {
    if (siteConfig.googleAnalyticsId && typeof window !== 'undefined') {
      // Load Google Analytics script
      const script = document.createElement('script');
      script.src = `https://www.googletagmanager.com/gtag/js?id=${siteConfig.googleAnalyticsId}`;
      script.async = true;
      document.head.appendChild(script);

      // Initialize Google Analytics
      window.dataLayer = window.dataLayer || [];
      function gtag() {
        window.dataLayer.push(arguments);
      }
      gtag('js', new Date());
      gtag('config', siteConfig.googleAnalyticsId);
    }
  }, []);

  return (
    <>
      <Head>
        <link rel="icon" href="/favicon.ico" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        {/* Default meta tags - overridden by page-specific ones */}
        <meta name="description" content={siteConfig.description} />
        <meta property="og:site_name" content={siteConfig.title} />
        <meta property="og:type" content="website" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="theme-color" content={siteConfig.primaryColor} />
        {/* Custom styles from site config */}
        <style jsx global>{`
          :root {
            --primary-color: ${siteConfig.primaryColor};
            --secondary-color: ${siteConfig.secondaryColor};
          }
        `}</style>
      </Head>

      <div className="flex min-h-screen flex-col">
        <Header />
        <main className="flex-1">{children}</main>
        <Footer />
      </div>
    </>
  );
}

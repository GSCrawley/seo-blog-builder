import Document, { Html, Head, Main, NextScript } from 'next/document';
import siteConfig from '../site.config';

class MyDocument extends Document {
  render() {
    return (
      <Html lang="en">
        <Head>
          {/* Favicon */}
          <link rel="icon" href="/favicon.ico" />
          
          {/* Fonts */}
          <link 
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" 
            rel="stylesheet"
          />
          
          {/* Apply theme colors as CSS variables */}
          <style>
            {`
              :root {
                --color-primary: ${siteConfig.colors.primary};
                --color-secondary: ${siteConfig.colors.secondary};
                --color-background: ${siteConfig.colors.background};
                --color-text: ${siteConfig.colors.text};
                --color-accent: ${siteConfig.colors.accent};
              }
            `}
          </style>
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}

export default MyDocument;

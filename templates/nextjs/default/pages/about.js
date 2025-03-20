import Head from 'next/head';
import Layout from '../components/Layout';
import siteConfig from '../site.config';

export default function About() {
  return (
    <Layout>
      <Head>
        <title>About - {siteConfig.title}</title>
        <meta
          name="description"
          content={`Learn more about ${siteConfig.title} and our mission to provide valuable information.`}
        />
      </Head>

      <div className="mx-auto max-w-4xl px-4 py-8">
        <div className="mb-12 text-center">
          <h1 className="mb-4 text-4xl font-bold">About Us</h1>
          <p className="text-xl text-gray-600">
            Learn more about our mission and values
          </p>
        </div>

        <div className="prose prose-lg mx-auto">
          <h2>Our Mission</h2>
          <p>
            At {siteConfig.title}, we are dedicated to providing high-quality, 
            accurate, and valuable information to our readers. Our goal is to 
            help you make informed decisions about products and services that 
            can improve your life.
          </p>

          <h2>Who We Are</h2>
          <p>
            We are a team of passionate experts with extensive knowledge in our 
            field. With years of experience and a dedication to staying up-to-date 
            with the latest developments, we are committed to sharing our insights 
            and expertise with you.
          </p>

          <h2>Our Approach</h2>
          <p>
            We believe in thorough research, hands-on testing, and honest 
            evaluations. Every article, review, and guide published on our 
            site is crafted with care and attention to detail. We strive to 
            provide comprehensive coverage of topics that matter to our readers.
          </p>

          <h2>Affiliate Disclosure</h2>
          <p>
            {siteConfig.affiliateDisclosure}
          </p>

          <h2>Contact Us</h2>
          <p>
            Have questions or feedback? We'd love to hear from you! 
            Contact us through our <a href="/contact/">contact page</a> or 
            follow us on social media to stay connected.
          </p>
        </div>
      </div>
    </Layout>
  );
}

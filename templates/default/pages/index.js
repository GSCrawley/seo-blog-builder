import Head from 'next/head';
import siteConfig from '../site.config';
import { getFeaturedPosts } from '../lib/posts';
import PostCard from '../components/PostCard';
import Hero from '../components/Hero';

export default function Home({ posts }) {
  return (
    <>
      <Head>
        <title>{siteConfig.title}</title>
        <meta name="description" content={siteConfig.description} />
        <meta property="og:title" content={siteConfig.title} />
        <meta property="og:description" content={siteConfig.description} />
        <meta property="og:url" content={siteConfig.siteUrl} />
        <meta property="og:type" content="website" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={siteConfig.title} />
        <meta name="twitter:description" content={siteConfig.description} />
      </Head>

      <Hero 
        title={siteConfig.title}
        subtitle={siteConfig.description}
      />
      
      <section className="container mx-auto px-4 py-12">
        <h2 className="text-3xl font-bold mb-8">Latest Posts</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {posts.map((post) => (
            <PostCard key={post.slug} post={post} />
          ))}
        </div>
      </section>
    </>
  );
}

export async function getStaticProps() {
  const posts = getFeaturedPosts();
  
  return {
    props: {
      posts,
    },
  };
}

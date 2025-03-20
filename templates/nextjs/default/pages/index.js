import Head from 'next/head';
import Link from 'next/link';
import { useState } from 'react';
import { format } from 'date-fns';
import siteConfig from '../site.config';
import { getAllPosts } from '../lib/api';
import Layout from '../components/Layout';
import PostPreview from '../components/PostPreview';
import FeaturedPost from '../components/FeaturedPost';

export default function Home({ posts }) {
  const featuredPost = posts[0];
  const recentPosts = posts.slice(1, 4);

  return (
    <Layout>
      <Head>
        <title>{siteConfig.title} - {siteConfig.description}</title>
        <meta name="description" content={siteConfig.description} />
        <meta property="og:title" content={siteConfig.title} />
        <meta property="og:description" content={siteConfig.description} />
        <meta property="og:url" content={siteConfig.siteUrl} />
        <meta name="twitter:card" content="summary_large_image" />
      </Head>

      <section className="mx-auto max-w-6xl px-4 py-8">
        <div className="mb-12 text-center">
          <h1 className="mb-4 text-4xl font-bold md:text-5xl">{siteConfig.title}</h1>
          <p className="text-xl text-gray-600">{siteConfig.description}</p>
        </div>

        {featuredPost && (
          <div className="mb-12">
            <h2 className="mb-6 text-2xl font-bold">Featured Article</h2>
            <FeaturedPost post={featuredPost} />
          </div>
        )}

        <div className="mb-12">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold">Recent Articles</h2>
            <Link href="/blog/" className="text-blue-600 hover:underline">
              View All
            </Link>
          </div>
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {recentPosts.map((post) => (
              <PostPreview key={post.slug} post={post} />
            ))}
          </div>
        </div>

        <div className="bg-gray-50 p-8 rounded-lg text-center">
          <h2 className="mb-4 text-2xl font-bold">Stay Updated</h2>
          <p className="mb-4 text-gray-600">Join our newsletter to receive the latest updates and tips.</p>
          <div className="flex justify-center">
            <input
              type="email"
              placeholder="Your email address"
              className="mr-2 w-full max-w-xs rounded-md border px-4 py-2 focus:border-blue-500 focus:outline-none"
            />
            <button className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
              Subscribe
            </button>
          </div>
        </div>
      </section>
    </Layout>
  );
}

export async function getStaticProps() {
  const posts = getAllPosts(['title', 'date', 'slug', 'author', 'coverImage', 'excerpt']);

  return {
    props: { posts },
  };
}

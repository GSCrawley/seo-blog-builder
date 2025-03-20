import Head from 'next/head';
import { useState } from 'react';
import { getAllPosts } from '../../lib/api';
import Layout from '../../components/Layout';
import PostGrid from '../../components/PostGrid';
import Pagination from '../../components/Pagination';
import siteConfig from '../../site.config';

export default function Blog({ posts }) {
  const [currentPage, setCurrentPage] = useState(1);
  const postsPerPage = siteConfig.postsPerPage;
  const indexOfLastPost = currentPage * postsPerPage;
  const indexOfFirstPost = indexOfLastPost - postsPerPage;
  const currentPosts = posts.slice(indexOfFirstPost, indexOfLastPost);
  const totalPages = Math.ceil(posts.length / postsPerPage);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  return (
    <Layout>
      <Head>
        <title>Blog - {siteConfig.title}</title>
        <meta 
          name="description" 
          content={`Articles and guides about ${siteConfig.title}. Expert advice, tips, and reviews.`} 
        />
      </Head>

      <div className="mx-auto max-w-6xl px-4 py-8">
        <div className="mb-12 text-center">
          <h1 className="mb-4 text-4xl font-bold">Blog</h1>
          <p className="text-xl text-gray-600">
            Latest articles, guides, and tutorials
          </p>
        </div>

        <PostGrid posts={currentPosts} />

        {totalPages > 1 && (
          <Pagination 
            currentPage={currentPage} 
            totalPages={totalPages} 
            paginate={paginate} 
          />
        )}
      </div>
    </Layout>
  );
}

export async function getStaticProps() {
  const posts = getAllPosts([
    'title',
    'date',
    'slug',
    'author',
    'coverImage',
    'excerpt',
  ]);

  return {
    props: { posts },
  };
}

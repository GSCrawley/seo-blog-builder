import Head from 'next/head';
import { format } from 'date-fns';
import markdownIt from 'markdown-it';
import Layout from '../../components/Layout';
import { getPostBySlug, getAllPosts } from '../../lib/api';
import siteConfig from '../../site.config';
import PostHeader from '../../components/PostHeader';
import ShareButtons from '../../components/ShareButtons';
import RelatedPosts from '../../components/RelatedPosts';
import AuthorBox from '../../components/AuthorBox';
import TableOfContents from '../../components/TableOfContents';
import AffiliateDisclosure from '../../components/AffiliateDisclosure';

const md = markdownIt({
  html: true,
  linkify: true,
  typographer: true,
});

export default function Post({ post, relatedPosts }) {
  const { title, date, author, content, excerpt, coverImage, slug, tags } = post;
  const formattedDate = format(new Date(date), siteConfig.dateFormat);
  const hasAffiliateLinks = content.includes('affiliate') || content.includes('product-link');
  
  // Generate content HTML
  const contentHtml = md.render(content || '');

  return (
    <Layout>
      <Head>
        <title>{title} - {siteConfig.title}</title>
        <meta name="description" content={excerpt} />
        <meta property="og:title" content={title} />
        <meta property="og:description" content={excerpt} />
        <meta property="og:url" content={`${siteConfig.siteUrl}/blog/${slug}/`} />
        {coverImage && <meta property="og:image" content={coverImage} />}
        <meta name="twitter:card" content="summary_large_image" />
      </Head>

      <article className="mx-auto max-w-4xl px-4 py-8">
        <PostHeader
          title={title}
          coverImage={coverImage}
          date={formattedDate}
          author={author}
          tags={tags}
        />

        <div className="blog-post-container flex flex-wrap md:flex-nowrap">
          <aside className="w-full md:w-64 md:pr-8">
            <div className="sticky top-24">
              <TableOfContents html={contentHtml} />
            </div>
          </aside>

          <div className="blog-content flex-1">
            {hasAffiliateLinks && <AffiliateDisclosure />}
            
            <div 
              className="prose prose-lg max-w-none" 
              dangerouslySetInnerHTML={{ __html: contentHtml }} 
            />

            <div className="mt-12">
              <ShareButtons title={title} url={`${siteConfig.siteUrl}/blog/${slug}/`} />
            </div>

            <div className="mt-12">
              <AuthorBox author={author} />
            </div>
          </div>
        </div>

        {relatedPosts.length > 0 && (
          <div className="mt-16">
            <RelatedPosts posts={relatedPosts} />
          </div>
        )}
      </article>
    </Layout>
  );
}

export async function getStaticProps({ params }) {
  const post = getPostBySlug(params.slug, [
    'title',
    'date',
    'slug',
    'author',
    'content',
    'coverImage',
    'excerpt',
    'tags',
  ]);

  // Get related posts based on tags
  const allPosts = getAllPosts(['title', 'slug', 'excerpt', 'tags', 'date', 'coverImage']);
  const relatedPosts = allPosts
    .filter(p => 
      p.slug !== params.slug && 
      p.tags && 
      post.tags && 
      p.tags.some(tag => post.tags.includes(tag))
    )
    .slice(0, 3);

  return {
    props: {
      post,
      relatedPosts,
    },
  };
}

export async function getStaticPaths() {
  const posts = getAllPosts(['slug']);

  return {
    paths: posts.map((post) => {
      return {
        params: {
          slug: post.slug,
        },
      };
    }),
    fallback: false,
  };
}

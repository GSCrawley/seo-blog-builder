import Link from 'next/link';
import Image from 'next/image';
import { format } from 'date-fns';
import siteConfig from '../site.config';

export default function RelatedPosts({ posts }) {
  if (!posts || posts.length === 0) return null;

  return (
    <section>
      <h2 className="mb-6 text-2xl font-bold">Related Articles</h2>
      <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
        {posts.map((post) => (
          <div
            key={post.slug}
            className="group flex flex-col overflow-hidden rounded-lg border border-gray-200 hover:shadow-md"
          >
            {post.coverImage && (
              <Link href={`/blog/${post.slug}/`}>
                <div className="relative h-40 w-full">
                  <Image
                    src={post.coverImage}
                    alt={post.title}
                    fill
                    sizes="(max-width: 768px) 100vw, 33vw"
                    className="object-cover transition-transform duration-200 group-hover:scale-105"
                  />
                </div>
              </Link>
            )}
            <div className="flex flex-1 flex-col justify-between p-5">
              <div>
                <Link
                  href={`/blog/${post.slug}/`}
                  className="text-lg font-semibold text-gray-900 hover:text-blue-600"
                >
                  {post.title}
                </Link>
                <p className="mt-2 text-sm text-gray-600 line-clamp-2">
                  {post.excerpt}
                </p>
              </div>
              <div className="mt-3">
                <Link
                  href={`/blog/${post.slug}/`}
                  className="text-sm font-medium text-blue-600 hover:text-blue-800"
                >
                  Read more →
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

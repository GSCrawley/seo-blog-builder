import Link from 'next/link';
import Image from 'next/image';
import { format } from 'date-fns';
import siteConfig from '../site.config';

export default function FeaturedPost({ post }) {
  const { title, slug, excerpt, coverImage, date, author } = post;
  const formattedDate = format(new Date(date), siteConfig.dateFormat);

  return (
    <div className="group grid gap-8 md:grid-cols-2">
      {coverImage && (
        <Link href={`/blog/${slug}/`}>
          <div className="relative h-64 w-full overflow-hidden rounded-lg md:h-80">
            <Image
              src={coverImage}
              alt={title}
              fill
              sizes="(max-width: 768px) 100vw, 50vw"
              className="object-cover transition-transform duration-300 group-hover:scale-105"
            />
          </div>
        </Link>
      )}
      <div className="flex flex-col justify-center">
        <div className="mb-2 text-sm font-medium text-blue-600">
          Featured Article
        </div>
        <Link href={`/blog/${slug}/`}>
          <h3 className="mb-4 text-2xl font-bold text-gray-900 hover:text-blue-700 md:text-3xl">
            {title}
          </h3>
        </Link>
        <p className="mb-5 text-gray-600 line-clamp-3 md:text-lg">
          {excerpt}
        </p>
        <div className="mb-4 text-sm text-gray-500">
          {formattedDate} • {author || siteConfig.defaultAuthor}
        </div>
        <Link
          href={`/blog/${slug}/`}
          className="inline-block rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          Read Article
        </Link>
      </div>
    </div>
  );
}

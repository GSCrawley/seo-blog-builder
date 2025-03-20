import Link from 'next/link';
import Image from 'next/image';
import { format } from 'date-fns';
import siteConfig from '../site.config';

export default function PostPreview({ post }) {
  const { title, slug, excerpt, coverImage, date, author } = post;
  const formattedDate = format(new Date(date), siteConfig.dateFormat);

  return (
    <div className="group flex flex-col overflow-hidden rounded-lg border border-gray-200 hover:shadow-md">
      {coverImage && (
        <Link href={`/blog/${slug}/`}>
          <div className="relative h-48 w-full">
            <Image
              src={coverImage}
              alt={title}
              fill
              sizes="(max-width: 768px) 100vw, 33vw"
              className="object-cover transition-transform duration-200 group-hover:scale-105"
            />
          </div>
        </Link>
      )}
      <div className="flex flex-1 flex-col justify-between p-6">
        <div>
          <Link href={`/blog/${slug}/`} className="text-xl font-semibold text-gray-900 hover:text-blue-600">
            {title}
          </Link>
          <p className="mt-3 text-gray-600 line-clamp-3">{excerpt}</p>
        </div>
        <div className="mt-4">
          <div className="text-sm text-gray-500">
            {formattedDate} • {author || siteConfig.defaultAuthor}
          </div>
          <Link
            href={`/blog/${slug}/`}
            className="mt-2 inline-block text-sm font-medium text-blue-600 hover:text-blue-800"
          >
            Read more →
          </Link>
        </div>
      </div>
    </div>
  );
}

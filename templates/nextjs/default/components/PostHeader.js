import Image from 'next/image';
import Link from 'next/link';

export default function PostHeader({ title, coverImage, date, author, tags }) {
  return (
    <div className="mb-8">
      <h1 className="mb-4 text-4xl font-bold tracking-tight text-gray-900">
        {title}
      </h1>
      
      <div className="mb-6 flex items-center text-gray-600">
        <div className="flex items-center">
          <span className="mr-2 text-sm">By</span>
          <span className="font-medium">{author}</span>
        </div>
        <span className="mx-2">•</span>
        <span className="text-sm">{date}</span>
        
        {tags && tags.length > 0 && (
          <>
            <span className="mx-2">•</span>
            <div className="flex flex-wrap">
              {tags.map((tag) => (
                <Link
                  key={tag}
                  href={`/tags/${tag.toLowerCase()}/`}
                  className="mr-2 text-sm text-blue-600 hover:underline"
                >
                  #{tag}
                </Link>
              ))}
            </div>
          </>
        )}
      </div>
      
      {coverImage && (
        <div className="relative mb-8 h-72 w-full overflow-hidden rounded-lg sm:h-96">
          <Image
            src={coverImage}
            alt={title}
            fill
            sizes="(max-width: 768px) 100vw, 1200px"
            className="object-cover"
          />
        </div>
      )}
    </div>
  );
}

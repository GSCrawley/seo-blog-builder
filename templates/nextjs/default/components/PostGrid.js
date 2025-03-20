import PostPreview from './PostPreview';

export default function PostGrid({ posts }) {
  if (!posts || posts.length === 0) {
    return (
      <div className="text-center py-12">
        <h3 className="text-xl font-medium text-gray-600">No posts found</h3>
        <p className="mt-2 text-gray-500">Check back later for new content.</p>
      </div>
    );
  }

  return (
    <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
      {posts.map((post) => (
        <PostPreview key={post.slug} post={post} />
      ))}
    </div>
  );
}

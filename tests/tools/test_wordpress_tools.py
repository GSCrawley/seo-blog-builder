"""
Tests for WordPress tools.
"""
import unittest
from unittest.mock import patch, MagicMock
from app.tools.wordpress_tools import (
    CreatePostTool, CreateCategoryTool, CreateTagTool,
    UploadMediaTool, SetupBlogTool
)

class TestWordPressTools(unittest.TestCase):
    """Test cases for WordPress tools."""
    
    @patch('app.services.site_generation.wordpress_service.WordPressService')
    def test_create_post_tool(self, MockWordPressService):
        """Test the CreatePostTool."""
        # Mock WordPress service
        mock_service_instance = MockWordPressService.return_value
        mock_service_instance.create_post.return_value = {
            'id': 123,
            'title': {'rendered': 'Test Post'},
            'link': 'https://example.com/test-post'
        }
        
        # Create tool instance
        tool = CreatePostTool()
        
        # Execute the tool
        result = tool._run(
            site_key='test',
            title='Test Post',
            content='Test content',
            excerpt='Test excerpt',
            status='draft',
            categories=[1, 2],
            tags=[3, 4]
        )
        
        # Verify WordPress service was initialized correctly
        MockWordPressService.assert_called_once_with(site_key='test')
        
        # Verify create_post was called with correct parameters
        mock_service_instance.create_post.assert_called_once_with(
            title='Test Post',
            content='Test content',
            excerpt='Test excerpt',
            status='draft',
            categories=[1, 2],
            tags=[3, 4],
            featured_media_id=None
        )
        
        # Verify the result
        self.assertEqual(result['id'], 123)
        self.assertEqual(result['title']['rendered'], 'Test Post')
    
    @patch('app.services.site_generation.wordpress_service.WordPressService')
    def test_create_category_tool(self, MockWordPressService):
        """Test the CreateCategoryTool."""
        # Mock WordPress service
        mock_service_instance = MockWordPressService.return_value
        mock_service_instance.create_category.return_value = {
            'id': 45,
            'name': 'Test Category',
            'description': 'Test description'
        }
        
        # Create tool instance
        tool = CreateCategoryTool()
        
        # Execute the tool
        result = tool._run(
            site_key='test',
            name='Test Category',
            description='Test description',
            parent=0
        )
        
        # Verify WordPress service was initialized correctly
        MockWordPressService.assert_called_once_with(site_key='test')
        
        # Verify create_category was called with correct parameters
        mock_service_instance.create_category.assert_called_once_with(
            name='Test Category',
            description='Test description',
            parent=0
        )
        
        # Verify the result
        self.assertEqual(result['id'], 45)
        self.assertEqual(result['name'], 'Test Category')
    
    @patch('app.services.site_generation.wordpress_service.WordPressService')
    def test_create_tag_tool(self, MockWordPressService):
        """Test the CreateTagTool."""
        # Mock WordPress service
        mock_service_instance = MockWordPressService.return_value
        mock_service_instance.create_tag.return_value = {
            'id': 67,
            'name': 'Test Tag',
            'description': 'Test description'
        }
        
        # Create tool instance
        tool = CreateTagTool()
        
        # Execute the tool
        result = tool._run(
            site_key='test',
            name='Test Tag',
            description='Test description'
        )
        
        # Verify WordPress service was initialized correctly
        MockWordPressService.assert_called_once_with(site_key='test')
        
        # Verify create_tag was called with correct parameters
        mock_service_instance.create_tag.assert_called_once_with(
            name='Test Tag',
            description='Test description'
        )
        
        # Verify the result
        self.assertEqual(result['id'], 67)
        self.assertEqual(result['name'], 'Test Tag')
    
    @patch('app.services.site_generation.wordpress_service.WordPressService')
    def test_upload_media_tool(self, MockWordPressService):
        """Test the UploadMediaTool."""
        # Mock WordPress service
        mock_service_instance = MockWordPressService.return_value
        mock_service_instance.upload_media.return_value = {
            'id': 89,
            'title': {'rendered': 'Test Image'},
            'source_url': 'https://example.com/wp-content/uploads/test-image.jpg'
        }
        
        # Create tool instance
        tool = UploadMediaTool()
        
        # Execute the tool
        result = tool._run(
            site_key='test',
            file_path='/path/to/test-image.jpg',
            title='Test Image'
        )
        
        # Verify WordPress service was initialized correctly
        MockWordPressService.assert_called_once_with(site_key='test')
        
        # Verify upload_media was called with correct parameters
        mock_service_instance.upload_media.assert_called_once_with(
            file_path='/path/to/test-image.jpg',
            title='Test Image'
        )
        
        # Verify the result
        self.assertEqual(result['id'], 89)
        self.assertEqual(result['title']['rendered'], 'Test Image')
    
    @patch('app.services.site_generation.wordpress_service.WordPressService')
    def test_setup_blog_tool(self, MockWordPressService):
        """Test the SetupBlogTool."""
        # Mock WordPress service
        mock_service_instance = MockWordPressService.return_value
        mock_service_instance.setup_blog.return_value = {
            'status': 'success',
            'categories': {'Category 1': 10, 'Category 2': 11},
            'tags': {'Tag 1': 20, 'Tag 2': 21},
            'posts': [
                {'id': 100, 'title': 'Post 1', 'link': 'https://example.com/post-1'},
                {'id': 101, 'title': 'Post 2', 'link': 'https://example.com/post-2'}
            ]
        }
        
        # Create test blog data
        blog_data = {
            'categories': [
                {'name': 'Category 1', 'description': 'First category'},
                {'name': 'Category 2', 'description': 'Second category'}
            ],
            'tags': [
                {'name': 'Tag 1', 'description': 'First tag'},
                {'name': 'Tag 2', 'description': 'Second tag'}
            ],
            'posts': [
                {
                    'title': 'Post 1',
                    'content': 'Content of the first post',
                    'categories': ['Category 1'],
                    'tags': ['Tag 1']
                },
                {
                    'title': 'Post 2',
                    'content': 'Content of the second post',
                    'categories': ['Category 2'],
                    'tags': ['Tag 2']
                }
            ]
        }
        
        # Create tool instance
        tool = SetupBlogTool()
        
        # Execute the tool
        result = tool._run(
            site_key='test',
            blog_data=blog_data
        )
        
        # Verify WordPress service was initialized correctly
        MockWordPressService.assert_called_once_with(site_key='test')
        
        # Verify setup_blog was called with correct parameters
        mock_service_instance.setup_blog.assert_called_once_with(blog_data=blog_data)
        
        # Verify the result
        self.assertEqual(result['status'], 'success')
        self.assertEqual(len(result['posts']), 2)
        self.assertEqual(result['categories']['Category 1'], 10)
        self.assertEqual(result['tags']['Tag 1'], 20)

if __name__ == '__main__':
    unittest.main()

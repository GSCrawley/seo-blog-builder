"""
Tests for WordPress service.
"""
import unittest
from unittest.mock import patch, MagicMock, mock_open
import json
import os
from app.services.site_generation.wordpress_service import WordPressService

class TestWordPressService(unittest.TestCase):
    """Test cases for WordPressService."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock site configuration
        self.mock_site_config = {
            "URL": "https://test-blog.example.com/wp-json",
            "USER": "test_user",
            "PASS": "test_password",
            "authType": "basic"
        }
        
        # Create a patch for settings.WP_SITES
        self.settings_patch = patch('app.config.settings.WP_SITES', {
            'test': self.mock_site_config
        })
        self.mock_settings = self.settings_patch.start()
        
        # Initialize the service with our test site
        self.service = WordPressService(site_key='test')
    
    def tearDown(self):
        """Tear down test fixtures."""
        self.settings_patch.stop()
    
    @patch('requests.post')
    def test_create_post(self, mock_post):
        """Test creating a post."""
        # Mock response data
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'id': 123,
            'title': {'rendered': 'Test Post'},
            'content': {'rendered': '<p>This is a test post.</p>'},
            'link': 'https://test-blog.example.com/test-post'
        }
        mock_post.return_value = mock_response
        mock_response.raise_for_status = MagicMock()
        
        # Call the create_post method
        result = self.service.create_post(
            title="Test Post",
            content="This is a test post.",
            excerpt="Test excerpt",
            status="draft"
        )
        
        # Assert that the correct endpoint was called
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['json']['title'], "Test Post")
        self.assertEqual(kwargs['json']['content'], "This is a test post.")
        self.assertEqual(kwargs['json']['excerpt'], "Test excerpt")
        self.assertEqual(kwargs['json']['status'], "draft")
        
        # Assert that the response was processed correctly
        self.assertEqual(result['id'], 123)
        self.assertEqual(result['title']['rendered'], 'Test Post')
    
    @patch('requests.post')
    def test_create_category(self, mock_post):
        """Test creating a category."""
        # Mock response data
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'id': 45,
            'name': 'Test Category',
            'description': 'A test category',
            'count': 0
        }
        mock_post.return_value = mock_response
        mock_response.raise_for_status = MagicMock()
        
        # Call the create_category method
        result = self.service.create_category(
            name="Test Category",
            description="A test category"
        )
        
        # Assert that the correct endpoint was called
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['json']['name'], "Test Category")
        self.assertEqual(kwargs['json']['description'], "A test category")
        
        # Assert that the response was processed correctly
        self.assertEqual(result['id'], 45)
        self.assertEqual(result['name'], 'Test Category')
    
    @patch('requests.post')
    def test_create_tag(self, mock_post):
        """Test creating a tag."""
        # Mock response data
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'id': 67,
            'name': 'Test Tag',
            'description': 'A test tag',
            'count': 0
        }
        mock_post.return_value = mock_response
        mock_response.raise_for_status = MagicMock()
        
        # Call the create_tag method
        result = self.service.create_tag(
            name="Test Tag",
            description="A test tag"
        )
        
        # Assert that the correct endpoint was called
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['json']['name'], "Test Tag")
        self.assertEqual(kwargs['json']['description'], "A test tag")
        
        # Assert that the response was processed correctly
        self.assertEqual(result['id'], 67)
        self.assertEqual(result['name'], 'Test Tag')
    
    @patch('requests.post')
    @patch('builtins.open', new_callable=mock_open, read_data=b'test file content')
    def test_upload_media(self, mock_file, mock_post):
        """Test uploading media."""
        # Mock response data
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'id': 89,
            'title': {'rendered': 'test-image.jpg'},
            'source_url': 'https://test-blog.example.com/wp-content/uploads/test-image.jpg'
        }
        mock_post.return_value = mock_response
        mock_response.raise_for_status = MagicMock()
        
        # Call the upload_media method
        result = self.service.upload_media(
            file_path="test-image.jpg",
            title="Test Image"
        )
        
        # Assert that the file was opened
        mock_file.assert_called_once_with("test-image.jpg", 'rb')
        
        # Assert that the post request was made with files
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertIn('files', kwargs)
        
        # Assert that the response was processed correctly
        self.assertEqual(result['id'], 89)
        self.assertEqual(result['title']['rendered'], 'test-image.jpg')
    
    @patch('app.services.site_generation.wordpress_service.WordPressService.create_category')
    @patch('app.services.site_generation.wordpress_service.WordPressService.create_tag')
    @patch('app.services.site_generation.wordpress_service.WordPressService.create_post')
    def test_setup_blog(self, mock_create_post, mock_create_tag, mock_create_category):
        """Test setting up a complete blog."""
        # Mock responses
        mock_create_category.side_effect = [
            {'id': 10, 'name': 'Category 1'},
            {'id': 11, 'name': 'Category 2'}
        ]
        
        mock_create_tag.side_effect = [
            {'id': 20, 'name': 'Tag 1'},
            {'id': 21, 'name': 'Tag 2'}
        ]
        
        mock_create_post.side_effect = [
            {
                'id': 100, 
                'title': {'rendered': 'Post 1'}, 
                'link': 'https://test-blog.example.com/post-1'
            },
            {
                'id': 101, 
                'title': {'rendered': 'Post 2'}, 
                'link': 'https://test-blog.example.com/post-2'
            }
        ]
        
        # Create blog data
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
                    'excerpt': 'Post 1 excerpt',
                    'categories': ['Category 1'],
                    'tags': ['Tag 1']
                },
                {
                    'title': 'Post 2',
                    'content': 'Content of the second post',
                    'excerpt': 'Post 2 excerpt',
                    'categories': ['Category 2'],
                    'tags': ['Tag 2']
                }
            ]
        }
        
        # Call the setup_blog method
        result = self.service.setup_blog(blog_data)
        
        # Assert that category creation was called correctly
        self.assertEqual(mock_create_category.call_count, 2)
        mock_create_category.assert_any_call(
            name='Category 1',
            description='First category',
            parent=0
        )
        
        # Assert that tag creation was called correctly
        self.assertEqual(mock_create_tag.call_count, 2)
        mock_create_tag.assert_any_call(
            name='Tag 1',
            description='First tag'
        )
        
        # Assert that post creation was called correctly
        self.assertEqual(mock_create_post.call_count, 2)
        
        # Assert that the results are structured correctly
        self.assertEqual(result['status'], 'success')
        self.assertEqual(len(result['categories']), 2)
        self.assertEqual(len(result['tags']), 2)
        self.assertEqual(len(result['posts']), 2)
        
        # Verify post IDs in the result
        post_ids = [post['id'] for post in result['posts']]
        self.assertIn(100, post_ids)
        self.assertIn(101, post_ids)

if __name__ == '__main__':
    unittest.main()

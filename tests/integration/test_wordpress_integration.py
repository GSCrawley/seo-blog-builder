"""
Integration tests for WordPress service.
"""
import unittest
import os
import json
import time
from unittest.mock import patch
import threading
import http.server
import socketserver

from app.services.site_generation.wordpress_service import WordPressService
from app.config import settings

# Mock WordPress REST API server
class MockWordPressHandler(http.server.SimpleHTTPRequestHandler):
    """
    Simple handler for mock WordPress REST API.
    """
    def do_POST(self):
        """Handle POST requests."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data) if post_data else {}
        
        # Handle different endpoints
        if self.path == '/wp-json/wp/v2/posts':
            self._handle_create_post(data)
        elif self.path == '/wp-json/wp/v2/categories':
            self._handle_create_category(data)
        elif self.path == '/wp-json/wp/v2/tags':
            self._handle_create_tag(data)
        elif self.path == '/wp-json/wp/v2/media':
            self._handle_upload_media(data)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())
    
    def _handle_create_post(self, data):
        """Handle post creation."""
        # Simulate creating a post and returning a response
        response = {
            'id': 123,
            'title': {'rendered': data.get('title', '')},
            'content': {'rendered': data.get('content', '')},
            'excerpt': {'rendered': data.get('excerpt', '')},
            'status': data.get('status', 'draft'),
            'link': f'https://example.com/{data.get("title", "").lower().replace(" ", "-")}'
        }
        
        self.send_response(201)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def _handle_create_category(self, data):
        """Handle category creation."""
        # Simulate creating a category and returning a response
        response = {
            'id': 45,
            'name': data.get('name', ''),
            'description': data.get('description', ''),
            'parent': data.get('parent', 0),
            'count': 0
        }
        
        self.send_response(201)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def _handle_create_tag(self, data):
        """Handle tag creation."""
        # Simulate creating a tag and returning a response
        response = {
            'id': 67,
            'name': data.get('name', ''),
            'description': data.get('description', ''),
            'count': 0
        }
        
        self.send_response(201)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def _handle_upload_media(self, data):
        """Handle media upload."""
        # Simulate uploading media and returning a response
        response = {
            'id': 89,
            'title': {'rendered': 'Uploaded Media'},
            'source_url': 'https://example.com/wp-content/uploads/test-image.jpg'
        }
        
        self.send_response(201)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        """Suppress logging in tests."""
        return

@unittest.skipIf(
    os.environ.get('SKIP_INTEGRATION_TESTS', 'True').lower() == 'true',
    'Skipping integration tests by default'
)
class TestWordPressIntegration(unittest.TestCase):
    """Integration tests for WordPress service."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the mock WordPress server."""
        # Set up a mock WordPress server
        cls.mock_server_port = 8088
        cls.handler = MockWordPressHandler
        cls.httpd = socketserver.TCPServer(("", cls.mock_server_port), cls.handler)
        
        # Start server in a thread
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        
        # Give the server time to start
        time.sleep(0.5)
    
    @classmethod
    def tearDownClass(cls):
        """Shut down the mock WordPress server."""
        # Shut down the server
        cls.httpd.shutdown()
        cls.server_thread.join()
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a patch for settings.WP_SITES
        self.mock_site_config = {
            "URL": f"http://localhost:{self.mock_server_port}/wp-json",
            "USER": "test_user",
            "PASS": "test_password",
            "authType": "basic"
        }
        
        self.settings_patch = patch('app.config.settings.WP_SITES', {
            'test': self.mock_site_config
        })
        self.mock_settings = self.settings_patch.start()
        
        # Initialize the service with our test site
        self.service = WordPressService(site_key='test')
    
    def tearDown(self):
        """Tear down test fixtures."""
        self.settings_patch.stop()
    
    def test_create_post(self):
        """Test creating a post with mock server."""
        # Create a post
        post = self.service.create_post(
            title="Integration Test Post",
            content="This is a test post for integration testing.",
            excerpt="Test excerpt",
            status="draft"
        )
        
        # Verify the response
        self.assertEqual(post['id'], 123)
        self.assertEqual(post['title']['rendered'], "Integration Test Post")
        self.assertEqual(post['status'], "draft")
    
    def test_create_category(self):
        """Test creating a category with mock server."""
        # Create a category
        category = self.service.create_category(
            name="Integration Test Category",
            description="Test category description",
            parent=0
        )
        
        # Verify the response
        self.assertEqual(category['id'], 45)
        self.assertEqual(category['name'], "Integration Test Category")
        self.assertEqual(category['description'], "Test category description")
    
    def test_create_tag(self):
        """Test creating a tag with mock server."""
        # Create a tag
        tag = self.service.create_tag(
            name="Integration Test Tag",
            description="Test tag description"
        )
        
        # Verify the response
        self.assertEqual(tag['id'], 67)
        self.assertEqual(tag['name'], "Integration Test Tag")
        self.assertEqual(tag['description'], "Test tag description")

if __name__ == '__main__':
    unittest.main()

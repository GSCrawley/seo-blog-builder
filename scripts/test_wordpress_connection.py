#!/usr/bin/env python
"""
Script to test WordPress connection and basic operations.
"""
import sys
import os
import json
import argparse
import logging

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import after path is set
from app.services.site_generation.wordpress_service import WordPressService
from app.config import settings

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_connection(site_key):
    """
    Test connection to WordPress site.
    
    Args:
        site_key: Key for the WordPress site in configuration
    """
    logger.info(f"Testing connection to WordPress site: {site_key}")
    
    if site_key not in settings.WP_SITES:
        logger.error(f"WordPress site not found in configuration: {site_key}")
        logger.info(f"Available sites: {list(settings.WP_SITES.keys())}")
        return False
    
    # Get site config
    site_config = settings.WP_SITES[site_key]
    logger.info(f"Site URL: {site_config['URL']}")
    
    try:
        # Create WordPress service
        wp_service = WordPressService(site_key=site_key)
        logger.info("WordPress service created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating WordPress service: {e}")
        return False

def test_operations(site_key):
    """
    Test basic WordPress operations.
    
    Args:
        site_key: Key for the WordPress site in configuration
    """
    try:
        # Create WordPress service
        wp_service = WordPressService(site_key=site_key)
        
        # Create a test category
        logger.info("Creating test category...")
        category = wp_service.create_category(
            name="Test Category",
            description="A test category created by the SEO Blog Builder"
        )
        logger.info(f"Category created: ID={category['id']}, Name={category['name']}")
        
        # Create a test tag
        logger.info("Creating test tag...")
        tag = wp_service.create_tag(
            name="Test Tag",
            description="A test tag created by the SEO Blog Builder"
        )
        logger.info(f"Tag created: ID={tag['id']}, Name={tag['name']}")
        
        # Create a test post
        logger.info("Creating test post...")
        post = wp_service.create_post(
            title="Test Post from SEO Blog Builder",
            content="<p>This is a test post created by the SEO Blog Builder application.</p>",
            excerpt="Test post excerpt",
            status="draft",
            categories=[category['id']],
            tags=[tag['id']]
        )
        logger.info(f"Post created: ID={post['id']}, Title={post['title']['rendered']}")
        logger.info(f"Post URL: {post['link']}")
        
        return True
    except Exception as e:
        logger.error(f"Error during operations test: {e}")
        return False

def test_full_blog_setup(site_key):
    """
    Test full blog setup.
    
    Args:
        site_key: Key for the WordPress site in configuration
    """
    try:
        # Create WordPress service
        wp_service = WordPressService(site_key=site_key)
        
        # Create blog data
        blog_data = {
            'categories': [
                {'name': 'Technology', 'description': 'Technology articles'},
                {'name': 'Marketing', 'description': 'Marketing strategies'},
                {'name': 'SEO', 'description': 'Search Engine Optimization tips'}
            ],
            'tags': [
                {'name': 'WordPress', 'description': 'WordPress related'},
                {'name': 'Blogging', 'description': 'Blogging tips'},
                {'name': 'AI', 'description': 'Artificial Intelligence'}
            ],
            'posts': [
                {
                    'title': 'Getting Started with WordPress',
                    'content': '<p>This is a test post about WordPress.</p>',
                    'excerpt': 'Learn how to get started with WordPress',
                    'categories': ['Technology'],
                    'tags': ['WordPress', 'Blogging']
                },
                {
                    'title': 'SEO Tips for Beginners',
                    'content': '<p>This is a test post about SEO.</p>',
                    'excerpt': 'Essential SEO tips for beginners',
                    'categories': ['SEO'],
                    'tags': ['Blogging']
                }
            ]
        }
        
        # Set up the blog
        logger.info("Setting up test blog...")
        result = wp_service.setup_blog(blog_data)
        
        if result['status'] == 'success':
            logger.info("Blog setup successful!")
            logger.info(f"Created {len(result['categories'])} categories")
            logger.info(f"Created {len(result['tags'])} tags")
            logger.info(f"Created {len(result['posts'])} posts")
            
            # Print post URLs
            for post in result['posts']:
                logger.info(f"Post: {post['title']} - URL: {post['link']}")
            
            return True
        else:
            logger.error(f"Blog setup failed: {result.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        logger.error(f"Error during full blog setup test: {e}")
        return False

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Test WordPress integration.')
    parser.add_argument('--site-key', '-s', default='default', 
                        help='WordPress site key in configuration')
    parser.add_argument('--test', '-t', choices=['connection', 'operations', 'full'],
                        default='connection', help='Test to run')
    args = parser.parse_args()
    
    if args.test == 'connection':
        success = test_connection(args.site_key)
    elif args.test == 'operations':
        success = test_operations(args.site_key)
    elif args.test == 'full':
        success = test_full_blog_setup(args.site_key)
    
    if success:
        logger.info("Test completed successfully")
        return 0
    else:
        logger.error("Test failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())

"""
Static site generation service for creating and deploying Next.js-based blogs.
"""
import logging
import os
import shutil
import subprocess
import json
import tempfile
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
import requests

from app.config import settings
from app.models.static_site import StaticSite, SiteStatus, DeploymentProvider, Deployment
from app.models.content import ContentItem, ContentStatus
from app.utils.helpers import slugify

logger = logging.getLogger(__name__)

class StaticSiteGenerationService:
    """
    Service for generating and deploying static Next.js-based blog sites.
    """
    
    def __init__(self):
        """Initialize the static site generation service."""
        self.templates_dir = settings.TEMPLATES_DIR
        self.sites_dir = settings.SITES_DIR
        self.default_domain = settings.DEFAULT_DOMAIN
        
    def create_site(self, project_id: str, site_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new static site project structure.
        
        Args:
            project_id: Unique identifier for the project
            site_config: Configuration for the site including title, description, niche, etc.
            
        Returns:
            Dict: Information about the created site
        """
        logger.info(f"Creating static site for project {project_id}")
        
        try:
            # Generate a unique identifier for the site
            site_id = f"SITE-{uuid.uuid4().hex[:8].upper()}"
            
            # Set up subdomain
            subdomain = site_config.get('subdomain', None)
            if not subdomain:
                # Generate subdomain from title if not provided
                subdomain = slugify(site_config.get('title', f'site-{site_id.lower()}'))
            
            # Select template
            template_id = site_config.get('template_id', 'default')
            template_path = os.path.join(self.templates_dir, template_id)
            
            if not os.path.exists(template_path):
                logger.error(f"Template {template_id} not found")
                return {
                    "success": False,
                    "error": f"Template {template_id} not found",
                    "message": "Failed to create site: template not found"
                }
            
            # Create site directory
            site_path = os.path.join(self.sites_dir, subdomain)
            os.makedirs(site_path, exist_ok=True)
            
            # Copy template to site directory
            self._copy_template(template_path, site_path)
            
            # Configure site (package.json, next.config.js, etc.)
            self._configure_site(site_path, site_config)
            
            # Create initial content structure
            self._initialize_content_structure(site_path)
            
            # Return site information
            site_info = {
                "success": True,
                "site_id": site_id,
                "subdomain": subdomain,
                "title": site_config.get('title'),
                "template_id": template_id,
                "site_path": site_path,
                "status": SiteStatus.PLANNING
            }
            
            logger.info(f"Successfully created static site structure for {subdomain}")
            return site_info
            
        except Exception as e:
            logger.error(f"Error creating static site: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create static site"
            }
    
    def _copy_template(self, template_path: str, site_path: str) -> None:
        """
        Copy template files to the site directory.
        
        Args:
            template_path: Path to the template directory
            site_path: Path to the site directory
        """
        logger.info(f"Copying template from {template_path} to {site_path}")
        
        # Copy all files except node_modules and .next
        for item in os.listdir(template_path):
            if item in ['node_modules', '.next', '.git']:
                continue
                
            source = os.path.join(template_path, item)
            destination = os.path.join(site_path, item)
            
            if os.path.isdir(source):
                shutil.copytree(source, destination, dirs_exist_ok=True)
            else:
                shutil.copy2(source, destination)
    
    def _configure_site(self, site_path: str, site_config: Dict[str, Any]) -> None:
        """
        Configure the site files with the provided configuration.
        
        Args:
            site_path: Path to the site directory
            site_config: Configuration for the site
        """
        logger.info(f"Configuring site at {site_path}")
        
        # Update package.json
        package_path = os.path.join(site_path, 'package.json')
        if os.path.exists(package_path):
            with open(package_path, 'r') as f:
                package_data = json.load(f)
                
            # Update name and description
            package_data['name'] = slugify(site_config.get('title', 'seo-blog'))
            package_data['description'] = site_config.get('description', 'An SEO-optimized blog')
            
            # Write updated package.json
            with open(package_path, 'w') as f:
                json.dump(package_data, f, indent=2)
        
        # Update site configuration
        site_config_path = os.path.join(site_path, 'site.config.js')
        if os.path.exists(site_config_path):
            with open(site_config_path, 'r') as f:
                config_content = f.read()
            
            # Replace configuration values
            replacements = {
                "'SITE_TITLE'": f"'{site_config.get('title', 'SEO Blog')}'",
                "'SITE_DESCRIPTION'": f"'{site_config.get('description', 'An SEO-optimized blog')}'",
                "'SITE_URL'": f"'https://{site_config.get('subdomain')}.{self.default_domain}'",
                "'DEFAULT_AUTHOR'": f"'{site_config.get('author', 'Content Creator')}'",
                "'PRIMARY_COLOR'": f"'{site_config.get('primary_color', '#3498db')}'",
                "'SECONDARY_COLOR'": f"'{site_config.get('secondary_color', '#2ecc71')}'",
                "'GOOGLE_ANALYTICS_ID'": f"'{site_config.get('google_analytics_id', '')}'",
            }
            
            for key, value in replacements.items():
                config_content = config_content.replace(key, value)
            
            # Write updated configuration
            with open(site_config_path, 'w') as f:
                f.write(config_content)
        
        # Create or update .env.local for environment variables
        env_path = os.path.join(site_path, '.env.local')
        with open(env_path, 'w') as f:
            f.write(f"NEXT_PUBLIC_SITE_TITLE={site_config.get('title', 'SEO Blog')}\n")
            f.write(f"NEXT_PUBLIC_SITE_DESCRIPTION={site_config.get('description', 'An SEO-optimized blog')}\n")
            f.write(f"NEXT_PUBLIC_SITE_URL=https://{site_config.get('subdomain')}.{self.default_domain}\n")
            if site_config.get('google_analytics_id'):
                f.write(f"NEXT_PUBLIC_GA_ID={site_config.get('google_analytics_id')}\n")
    
    def _initialize_content_structure(self, site_path: str) -> None:
        """
        Initialize the content directory structure.
        
        Args:
            site_path: Path to the site directory
        """
        logger.info(f"Initializing content structure at {site_path}")
        
        # Create content directories
        content_path = os.path.join(site_path, 'content')
        os.makedirs(content_path, exist_ok=True)
        
        # Create subdirectories for different content types
        for content_type in ['posts', 'pages', 'products']:
            os.makedirs(os.path.join(content_path, content_type), exist_ok=True)
        
        # Create assets directory for images
        assets_path = os.path.join(site_path, 'public', 'assets')
        os.makedirs(assets_path, exist_ok=True)
        
        # Create initial placeholder content
        placeholder_post = os.path.join(content_path, 'posts', 'hello-world.mdx')
        with open(placeholder_post, 'w') as f:
            f.write("""---
title: Hello World
description: Welcome to your new blog
date: '2023-01-01'
tags: ['welcome', 'introduction']
draft: false
---

# Welcome to Your New Blog

This is a placeholder post that will be replaced with your actual content.
""")

    def add_content(self, site_id: str, content_item: ContentItem) -> Dict[str, Any]:
        """
        Add a content item to the static site.
        
        Args:
            site_id: Unique identifier for the site
            content_item: Content item to add to the site
            
        Returns:
            Dict: Information about the added content
        """
        logger.info(f"Adding content {content_item.id} to site {site_id}")
        
        try:
            # Get site information
            # In a real implementation, this would come from the database
            site = self._get_site_by_id(site_id)
            
            if not site:
                logger.error(f"Site {site_id} not found")
                return {
                    "success": False,
                    "error": f"Site {site_id} not found",
                    "message": "Failed to add content: site not found"
                }
            
            # Determine content directory based on content type
            content_dir = 'posts'
            if content_item.content_type in ['LANDING_PAGE', 'ABOUT_PAGE', 'HOMEPAGE']:
                content_dir = 'pages'
            elif content_item.content_type in ['PRODUCT_REVIEW']:
                content_dir = 'products'
            
            # Create content file path
            content_path = os.path.join(site['site_path'], 'content', content_dir, f"{content_item.slug}.mdx")
            
            # Create frontmatter
            frontmatter = {
                "title": content_item.title,
                "description": content_item.meta_description or content_item.summary,
                "date": content_item.publish_date.isoformat() if content_item.publish_date else datetime.now().isoformat(),
                "tags": content_item.tags or [],
                "categories": content_item.categories or [],
                "author": content_item.author or "Content Creator",
                "featuredImage": content_item.featured_image,
                "seoKeywords": [content_item.primary_keyword] + (content_item.secondary_keywords or []),
                "draft": content_item.status != ContentStatus.PUBLISHED
            }
            
            # Filter out None values from frontmatter
            frontmatter = {k: v for k, v in frontmatter.items() if v is not None}
            
            # Write content file with frontmatter and markdown content
            with open(content_path, 'w') as f:
                f.write("---\n")
                f.write(json.dumps(frontmatter, indent=2))
                f.write("\n---\n\n")
                f.write(content_item.markdown_content or "")
            
            # Update content item with file path information
            content_update = {
                "content_path": content_path,
                "frontmatter": frontmatter,
                "status": ContentStatus.PUBLISHED if content_item.status == ContentStatus.READY else content_item.status
            }
            
            logger.info(f"Successfully added content {content_item.id} to site {site_id}")
            return {
                "success": True,
                "content_id": content_item.id,
                "content_path": content_path,
                "updates": content_update
            }
            
        except Exception as e:
            logger.error(f"Error adding content to site: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to add content to site"
            }
    
    def build_site(self, site_id: str) -> Dict[str, Any]:
        """
        Build the static site for production.
        
        Args:
            site_id: Unique identifier for the site
            
        Returns:
            Dict: Information about the build process
        """
        logger.info(f"Building static site {site_id}")
        
        try:
            # Get site information
            site = self._get_site_by_id(site_id)
            
            if not site:
                logger.error(f"Site {site_id} not found")
                return {
                    "success": False,
                    "error": f"Site {site_id} not found",
                    "message": "Failed to build site: site not found"
                }
            
            # Change to site directory
            current_dir = os.getcwd()
            os.chdir(site['site_path'])
            
            # Install dependencies
            logger.info(f"Installing dependencies for site {site_id}")
            subprocess.run(['npm', 'install'], check=True, capture_output=True)
            
            # Build site
            logger.info(f"Building static site {site_id}")
            build_process = subprocess.run(['npm', 'run', 'build'], check=True, capture_output=True)
            
            # Change back to original directory
            os.chdir(current_dir)
            
            # Record build information
            build_info = {
                "success": True,
                "site_id": site_id,
                "build_output": build_process.stdout.decode(),
                "build_errors": build_process.stderr.decode(),
                "build_time": datetime.now().isoformat(),
                "build_status": "success",
                "output_dir": os.path.join(site['site_path'], 'out')
            }
            
            logger.info(f"Successfully built static site {site_id}")
            return build_info
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error building static site: {e.stderr.decode()}")
            return {
                "success": False,
                "error": e.stderr.decode(),
                "message": "Failed to build static site"
            }
        except Exception as e:
            logger.error(f"Error building static site: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to build static site"
            }
    
    def deploy_site(self, site_id: str, deployment_provider: DeploymentProvider = DeploymentProvider.VERCEL) -> Dict[str, Any]:
        """
        Deploy the static site to the specified provider.
        
        Args:
            site_id: Unique identifier for the site
            deployment_provider: Provider to deploy to
            
        Returns:
            Dict: Information about the deployment
        """
        logger.info(f"Deploying static site {site_id} to {deployment_provider}")
        
        try:
            # Get site information
            site = self._get_site_by_id(site_id)
            
            if not site:
                logger.error(f"Site {site_id} not found")
                return {
                    "success": False,
                    "error": f"Site {site_id} not found",
                    "message": "Failed to deploy site: site not found"
                }
            
            # Build site if it hasn't been built yet
            if not os.path.exists(os.path.join(site['site_path'], 'out')):
                build_result = self.build_site(site_id)
                if not build_result['success']:
                    return build_result
            
            # Deploy to selected provider
            if deployment_provider == DeploymentProvider.VERCEL:
                deployment_result = self._deploy_to_vercel(site)
            elif deployment_provider == DeploymentProvider.NETLIFY:
                deployment_result = self._deploy_to_netlify(site)
            else:
                logger.error(f"Unsupported deployment provider: {deployment_provider}")
                return {
                    "success": False,
                    "error": f"Unsupported deployment provider: {deployment_provider}",
                    "message": "Failed to deploy site: unsupported provider"
                }
            
            logger.info(f"Successfully deployed static site {site_id} to {deployment_provider}")
            return deployment_result
            
        except Exception as e:
            logger.error(f"Error deploying static site: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to deploy static site"
            }
    
    def _deploy_to_vercel(self, site: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deploy the static site to Vercel.
        
        Args:
            site: Site information
            
        Returns:
            Dict: Information about the Vercel deployment
        """
        logger.info(f"Deploying site {site['site_id']} to Vercel")
        
        try:
            # Check for required environment variables
            vercel_token = settings.VERCEL_TOKEN
            if not vercel_token:
                logger.error("Vercel API token not found in settings")
                return {
                    "success": False,
                    "error": "Vercel API token not configured",
                    "message": "Failed to deploy to Vercel: missing API token"
                }
            
            # Create deployment via Vercel API
            headers = {
                "Authorization": f"Bearer {vercel_token}",
                "Content-Type": "application/json"
            }
            
            # Prepare the deployment payload
            deployment_data = {
                "name": site['subdomain'],
                "target": "production",
                "source": "upload",
                "meta": {
                    "siteId": site['site_id'],
                    "type": "static-next-site"
                }
            }
            
            # Create the deployment
            response = requests.post(
                "https://api.vercel.com/v13/deployments",
                headers=headers,
                json=deployment_data
            )
            
            if response.status_code != 200:
                logger.error(f"Error creating Vercel deployment: {response.text}")
                return {
                    "success": False,
                    "error": response.text,
                    "message": "Failed to create Vercel deployment"
                }
            
            deployment = response.json()
            
            # Upload the files
            upload_url = deployment.get("upload", {}).get("url")
            if not upload_url:
                logger.error("No upload URL provided by Vercel")
                return {
                    "success": False,
                    "error": "No upload URL provided",
                    "message": "Failed to deploy to Vercel: no upload URL"
                }
            
            # Create a zip file of the build output
            output_dir = os.path.join(site['site_path'], 'out')
            zip_file_path = os.path.join(tempfile.gettempdir(), f"{site['site_id']}.zip")
            
            shutil.make_archive(
                zip_file_path.replace('.zip', ''),
                'zip',
                output_dir
            )
            
            # Upload the zip file
            with open(zip_file_path, 'rb') as f:
                upload_response = requests.put(
                    upload_url,
                    data=f,
                    headers={
                        "Content-Type": "application/zip"
                    }
                )
            
            if upload_response.status_code not in [200, 201, 202, 204]:
                logger.error(f"Error uploading files to Vercel: {upload_response.text}")
                return {
                    "success": False,
                    "error": upload_response.text,
                    "message": "Failed to upload files to Vercel"
                }
            
            # Clean up the zip file
            os.remove(zip_file_path)
            
            # Wait for deployment to complete
            deployment_id = deployment.get("id")
            deployment_url = deployment.get("url")
            
            logger.info(f"Vercel deployment created with ID: {deployment_id}")
            
            # Return deployment information
            return {
                "success": True,
                "deployment_id": deployment_id,
                "deployment_url": f"https://{deployment_url}",
                "provider": "vercel",
                "status": "deployed"
            }
            
        except Exception as e:
            logger.error(f"Error deploying to Vercel: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to deploy to Vercel"
            }
    
    def _deploy_to_netlify(self, site: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deploy the static site to Netlify.
        
        Args:
            site: Site information
            
        Returns:
            Dict: Information about the Netlify deployment
        """
        logger.info(f"Deploying site {site['site_id']} to Netlify")
        
        try:
            # Check for required environment variables
            netlify_token = settings.NETLIFY_TOKEN
            if not netlify_token:
                logger.error("Netlify API token not found in settings")
                return {
                    "success": False,
                    "error": "Netlify API token not configured",
                    "message": "Failed to deploy to Netlify: missing API token"
                }
            
            # Create a zip file of the build output
            output_dir = os.path.join(site['site_path'], 'out')
            zip_file_path = os.path.join(tempfile.gettempdir(), f"{site['site_id']}.zip")
            
            shutil.make_archive(
                zip_file_path.replace('.zip', ''),
                'zip',
                output_dir
            )
            
            # Create or get site on Netlify
            headers = {
                "Authorization": f"Bearer {netlify_token}",
                "Content-Type": "application/json"
            }
            
            # Check if site already exists
            site_name = f"{site['subdomain']}-{site['site_id'].lower()}"
            site_response = requests.get(
                f"https://api.netlify.com/api/v1/sites?name={site_name}",
                headers=headers
            )
            
            netlify_site_id = None
            
            if site_response.status_code == 200 and site_response.json():
                netlify_site_id = site_response.json()[0].get("id")
            else:
                # Create new site
                create_site_response = requests.post(
                    "https://api.netlify.com/api/v1/sites",
                    headers=headers,
                    json={
                        "name": site_name,
                        "custom_domain": f"{site['subdomain']}.{self.default_domain}" if self.default_domain else None
                    }
                )
                
                if create_site_response.status_code not in [200, 201]:
                    logger.error(f"Error creating Netlify site: {create_site_response.text}")
                    return {
                        "success": False,
                        "error": create_site_response.text,
                        "message": "Failed to create Netlify site"
                    }
                
                netlify_site_id = create_site_response.json().get("id")
            
            # Deploy the site
            with open(zip_file_path, 'rb') as f:
                deploy_response = requests.post(
                    f"https://api.netlify.com/api/v1/sites/{netlify_site_id}/deploys",
                    headers={
                        "Authorization": f"Bearer {netlify_token}",
                        "Content-Type": "application/zip"
                    },
                    data=f
                )
            
            # Clean up the zip file
            os.remove(zip_file_path)
            
            if deploy_response.status_code not in [200, 201]:
                logger.error(f"Error deploying to Netlify: {deploy_response.text}")
                return {
                    "success": False,
                    "error": deploy_response.text,
                    "message": "Failed to deploy to Netlify"
                }
            
            deployment = deploy_response.json()
            
            # Return deployment information
            return {
                "success": True,
                "deployment_id": deployment.get("id"),
                "deployment_url": deployment.get("ssl_url") or deployment.get("url"),
                "netlify_site_id": netlify_site_id,
                "provider": "netlify",
                "status": "deployed"
            }
            
        except Exception as e:
            logger.error(f"Error deploying to Netlify: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to deploy to Netlify"
            }
    
    def _get_site_by_id(self, site_id: str) -> Optional[Dict[str, Any]]:
        """
        Get site information by ID.
        In a real implementation, this would query the database.
        For now, we'll use a placeholder implementation.
        
        Args:
            site_id: Unique identifier for the site
            
        Returns:
            Optional[Dict]: Site information or None if not found
        """
        # This is a placeholder. In a real implementation, we would query the database.
        # For testing purposes, we'll look for the site directory based on the ID pattern
        
        # Find the site directory
        for subdomain in os.listdir(self.sites_dir):
            site_path = os.path.join(self.sites_dir, subdomain)
            if os.path.isdir(site_path):
                # For testing, we'll assume the directory name matches the site ID
                # In a real implementation, we would query the database
                if site_id.lower() in subdomain.lower():
                    return {
                        "site_id": site_id,
                        "subdomain": subdomain,
                        "site_path": site_path
                    }
        
        return None

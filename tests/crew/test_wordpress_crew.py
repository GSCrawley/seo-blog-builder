"""
Tests for WordPress crew configuration.
"""
import unittest
from unittest.mock import patch, MagicMock
from crewai import Crew, Task, Agent

from app.crew.crew_manager import CrewManager

class TestWordPressCrew(unittest.TestCase):
    """Test cases for WordPress crew configuration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.crew_manager = CrewManager()
    
    @patch('app.crew.agent_factory.AgentFactory')
    @patch('app.crew.tasks.TaskFactory')
    def test_create_wordpress_crew(self, MockTaskFactory, MockAgentFactory):
        """Test creating a WordPress crew."""
        # Mock agents
        mock_wp_agent = MagicMock(spec=Agent)
        mock_design_agent = MagicMock(spec=Agent)
        mock_seo_agent = MagicMock(spec=Agent)
        mock_qa_agent = MagicMock(spec=Agent)
        
        # Mock agent factory
        mock_agent_factory = MockAgentFactory.return_value
        mock_agent_factory.create_wordpress_setup_agent.return_value = mock_wp_agent
        mock_agent_factory.create_design_implementation_agent.return_value = mock_design_agent
        mock_agent_factory.create_seo_strategy_agent.return_value = mock_seo_agent
        mock_agent_factory.create_testing_qa_agent.return_value = mock_qa_agent
        
        # Mock tasks
        mock_setup_task = MagicMock(spec=Task)
        mock_publishing_task = MagicMock(spec=Task)
        
        # Mock task factory
        mock_task_factory = MockTaskFactory.return_value
        mock_task_factory.create_wordpress_setup_task.return_value = mock_setup_task
        mock_task_factory.create_wordpress_publishing_task.return_value = mock_publishing_task
        
        # Replace instance attributes with mocks
        self.crew_manager.agent_factory = mock_agent_factory
        self.crew_manager.task_factory = mock_task_factory
        
        # Test site data
        site_data = {
            'site_name': 'Test Blog',
            'domain': 'testblog.com'
        }
        
        # Test content data
        content_data = {
            'content_pieces': [
                {
                    'title': 'Test Post 1',
                    'content': 'Content for test post 1',
                    'excerpt': 'Excerpt for test post 1'
                },
                {
                    'title': 'Test Post 2',
                    'content': 'Content for test post 2',
                    'excerpt': 'Excerpt for test post 2'
                }
            ]
        }
        
        # Create the WordPress crew
        crew = self.crew_manager.create_wordpress_crew(
            project_id='test-project',
            site_data=site_data,
            content_data=content_data,
            site_key='test-site'
        )
        
        # Verify the correct agents were created
        mock_agent_factory.create_wordpress_setup_agent.assert_called_once()
        mock_agent_factory.create_design_implementation_agent.assert_called_once()
        mock_agent_factory.create_seo_strategy_agent.assert_called_once()
        mock_agent_factory.create_testing_qa_agent.assert_called_once()
        
        # Verify the correct tasks were created
        mock_task_factory.create_wordpress_setup_task.assert_called_once_with(
            project_id='test-project',
            site_data=site_data,
            agent=mock_wp_agent
        )
        
        mock_task_factory.create_wordpress_publishing_task.assert_called_once_with(
            project_id='test-project',
            content_data=content_data,
            site_key='test-site',
            agent=mock_wp_agent,
            context=[mock_setup_task]
        )
        
        # Verify the crew has the correct agents and tasks
        self.assertIsInstance(crew, Crew)
        self.assertEqual(len(crew.tasks), 2)
        self.assertIn(mock_setup_task, crew.tasks)
        self.assertIn(mock_publishing_task, crew.tasks)
        
        # Verify agents are part of the crew
        for agent in [mock_wp_agent, mock_design_agent, mock_seo_agent, mock_qa_agent]:
            self.assertIn(agent, crew.agents)
        
        # Verify the crew has sequential process
        self.assertEqual(crew.process.value, 'sequential')
    
    @patch('app.crew.agent_factory.AgentFactory')
    @patch('app.crew.tasks.TaskFactory')
    def test_create_wordpress_crew_without_content(self, MockTaskFactory, MockAgentFactory):
        """Test creating a WordPress crew without content data."""
        # Mock agents
        mock_wp_agent = MagicMock(spec=Agent)
        mock_design_agent = MagicMock(spec=Agent)
        mock_seo_agent = MagicMock(spec=Agent)
        mock_qa_agent = MagicMock(spec=Agent)
        
        # Mock agent factory
        mock_agent_factory = MockAgentFactory.return_value
        mock_agent_factory.create_wordpress_setup_agent.return_value = mock_wp_agent
        mock_agent_factory.create_design_implementation_agent.return_value = mock_design_agent
        mock_agent_factory.create_seo_strategy_agent.return_value = mock_seo_agent
        mock_agent_factory.create_testing_qa_agent.return_value = mock_qa_agent
        
        # Mock tasks
        mock_setup_task = MagicMock(spec=Task)
        
        # Mock task factory
        mock_task_factory = MockTaskFactory.return_value
        mock_task_factory.create_wordpress_setup_task.return_value = mock_setup_task
        
        # Replace instance attributes with mocks
        self.crew_manager.agent_factory = mock_agent_factory
        self.crew_manager.task_factory = mock_task_factory
        
        # Test site data
        site_data = {
            'site_name': 'Test Blog',
            'domain': 'testblog.com'
        }
        
        # Create the WordPress crew without content data
        crew = self.crew_manager.create_wordpress_crew(
            project_id='test-project',
            site_data=site_data,
            site_key='test-site'
        )
        
        # Verify the correct agents were created
        mock_agent_factory.create_wordpress_setup_agent.assert_called_once()
        
        # Verify only the setup task was created (no publishing task)
        mock_task_factory.create_wordpress_setup_task.assert_called_once()
        self.assertFalse(mock_task_factory.create_wordpress_publishing_task.called)
        
        # Verify the crew has only the setup task
        self.assertIsInstance(crew, Crew)
        self.assertEqual(len(crew.tasks), 1)
        self.assertIn(mock_setup_task, crew.tasks)

if __name__ == '__main__':
    unittest.main()

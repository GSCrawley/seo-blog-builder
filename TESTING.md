# Testing Guide for SEO Blog Builder

## Overview

This document outlines the testing strategy for the SEO Blog Builder application, focusing on ensuring that each component works correctly before proceeding to the next development phase.

## Testing Structure

The tests are organized into several categories:

1. **Unit Tests**: Test individual components in isolation
   - Service tests
   - Tool tests 
   - Agent tests

2. **Integration Tests**: Test interactions between components
   - Crew tests
   - API endpoint tests

3. **End-to-End Tests**: Test complete workflows
   - Full blog creation workflows

## Running Tests

To run all tests, execute the following command from the project root:

```bash
python run_tests.py
```

To run specific test modules, use:

```bash
python -m unittest tests/services/test_wordpress_service.py
```

## Test Coverage

The current test suite covers:

1. **WordPress Service**
   - Post creation
   - Category creation
   - Tag creation
   - Media uploads
   - Complete blog setup

2. **WordPress Tools**
   - CreatePostTool
   - CreateCategoryTool
   - CreateTagTool
   - UploadMediaTool
   - SetupBlogTool

3. **WordPress Crew Configuration**
   - WordPress crew creation with and without content

## Mock Testing Approach

The tests use mocking to isolate components:

1. External API calls are mocked using `unittest.mock.patch`
2. File operations are mocked using `mock_open`
3. Database interactions are mocked
4. CrewAI components (Agents, Tasks, Crews) are mocked for isolation

## Test-Driven Development

We follow a TDD approach for implementing new features:

1. Write tests first to define expected behavior
2. Implement the feature to satisfy the tests
3. Refactor the code while maintaining test coverage

## Integration with CI/CD

Tests are integrated with CI/CD processes:

1. Tests run automatically on each commit
2. Test failures prevent merge to main branch
3. Code coverage reports are generated
4. Performance benchmarks are tracked

## Manual Testing Checklist

For WordPress integration, manually test the following:

1. **WordPress Connection**
   - [ ] Connect to test WordPress site
   - [ ] Validate API credentials
   - [ ] Check permissions

2. **Content Creation**
   - [ ] Create a test post
   - [ ] Create test categories and tags
   - [ ] Upload test images
   - [ ] Verify internal linking

3. **SEO Configuration**
   - [ ] Verify meta tags
   - [ ] Check XML sitemap generation
   - [ ] Validate schema markup

## Adding New Tests

When adding new features, follow these steps:

1. Create a new test file in the appropriate directory
2. Include both positive and negative test cases
3. Mock external dependencies
4. Ensure tests are isolated and repeatable
5. Test edge cases and error handling

## Troubleshooting Tests

Common testing issues and solutions:

1. **Mocking Issues**
   - Ensure the correct path is used for patching
   - Check that mock objects are properly configured

2. **Integration Test Failures**
   - Verify component interfaces have not changed
   - Check that dependencies are properly mocked

3. **Slow Tests**
   - Use setup/teardown methods efficiently
   - Minimize database operations
   - Consider using test fixtures

## Next Steps for Testing

1. Implement integration tests for the API endpoints
2. Add automated UI tests for the frontend
3. Develop end-to-end tests for complete blog creation workflow
4. Set up continuous monitoring for deployed blogs

## Best Practices

1. Keep tests focused on a single responsibility
2. Maintain independence between tests
3. Avoid brittle tests with too many mocks
4. Test both normal and error paths
5. Regularly review and update tests

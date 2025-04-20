#!/usr/bin/env python
"""
Test runner script for SEO Blog Builder.
"""
import unittest
import sys
import os
import argparse

def run_tests(test_type=None, verbose=2):
    """
    Run tests and return the exit code.
    
    Args:
        test_type: Type of tests to run (unit, integration, all)
        verbose: Verbosity level (1-3)
    
    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    if test_type == 'unit':
        print("Running unit tests...")
        # Skip integration tests by default
        os.environ['SKIP_INTEGRATION_TESTS'] = 'True'
        # Load all tests excluding integration tests
        test_suite = unittest.TestLoader().discover('tests', pattern='test_*.py')
        
        # Filter out integration tests
        filtered_suite = unittest.TestSuite()
        for suite in test_suite:
            for test_case in suite:
                if 'integration' not in str(test_case):
                    filtered_suite.addTest(test_case)
        
        test_runner = unittest.TextTestRunner(verbosity=verbose)
        result = test_runner.run(filtered_suite)
    
    elif test_type == 'integration':
        print("Running integration tests...")
        # Enable integration tests
        os.environ['SKIP_INTEGRATION_TESTS'] = 'False'
        # Load only integration tests
        test_suite = unittest.TestLoader().discover('tests/integration', pattern='test_*.py')
        test_runner = unittest.TextTestRunner(verbosity=verbose)
        result = test_runner.run(test_suite)
    
    else:  # All tests
        print("Running all tests...")
        # Enable integration tests
        os.environ['SKIP_INTEGRATION_TESTS'] = 'False'
        # Load all tests
        test_suite = unittest.TestLoader().discover('tests', pattern='test_*.py')
        test_runner = unittest.TextTestRunner(verbosity=verbose)
        result = test_runner.run(test_suite)
    
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run SEO Blog Builder tests.')
    parser.add_argument('--type', '-t', choices=['unit', 'integration', 'all'], 
                        default='unit', help='Type of tests to run')
    parser.add_argument('--verbose', '-v', type=int, choices=[1, 2, 3], 
                        default=2, help='Verbosity level')
    args = parser.parse_args()
    
    sys.exit(run_tests(args.type, args.verbose))

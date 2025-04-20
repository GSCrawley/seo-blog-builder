#!/bin/bash
# Make the development scripts executable

# Change to the directory of this script
cd "$(dirname "$0")"

# Make scripts executable
chmod +x dev.sh
chmod +x stop_dev.sh
chmod +x make_scripts_executable.sh
chmod +x run_tests.py
chmod +x scripts/test_wordpress_connection.py

echo "Scripts are now executable."

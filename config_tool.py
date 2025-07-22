#!/usr/bin/env python
"""
Configuration Manager Tool for Design Thinking Coach
CLI tool to view, edit, and manage the master configuration
"""

import sys
import os
import argparse
import yaml
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))

from chatbot.utils import load_yaml, save_yaml

CONFIG_PATH = "config/master_config.yaml"

def print_help():
    """Print help message"""
    print("\nDesign Thinking Coach Configuration Manager")
    print("------------------------------------------")
    print("\nCommands:")
    print("  view           - View the current configuration")
    print("  edit           - Edit the configuration in your default editor")
    print("  set KEY VALUE  - Set a configuration value")
    print("  reset          - Reset the configuration to default")
    print("  help           - Show this help message")
    print("\nExamples:")
    print("  python config_tool.py view")
    print("  python config_tool.py edit")
    print("  python config_tool.py set model.temperature 0.5")
    print("  python config_tool.py reset")
    print("\n")

def view_config():
    """View the current configuration"""
    if not os.path.exists(CONFIG_PATH):
        print(f"Error: Configuration file not found at {CONFIG_PATH}")
        return
    
    config = load_yaml(CONFIG_PATH)
    print(yaml.dump(config, default_flow_style=False, sort_keys=False))

def edit_config():
    """Open the configuration file in the default editor"""
    if not os.path.exists(CONFIG_PATH):
        print(f"Error: Configuration file not found at {CONFIG_PATH}")
        return
    
    # Determine the editor to use
    editor = os.environ.get('EDITOR', 'nano')
    
    # Open the configuration file in the editor
    os.system(f"{editor} {CONFIG_PATH}")
    print(f"Configuration file opened in {editor}. Changes saved.")

def set_config_value(key_path, value):
    """Set a configuration value at the specified key path"""
    if not os.path.exists(CONFIG_PATH):
        print(f"Error: Configuration file not found at {CONFIG_PATH}")
        return
    
    config = load_yaml(CONFIG_PATH)
    
    # Parse the key path
    keys = key_path.split('.')
    
    # Navigate to the correct location
    current = config
    for i, key in enumerate(keys[:-1]):
        if key not in current:
            print(f"Error: Key '{key}' not found in configuration")
            return
        current = current[key]
    
    # Set the value
    try:
        # Attempt to convert the value to the appropriate type
        if value.lower() == "true":
            parsed_value = True
        elif value.lower() == "false":
            parsed_value = False
        elif value.isdigit():
            parsed_value = int(value)
        elif value.replace('.', '', 1).isdigit() and value.count('.') < 2:
            parsed_value = float(value)
        else:
            parsed_value = value
        
        current[keys[-1]] = parsed_value
        save_yaml(CONFIG_PATH, config)
        print(f"Configuration updated: {key_path} = {parsed_value}")
    except Exception as e:
        print(f"Error setting configuration value: {e}")

def reset_config():
    """Reset the configuration to default"""
    # Define the path for the default configuration
    default_config_path = "config/default_master_config.yaml"
    
    # Check if a default configuration exists
    if os.path.exists(default_config_path):
        # Copy the default configuration to the main configuration file
        config = load_yaml(default_config_path)
        save_yaml(CONFIG_PATH, config)
        print("Configuration reset to default")
    else:
        print(f"Default configuration not found at {default_config_path}")
        print("Please manually reset the configuration file")

def main():
    """Main entry point for the configuration tool"""
    parser = argparse.ArgumentParser(description="Design Thinking Coach Configuration Tool")
    parser.add_argument('command', nargs='?', default='help', 
                        help='Command to execute (view, edit, set, reset, help)')
    parser.add_argument('args', nargs='*', help='Additional arguments for the command')
    
    args = parser.parse_args()
    
    if args.command == 'help':
        print_help()
    elif args.command == 'view':
        view_config()
    elif args.command == 'edit':
        edit_config()
    elif args.command == 'set':
        if len(args.args) < 2:
            print("Error: 'set' command requires a key and value")
            print("Example: python config_tool.py set model.temperature 0.5")
        else:
            key = args.args[0]
            value = args.args[1]
            set_config_value(key, value)
    elif args.command == 'reset':
        reset_config()
    else:
        print(f"Error: Unknown command '{args.command}'")
        print_help()

if __name__ == "__main__":
    main()

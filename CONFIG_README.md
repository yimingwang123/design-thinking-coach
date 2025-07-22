# Design Thinking Coach Configuration System

This document explains how to use the centralized configuration system for the Design Thinking Coach application.

## Overview

The application now uses a single master configuration file located at `config/master_config.yaml`. This file controls all aspects of the application, including:

- Application general settings
- AI model settings
- Prompt templates
- Framework stages
- Server configuration

## How to Use

### Using the Configuration Tool

The easiest way to manage the configuration is using the provided tool:

```bash
# View the current configuration
python config_tool.py view

# Edit the configuration in your default text editor
python config_tool.py edit

# Set a specific configuration value
python config_tool.py set model.temperature 0.7

# Reset the configuration to defaults
python config_tool.py reset
```

### Direct Editing

You can also edit the `config/master_config.yaml` file directly in any text editor. The configuration uses YAML format.

### Reloading Configuration

After making changes to the configuration, you can apply them without restarting the server by calling:

```
POST /api/config/reload
```

This endpoint reloads all configuration settings across the application.

## Configuration Sections

### Application Settings

```yaml
application:
  name: "Design Thinking Coach"
  version: "1.0.0"
  description: "AI-powered Design Thinking Coach using Azure OpenAI"
  save_conversations: true
  log_level: "INFO"
```

### AI Model Settings

```yaml
model:
  provider: "azure"
  deployment_name: "gpt-4.1-mini"
  endpoint_url: "https://your-endpoint.openai.azure.com/"
  api_version: "2025-01-01-preview"
  temperature: 0.3
  max_tokens: 1000
  top_p: 0.95
  frequency_penalty: 0
  presence_penalty: 0
  mock_responses: false
```

### Prompts

```yaml
prompts:
  system_prompt: |
    You are the Design Thinking Coach...
  
  examples: |
    User: "Example question"
    Assistant: "Example response"
```

### Framework Stages

```yaml
framework:
  stages:
    - key: "problemStatement"
      title: "Problem Statement"
      description: "Kernproblem definieren"
      icon: "❗"
      keywords: ["problem", "statement", "definition"]
    # Additional stages...
```

### Server Configuration

```yaml
server:
  host: "0.0.0.0"
  port: 8000
  cors_origins: ["*"]
  reload: true
  log_level: "info"
```

## Environment Variables

Environment variables can override certain configuration values:

- `ENDPOINT_URL`: Override the Azure OpenAI endpoint URL
- `DEPLOYMENT_NAME`: Override the model deployment name
- `AZURE_OPENAI_API_KEY`: Set the API key for Azure OpenAI
- `MOCK_RESPONSES`: Set to "true" to use mock responses
- `PORT`: Override the server port
- `HOST`: Override the server host
- `CONFIG_PATH`: Change the path to the master config file

## Development Mode

To run the application in development mode without an Azure OpenAI API key:

1. Set `model.mock_responses: true` in the configuration
2. Or set the environment variable `MOCK_RESPONSES=true`

This will use pre-defined mock responses for testing purposes.

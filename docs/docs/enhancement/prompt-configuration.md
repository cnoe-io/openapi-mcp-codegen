# Prompt Configuration

Declarative prompt configuration using `prompt.yaml` for consistent LLM enhancement patterns.

## prompt.yaml Structure

```yaml
operation_description:
  system_prompt: |
    You are an expert at writing concise, OpenAI-compatible tool descriptions.
    Follow these strict rules:
    1. Keep descriptions under {max_length} characters
    2. Start with what the operation does (verb + object)
    3. Add one use case: 'Use when: <scenario>'
    4. NO markdown formatting or special characters
    5. Focus on agentic purpose

  user_prompt_template: |
    API: {method} {path}
    Operation ID: {operation_id}
    Summary: {summary}
    Original Description: {description}

    Write a concise, agent-focused tool description.

parameter_description:
  system_prompt: |
    Write brief, practical parameter descriptions for AI agents.

  user_prompt_template: |
    Parameter: {param_name}
    Type: {param_type}
    Required: {param_required}
    Original: {original_description}

    Write usage guidance for this parameter.
```

## Benefits

- **Version Control**: Prompts tracked in git and reviewable in PRs
- **Team Collaboration**: Non-developers can improve prompt quality
- **A/B Testing**: Easy to test different prompt strategies
- **Consistency**: Same prompts used across all API operations

*Documentation in progress. See examples for working prompt configurations.*

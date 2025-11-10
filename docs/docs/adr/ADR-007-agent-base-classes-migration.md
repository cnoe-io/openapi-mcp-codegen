# ADR-007: Agent Base Classes Migration to cnoe-agent-utils

## Status
**ACCEPTED** ✅ *Implemented*

## Context

Agent development in CNOE was suffering from significant code duplication and inconsistency across different agent implementations. Each agent project (argo-workflows, argocd, etc.) maintained its own copies of base agent classes, context management utilities, and A2A protocol integration code.

### Problems Identified:
1. **Code Duplication**: ~1000+ lines of identical base agent code duplicated across multiple agent projects
2. **Inconsistent Patterns**: Different agents implementing base functionality slightly differently
3. **Maintenance Burden**: Bug fixes and improvements needed to be applied to multiple repositories
4. **Missing Features**: Some agents lacked advanced features like smart context management and enhanced streaming
5. **Integration Gaps**: Inconsistent A2A protocol integration across agents

### User Request:
> "add the common code used in argocon/ai-platform-engineering/ai_platform_engineering/agents/argocd like agent code like base_langgraph to cnoe-agent-utils"

## Decision

We will migrate all common agent base classes and utilities to cnoe-agent-utils package, creating a centralized library for CNOE agent development that eliminates code duplication and ensures consistency.

### Implementation Strategy:

1. **Create Agent Base Classes in cnoe-agent-utils**:
   - Migrate `BaseLangGraphAgent` and `BaseLangGraphAgentExecutor` from argocon project
   - Migrate `BaseStrandsAgent` and `BaseStrandsAgentExecutor` for Strands framework support
   - Add comprehensive context management utilities with provider-specific token limits
   - Include A2A protocol integration with streaming support

2. **Update Package Structure**:
   - Add new `cnoe_agent_utils.agents` module with optional dependencies
   - Update pyproject.toml with new dependency groups (`[langgraph]`, `[strands]`, `[a2a]`, `[agents-all]`)
   - Graceful handling of missing dependencies with informative error messages

3. **Migrate Existing Agents**:
   - Update argo-workflows agent to use cnoe-agent-utils base classes
   - Remove local copies of base agent files
   - Add development guide with both git branch and local development approaches
   - Include Docker support with multi-stage builds

4. **Enhanced Features**:
   - Smart context management with automatic token counting and message trimming
   - Provider-specific context limits (AWS Bedrock: 150K, Azure OpenAI: 100K, etc.)
   - Enhanced streaming with tool call notifications and status updates
   - Multi-server MCP support with HTTP/stdio transport modes

## Consequences

### Positive:
- ✅ **Code Reuse**: Eliminated ~1000 lines of duplicated base agent code
- ✅ **Consistency**: All agents now follow the same architectural patterns
- ✅ **Maintainability**: Single source of truth for agent base functionality
- ✅ **Enhanced Features**: Better context management, streaming, and A2A protocol support
- ✅ **Optional Dependencies**: Install only required components (langgraph, strands, a2a)
- ✅ **Future-Ready**: Easy to extend with new agent frameworks
- ✅ **Developer Experience**: Clear development patterns with comprehensive documentation

### Negative (if any):
- ⚠️ **Dependency Management**: Agents now depend on external package for core functionality
- ⚠️ **Version Coordination**: Need to coordinate cnoe-agent-utils releases with agent updates

### Architecture Changes:

#### Before (Duplicated):
```
argo-workflows/
├── base_langgraph_agent.py          # 985 lines - duplicated
├── base_langgraph_agent_executor.py # 340 lines - duplicated
├── context_config.py                # 170 lines - duplicated
└── agent.py                         # Agent-specific

argocd/
├── base_langgraph_agent.py          # 985 lines - duplicated
├── base_langgraph_agent_executor.py # 340 lines - duplicated
├── context_config.py                # 170 lines - duplicated
└── agent.py                         # Agent-specific
```

#### After (Centralized):
```
cnoe-agent-utils/
└── cnoe_agent_utils/agents/
    ├── base_langgraph_agent.py      # 985 lines - centralized
    ├── base_langgraph_agent_executor.py # 340 lines - centralized
    ├── base_strands_agent.py        # 547 lines - new
    ├── base_strands_agent_executor.py # 336 lines - new
    └── context_config.py            # 170 lines - centralized

argo-workflows/
├── agent.py                         # Uses cnoe_agent_utils.agents
├── agent_executor.py               # Uses cnoe_agent_utils.agents
└── helpers.py                       # Agent-specific utilities

argocd/
├── agent.py                         # Uses cnoe_agent_utils.agents
├── agent_executor.py               # Uses cnoe_agent_utils.agents
└── helpers.py                       # Agent-specific utilities
```

### Implementation Status
**COMPLETED** ✅

#### cnoe-agent-utils Enhancements:
- ✅ Created `cnoe_agent_utils.agents` module with base classes
- ✅ Added context management with provider-specific limits
- ✅ Implemented optional dependencies with graceful error handling
- ✅ Added comprehensive documentation and usage examples
- ✅ Updated package version to 0.4.0 with new features
- ✅ Created feature branch `feature/agent-base-classes` for development

#### Agent Migration (argo-workflows):
- ✅ Updated pyproject.toml to use git branch dependency
- ✅ Migrated imports to use `cnoe_agent_utils.agents`
- ✅ Removed local copies of base agent files
- ✅ Added helpers.py to match argocd pattern
- ✅ Created development guide with local vs git branch approaches
- ✅ Added Docker support with Dockerfile.a2a and CI/CD workflow

### Development Approaches:

#### 1. Git Branch (CI/Remote Development):
```toml
"cnoe-agent-utils[langgraph,a2a] @ git+https://github.com/cnoe-io/cnoe-agent-utils.git@feature/agent-base-classes"
```

#### 2. Local Development (Fast Iteration):
```toml
[tool.uv.sources]
cnoe-agent-utils = { path = "../../../../cnoe-agent-utils", extras = ["langgraph", "a2a"] }
```

### Usage Example:

#### Before (Duplicated Code):
```python
from .base_langgraph_agent import BaseLangGraphAgent
from .base_langgraph_agent_executor import BaseLangGraphAgentExecutor

class MyAgent(BaseLangGraphAgent):
    # Implementation using local base classes
```

#### After (Centralized Library):
```python
from cnoe_agent_utils.agents import BaseLangGraphAgent, BaseLangGraphAgentExecutor

class MyAgent(BaseLangGraphAgent):
    # Same implementation, enhanced base classes
```

### Environment Variables:

#### Context Management:
- `LLM_PROVIDER`: Provider name (aws-bedrock, azure-openai, etc.)
- `MAX_CONTEXT_TOKENS`: Global context limit override
- `MIN_MESSAGES_TO_KEEP`: Minimum recent messages to preserve
- `ENABLE_AUTO_COMPRESSION`: Enable automatic message trimming

#### Provider-Specific Limits:
- `AWS_BEDROCK_MAX_CONTEXT_TOKENS`: Override for AWS Bedrock (default: 150,000)
- `AZURE_OPENAI_MAX_CONTEXT_TOKENS`: Override for Azure OpenAI (default: 100,000)
- `OPENAI_MAX_CONTEXT_TOKENS`: Override for OpenAI (default: 100,000)

#### Agent Behavior:
- `ENABLE_STREAMING`: Enable token-by-token streaming (default: true)
- `STREAM_TOOL_OUTPUT`: Stream intermediate tool outputs (default: false)
- `MCP_MODE`: Transport mode ("stdio" or "http", default: "stdio")

## Next Steps

1. **Testing & Validation**: ✅ Test argo-workflows agent with new cnoe-agent-utils integration
2. **PyPI Release**: Create cnoe-agent-utils v0.4.0 release once stable
3. **Agent Migration**: Migrate other agents (argocd, backstage, etc.) to use cnoe-agent-utils
4. **Documentation**: Update architecture documentation and migration guides
5. **CI/CD**: Update agent CI/CD pipelines to use released version instead of git branch

## References

- **cnoe-agent-utils repository**: https://github.com/cnoe-io/cnoe-agent-utils
- **Feature branch**: `feature/agent-base-classes`
- **ArgoCD agent pattern**: `/ai-platform-engineering/agents/argocd/`
- **Migration documentation**: `examples/argo-workflows/working_argo_agent/MIGRATION_SUMMARY.md`

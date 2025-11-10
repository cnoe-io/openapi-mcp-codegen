# LangFuse Integration

LangFuse provides observability and evaluation capabilities for AI agents using generated MCP servers.

## Features

- **Distributed Tracing**: Track agent interactions across tool calls
- **Evaluation Framework**: Automated assessment of agent performance
- **Dataset Building**: Interactive dataset creation for testing
- **Real-time Monitoring**: Performance metrics and error tracking

## Configuration

```bash
# LangFuse Configuration
LANGFUSE_HOST=http://localhost:3000
LANGFUSE_PUBLIC_KEY=pk-...
LANGFUSE_SECRET_KEY=sk-...
```

## Evaluation Workflow

```bash
# Build evaluation dataset interactively
make run-a2a-eval-mode

# Run automated evaluation
make eval
```

## Metrics

LangFuse tracks:
- **Correctness**: Did the agent complete the task successfully?
- **Hallucination**: Did the agent make up information?
- **Trajectory**: Did the agent use tools efficiently?

*LangFuse integration documentation in progress. See examples with `--generate-eval` for working implementations.*

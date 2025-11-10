import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  docsSidebar: [
    {
      type: 'doc',
      id: 'index', // docs/index.md
      label: 'Introduction',
    },
    {
      type: 'category',
      label: 'Getting Started',
      items: [
        {
          type: 'doc',
          id: 'getting-started/quick-start',
        },
        {
          type: 'doc',
          id: 'getting-started/installation',
        },
        {
          type: 'doc',
          id: 'getting-started/basic-usage',
        },
        {
          type: 'doc',
          id: 'getting-started/configuration',
        },
        {
          type: 'doc',
          id: 'getting-started/examples',
        }
      ],
    },
    {
      type: 'category',
      label: 'Core Components',
      items: [
        {
          type: 'doc',
          id: 'core-components/index',
          label: 'Overview',
        },
        {
          type: 'doc',
          id: 'core-components/mcp-server-generator',
          label: 'MCP Server Generator',
        },
        {
          type: 'doc',
          id: 'core-components/a2a-agent-generator',
          label: 'A2A Agent Generator',
        }
      ],
    },
    {
      type: 'category',
      label: 'Architecture',
      items: [
        {
          type: 'doc',
          id: 'architecture/overview',
        },
        {
          type: 'doc',
          id: 'architecture/enhancement-pipeline',
        },
        {
          type: 'doc',
          id: 'architecture/code-generation',
        },
        {
          type: 'doc',
          id: 'architecture/smart-parameter-handling',
        }
      ],
    },
    {
      type: 'category',
      label: 'Enhancement Pipeline',
      items: [
        {
          type: 'doc',
          id: 'enhancement/openapi-overlay',
        },
        {
          type: 'doc',
          id: 'enhancement/llm-integration',
        },
        {
          type: 'doc',
          id: 'enhancement/prompt-configuration',
        }
      ],
    },
    {
      type: 'category',
      label: 'Examples',
      items: [
        {
          type: 'doc',
          id: 'examples/petstore',
        },
        {
          type: 'doc',
          id: 'examples/argo-workflows',
        },
        {
          type: 'doc',
          id: 'examples/splunk',
        },
        {
          type: 'doc',
          id: 'examples/backstage',
        }
      ],
    },
    {
      type: 'category',
      label: 'CLI Reference',
      items: [
        {
          type: 'doc',
          id: 'cli/commands',
        },
        {
          type: 'doc',
          id: 'cli/configuration-files',
        },
        {
          type: 'doc',
          id: 'cli/troubleshooting',
        }
      ],
    },
    {
      type: 'category',
      label: 'Integration',
      items: [
        {
          type: 'doc',
          id: 'integration/ai-agents',
        },
        {
          type: 'doc',
          id: 'integration/agentgateway',
        },
        {
          type: 'doc',
          id: 'integration/langfuse',
        }
      ],
    },
    {
      type: 'category',
      label: 'ArgoCon 2025 Presentation',
      items: [
        {
          type: 'doc',
          id: 'argocon/index',
          label: 'Presentation Overview',
        },
        {
          type: 'doc',
          id: 'argocon/setup',
          label: 'Argo Workflows Setup',
        },
            {
              type: 'doc',
              id: 'argocon/presentation',
              label: 'Detailed Presentation Content',
            }
      ],
    },
        {
          type: 'category',
          label: 'ADRs (Architecture Decision Records)',
          items: [
            {
              type: 'doc',
              id: 'adr/ADR-001-openapi-mcp-architecture',
              label: 'ADR-001: Architecture Overview',
            },
            {
              type: 'doc',
              id: 'adr/ADR-002-openapi-specification-fixes',
              label: 'ADR-002: Specification Fixes',
            },
            {
              type: 'doc',
              id: 'adr/ADR-004-openapi-overlay-enhancement',
              label: 'ADR-004: Overlay Enhancement Strategy',
            },
            {
              type: 'doc',
              id: 'adr/ADR-005-enhanced-openapi-conversion',
              label: 'ADR-005: Enhanced OpenAPI Conversion',
            },
            {
              type: 'doc',
              id: 'adr/ADR-006-a2a-agent-refactoring',
              label: 'ADR-006: A2A Agent Refactoring',
            },
            {
              type: 'doc',
              id: 'adr/ADR-007-agent-base-classes-migration',
              label: 'ADR-007: Agent Base Classes Migration',
            },
            {
              type: 'doc',
              id: 'adr/ADR-008-openapi-enhancement-proposal',
              label: 'ADR-008: OpenAPI Enhancement Proposal',
            }
          ],
        },
    {
      type: 'doc',
      id: 'contributing',
      label: 'Contributing',
    },
  ]
};

export default sidebars;
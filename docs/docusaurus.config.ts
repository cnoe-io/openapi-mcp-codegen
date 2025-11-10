import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'OpenAPI MCP Codegen',
  tagline: 'Transform OpenAPI specifications into AI-ready MCP servers',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://cnoe-io.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/openapi-mcp-codegen/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'cnoe.io', // Usually your GitHub org/user name.
  projectName: 'openapi-mcp-codegen', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  plugins: [[
    require.resolve('docusaurus-lunr-search'), {
      languages: ['en'],
      title: { boost: 200 },
      content: { boost: 2 },
      keywords: { boost: 100 }
    }
  ]],

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/', // Serve the docs at the site's root
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/cnoe-io/openapi-mcp-codegen/tree/main/docs',
        },
        blog: false, // Disable blog functionality
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/logo.svg',
    navbar: {
      title: 'OpenAPI MCP Codegen',
      logo: {
        alt: 'OpenAPI MCP Codegen Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Docs',
        },
        // Uncomment the following lines to enable versioning
        // {
        //   type: 'docsVersionDropdown',
        // },
        // --- START: GITHUB BADGES ---
        {
          type: 'html',
          position: 'right',
          value: `
            <a href="https://github.com/cnoe-io/openapi-mcp-codegen" target="_blank" rel="noopener" style="margin-right: 8px;">
              <img alt="GitHub stars" src="https://img.shields.io/github/stars/cnoe-io/ai-platform-engineering?style=social" style="vertical-align: middle;" />
            </a>
            <a href="https://github.com/cnoe-io/openapi-mcp-codegen/issues" target="_blank" rel="noopener">
              <img alt="GitHub issues" src="https://img.shields.io/github/issues/cnoe-io/ai-platform-engineering?style=social" style="vertical-align: middle;" />
            </a>
          `,
        },
        // --- END: GITHUB BADGES ---
        {
          href: 'https://github.com/cnoe-io/openapi-mcp-codegen',
          label: 'GitHub',
          position: 'right',
          className: 'header-github-link',
          'aria-label': 'GitHub repository',
        }
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Getting Started',
              to: '/getting-started',
            },
            {
              label: 'Architecture',
              to: '/architecture',
            },
            {
              label: 'Examples',
              to: '/examples/petstore',
            },
            {
              label: 'Contributing',
              to: '/contributing',
            },
          ],
        },
        {
          title: 'Project',
          items: [
            {
              label: 'GitHub Repository',
              href: 'https://github.com/cnoe-io/openapi-mcp-codegen',
            },
            {
              label: 'GitHub Issues',
              href: 'https://github.com/cnoe-io/openapi-mcp-codegen/issues',
            },
            {
              label: 'GitHub Discussions',
              href: 'https://github.com/cnoe-io/openapi-mcp-codegen/discussions',
            },
            {
              label: 'ArgoCon 2025 Presentation',
              to: '/argocon/README',
            }
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'CAIPE (Maintained by)',
              href: 'https://github.com/cnoe-io/ai-platform-engineering',
            },
            {
              label: 'CNOE Agent Utils',
              href: 'https://github.com/cnoe-io/cnoe-agent-utils',
            },
            {
              label: 'CNOE.io',
              href: 'https://cnoe.io',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} CAIPE Maintainers. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: [
        'bash',
        'yaml',
        'diff'
      ],
    },
    mermaid: {
      theme: {dark: 'forest'},
    },
  } satisfies Preset.ThemeConfig,

  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],
};

export default config;

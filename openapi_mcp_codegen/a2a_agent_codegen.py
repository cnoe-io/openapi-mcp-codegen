#!/usr/bin/env python3
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0

"""
A2A Agent Code Generator

This module provides functionality to generate standalone A2A (Agent-to-Agent)
compatible agents that connect to external MCP servers. The generated agents
follow the same structure as other A2A agents (like the GitHub agent) but are
configurable to connect to any MCP server URL.
"""

import os
import re
import json
import yaml
import logging
import datetime
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("a2a_agent_codegen")

def camel_to_snake(name):
    """Convert CamelCase to snake_case."""
    if name.isupper():
        return "_".join(name).lower()
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    # Replace multiple underscores with a single underscore
    s3 = re.sub(r'_+', '_', s2)
    return s3


def truncate_function_name(name: str, http_method: str = "", used_names: set = None, target_length: int = 30, max_length: int = 64) -> str:
    """
    Truncate function names with consistent service abbreviations and aggressive length limits.
    Always applies service prefix abbreviations for consistency, then applies length-based truncation.
    Adds HTTP method prefix to ensure uniqueness when duplicates would occur.

    Args:
        name: Original function name
        http_method: HTTP method (GET, POST, etc.) to add as prefix if needed for uniqueness
        used_names: Set of already used function names to check for duplicates
        target_length: Target length to aim for (default: 30)
        max_length: Hard limit - anything over this MUST be truncated (default: 64)

    Always applies consistent abbreviations for known service patterns.
    Based on RULE-LLM-LIMITATION-1 from prompt.yaml.
    """
    if used_names is None:
        used_names = set()

    # Always apply consistent service prefix abbreviations first (regardless of length)
    abbreviated = name

    # Known service patterns that should always be abbreviated for consistency
    service_patterns = {
        'workflow_service_': 'wf_svc_',
        'event_source_service_': 'evt_src_svc_',
        'event_service_': 'evt_svc_',
        'sensor_service_': 'sns_svc_',
        'artifact_service_': 'art_svc_',
        'info_service_': 'info_svc_',
        'cluster_workflow_template_service_': 'clust_wf_tpl_svc_',
        'workflow_template_service_': 'wf_tpl_svc_',
        'cron_workflow_service_': 'cron_wf_svc_',
    }

    # Apply service pattern abbreviations
    for full_pattern, abbrev_pattern in service_patterns.items():
        if abbreviated.startswith(full_pattern):
            abbreviated = abbreviated.replace(full_pattern, abbrev_pattern, 1)
            break

    # Continue to HTTP prefix logic even for short names to ensure consistency

    # Log warning for names that will be truncated
    if len(name) > max_length:
        logger.warning(f"Function name '{name}' ({len(name)} chars) exceeds {max_length} hard limit, truncating...")
    else:
        logger.info(f"Function name '{name}' ({len(name)} chars) exceeds {target_length} target, applying abbreviations...")

    # Apply aggressive abbreviation rules for target length
    abbreviations = {
        # Service/System abbreviations
        'service': 'svc',
        'account': 'acct',
        'permissions': 'perms',
        'configuration': 'cfg',
        'template': 'tpl',
        'templates': 'tpls',
        'namespace': 'ns',
        'workflow': 'wf',
        'workflows': 'wfs',
        'archived': 'arch',
        'cluster': 'clust',
        'selector': 'sel',
        'metadata': 'meta',
        'artifact': 'art',
        'artifacts': 'arts',
        'event_source': 'evt_src',
        'event_sources': 'evt_srcs',
        'cron_workflow': 'cron_wf',
        'cron_workflows': 'cron_wfs',
        'sensor': 'sns',
        'sensors': 'snss',
        # Action abbreviations
        'retrieve': 'get',
        'terminate': 'term',
        'resubmit': 'resub',
        'suspend': 'susp',
        'resume': 'res',
        'delete': 'del',
        'create': 'new',
        'update': 'upd',
        'list': 'ls'
    }

    # Remove unnecessary connector words
    connectors_to_remove = ['_all_', '_by_', '_with_', '_and_', '_from_', '_using_']

    abbreviated = name

    # Apply abbreviations
    for full_word, abbrev in abbreviations.items():
        abbreviated = abbreviated.replace(full_word, abbrev)

    # Remove connector words
    for connector in connectors_to_remove:
        abbreviated = abbreviated.replace(connector, '_')

    # Clean up multiple underscores
    abbreviated = re.sub(r'_+', '_', abbreviated)
    abbreviated = abbreviated.strip('_')

    # Apply more aggressive truncation if still over target length
    if len(abbreviated) > target_length:
        parts = abbreviated.split('_')
        if len(parts) > 4:
            # For long functions, keep first part (action) + key middle part + last part
            abbreviated = '_'.join([parts[0], parts[1], parts[-1]])
        elif len(parts) > 3:
            # Keep first 2 and last part
            abbreviated = '_'.join(parts[:2] + parts[-1:])

    # Clean up multiple underscores again after aggressive truncation
    abbreviated = re.sub(r'_+', '_', abbreviated)
    abbreviated = abbreviated.strip('_')

    # ALWAYS add HTTP method prefix at the front for consistency
    final_name = abbreviated
    should_add_prefix = False

    # Check if the function name already starts with an HTTP verb
    starts_with_http_verb = any(final_name.startswith(verb + '_') for verb in [
        'get', 'post', 'put', 'patch', 'del', 'delete', 'head', 'opts', 'options'
    ])

    # Always add HTTP method prefix unless it already starts with one
    if http_method and not starts_with_http_verb:
        should_add_prefix = True
    elif http_method and final_name in used_names:
        # Always add prefix for duplicates even if already has HTTP verb
        should_add_prefix = True

    if should_add_prefix:
        # Add HTTP method prefix
        method_abbrev = {
            "GET": "get",
            "POST": "post",
            "PUT": "put",
            "PATCH": "patch",
            "DELETE": "del",
            "HEAD": "head",
            "OPTIONS": "opts"
        }
        prefix = method_abbrev.get(http_method.upper(), http_method.lower()[:3])

        # Reserve space for prefix + underscore, respecting max_length
        max_base_length = max_length - len(prefix) - 1
        if len(abbreviated) > max_base_length:
            abbreviated = abbreviated[:max_base_length].rstrip('_')

        final_name = f"{prefix}_{abbreviated}"

        if final_name != abbreviated:
            reason = "for consistency" if not (abbreviated in used_names) else "to avoid duplicate"
            logger.info(f"Added method prefix {reason}: '{abbreviated}' → '{final_name}'")

    # Hard limit enforcement - must not exceed max_length
    if len(final_name) > max_length:
        logger.warning(f"Applying hard truncation to enforce {max_length} char limit")
        final_name = final_name[:max_length].rstrip('_')

    # Add to used names set
    used_names.add(final_name)

    logger.info(f"Truncated '{name}' ({len(name)}) → '{final_name}' ({len(final_name)})")
    return final_name

class A2AAgentGenerator:
    """
    A2AAgentGenerator is a class responsible for generating standalone A2A agents
    that connect to external MCP servers. It creates agent structures similar to
    existing A2A agents (like GitHub agent) but configurable for any MCP server URL.

    Attributes:
        script_dir (str): Directory containing Jinja2 templates used for code generation.
        spec_path (str): Path to the OpenAPI specification file (YAML or JSON format).
        output_dir (str): Directory where the generated agent will be stored.
        config_path (str): Path to the configuration file containing metadata and settings.
        env (Environment): Jinja2 environment for loading and rendering templates.
        config (dict): Configuration data loaded from the configuration file.
        spec (dict): Parsed OpenAPI specification loaded from the spec file.
    """

    def __init__(
        self,
        script_dir: str,
        spec_path: str,
        output_dir: str,
        config_path: str,
        dry_run: bool = False
    ):
        """
        Initialize the A2AAgentGenerator with paths and configuration.

        Args:
            script_dir (str): Directory containing the templates.
            spec_path (str): Path to the OpenAPI specification file.
            output_dir (str): Directory where generated agent will be stored.
            config_path (str): Path to the configuration file.
            dry_run (bool): If True, don't write files to disk.
        """
        logger.info("Initializing A2AAgentGenerator")
        self.script_dir = script_dir
        self.spec_path = spec_path
        self.output_dir = output_dir
        self.dry_run = dry_run
        self.env = Environment(loader=FileSystemLoader(os.path.join(script_dir, 'templates')))

        with open(config_path, encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        self.spec = self._load_spec()
        self.used_function_names = set()  # Track function names to avoid duplicates

    def _load_spec(self) -> Dict[str, Any]:
        """
        Load the OpenAPI specification from either JSON or YAML file.

        Returns:
            Dictionary containing the parsed OpenAPI specification.
        """
        logger.info(f"Loading OpenAPI specification from {self.spec_path}")
        with open(self.spec_path, 'r', encoding='utf-8') as f:
            if self.spec_path.endswith('.yaml') or self.spec_path.endswith('.yml'):
                return yaml.safe_load(f)
            else:
                return json.load(f)

    def get_file_header_kwargs(self) -> Dict[str, Any]:
        """
        Generate kwargs for file header template.

        Returns:
            Dictionary with file header information.
        """
        return {
            'file_header': f'# Copyright 2025 CNOE Contributors\n# SPDX-License-Identifier: Apache-2.0',
            'author': self.config.get('author', 'Generated User'),
            'author_email': self.config.get('author_email', 'user@example.com'),
            'timestamp': self.config.get('timestamp', datetime.datetime.now().isoformat())
        }

    def render_template(self, template_name: str, output_path: str, **kwargs):
        """
        Render a Jinja2 template to a file.

        Args:
            template_name (str): Name of the template file.
            output_path (str): Path where the rendered file will be saved.
            **kwargs: Template variables.
        """
        if self.dry_run:
            logger.info(f"[DRY RUN] Would render template: {template_name} to {output_path}")
            return

        logger.info(f"Rendering template: {template_name} to {output_path}")
        template = self.env.get_template(template_name)
        rendered_content = template.render(**kwargs)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_content)
        logger.info(f"Generated file: {output_path}")

    def run_ruff_lint(self, input_file: str):
        """
        Run Ruff linter and formatter on a file.

        Args:
            input_file (str): Path to the file to lint and format.
        """
        if self.dry_run:
            logger.info(f"[DRY RUN] Would run Ruff on {input_file}")
            return

        try:
            logger.info(f"Running Ruff format on {input_file}")
            subprocess.run(['ruff', 'format', input_file], check=False, capture_output=True, text=True)

            logger.info(f"Running Ruff lint on {input_file}")
            result = subprocess.run(['ruff', 'check', '--fix', input_file], capture_output=True, text=True)

            if result.stdout:
                logger.info(result.stdout.strip())
            if result.returncode == 0:
                logger.info("Ruff linting completed")
            else:
                logger.warning(f"Ruff found issues in {input_file}: {result.stderr}")
        except FileNotFoundError:
            logger.warning("Ruff not found. Skipping code formatting.")

    def generate_a2a_agent(self, agent_name: str, mcp_server_url: str, agent_description: str = None):
        """
        Generate a standalone A2A agent that connects to an external MCP server.
        This creates an agent structure similar to the GitHub agent but configurable
        for any MCP server URL (like AgentGateway).

        Args:
            agent_name (str): Name of the agent (e.g., 'argo_workflows')
            mcp_server_url (str): URL of the MCP server to connect to
            agent_description (str): Optional description of the agent
        """
        logger.info(f"Generating standalone A2A agent: {agent_name}")

        # Sanitize agent name
        sanitized_name = agent_name.lower().replace(' ', '_').replace('-', '_')

        # Set up output directory structure
        agent_output_dir = os.path.join(self.output_dir, f"agent_{sanitized_name}")
        if not self.dry_run:
            os.makedirs(agent_output_dir, exist_ok=True)

        # Create agent package directory
        agent_pkg_dir = os.path.join(agent_output_dir, f"agent_{sanitized_name}")
        if not self.dry_run:
            os.makedirs(agent_pkg_dir, exist_ok=True)

        # Create protocol bindings directory
        protocol_dir = os.path.join(agent_pkg_dir, "protocol_bindings")
        if not self.dry_run:
            os.makedirs(protocol_dir, exist_ok=True)

        # Create a2a_server directory
        a2a_server_dir = os.path.join(protocol_dir, "a2a_server")
        if not self.dry_run:
            os.makedirs(a2a_server_dir, exist_ok=True)

        # Create clients directory
        clients_dir = os.path.join(agent_output_dir, "clients")
        if not self.dry_run:
            os.makedirs(clients_dir, exist_ok=True)

        # Create a2a client subdirectory
        a2a_client_dir = os.path.join(clients_dir, "a2a")
        if not self.dry_run:
            os.makedirs(a2a_client_dir, exist_ok=True)

        # Prepare template context
        file_header_kwargs = self.get_file_header_kwargs()

        # Use provided description or generate from spec
        if agent_description is None:
            agent_description = f"An AI agent that interacts with {agent_name} via MCP server."

        # Extract skills from config.yaml if available, otherwise fallback to OpenAPI spec
        skills = []
        skill_examples = []

        # Try to get skills from config first
        config_skills = self.config.get("skills", [])
        if config_skills:
            # Use skills from config.yaml
            skills = config_skills
            # For backward compatibility, also create a flattened list of examples for simple template usage
            for skill in config_skills:
                skill_examples.extend([f"'{example}'" for example in skill.get("examples", [])])
        else:
            # Fallback to extracting from OpenAPI spec (original behavior)
            for path, ops in self.spec.get("paths", {}).items():
                for method, op in ops.items():
                    if method.upper() not in {"GET", "POST", "PUT", "DELETE"}:
                        continue
                    operation_desc = op.get("summary") or op.get("description", "")
                    if operation_desc:
                        skill_examples.append(f"'{operation_desc.strip()}'")

            # Limit to reasonable number of examples
            skill_examples = skill_examples[:5]

        # Get system prompt from config if available
        config_system_prompt = self.config.get("system_prompt")
        if config_system_prompt:
            system_prompt = config_system_prompt.strip()
        else:
            # Fallback system prompt
            system_prompt = f"""You are a {agent_name.replace('_', ' ').title()} expert assistant. You help users manage and interact with {agent_name.replace('_', ' ').title()} services.

Your capabilities include:
- Managing {agent_name.replace('_', ' ').title()} resources and configurations
- Monitoring service status and performance
- Handling API operations and data retrieval
- Troubleshooting issues and providing solutions
- Providing best practices and recommendations

Always provide clear, actionable responses and include relevant resource names, status information, and next steps when available."""

        context = {
            **file_header_kwargs,
            'agent_name': sanitized_name,
            'agent_display_name': agent_name.replace('_', ' ').title(),
            'agent_description': agent_description,
            'mcp_server_url': mcp_server_url,
            'skill_examples': skill_examples,
            'skills': skills,
            'system_prompt': system_prompt,
            'timestamp': datetime.datetime.now().isoformat()
        }

        # Generate agent files using templates
        self._generate_a2a_agent_files(agent_output_dir, agent_pkg_dir, context)

        logger.info(f"A2A agent '{agent_name}' generated successfully in {agent_output_dir}")
        return agent_output_dir

    def _generate_a2a_agent_files(self, agent_output_dir: str, agent_pkg_dir: str, context: dict):
        """Generate all files for the standalone A2A agent."""

        # Generate main agent package files
        self.render_template("a2a_agent/agent_card.tpl",
                            os.path.join(agent_pkg_dir, "agentcard.py"), **context)

        self.render_template("a2a_agent/__init__.tpl",
                            os.path.join(agent_pkg_dir, "__init__.py"), **context)

        self.render_template("a2a_agent/__main__.tpl",
                            os.path.join(agent_pkg_dir, "__main__.py"), **context)

        # Generate protocol bindings
        protocol_dir = os.path.join(agent_pkg_dir, "protocol_bindings")
        a2a_server_dir = os.path.join(protocol_dir, "a2a_server")

        self.render_template("init_empty.tpl",
                            os.path.join(protocol_dir, "__init__.py"), **context)

        self.render_template("a2a_agent/protocol_bindings/a2a_server/agent.tpl",
                            os.path.join(a2a_server_dir, "agent.py"), **context)

        self.render_template("a2a_agent/protocol_bindings/a2a_server/agent_executor.tpl",
                            os.path.join(a2a_server_dir, "agent_executor.py"), **context)

        self.render_template("init_empty.tpl",
                            os.path.join(a2a_server_dir, "__init__.py"), **context)

        # Generate utils directory with local dependencies
        utils_dir = os.path.join(agent_pkg_dir, "utils")

        self.render_template("a2a_agent/utils/__init__.tpl",
                            os.path.join(utils_dir, "__init__.py"), **context)

        # Note: base_agent.py and base_agent_executor.py are no longer generated
        # since we now use cnoe_agent_utils.agents.BaseLangGraphAgent and BaseLangGraphAgentExecutor

        self.render_template("a2a_agent/utils/prompt_templates.tpl",
                            os.path.join(utils_dir, "prompt_templates.py"), **context)

        # Generate client files
        clients_dir = os.path.join(agent_output_dir, "clients")
        a2a_client_dir = os.path.join(clients_dir, "a2a")

        self.render_template("a2a_agent/clients/a2a/agent.tpl",
                            os.path.join(a2a_client_dir, "agent.py"), **context)

        # Generate project files
        self.render_template("a2a_agent/pyproject.tpl",
                            os.path.join(agent_output_dir, "pyproject.toml"), **context)

        self.render_template("a2a_agent/Makefile.tpl",
                            os.path.join(agent_output_dir, "Makefile"), **context)

        self.render_template("a2a_agent/README.tpl",
                            os.path.join(agent_output_dir, "README.md"), **context)

        # Generate configuration files
        self.render_template("a2a_agent/langgraph.json.tpl",
                            os.path.join(agent_output_dir, "langgraph.json"), **context)

        # Generate .env.example file
        self.render_template("a2a_agent/env.tpl",
                            os.path.join(agent_output_dir, ".env.example"), **context)

        # Run ruff formatting on generated files
        python_files = [
            os.path.join(agent_pkg_dir, "agentcard.py"),
            os.path.join(agent_pkg_dir, "__main__.py"),
            os.path.join(a2a_server_dir, "agent.py"),
            os.path.join(a2a_server_dir, "agent_executor.py"),
            os.path.join(utils_dir, "base_agent.py"),
            os.path.join(utils_dir, "base_agent_executor.py"),
            os.path.join(utils_dir, "prompt_templates.py"),
            os.path.join(a2a_client_dir, "agent.py"),
        ]

        for file_path in python_files:
            if not self.dry_run and os.path.exists(file_path):
                self.run_ruff_lint(file_path)

#!/usr/bin/env bash
# workspaceOpen hook: load repo-bundled Cursor plugins for everyone who opens
# this workspace. Emits an absolute path so it is portable across checkouts.
# Docs: https://cursor.com/docs/hooks (#workspaceOpen, pluginPaths output)
set -euo pipefail

root="${CURSOR_PROJECT_DIR:-$(pwd)}"
plugin_dir="${root}/.cursor/plugins/acme-sdk-accelerator"

if [ -d "${plugin_dir}" ]; then
  printf '{"pluginPaths":["%s"]}\n' "${plugin_dir}"
else
  printf '{"pluginPaths":[]}\n'
fi

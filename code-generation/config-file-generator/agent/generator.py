"""Config file generation engine.

Generates ESLint, Prettier, TSConfig, EditorConfig, gitignore,
Dockerfile, docker-compose, GitHub Actions, and more from presets.
"""
from __future__ import annotations

import json
from dataclasses import dataclass


# --- Config Templates ---

TEMPLATES = {
    "eslint": {
        "description": "ESLint configuration",
        "filename": ".eslintrc.json",
        "presets": {
            "default": {
                "env": {"browser": True, "es2024": True, "node": True},
                "extends": ["eslint:recommended"],
                "parserOptions": {"ecmaVersion": "latest", "sourceType": "module"},
                "rules": {
                    "no-unused-vars": "warn",
                    "no-console": "warn",
                    "eqeqeq": "error",
                    "no-var": "error",
                    "prefer-const": "error",
                },
            },
            "react": {
                "env": {"browser": True, "es2024": True},
                "extends": ["eslint:recommended", "plugin:react/recommended", "plugin:react-hooks/recommended"],
                "parserOptions": {"ecmaVersion": "latest", "sourceType": "module", "ecmaFeatures": {"jsx": True}},
                "plugins": ["react", "react-hooks"],
                "settings": {"react": {"version": "detect"}},
                "rules": {"react/prop-types": "off", "no-unused-vars": "warn"},
            },
            "typescript": {
                "parser": "@typescript-eslint/parser",
                "extends": ["eslint:recommended", "plugin:@typescript-eslint/recommended"],
                "plugins": ["@typescript-eslint"],
                "rules": {
                    "@typescript-eslint/no-unused-vars": "warn",
                    "@typescript-eslint/explicit-function-return-type": "off",
                    "@typescript-eslint/no-explicit-any": "warn",
                },
            },
            "nextjs": {
                "extends": ["next/core-web-vitals", "next/typescript"],
                "rules": {"@next/next/no-img-element": "off"},
            },
        },
    },
    "prettier": {
        "description": "Prettier configuration",
        "filename": ".prettierrc",
        "presets": {
            "default": {
                "semi": True, "singleQuote": True, "tabWidth": 2,
                "trailingComma": "all", "printWidth": 100,
                "arrowParens": "always", "endOfLine": "lf",
            },
            "minimal": {
                "semi": False, "singleQuote": True, "tabWidth": 2,
            },
            "standard": {
                "semi": True, "singleQuote": False, "tabWidth": 4,
                "trailingComma": "es5", "printWidth": 80,
            },
        },
    },
    "tsconfig": {
        "description": "TypeScript configuration",
        "filename": "tsconfig.json",
        "presets": {
            "default": {
                "compilerOptions": {
                    "target": "ES2022", "module": "ESNext", "moduleResolution": "bundler",
                    "strict": True, "esModuleInterop": True, "skipLibCheck": True,
                    "forceConsistentCasingInFileNames": True, "resolveJsonModule": True,
                    "declaration": True, "declarationMap": True, "sourceMap": True,
                    "outDir": "./dist",
                },
                "include": ["src/**/*"],
                "exclude": ["node_modules", "dist"],
            },
            "nextjs": {
                "compilerOptions": {
                    "target": "ES2017", "lib": ["dom", "dom.iterable", "esnext"],
                    "allowJs": True, "skipLibCheck": True, "strict": True,
                    "noEmit": True, "esModuleInterop": True,
                    "module": "esnext", "moduleResolution": "bundler",
                    "resolveJsonModule": True, "isolatedModules": True,
                    "jsx": "preserve", "incremental": True,
                    "plugins": [{"name": "next"}],
                    "paths": {"@/*": ["./*"]},
                },
                "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
                "exclude": ["node_modules"],
            },
        },
    },
    "editorconfig": {
        "description": "EditorConfig",
        "filename": ".editorconfig",
        "format": "ini",
        "presets": {
            "default": {
                "root": True,
                "[*]": {
                    "indent_style": "space", "indent_size": 2, "end_of_line": "lf",
                    "charset": "utf-8", "trim_trailing_whitespace": True,
                    "insert_final_newline": True,
                },
                "[*.md]": {"trim_trailing_whitespace": False},
                "[*.py]": {"indent_size": 4},
                "[Makefile]": {"indent_style": "tab"},
            },
        },
    },
    "gitignore": {
        "description": "Git ignore rules",
        "filename": ".gitignore",
        "format": "text",
        "presets": {
            "node": [
                "node_modules/", "dist/", "build/", ".next/", ".nuxt/",
                ".cache/", "coverage/", "*.log", ".env", ".env.local",
                ".DS_Store", "*.tsbuildinfo",
            ],
            "python": [
                "__pycache__/", "*.pyc", ".venv/", "venv/", "dist/",
                "*.egg-info/", ".pytest_cache/", ".mypy_cache/",
                "htmlcov/", ".coverage", ".env", ".DS_Store",
            ],
            "rust": [
                "target/", "Cargo.lock", "*.pdb", ".DS_Store",
            ],
            "go": [
                "bin/", "*.exe", "*.test", "vendor/", ".DS_Store",
            ],
        },
    },
    "dockerfile": {
        "description": "Dockerfile",
        "filename": "Dockerfile",
        "format": "dockerfile",
        "presets": {
            "node": [
                "FROM node:20-alpine AS builder",
                "WORKDIR /app",
                "COPY package*.json ./",
                "RUN npm ci",
                "COPY . .",
                "RUN npm run build",
                "",
                "FROM node:20-alpine",
                "WORKDIR /app",
                "COPY --from=builder /app/dist ./dist",
                "COPY --from=builder /app/node_modules ./node_modules",
                "COPY --from=builder /app/package.json ./",
                "EXPOSE 3000",
                'CMD ["node", "dist/index.js"]',
            ],
            "python": [
                "FROM python:3.12-slim",
                "WORKDIR /app",
                "COPY requirements.txt .",
                "RUN pip install --no-cache-dir -r requirements.txt",
                "COPY . .",
                "EXPOSE 8000",
                'CMD ["python", "main.py"]',
            ],
        },
    },
    "github-actions": {
        "description": "GitHub Actions CI workflow",
        "filename": ".github/workflows/ci.yml",
        "format": "yaml",
        "presets": {
            "node": """name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build
""",
            "python": """name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
""",
        },
    },
}


def list_config_types() -> list[dict]:
    """List all available config types."""
    return [
        {"type": name, "description": t["description"], "filename": t["filename"],
         "presets": list(t["presets"].keys())}
        for name, t in TEMPLATES.items()
    ]


def list_presets(config_type: str) -> list[str]:
    """List available presets for a config type."""
    template = TEMPLATES.get(config_type)
    if not template:
        return []
    return list(template["presets"].keys())


def generate_config(config_type: str, preset: str = "default",
                    overrides: dict | None = None) -> dict:
    """Generate a config file.

    Returns:
        dict with filename, content, format.
    """
    template = TEMPLATES.get(config_type)
    if not template:
        return {"error": f"Unknown config type: {config_type}"}

    presets = template["presets"]
    if preset not in presets:
        return {"error": f"Unknown preset: {preset}. Available: {list(presets.keys())}"}

    config_data = presets[preset]
    fmt = template.get("format", "json")

    # Apply overrides for dict-based configs
    if overrides and isinstance(config_data, dict):
        config_data = {**config_data, **overrides}

    # Format output
    if fmt == "json":
        content = json.dumps(config_data, indent=2)
    elif fmt == "text":
        content = "\n".join(config_data) + "\n"
    elif fmt == "dockerfile":
        content = "\n".join(config_data) + "\n"
    elif fmt == "yaml":
        content = config_data  # already a string
    elif fmt == "ini":
        content = format_editorconfig(config_data)
    else:
        content = json.dumps(config_data, indent=2)

    return {
        "filename": template["filename"],
        "content": content,
        "format": fmt,
        "config_type": config_type,
        "preset": preset,
    }


def format_editorconfig(data: dict) -> str:
    """Format EditorConfig data to INI-style format."""
    lines = []
    if data.get("root"):
        lines.append("root = true\n")

    for section, values in data.items():
        if section == "root":
            continue
        lines.append(f"{section}")
        for key, val in values.items():
            val_str = str(val).lower() if isinstance(val, bool) else str(val)
            lines.append(f"{key} = {val_str}")
        lines.append("")

    return "\n".join(lines)


def generate_multiple(config_types: list[str], preset: str = "default") -> list[dict]:
    """Generate multiple config files at once."""
    return [generate_config(ct, preset) for ct in config_types]


def detect_project_type(files: list[str]) -> str:
    """Detect project type from file listing."""
    file_set = set(f.lower() for f in files)

    if "package.json" in file_set:
        if "next.config.js" in file_set or "next.config.mjs" in file_set or "next.config.ts" in file_set:
            return "nextjs"
        if any("react" in f for f in file_set):
            return "react"
        return "node"
    if "requirements.txt" in file_set or "pyproject.toml" in file_set:
        return "python"
    if "cargo.toml" in file_set:
        return "rust"
    if "go.mod" in file_set:
        return "go"
    return "unknown"

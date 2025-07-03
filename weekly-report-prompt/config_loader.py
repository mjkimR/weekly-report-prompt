from pathlib import Path

import yaml
import os


class ConfigLoader:
    def __init__(self, config_path=None, template_path=None):
        if config_path is None:
            config_path = os.path.join(Path(__file__).parent.parent, "config", "config.yaml")
        if template_path is None:
            template_path = os.path.join(Path(__file__).parent.parent, "config", "template.md")

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template file not found: {template_path}")
        with open(template_path, 'r', encoding='utf-8') as f:
            self.template = f.read()

    def get(self, key, default=None):
        return self.config.get(key, default)

    def get_author(self):
        return self.config.get('author')

    def get_repositories(self):
        return self.config.get('repository', [])

    def get_max_diff_lines(self):
        return self.config.get('max_diff_lines', 25)

    def get_lang(self):
        return self.config.get('lang', 'ko')

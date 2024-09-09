from requests import get
from re import match as re_match
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from datetime import datetime
from jinja2.environment import Environment
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files


class MoneroMetricsPlugin(BasePlugin):

    metrics_data: dict = {}

    config_scheme = (
        ('endpoints', config_options.Type(list, default=[])),
        ('time_format', config_options.Type(str, default='%Y-%m-%d %H:%M:%S')),  # Default time format
        ('defaults', config_options.Type(dict, default={})),  # default fallback values
    )

    def __init__(self):
        super().__init__()
        self.metrics_data = {key: value for key, value in self.config['defaults'].items if key.startswith('monero_'}

    # Collect metrics
    def on_pre_build(self, config: MkDocsConfig):
        self.metrics_data.update(self.collect_metrics())

    # Inject metrics into the jinja2 template globals
    def on_env(self, env: Environment, config: MkDocsConfig, files: Files):
        env.globals.update(self.metrics_data)

    def collect_metrics(self) -> dict[str, str | float | int]:
        all_metrics = {}
        for endpoint in self.config['endpoints']:
            try:
                response = get(endpoint)
                response.raise_for_status()
                metrics = self.parse_metrics(response.text)
                all_metrics.update(metrics)
            except Exception as e:
                print(f"Error fetching metrics from {endpoint}: {e}")
        return all_metrics

    def parse_metrics(self, metrics_text: str) -> dict[str, str | float | int]:
        metrics: dict[str, str | float | int] = {}
        for line in metrics_text.splitlines():
            match = re_match(r'([^#\s]+)\s+([0-9.e+-]+)', line)
            if match and line.startswith('monero_'):
                key = match.group(1)
                value = float(match.group(2))
                metrics[key] = self.format_metric(key, value)
        return metrics

    def format_metric(self, key: str, value: float) -> string | float | int:
        if key.endswith('_timestamp') or key.endswith('_file_last_update'):
            return datetime.utcfromtimestamp(value).strftime(self.config['time_format'])
        if key.endswith('_file_size'):
            return f'{(value / (1024**3)):.2f} GB'
        if key.endswith('_height'):
            return int(value)
        return value


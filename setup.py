from setuptools import setup

setup(
    name='mkdocs-monero-metrics-plugin',
    version='0.1',
    py_modules=['mkdocs_monero_metrics_plugin'],
    install_requires=[
        'mkdocs',
        'requests',
        'jinja2',
    ],
    entry_points={
        'mkdocs.plugins': [
            'monero-metrics = mkdocs_monero_metrics_plugin:MoneroMetricsPlugin',
        ]
    }
)

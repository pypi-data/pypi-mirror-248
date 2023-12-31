# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ai']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'opentelemetry-semantic-conventions-ai',
    'version': '0.0.13',
    'description': 'OpenTelemetry Semantic Conventions Extension for Large Language Models',
    'long_description': '# OpenTelemetry Semantic Conventions extensions for gen-AI applications\n\n<a href="https://pypi.org/project/opentelemetry-semantic-conventions-ai/">\n    <img src="https://badge.fury.io/py/opentelemetry-semantic-conventions-ai.svg">\n</a>\n\nThis is an extension of the standard [OpenTelemetry Semantic Conventions](https://github.com/open-telemetry/semantic-conventions) for gen AI applications. It defines additional attributes for spans that are useful for debugging and monitoring prompts, completions, token usage, etc.\n',
    'author': 'Gal Kleinman',
    'author_email': 'gal@traceloop.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.1,<4',
}


setup(**setup_kwargs)

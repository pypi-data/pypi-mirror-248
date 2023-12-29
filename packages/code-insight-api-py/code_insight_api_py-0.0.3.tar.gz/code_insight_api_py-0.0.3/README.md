# code-insight-api-py
A Python client for Revenera Code Insight

[![License](https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg)](https://opensource.org/licenses/Apache-2.0)
![Python 3.9](https://upload.wikimedia.org/wikipedia/commons/1/1b/Blue_Python_3.9_Shield_Badge.svg)
[![PyPI](https://img.shields.io/pypi/v/code-insight-api-py?style=plastic)](https://pypi.org/project/code-insight-api-py/)
[![Download Stats](https://img.shields.io/pypi/dm/code-insight-api-py)](https://pypistats.org/packages/code-insight-api-py)

## Basic Usage

```python
import code_insight_api_py as cia
client = cia.CodeInsightApiClient("<your-base-url>","<your-api-token>")

projects = client.projects.all()
```


## References
* [Code Insight Rest API Documentation](https://codeinsightapi-2023r2.redoc.ly/)
* [Code Insight Rest API Python Examples](https://github.com/flexera-public/sca-codeinsight-restapi-python/tree/master)
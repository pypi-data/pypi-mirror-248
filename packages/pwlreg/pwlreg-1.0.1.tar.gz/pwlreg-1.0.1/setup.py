# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pwlreg']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.1,<2.0.0', 'scikit-learn>=1.2.0,<2.0.0', 'scipy>=1.9.3,<2.0.0']

setup_kwargs = {
    'name': 'pwlreg',
    'version': '1.0.1',
    'description': 'A scikit-learn-compatible implementation of Piecewise Linear Regression',
    'long_description': '# pwlreg\n\n[![Tests](https://github.com/ensley-nexant/pwlreg/actions/workflows/tests.yml/badge.svg)](https://github.com/ensley-nexant/pwlreg/actions/workflows/tests.yml)\n[![codecov](https://codecov.io/gh/ensley-nexant/pwlreg/branch/main/graph/badge.svg?token=x8l1hx77eL)](https://codecov.io/gh/ensley-nexant/pwlreg)\n\nA scikit-learn-compatible implementation of Piecewise Linear Regression\n\n## Installation\n\n```\npip install pwlreg\n```\n\n## Documentation\n\n[See the documentation here](https://ensley-nexant.github.io/pwlreg/).\n\n\n```python\nimport numpy as np\nimport matplotlib.pyplot as plt\n\nimport pwlreg as pw\n\n\nx = np.array([1., 2., 3., 4., 5., 6., 7., 8., 9., 10.])\ny = np.array([1., 1.5, 0.5, 1., 1.25, 2.75, 4, 5.25, 6., 8.5])\n\nm = pw.AutoPiecewiseRegression(n_segments=2, degree=[0, 1])\nm.fit(x, y)\n\nxx = np.linspace(1, 10, 100)\nplt.plot(x, y, "o")\nplt.plot(xx, m.predict(xx), "-")\nplt.show()\n```\n\n![pwlreg toy example](docs/img/img.png)\n\n```python\nm.coef_         # [ 1.00  -5.50  1.35 ]\nm.breakpoints_  # [ 1.000000  4.814815  10.000000 ]\n```\n\n$$\nx =\n\\begin{cases}\n1,            & 1 \\leq x < 4.815 \\\\\n-5.5 + 1.35x, & 4.815 \\leq x < 10\n\\end{cases}\n$$\n',
    'author': 'John Ensley',
    'author_email': 'jensley@resource-innovations.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ensley-nexant/pwlreg',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

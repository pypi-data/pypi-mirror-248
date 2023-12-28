# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lassen',
 'lassen.alembic',
 'lassen.assets',
 'lassen.core',
 'lassen.datasets',
 'lassen.db',
 'lassen.store',
 'lassen.stubs',
 'lassen.stubs.common',
 'lassen.stubs.generators',
 'lassen.stubs.templates',
 'lassen.tests',
 'lassen.tests.conftest_helpers',
 'lassen.tests.datasets',
 'lassen.tests.db',
 'lassen.tests.fixtures',
 'lassen.tests.fixtures.stubs',
 'lassen.tests.fixtures.test_harness.test_harness',
 'lassen.tests.fixtures.test_harness.test_harness.migrations',
 'lassen.tests.store',
 'lassen.tests.stubs',
 'lassen.tests.stubs.generators']

package_data = \
{'': ['*'], 'lassen.tests.fixtures': ['test_harness/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'alembic-autogenerate-enums>=0.1.1,<0.2.0',
 'alembic>=1.11.1,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'fastapi>=0.101.0,<0.102.0',
 'inflection>=0.5.1,<0.6.0',
 'pydantic-settings>=2.0.3,<3.0.0',
 'pydantic>=2.2.1,<3.0.0',
 'python-dotenv>=1.0.0,<2.0.0']

extras_require = \
{'aws': ['aioboto3>=12.0.0,<13.0.0', 'brotli>=1.0.9,<2.0.0'],
 'database': ['SQLAlchemy>=2.0.15,<3.0.0', 'psycopg2>=2.9.6,<3.0.0'],
 'datasets': ['datasets>=2.13.0,<3.0.0',
              'numpy>=1.24.3,<2.0.0',
              'pandas>=2.0.2,<3.0.0']}

entry_points = \
{'console_scripts': ['generate-lassen = lassen.stubs.generate:cli',
                     'migrate = lassen.alembic.cli:main']}

setup_kwargs = {
    'name': 'lassen',
    'version': '0.5.0',
    'description': 'Common webapp scaffolding.',
    'long_description': '# lassen\n\n**40.4881° N, 121.5049° W**\n\nCore utilities for MonkeySee web applications. Not guaranteed to be backwards compatible, use at your own risk.\n\nAt its core, Lassen tries to:\n\n- Provide a suite of conventions for the 99% case of CRUD backends: manipulating data, storing it, and serving to frontends.\n- Create typehinted definitions for everything to provide robust mypy support up and down the stack.\n- Configure settings by environment variables, with a standard set of keys for database connections and web services.\n- Make common things trivial and hard things possible.\n\nWe also build connective tissue between fast, more tailored libraries:\n\n- FastAPI for webapp routes\n- Pydantic for data validation\n- SQLAlchemy for database management\n- Alembic for database migrations\n\n## Design Philosophy\n\nBackends revolve around a core set of data objects. In the early days of design, these typically mirror the business objectives almost 1:1 (User, Team, Project). As complexity grows, they might also start to include auxiliary metadata, such as state enums or locally cached copies of other tables. These objects might be further optimized for the database engine: indexes, refactored foreign keys, etc. This creates a divergence between the data objects and the API that hosts it to the outside world.\n\nIn some ways database tables are like choosing the best data structure. They should efficiently move data from disk to memory to remote clients, and back again. So long as the data conversion is fast and lossless, it doesn\'t matter as much how the sausage is made.\n\nA web API on the other hand aims to provide semantic objects to clients. These should be the objects and actions that represent your domain. The API layer should intentionally contrain the state/action space to be context aware. Useful APIs don\'t just mirror the database.\n\nIn Lassen, we view CRUD actions as projections on top of the underlying data objects. They might involve field merges, field subset, etc. Most libraries solve for this divergence by forcing a forking of class definitions: a separate definition to Create, to Update, etc. This often creates redundent code that\'s hard to sift through and reason about when adding new behavior.\n\nRather than configuring this CRUD at a class level, we focus on the CRUD actions that users can perform on each field. The `Stub` class defined below specifies _one_ key that is backed by a database value, and then generates CRUD schemas for API use depending on the allowed permissions for each field. Through this key-wise definition, we aim to clearly delineate in code and API contracts what is permitted, while aligning access patterns with the data values themselves.\n\n## Structure\n\n**Stores:** Each datamodel is expected to have its own store. Base classes that provide standard logic are provided by `lassen.store`\n- StoreBase: Base class for all stores\n- StoreFilterMixin: Mixin for filtering stores that specify an additional schema to use to filter\n- StoreS3Mixin: Mixin for stores that use S3 for external storage of a piece of data. Support compression on both upload and downloads.\n\n**Schemas:** Each datamodel should define a Model class (SQLAlchemy base object) and a series of Schema objects (Pydantic) that allow the Store to serialize the models. These schemas are also often used for direct CRUD referencing in the API layer.\n\nWe use a base `Stub` file to generate these schemas from a centralized definition. When defining generators you should use a path that can be fully managed by lassen, since we will remove and regenerate these files on each run.\n\n```python\nSTORE_GENERATOR = StoreGenerator("models/auto")\nSCHEMA_GENERATOR = SchemaGenerator("schemas/auto")\n```\n\n```bash\npoetry run generate-lassen\n```\n\n**Migrations:** Lassen includes a templated alembic.init and env.py file. Client applications just need to have a `migrations` folder within their project root. After this you can swap `poetry run alembic` with `poetry run migrate`.\n\n```sh\npoetry run migrate upgrade head\n```\n\n**Settings:** Application settings should subclass our core settings. This provides a standard way to load settings from environment variables and includes common database keys.\n\n```python\nfrom lassen.core.config import CoreSettings, register_settings\n\n@register_settings\nclass ClientSettings(CoreSettings):\n    pass\n```\n\n**Schemas:** For helper schemas when returning results via API, see [lassen.schema](./lassen/schema.py).\n\n## Development\n\nInstall all the extra dependencies so you can fully run the unit test suite.\n\n```sh\npoetry install --extras "aws database datasets"\n\ncreateuser lassen\ncreatedb -O lassen lassen_db\ncreatedb -O lassen lassen_test_db\n```\n\nUnit Tests:\n\n```sh\npoetry run pytest\n```\n',
    'author': 'Pierce Freeman',
    'author_email': 'pierce@freeman.vc',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)

import setuptools

__version__ = "0.0.8"

setuptools.setup(name='datasherlock',
                 version=__version__,
                 description='datasherlock',
                 long_description=open('README.md').read().strip(),
                 author='datasherlock',
                 author_email='founder@textquery.dev',
                 url='http://datasherlocks.io',
                 py_modules=['sherlockai'],
                 install_requires=[
                    "pytest",
                    "pytest-cov",
                    "grpcio==1.50.0",
                    "grpcio-tools==1.50.0",
                    "protobuf==4.21.9",
                    "pandas",
                    "pymysql",
                    "psycopg2-binary",
                    "mysql-connector-python",
                    "google-cloud-bigquery"  
                 ],
                 zip_safe=False,
                 keywords='datasherlocks',
                 classifiers=[
                        # Indicate who your project is intended for
                        'Intended Audience :: Developers',

                        # Specify the Python versions you support here. In particular, ensure
                        # that you indicate whether you support Python 2, Python 3 or both.
                        'Programming Language :: Python :: 3',
                        'Programming Language :: Python :: 3.4',
                        'Programming Language :: Python :: 3.5',
                        'Programming Language :: Python :: 3.6',
                    ],
  )

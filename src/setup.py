"""
    https://packaging.python.org/distributing/
    https://pypi.python.org/pypi?%3Aaction=list_classifiers
    http://semver.org/

    zero or more dev releases (denoted with a ”.devN” suffix)
    zero or more alpha releases (denoted with a ”.aN” suffix)
    zero or more beta releases (denoted with a ”.bN” suffix)
    zero or more release candidates (denoted with a ”.rcN” suffix)
"""

from setuptools import setup, find_packages

setup(name='warden-api',
          version='3.0.2',
          description='Aplicación para manejar los perfiles de los sistemas',
          url='https://github.com/pablodanielrey/warden-api',
          author='Desarrollo DiTeSi, FCE',
          author_email='ditesi@econo.unlp.edu.ar',
          classifiers=[
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5'
          ],
          packages=find_packages(exclude=['contrib', 'docs', 'test*']),
          install_requires=['Flask',
                            'flask_jsontools',
                            'gunicorn',
                            'ptvsd',
                            'microservices_common>=2.0.4a4',
                            'requests',
                            'psycopg2-binary'
                            ],
          entry_points={
            'console_scripts': [
                'flask=warden.web.main:main'
            ]
          }

      )

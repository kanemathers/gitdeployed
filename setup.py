import os

from setuptools import setup, find_packages

here    = os.path.abspath(os.path.dirname(__file__))
README  = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'gitpython',
    'py-bcrypt',
    ]

setup(name='gitdeployed',
      version='0.7',
      description='gitdeployed',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Kane Mathers',
      author_email='kane@kanemathers.name',
      url='https://github.com/kanemathers/gitdeployed',
      keywords='web wsgi bfg pylons pyramid angularjs git service hooks',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='gitdeployed',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = gitdeployed:main
      [console_scripts]
      gitdeployed = gitdeployed.scripts.gitdeployed:main
      """,
      )

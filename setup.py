from setuptools import setup, find_packages
from webmentiontools import __version__

setup(version=__version__,
      name="webmentiontools",
      author="André Jaenisch",
      author_email="andre.jaenisch@posteo.de",
      description="Tools for webmention.org.",
      long_description=open('README.md').read(),
      packages=['webmentiontools'],
      install_requires=['beautifulsoup4', 'requests', 'docopt',],
      scripts=['bin/webmention-tools'],
      url='https://github.com/Ryuno-Ki/webmention-tools',
      license='LICENSE',
      include_package_data=True,
)

from setuptools import setup, find_packages
from webmentiontools import __version__

setup(version=__version__,
      name="webmention-tools",
      author="Panayotis Vryonis",
      author_email="vrypan@gmail.com",
      maintainer="André Jaenisch",
      maintainer_email="andre.jaenisch@posteo.de",
      description="Tools for webmention.org.",
      long_description=open("README.rst").read(),
      packages=["webmentiontools",],
      install_requires=["beautifulsoup4", "requests", "docopt",],
      scripts=["bin/webmention-tools",],
      url="https://github.com/Ryuno-Ki/webmention-tools",
      license="MIT",
      data_files=[("", ["LICENSE.txt",])],
      platforms=["Linux",],
      keywords=["webmention"],
      include_package_data=True,
      classifiers=[
          "Development Status :: 1 - Planning",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Topic :: Internet :: WWW/HTTP"
      ]
)

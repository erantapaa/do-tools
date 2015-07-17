from setuptools import setup

setup(name='droplet_utils',
      version='0.1',
      description='Utils I find useful for working with droplets.',
      url='',
      author='Erik Rantapaa',
      author_email='erantapaa@gmail.com',
      license='MIT',
      packages=['droplet_utils'],
      install_requires=[
          'psutil', 'tabulate', 'argparse'
      ],
      scripts=['bin/lighter'],
      zip_safe=False)

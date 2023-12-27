from setuptools import setup, find_packages

setup(name='remotehotkey',
      version='0.1.8',
      description='remotehotkey',
      url='',
      author='gw',
      author_email='',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
            "flask",
          # optional
          'opencv-python',
          'numpy',
          'mss',
          "pynput",
      ],
      zip_safe=False)

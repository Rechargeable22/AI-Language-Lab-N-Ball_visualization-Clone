from setuptools import setup, find_packages

setup(name='N-Balls-Visualization',
      version='0.1',
      description='High dimensions balls visualization',
      url='https://github.com/ghanem-mhd/N-Balls-Visualization',
      author='Mohamamd Ghanem',
      author_email='ghanem.mhd95@gmail.com',
      license='MIT',
      packages= find_packages(),
      package_data = {'': ['*.pickle'],},
      zip_safe=False)

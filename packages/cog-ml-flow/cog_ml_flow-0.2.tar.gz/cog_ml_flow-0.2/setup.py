from setuptools import setup, find_packages
setup(name='cog_ml_flow',
      version='0.2',
      url='',
      license='MIT',
      author='Veena Rao',
      author_email='veena.rao@hiro-microdatacenters.nl',
      description='cog mlflow',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False,
      #install_requires=["mlflow"]
      )
from setuptools import setup
setup(name='crabs',
      description='CRABS: Creating Reference databases for Amplicon-Based Sequencing',
      author='Gert-Jan Jeunen',
	  author_email='gjeunen@gmail.com',
	  url='https://github.com/gjeunen/reference_database_creator',
	  version='0.2.0',
      packages=['crabs'],
      install_requires=[
          'biopython >= 1.81',
          'tqdm',
          'numpy',
          'pandas >=0.23.4',
          'matplotlib'
      ],
      python_requires=">=3.6",
      entry_points={
          "console_scripts": [
              "crabs = crabs.crabs:main"
          ]
      }
)

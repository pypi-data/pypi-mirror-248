from setuptools import setup, find_packages
  
# reading long description from file
with open('DESCRIPTION.txt') as file:
    long_description = file.read()
  

# some more details
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: MacOS X',
    'Framework :: IDLE',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',#need to pick one
    'Natural Language :: English',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.11',
    'Topic :: Scientific/Engineering :: Bio-Informatics'
    'Topic :: Scientific/Engineering :: Information Analysis'
    ]
  
# calling the setup function 
setup(name='HIV_Isoform_Filter',
      version='1.0.2',
      description='Filters .gtf file of suspected HIV isoforms and confirms the isoform identities.',
      long_description=long_description,
      url='',#####
      author='Jessica Lauren ALbert',
      author_email='jessica.albert@seattlechildrens.org',
      license='MIT',
      packages = find_packages(),
      entry_points = {'console_scripts': ['HIV_Isoform_filter = HIV_Isoform_filter.__main__:main']},
      classifiers=CLASSIFIERS,
      keywords='HIV isoforms gtf_file CDS_region ONTsequencing',
      include_package_data = True
      )

from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='hejasverige.content',
      version=version,
      description="Content Types for Heja Sverige",
      long_description=open("README.md").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Daniel Grindelid',
      author_email='daniel.grindelid@swedwise.se',
      url='http://www.swedwise.com/hejasverige/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['hejasverige'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'plone.app.dexterity [grok]',
          'plone.app.referenceablebehavior',
          'plone.app.relationfield',
          'plone.namedfile [blobs]'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )

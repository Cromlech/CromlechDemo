from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='cromdemo',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          "Programming Language :: Python",
          ],
      keywords='',
      author='',
      author_email='',
      url='',
      license='ZPL2.1',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['cromdemo'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'crom',
          'cromlech.auth',
          'cromlech.browser',
          'cromlech.configuration',
          'cromlech.dawnlight',
          'cromlech.grok',
          'cromlech.i18n',
          'cromlech.security',
          'cromlech.location',
          'cromlech.webob',
          'cromlech.wsgistate',
          'dolmen.forms.base',
          'dolmen.forms.ztk',
          'dolmen.tales',
          'dolmen.template',
          'dolmen.view',
          'dolmen.viewlet',
          'fanstatic',
          'js.bootstrap',
          'js.jqueryui',
          'setuptools',
          'zope.interface',
          'zope.location',
          'zope.schema',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [paste.app_factory]
      demo = cromdemo.wsgi:demo_application

      [fanstatic.libraries]
      crom = cromdemo.browser.resources:Library
      """,
      )

from setuptools import setup, find_packages
from django_openai_assistant import __version__

setup(
    name='django-openai-assistant',
    version=__version__,
    license='MIT',
    author="Jean-Luc Vanhulst",
    author_email='jl@valor.vc',
    packages=['django_openai_assistant'],
    package_dir={'': 'src'},
    url='https://github.com/jlvanhulst/django-openai',
    keywords='django celery openai assistants',
    install_requires=[
         'openai','markdown','celery',
      ],

)
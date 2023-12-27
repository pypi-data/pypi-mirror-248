from setuptools import setup, find_packages

setup(
    name='django-openai-assistant',
    version='0.21',
    license='MIT',
    author="Jean-Luc Vanhulst",
    author_email='jl@valor.vc',
    packages=['django_openai_assistant'],
    package_dir={'': 'src'},
    url='https://github.com/jlvanhulst/django-openai',
    keywords='django celery openai assistants',
    install_requires=[
         'openai','markdown'
      ],

)
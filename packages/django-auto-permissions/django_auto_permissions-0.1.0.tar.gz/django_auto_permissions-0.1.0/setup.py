from setuptools import setup, find_packages

setup(
    name='django_auto_permissions',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    description='Automated permission generation for Django viewsets',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jeet Padhya',
    author_email='jeet.padhya@hotmail.com',
    url='https://github.com/jeetkreditserve/django_auto_permissions',
    install_requires=[
        'Django>=3.2',  # Specify the Django version requirement
        # Add other dependencies if needed
    ],
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)

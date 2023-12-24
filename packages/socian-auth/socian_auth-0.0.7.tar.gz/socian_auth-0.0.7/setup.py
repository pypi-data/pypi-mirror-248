import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='socian_auth',
    author='Socian Ltd.',
    author_email='admin@socian.ai',
    description='Socian Auth Python SDK for authentication and user management',
    keywords='socian auth authentication user-management sdk',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Socian-Ltd//socian_auth_sdk_python',
    project_urls={
        'Documentation': 'https://github.com/Socian-Ltd/socian_auth_sdk_python.git',
        'Source': 'https://github.com/Socian-Ltd/socian_auth_sdk_python.git',
        'Bug Reports': 'https://github.com/Socian-Ltd/socian_auth_sdk_python/issues',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=['requests'],
    license='MIT',
)

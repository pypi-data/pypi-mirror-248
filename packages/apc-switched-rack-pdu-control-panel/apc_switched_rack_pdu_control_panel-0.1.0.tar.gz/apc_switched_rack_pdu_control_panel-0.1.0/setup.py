from setuptools import find_namespace_packages, setup

with open('README.md', encoding='utf8') as f:
    long_description = f.read()

setup(
    name='apc_switched_rack_pdu_control_panel',
    version='0.1.0',
    description='APC switched rack PDU control panel',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/spike77453/apc-switched-rack-pdu-control-panel',
    author='Christian Schürmann',
    author_email='spike@fedoraproject.org',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: System',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    include_package_data=True,
    zip_safe=False,
    packages=find_namespace_packages(
        include=['apc_switched_rack_pdu_control_panel*']
    ),
    install_requires=[
        'Flask',
        'easysnmp',
    ],
)

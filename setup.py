import setuptools

setuptools.setup(
    name="cli-tasks",
    version="0.0.1",
    author="Sarath Menon",
    author_email="sarath.menon@rub.de",
    description="Command line task manager",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages('src'),
    package_dir={'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    install_requires=[''],
    #scripts=['bin/pathsampling', 'bin/pathsampling_kernel'],
    entry_points={
        'console_scripts': [
            'pathsampling = pathsampling.bin.gtis:main',
            'pathsampling_kernel = pathsampling.bin.gtiskernel:main',
        ],
    }
)

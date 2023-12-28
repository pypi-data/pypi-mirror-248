import setuptools

setuptools.setup(
    version='0.0.3',
    packages=setuptools.find_packages(exclude=['test']),
    python_requires='>=3.7',
    setup_requires=["numpy"],  # Just numpy here
    install_requires=["numpy"],  # Add any of your other dependencies here
)

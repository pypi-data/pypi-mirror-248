from setuptools import setup , find_packages 

classifiers = []

setup(
    name='tarda',
    version='0.0.5',
    description='A library for collection of IDS & robust-IDS and tools for evaluating them',
    long_description=open("README.md").read() + '\n\n' + open("CHANGELOG.txt").read(),
    url='https://github.com/spg-iitd/tardigrade',
    author='Swain Subrat Kumar',
    author_email='mailofswainsubrat@gmail.com',
    license='MIT',
    # classifiers=classifiers,
    keywords='ids adversarial network nids',
    packages=['tardigrade'],
    install_requires=['scapy', 'numpy', 'pandas', 'matplotlib', 'scikit-learn', 'scipy', 'tqdm', 'torch', 'torchvision', 'torchsummary', 'torchattacks', 'torchattacks', 'torchatta'],
    zip_safe=False
)

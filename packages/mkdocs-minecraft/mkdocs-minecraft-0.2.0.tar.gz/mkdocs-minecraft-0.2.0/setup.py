from setuptools import setup, find_packages


setup(
    name='mkdocs_minecraft',
    version='0.2.0',
    description='A MkDocs Minecraft Recipes plugin',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='mkdocs',
    url='',
    author='Katzen48 | Tobi',
    author_email='admin@katzen48.de',
    license='MIT',
    python_requires='>=3.7',
    install_requires=[
        'mkdocs>=1.5.3'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'minecraft = mkdocs_minecraft:MinecraftPlugin'
        ]
    }
)

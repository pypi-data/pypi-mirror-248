from setuptools import setup, find_packages

setup(
    name='econnect',
    version='0.1.2',
    description='Paquete para conectarse al Portal Cautivo de Etecsa en Cuba desde Python.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Alejandro Pérez Santana',
    author_email='alejandroperezsantana55@gmail.com',
    url='https://github.com/TheMrAleX/econnect',
    license_files=['LICENSE'],
    packages=find_packages(),
    install_requires=[paquete.strip() for paquete in open('requirements.txt').readlines()],
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP :: Session'
    ]
)
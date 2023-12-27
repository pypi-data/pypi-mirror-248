from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Engine FaaS SDK'
LONG_DESCRIPTION = 'Engine FaaS SDK'

# 配置
setup(
        name="enginefaas", 
        version=VERSION,
        author="faas engineer",
        author_email="faas@email.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        #packages=find_packages(),
        packages=["enginefaas", "enginefaas.common", "enginefaas.common.exception", "enginefaas.common.http", "enginefaas.common.profile"],
        install_requires=[],
        
        keywords=['python', 'faas'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3"
        ]
)
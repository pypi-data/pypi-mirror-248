from setuptools import setup

setup(
    name='Aipixy',
    version='1.0.0',
    author='Dan Arbib',
    author_email='support@aipixy.com',
    description='A Python library for the Aipixy API, enabling the generation of personalized and dynamic clone videos.',
    url='https://github.com/DanArbib/Aipixy-Python',
    packages=['Aipixy'],
    install_requires=[
        'requests'
    ],
)
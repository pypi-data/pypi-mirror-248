from setuptools import setup, find_packages


setup(
    name='sdpc_linux',
    version='2.0',
    description='a library for sdpcPY (linux version)',
    license='MIT License',

    url='https://github.com/WonderLandxD/sdpc-for-python',
    author='Jiawen Li',
    author_email='lijiawen21@mails.tsinghua.edu.cn',

    packages=find_packages(),
    include_package_data=True,
    platforms='linux',
    install_requires=['numpy', 'opencv-python']
)
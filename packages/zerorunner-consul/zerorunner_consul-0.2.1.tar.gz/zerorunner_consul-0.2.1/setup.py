# -*- coding: utf-8 -*-
# @author: xiao bai

from setuptools import setup, find_packages

#  token
# pypi-AgEIcHlwaS5vcmcCJDQ0NGUyYzY4LTIzYTQtNDRkYS1hOTUyLTA0NDk3NTA0YWI5YwACKlszLCI1NzQ3Yjk0OS00ZmIxLTQ2MDEtOTFmYS1lM2ZjNWYwZmQzNTYiXQAABiBGVJHl48BK4-r45ZNwrM6USSe1CjAg1j-BAvawgLb_Aw

setup(
    name='zerorunner-consul',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        "requests"
        # 任何依赖项都在这里列出
    ],
    extras_require={
        'asyncio': ['aiohttp'],
    },
    author='xiao.bai',
    author_email='546142369@qq.com',
    description='Python client for Consul (https://www.consul.io/)',
    license='MIT',
    keywords='',
    url='https://github.com/baizunxian/zerorunner-consul'
)

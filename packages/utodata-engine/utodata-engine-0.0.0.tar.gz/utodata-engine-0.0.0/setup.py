from setuptools import setup, find_packages
setup(
    name="utodata-engine",
    version="0.0.0",
    author="uto-dataplatform",
    author_email="data-platform@utopilot.ai",
    description="【友道智途-数据平台】数据引擎SDK：支持创建数据引擎工作流、创建、同步、更新训练数据集，获取工作流及节点信息等",
    packages=find_packages(),
    python_request='>=3.6',
    install_requires=[
        'requests'
    ]
)



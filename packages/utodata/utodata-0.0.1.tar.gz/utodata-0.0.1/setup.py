from setuptools import setup, find_packages
setup(
    name="utodata",
    version="0.0.1",
    author="uto-dataplatform",
    author_email="data-platform@utopilot.ai",
    description="友道智途-数据平台,数据闭环SDK",
    packages=find_packages(),
    python_request='>=3.7',
    install_requires=[
        'requests'
    ]
)



from setuptools import setup, find_packages
setup(
    name="train_dataset",
    version="0.0.0",
    author="zhangjingwei",
    author_email="zhangjingwei@utopilot.ai",
    description="create argo-workflow tasks & sync training datasets",
    packages=find_packages(),
    python_request='>=3.6',
    install_requires=[
        'requests'
    ]
)



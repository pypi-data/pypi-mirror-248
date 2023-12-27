import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "pepperize.cdk-serverless-cluster-from-snapshot",
    "version": "0.0.801",
    "description": "Deprecated: Use https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_rds.ServerlessClusterFromSnapshot.html",
    "license": "MIT",
    "url": "https://github.com/pepperize/cdk-serverless-cluster-from-snapshot.git",
    "long_description_content_type": "text/markdown",
    "author": "Patrick Florek<patrick.florek@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/pepperize/cdk-serverless-cluster-from-snapshot.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "pepperize_cdk_serverless_cluster_from_snapshot",
        "pepperize_cdk_serverless_cluster_from_snapshot._jsii"
    ],
    "package_data": {
        "pepperize_cdk_serverless_cluster_from_snapshot._jsii": [
            "cdk-serverless-cluster-from-snapshot@0.0.801.jsii.tgz"
        ],
        "pepperize_cdk_serverless_cluster_from_snapshot": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.8.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.93.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 7 - Inactive",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)

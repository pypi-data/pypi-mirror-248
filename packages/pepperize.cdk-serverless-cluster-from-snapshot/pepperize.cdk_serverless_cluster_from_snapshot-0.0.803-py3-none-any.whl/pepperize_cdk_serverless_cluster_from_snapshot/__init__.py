'''
[![GitHub](https://img.shields.io/github/license/pepperize/cdk-serverless-cluster-from-snapshot?style=flat-square)](https://github.com/pepperize/cdk-serverless-cluster-from-snapshot/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@pepperize/cdk-serverless-cluster-from-snapshot?style=flat-square)](https://www.npmjs.com/package/@pepperize/cdk-serverless-cluster-from-snapshot)
[![PyPI](https://img.shields.io/pypi/v/pepperize.cdk-serverless-cluster-from-snapshot?style=flat-square)](https://pypi.org/project/pepperize.cdk-serverless-cluster-from-snapshot/)
[![Nuget](https://img.shields.io/nuget/v/Pepperize.CDK.ServerlessClusterFromSnapshot?style=flat-square)](https://www.nuget.org/packages/Pepperize.CDK.ServerlessClusterFromSnapshot/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/pepperize/cdk-serverless-cluster-from-snapshot/release/main?label=release&style=flat-square)](https://github.com/pepperize/cdk-serverless-cluster-from-snapshot/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/pepperize/cdk-serverless-cluster-from-snapshot?sort=semver&style=flat-square)](https://github.com/pepperize/cdk-serverless-cluster-from-snapshot/releases)

# AWS RDS Aurora serverless cluster from snapshot

> Deprecated: Use https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_rds.ServerlessClusterFromSnapshot.html

This project provides a CDK construct creating a serverless database cluster from a snapshot with AWS RDS Aurora engine.

See [API.md](https://github.com/pepperize/cdk-serverless-cluster-from-snapshot/blob/main/API.md)

## Install

### TypeScript

```shell
npm install @pepperize/cdk-serverless-cluster-from-snapshot
```

or

```shell
yarn add @pepperize/cdk-serverless-cluster-from-snapshot
```

### Python

```shell
pip install pepperize.cdk-serverless-cluster-from-snapshot
```

### C# / .Net

```
dotnet add package Pepperize.CDK.ServerlessClusterFromSnapshot
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_rds as _aws_cdk_aws_rds_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.implements(_aws_cdk_aws_rds_ceddda9d.IServerlessCluster)
class ServerlessClusterFromSnapshot(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@pepperize/cdk-serverless-cluster-from-snapshot.ServerlessClusterFromSnapshot",
):
    '''(deprecated) A Serverless Cluster restored from a snapshot.

    :stability: deprecated
    :resource: AWS::RDS::DBInstance
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        engine: _aws_cdk_aws_rds_ceddda9d.IClusterEngine,
        snapshot_identifier: builtins.str,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        backup_retention: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        cluster_identifier: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[_aws_cdk_aws_rds_ceddda9d.Credentials] = None,
        default_database_name: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[builtins.bool] = None,
        enable_data_api: typing.Optional[builtins.bool] = None,
        parameter_group: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IParameterGroup] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        scaling: typing.Optional[typing.Union[_aws_cdk_aws_rds_ceddda9d.ServerlessScalingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        storage_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        subnet_group: typing.Optional[_aws_cdk_aws_rds_ceddda9d.ISubnetGroup] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param engine: (deprecated) What kind of database to start.
        :param snapshot_identifier: (deprecated) The identifier for the DB snapshot or DB cluster snapshot to restore from. You can use either the name or the Amazon Resource Name (ARN) to specify a DB cluster snapshot. However, you can use only the ARN to specify a DB snapshot. After you restore a DB cluster with a SnapshotIdentifier property, you must specify the same SnapshotIdentifier property for any future updates to the DB cluster. When you specify this property for an update, the DB cluster is not restored from the snapshot again, and the data in the database is not changed. However, if you don't specify the SnapshotIdentifier property, an empty DB cluster is created, and the original DB cluster is deleted. If you specify a property that is different from the previous snapshot restore property, a new DB cluster is restored from the specified SnapshotIdentifier property, and the original DB cluster is deleted.
        :param vpc: (deprecated) The VPC that this Aurora Serverless cluster has been created in.
        :param backup_retention: (deprecated) The number of days during which automatic DB snapshots are retained. Automatic backup retention cannot be disabled on serverless clusters. Must be a value from 1 day to 35 days. Default: Duration.days(1)
        :param cluster_identifier: (deprecated) An optional identifier for the cluster. Default: - A name is automatically generated.
        :param credentials: (deprecated) Credentials for the administrative user. Default: - A username of 'admin' and SecretsManager-generated password
        :param default_database_name: (deprecated) Name of a database which is automatically created inside the cluster. Default: - Database is not created in cluster.
        :param deletion_protection: (deprecated) Indicates whether the DB cluster should have deletion protection enabled. Default: - true if removalPolicy is RETAIN, false otherwise
        :param enable_data_api: (deprecated) Whether to enable the Data API. Default: false
        :param parameter_group: (deprecated) Additional parameters to pass to the database engine. Default: - no parameter group.
        :param removal_policy: (deprecated) The removal policy to apply when the cluster and its instances are removed from the stack or replaced during an update. Default: - RemovalPolicy.SNAPSHOT (remove the cluster and instances, but retain a snapshot of the data)
        :param scaling: (deprecated) Scaling configuration of an Aurora Serverless database cluster. Default: - Serverless cluster is automatically paused after 5 minutes of being idle. minimum capacity: 2 ACU maximum capacity: 16 ACU
        :param security_groups: (deprecated) Security group. Default: - a new security group is created.
        :param storage_encryption_key: (deprecated) The KMS key for storage encryption. If you specify the SnapshotIdentifier property, the StorageEncrypted property value is inherited from the snapshot, and if the DB cluster is encrypted, the specified KmsKeyId property is used. Default: - the default master key will be used for storage encryption
        :param subnet_group: (deprecated) Existing subnet group for the cluster. Default: - a new subnet group will be created.
        :param vpc_subnets: (deprecated) Where to place the instances within the VPC. Default: - the VPC default strategy if not specified.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02b4e7be41e42a4d0aba31d2cde08b3d9da054f652ab229cf3fcdf2fba029256)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ServerlessClusterFromSnapshotProps(
            engine=engine,
            snapshot_identifier=snapshot_identifier,
            vpc=vpc,
            backup_retention=backup_retention,
            cluster_identifier=cluster_identifier,
            credentials=credentials,
            default_database_name=default_database_name,
            deletion_protection=deletion_protection,
            enable_data_api=enable_data_api,
            parameter_group=parameter_group,
            removal_policy=removal_policy,
            scaling=scaling,
            security_groups=security_groups,
            storage_encryption_key=storage_encryption_key,
            subnet_group=subnet_group,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addRotationMultiUser")
    def add_rotation_multi_user(
        self,
        id: builtins.str,
        *,
        secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        automatically_after: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        endpoint: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint] = None,
        exclude_characters: typing.Optional[builtins.str] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_secretsmanager_ceddda9d.SecretRotation:
        '''(deprecated) Adds the multi user rotation to this cluster.

        :param id: -
        :param secret: The secret to rotate. It must be a JSON string with the following format:: { "engine": <required: database engine>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port will be used>, "masterarn": <required: the arn of the master secret which will be used to create users/change passwords> }
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: - 30 days
        :param endpoint: The VPC interface endpoint to use for the Secrets Manager API. If you enable private DNS hostnames for your VPC private endpoint (the default), you don't need to specify an endpoint. The standard Secrets Manager DNS hostname the Secrets Manager CLI and SDKs use by default (https://secretsmanager..amazonaws.com) automatically resolves to your VPC endpoint. Default: https://secretsmanager..amazonaws.com
        :param exclude_characters: Specifies characters to not include in generated passwords. Default: " %+~`#$&*()|[]{}:;<>?!'/
        :param vpc_subnets: Where to place the rotation Lambda function. Default: - same placement as instance or cluster

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fcef260575cff50f6020a8b1026eca3010c75a62054850c10123d8a2a5fcf86)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_rds_ceddda9d.RotationMultiUserOptions(
            secret=secret,
            automatically_after=automatically_after,
            endpoint=endpoint,
            exclude_characters=exclude_characters,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.SecretRotation, jsii.invoke(self, "addRotationMultiUser", [id, options]))

    @jsii.member(jsii_name="addRotationSingleUser")
    def add_rotation_single_user(
        self,
        *,
        automatically_after: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        endpoint: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint] = None,
        exclude_characters: typing.Optional[builtins.str] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_secretsmanager_ceddda9d.SecretRotation:
        '''(deprecated) Adds the single user rotation of the master password to this cluster.

        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: - 30 days
        :param endpoint: The VPC interface endpoint to use for the Secrets Manager API. If you enable private DNS hostnames for your VPC private endpoint (the default), you don't need to specify an endpoint. The standard Secrets Manager DNS hostname the Secrets Manager CLI and SDKs use by default (https://secretsmanager..amazonaws.com) automatically resolves to your VPC endpoint. Default: https://secretsmanager..amazonaws.com
        :param exclude_characters: Specifies characters to not include in generated passwords. Default: " %+~`#$&*()|[]{}:;<>?!'/
        :param vpc_subnets: Where to place the rotation Lambda function. Default: - same placement as instance or cluster

        :stability: deprecated
        '''
        options = _aws_cdk_aws_rds_ceddda9d.RotationSingleUserOptions(
            automatically_after=automatically_after,
            endpoint=endpoint,
            exclude_characters=exclude_characters,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.SecretRotation, jsii.invoke(self, "addRotationSingleUser", [options]))

    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(
        self,
    ) -> _aws_cdk_aws_secretsmanager_ceddda9d.SecretAttachmentTargetProps:
        '''(deprecated) Renders the secret attachment target specifications.

        :stability: deprecated
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.SecretAttachmentTargetProps, jsii.invoke(self, "asSecretAttachmentTarget", []))

    @jsii.member(jsii_name="grantDataApiAccess")
    def grant_data_api_access(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant the given identity to access to the Data API, including read access to the secret attached to the cluster if present.

        :param grantee: The principal to grant access to.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7470b0229ed4dc476cf44a05c9cace0d0dd92a87419e9ff947e198099945223)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantDataApiAccess", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> builtins.str:
        '''(deprecated) The ARN of the cluster.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterArn"))

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> _aws_cdk_aws_rds_ceddda9d.Endpoint:
        '''(deprecated) The endpoint to use for read/write operations.

        :stability: deprecated
        '''
        return typing.cast(_aws_cdk_aws_rds_ceddda9d.Endpoint, jsii.get(self, "clusterEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> builtins.str:
        '''(deprecated) Identifier of the cluster.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterIdentifier"))

    @builtins.property
    @jsii.member(jsii_name="clusterReadEndpoint")
    def cluster_read_endpoint(self) -> _aws_cdk_aws_rds_ceddda9d.Endpoint:
        '''(deprecated) The endpoint to use for read/write operations.

        :stability: deprecated
        '''
        return typing.cast(_aws_cdk_aws_rds_ceddda9d.Endpoint, jsii.get(self, "clusterReadEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''(deprecated) Access to the network connections.

        :stability: deprecated
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        '''(deprecated) The secret attached to this cluster.

        :stability: deprecated
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret], jsii.get(self, "secret"))

    @builtins.property
    @jsii.member(jsii_name="enableDataApi")
    def _enable_data_api(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: deprecated
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enableDataApi"))

    @_enable_data_api.setter
    def _enable_data_api(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55266b5c88e611e9ec1495d5d65d3a04e84a3c99a81ba74c3dc8a361e1d012f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableDataApi", value)


@jsii.data_type(
    jsii_type="@pepperize/cdk-serverless-cluster-from-snapshot.ServerlessClusterFromSnapshotProps",
    jsii_struct_bases=[],
    name_mapping={
        "engine": "engine",
        "snapshot_identifier": "snapshotIdentifier",
        "vpc": "vpc",
        "backup_retention": "backupRetention",
        "cluster_identifier": "clusterIdentifier",
        "credentials": "credentials",
        "default_database_name": "defaultDatabaseName",
        "deletion_protection": "deletionProtection",
        "enable_data_api": "enableDataApi",
        "parameter_group": "parameterGroup",
        "removal_policy": "removalPolicy",
        "scaling": "scaling",
        "security_groups": "securityGroups",
        "storage_encryption_key": "storageEncryptionKey",
        "subnet_group": "subnetGroup",
        "vpc_subnets": "vpcSubnets",
    },
)
class ServerlessClusterFromSnapshotProps:
    def __init__(
        self,
        *,
        engine: _aws_cdk_aws_rds_ceddda9d.IClusterEngine,
        snapshot_identifier: builtins.str,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        backup_retention: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        cluster_identifier: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[_aws_cdk_aws_rds_ceddda9d.Credentials] = None,
        default_database_name: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[builtins.bool] = None,
        enable_data_api: typing.Optional[builtins.bool] = None,
        parameter_group: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IParameterGroup] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        scaling: typing.Optional[typing.Union[_aws_cdk_aws_rds_ceddda9d.ServerlessScalingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        storage_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        subnet_group: typing.Optional[_aws_cdk_aws_rds_ceddda9d.ISubnetGroup] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(deprecated) Properties to configure an Aurora Serverless Cluster.

        :param engine: (deprecated) What kind of database to start.
        :param snapshot_identifier: (deprecated) The identifier for the DB snapshot or DB cluster snapshot to restore from. You can use either the name or the Amazon Resource Name (ARN) to specify a DB cluster snapshot. However, you can use only the ARN to specify a DB snapshot. After you restore a DB cluster with a SnapshotIdentifier property, you must specify the same SnapshotIdentifier property for any future updates to the DB cluster. When you specify this property for an update, the DB cluster is not restored from the snapshot again, and the data in the database is not changed. However, if you don't specify the SnapshotIdentifier property, an empty DB cluster is created, and the original DB cluster is deleted. If you specify a property that is different from the previous snapshot restore property, a new DB cluster is restored from the specified SnapshotIdentifier property, and the original DB cluster is deleted.
        :param vpc: (deprecated) The VPC that this Aurora Serverless cluster has been created in.
        :param backup_retention: (deprecated) The number of days during which automatic DB snapshots are retained. Automatic backup retention cannot be disabled on serverless clusters. Must be a value from 1 day to 35 days. Default: Duration.days(1)
        :param cluster_identifier: (deprecated) An optional identifier for the cluster. Default: - A name is automatically generated.
        :param credentials: (deprecated) Credentials for the administrative user. Default: - A username of 'admin' and SecretsManager-generated password
        :param default_database_name: (deprecated) Name of a database which is automatically created inside the cluster. Default: - Database is not created in cluster.
        :param deletion_protection: (deprecated) Indicates whether the DB cluster should have deletion protection enabled. Default: - true if removalPolicy is RETAIN, false otherwise
        :param enable_data_api: (deprecated) Whether to enable the Data API. Default: false
        :param parameter_group: (deprecated) Additional parameters to pass to the database engine. Default: - no parameter group.
        :param removal_policy: (deprecated) The removal policy to apply when the cluster and its instances are removed from the stack or replaced during an update. Default: - RemovalPolicy.SNAPSHOT (remove the cluster and instances, but retain a snapshot of the data)
        :param scaling: (deprecated) Scaling configuration of an Aurora Serverless database cluster. Default: - Serverless cluster is automatically paused after 5 minutes of being idle. minimum capacity: 2 ACU maximum capacity: 16 ACU
        :param security_groups: (deprecated) Security group. Default: - a new security group is created.
        :param storage_encryption_key: (deprecated) The KMS key for storage encryption. If you specify the SnapshotIdentifier property, the StorageEncrypted property value is inherited from the snapshot, and if the DB cluster is encrypted, the specified KmsKeyId property is used. Default: - the default master key will be used for storage encryption
        :param subnet_group: (deprecated) Existing subnet group for the cluster. Default: - a new subnet group will be created.
        :param vpc_subnets: (deprecated) Where to place the instances within the VPC. Default: - the VPC default strategy if not specified.

        :stability: deprecated
        '''
        if isinstance(scaling, dict):
            scaling = _aws_cdk_aws_rds_ceddda9d.ServerlessScalingOptions(**scaling)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f89db333d90ee77c4f24c45d7dd089f98417f7ff36c23d822417ea3efe321c)
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument snapshot_identifier", value=snapshot_identifier, expected_type=type_hints["snapshot_identifier"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument backup_retention", value=backup_retention, expected_type=type_hints["backup_retention"])
            check_type(argname="argument cluster_identifier", value=cluster_identifier, expected_type=type_hints["cluster_identifier"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument default_database_name", value=default_database_name, expected_type=type_hints["default_database_name"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument enable_data_api", value=enable_data_api, expected_type=type_hints["enable_data_api"])
            check_type(argname="argument parameter_group", value=parameter_group, expected_type=type_hints["parameter_group"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument scaling", value=scaling, expected_type=type_hints["scaling"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument storage_encryption_key", value=storage_encryption_key, expected_type=type_hints["storage_encryption_key"])
            check_type(argname="argument subnet_group", value=subnet_group, expected_type=type_hints["subnet_group"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "engine": engine,
            "snapshot_identifier": snapshot_identifier,
            "vpc": vpc,
        }
        if backup_retention is not None:
            self._values["backup_retention"] = backup_retention
        if cluster_identifier is not None:
            self._values["cluster_identifier"] = cluster_identifier
        if credentials is not None:
            self._values["credentials"] = credentials
        if default_database_name is not None:
            self._values["default_database_name"] = default_database_name
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if enable_data_api is not None:
            self._values["enable_data_api"] = enable_data_api
        if parameter_group is not None:
            self._values["parameter_group"] = parameter_group
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if scaling is not None:
            self._values["scaling"] = scaling
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if storage_encryption_key is not None:
            self._values["storage_encryption_key"] = storage_encryption_key
        if subnet_group is not None:
            self._values["subnet_group"] = subnet_group
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def engine(self) -> _aws_cdk_aws_rds_ceddda9d.IClusterEngine:
        '''(deprecated) What kind of database to start.

        :stability: deprecated
        '''
        result = self._values.get("engine")
        assert result is not None, "Required property 'engine' is missing"
        return typing.cast(_aws_cdk_aws_rds_ceddda9d.IClusterEngine, result)

    @builtins.property
    def snapshot_identifier(self) -> builtins.str:
        '''(deprecated) The identifier for the DB snapshot or DB cluster snapshot to restore from.

        You can use either the name or the Amazon Resource Name (ARN) to specify a DB cluster snapshot. However, you can use only the ARN to specify a DB snapshot.

        After you restore a DB cluster with a SnapshotIdentifier property, you must specify the same SnapshotIdentifier property for any future updates to the DB cluster. When you specify this property for an update, the DB cluster is not restored from the snapshot again, and the data in the database is not changed. However, if you don't specify the SnapshotIdentifier property, an empty DB cluster is created, and the original DB cluster is deleted. If you specify a property that is different from the previous snapshot restore property, a new DB cluster is restored from the specified SnapshotIdentifier property, and the original DB cluster is deleted.

        :stability: deprecated
        '''
        result = self._values.get("snapshot_identifier")
        assert result is not None, "Required property 'snapshot_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''(deprecated) The VPC that this Aurora Serverless cluster has been created in.

        :stability: deprecated
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def backup_retention(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(deprecated) The number of days during which automatic DB snapshots are retained.

        Automatic backup retention cannot be disabled on serverless clusters.
        Must be a value from 1 day to 35 days.

        :default: Duration.days(1)

        :stability: deprecated
        '''
        result = self._values.get("backup_retention")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''(deprecated) An optional identifier for the cluster.

        :default: - A name is automatically generated.

        :stability: deprecated
        '''
        result = self._values.get("cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def credentials(self) -> typing.Optional[_aws_cdk_aws_rds_ceddda9d.Credentials]:
        '''(deprecated) Credentials for the administrative user.

        :default: - A username of 'admin' and SecretsManager-generated password

        :stability: deprecated
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[_aws_cdk_aws_rds_ceddda9d.Credentials], result)

    @builtins.property
    def default_database_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Name of a database which is automatically created inside the cluster.

        :default: - Database is not created in cluster.

        :stability: deprecated
        '''
        result = self._values.get("default_database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deletion_protection(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Indicates whether the DB cluster should have deletion protection enabled.

        :default: - true if removalPolicy is RETAIN, false otherwise

        :stability: deprecated
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_data_api(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether to enable the Data API.

        :default: false

        :see: https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/data-api.html
        :stability: deprecated
        '''
        result = self._values.get("enable_data_api")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def parameter_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_rds_ceddda9d.IParameterGroup]:
        '''(deprecated) Additional parameters to pass to the database engine.

        :default: - no parameter group.

        :stability: deprecated
        '''
        result = self._values.get("parameter_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_rds_ceddda9d.IParameterGroup], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''(deprecated) The removal policy to apply when the cluster and its instances are removed from the stack or replaced during an update.

        :default: - RemovalPolicy.SNAPSHOT (remove the cluster and instances, but retain a snapshot of the data)

        :stability: deprecated
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def scaling(
        self,
    ) -> typing.Optional[_aws_cdk_aws_rds_ceddda9d.ServerlessScalingOptions]:
        '''(deprecated) Scaling configuration of an Aurora Serverless database cluster.

        :default:

        - Serverless cluster is automatically paused after 5 minutes of being idle.
        minimum capacity: 2 ACU
        maximum capacity: 16 ACU

        :stability: deprecated
        '''
        result = self._values.get("scaling")
        return typing.cast(typing.Optional[_aws_cdk_aws_rds_ceddda9d.ServerlessScalingOptions], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''(deprecated) Security group.

        :default: - a new security group is created.

        :stability: deprecated
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def storage_encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(deprecated) The KMS key for storage encryption.

        If you specify the SnapshotIdentifier property, the StorageEncrypted property value is inherited from the snapshot, and if the DB cluster is encrypted, the specified KmsKeyId property is used.

        :default: - the default master key will be used for storage encryption

        :stability: deprecated
        '''
        result = self._values.get("storage_encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def subnet_group(self) -> typing.Optional[_aws_cdk_aws_rds_ceddda9d.ISubnetGroup]:
        '''(deprecated) Existing subnet group for the cluster.

        :default: - a new subnet group will be created.

        :stability: deprecated
        '''
        result = self._values.get("subnet_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_rds_ceddda9d.ISubnetGroup], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(deprecated) Where to place the instances within the VPC.

        :default: - the VPC default strategy if not specified.

        :stability: deprecated
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerlessClusterFromSnapshotProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ServerlessClusterFromSnapshot",
    "ServerlessClusterFromSnapshotProps",
]

publication.publish()

def _typecheckingstub__02b4e7be41e42a4d0aba31d2cde08b3d9da054f652ab229cf3fcdf2fba029256(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    engine: _aws_cdk_aws_rds_ceddda9d.IClusterEngine,
    snapshot_identifier: builtins.str,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    backup_retention: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    cluster_identifier: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[_aws_cdk_aws_rds_ceddda9d.Credentials] = None,
    default_database_name: typing.Optional[builtins.str] = None,
    deletion_protection: typing.Optional[builtins.bool] = None,
    enable_data_api: typing.Optional[builtins.bool] = None,
    parameter_group: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IParameterGroup] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    scaling: typing.Optional[typing.Union[_aws_cdk_aws_rds_ceddda9d.ServerlessScalingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    storage_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    subnet_group: typing.Optional[_aws_cdk_aws_rds_ceddda9d.ISubnetGroup] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fcef260575cff50f6020a8b1026eca3010c75a62054850c10123d8a2a5fcf86(
    id: builtins.str,
    *,
    secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    automatically_after: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    endpoint: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IInterfaceVpcEndpoint] = None,
    exclude_characters: typing.Optional[builtins.str] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7470b0229ed4dc476cf44a05c9cace0d0dd92a87419e9ff947e198099945223(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55266b5c88e611e9ec1495d5d65d3a04e84a3c99a81ba74c3dc8a361e1d012f0(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f89db333d90ee77c4f24c45d7dd089f98417f7ff36c23d822417ea3efe321c(
    *,
    engine: _aws_cdk_aws_rds_ceddda9d.IClusterEngine,
    snapshot_identifier: builtins.str,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    backup_retention: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    cluster_identifier: typing.Optional[builtins.str] = None,
    credentials: typing.Optional[_aws_cdk_aws_rds_ceddda9d.Credentials] = None,
    default_database_name: typing.Optional[builtins.str] = None,
    deletion_protection: typing.Optional[builtins.bool] = None,
    enable_data_api: typing.Optional[builtins.bool] = None,
    parameter_group: typing.Optional[_aws_cdk_aws_rds_ceddda9d.IParameterGroup] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    scaling: typing.Optional[typing.Union[_aws_cdk_aws_rds_ceddda9d.ServerlessScalingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    storage_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    subnet_group: typing.Optional[_aws_cdk_aws_rds_ceddda9d.ISubnetGroup] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

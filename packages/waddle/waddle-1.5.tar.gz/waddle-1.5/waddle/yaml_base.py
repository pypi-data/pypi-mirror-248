from functools import partial

from ruamel.yaml import YAML
from ruamel.yaml.dumper import SafeDumper
from ruamel.yaml.nodes import ScalarNode
from .aws import get_parameter
from .aws.session import create_session
from .aws.pstore import create_kms_client
from .aws.pstore import create_ssm_client


class SsmValue:
    def __init__(
            self, key, profile=None, region=None, role_arn=None,
            session=None, ssm_client=None):
        self.key = key
        self.resolved = False
        self.m_value = None
        self.profile = profile
        self.region = region
        self.role_arn = role_arn
        self.session = session
        self.ssm_client = ssm_client

    @property
    def value(self):
        if self.resolved:
            return self.m_value
        self.m_value = get_parameter(
            self.key, profile=self.profile, region=self.region,
            session=self.session, client=self.ssm_client)
        self.resolved = True
        return self.m_value


def ssm_scalar_constructor(
        loader, node, profile=None, region=None, role_arn=None,
        session=None, ssm_client=None, special_values=None):
    key = loader.construct_scalar(node)
    result = SsmValue(key, profile, region, role_arn, session, ssm_client)
    if special_values is not None:
        special_values.append(result)
    return result


def ssm_representer(dumper: SafeDumper, value: SsmValue) -> ScalarNode:
    """
    round-trip serialize an ssm value
    """
    return dumper.represent_scalar("!ssm", value.key)


class KmsWrappedSecret:
    def __init__(
            self, encrypted_value, profile=None, region=None,
            role_arn=None, kms_key=None, session=None, kms_client=None):
        self.encrypted_value = encrypted_value
        self.kms_key = kms_key
        self.resolved = False
        self.m_value = None
        self.profile = profile
        self.region = region
        self.role_arn = role_arn
        self.session = session
        self.kms_client = kms_client

    @property
    def value(self):
        from murmuration import kms_wrapped
        if self.resolved:
            return self.m_value
        self.m_value = kms_wrapped.decrypt(
            self.encrypted_value, self.region, self.profile,
            self.session, client=self.kms_client)
        self.resolved = True
        return self.m_value


def kms_wrapped_scalar_constructor(
        loader, node, profile=None, region=None, role_arn=None,
        kms_key=None, session=None, kms_client=None, special_values=None):
    encrypted_value = loader.construct_scalar(node)
    result = KmsWrappedSecret(
        encrypted_value,
        profile=profile,
        region=region,
        role_arn=role_arn,
        kms_key=kms_key,
        session=session, kms_client=kms_client)
    if special_values is not None:
        special_values.append(result)
    return result


def kms_wrapped_representer(
        dumper: SafeDumper,
        value: KmsWrappedSecret) -> ScalarNode:
    """
    round-trip serialize a kms-wrapped secret
    """
    return dumper.represent_scalar("!kms_wrapped", value.encrypted_value)


class MasterKeyedSecret:
    def __init__(
            self, encrypted_value, master_key=None):
        self.encrypted_value = encrypted_value
        self.master_key = master_key
        self.resolved = False
        self.m_value = None

    @property
    def value(self):
        from murmuration import gcm
        if self.resolved:
            return self.m_value
        self.m_value = gcm.decrypt(self.encrypted_value, self.master_key.value)
        self.resolved = True
        return self.m_value


def master_keyed_scalar_constructor(
        loader, node, master_key=None, special_values=None):
    encrypted_value = loader.construct_scalar(node)
    result = MasterKeyedSecret(
        encrypted_value,
        master_key)
    if special_values is not None:
        special_values.append(result)
    return result


def master_keyed_representer(
        dumper: SafeDumper,
        value: MasterKeyedSecret) -> ScalarNode:
    """
    round-trip serialize a master-keyed secret
    """
    return dumper.represent_scalar("!secret", value.encrypted_value)


class Yaml(YAML):
    def __init__(self, profile=None, region=None, role_arn=None,
                 kms_key=None, master_key=None, session=None,
                 ssm_client=None, kms_client=None, width=4096):
        super().__init__(typ='rt')
        self.explicit_start = True
        self.preserve_quotes = True
        self.width = width
        self.special_values = []
        self.indent(sequence=4, mapping=2, offset=2)
        ssm_fn = partial(
            ssm_scalar_constructor,
            profile=profile,
            region=region,
            role_arn=role_arn,
            session=session,
            ssm_client=ssm_client,
            special_values=self.special_values)
        kms_wrapped_fn = partial(
            kms_wrapped_scalar_constructor,
            profile=profile,
            region=region,
            role_arn=role_arn,
            kms_key=kms_key,
            session=session,
            kms_client=kms_client,
            special_values=self.special_values)
        master_keyed_wrapped_fn = partial(
            master_keyed_scalar_constructor,
            master_key=master_key, special_values=self.special_values)
        self.constructor.add_constructor('!secret', master_keyed_wrapped_fn)
        self.constructor.add_constructor('!ssm', ssm_fn)
        self.constructor.add_constructor('!kms_wrapped', kms_wrapped_fn)
        self.representer.add_representer(SsmValue, ssm_representer)
        self.representer.add_representer(
            KmsWrappedSecret, kms_wrapped_representer)
        self.representer.add_representer(
            MasterKeyedSecret,
            master_keyed_representer)

    @classmethod
    def ssm_client(
            cls, profile=None, region=None, role_arn=None, session=None,
            ssm_client=None):
        return create_ssm_client(
            profile=profile, region=region, role_arn=role_arn,
            session=session, client=ssm_client)

    @classmethod
    def kms_client(
            cls, profile=None, region=None, role_arn=None, session=None,
            kms_client=None):
        return create_kms_client(
            profile=profile, region=region, role_arn=role_arn,
            session=session, client=kms_client)

    def reset_special_value_clients(
            self, profile, region, role_arn, master_key):
        session = create_session(
            profile=profile, region=region, role_arn=role_arn)
        ssm_client = self.ssm_client(session=session)
        kms_client = self.kms_client(session=session)
        for x in self.special_values:
            if isinstance(x, SsmValue):
                x.ssm_client = ssm_client
            elif isinstance(x, KmsWrappedSecret):
                x.kms_client = kms_client
            elif isinstance(x, MasterKeyedSecret):
                x.master_key = master_key


def dump_yaml(x, filename):
    y = Yaml()
    if isinstance(filename, str):
        with open(filename, 'w') as f:
            y.dump(x, f)
    else:
        y.dump(x, filename)

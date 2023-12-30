from functools import partial

from ruamel.yaml import YAML
from ruamel.yaml.dumper import SafeDumper
from ruamel.yaml.nodes import ScalarNode
from .aws import get_parameter
from .aws.pstore import create_kms_client
from .aws.pstore import create_ssm_client


class SsmValue:
    def __init__(
            self, key, profile=None, region=None,
            session=None, ssm_client=None):
        self.key = key
        self.resolved = False
        self.m_value = None
        self.profile = profile
        self.region = region
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
        loader, node, profile=None, region=None,
        session=None, ssm_client=None):
    key = loader.construct_scalar(node)
    return SsmValue(key, profile, region, session, ssm_client)


def ssm_representer(dumper: SafeDumper, value: SsmValue) -> ScalarNode:
    """
    round-trip serialize an ssm value
    """
    return dumper.represent_scalar("!ssm", value.key)


class KmsWrappedSecret:
    def __init__(
            self, encrypted_value, profile=None, region=None,
            kms_key=None, session=None, kms_client=None):
        self.encrypted_value = encrypted_value
        self.kms_key = kms_key
        self.resolved = False
        self.m_value = None
        self.profile = profile
        self.region = region
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
        loader, node, profile=None, region=None,
        kms_key=None, session=None, kms_client=None):
    encrypted_value = loader.construct_scalar(node)
    return KmsWrappedSecret(
        encrypted_value,
        profile,
        region,
        kms_key,
        session, kms_client)


def kms_wrapped_representer(dumper: SafeDumper, value: KmsWrappedSecret) -> ScalarNode:
    """
    round-trip serialize a kms-wrapped secret
    """
    return dumper.represent_scalar("!kms_wrapped", value.encrypted_value)


class Yaml(YAML):
    def __init__(self, profile=None, region=None, kms_key=None, session=None,
                 ssm_client=None, kms_client=None, width=4096):
        super().__init__(typ='rt')
        self.explicit_start = True
        self.preserve_quotes = True
        self.width = 4096
        self.indent(sequence=4, mapping=2, offset=2)
        if profile or region or session or ssm_client or kms_client:
            ssm_client = create_ssm_client(
                profile=profile, region=region, session=session,
                client=ssm_client)
            kms_client = create_kms_client(
                profile=profile, region=region, session=session,
                client=kms_client)
        ssm_fn = partial(
            ssm_scalar_constructor,
            profile=profile,
            region=region,
            session=session,
            ssm_client=ssm_client)
        kms_wrapped_fn = partial(
            kms_wrapped_scalar_constructor,
            profile=profile,
            region=region,
            kms_key=kms_key,
            session=session,
            kms_client=kms_client)
        self.constructor.add_constructor('!ssm', ssm_fn)
        self.constructor.add_constructor('!kms_wrapped', kms_wrapped_fn)
        self.representer.add_representer(SsmValue, ssm_representer)
        self.representer.add_representer(
            KmsWrappedSecret, kms_wrapped_representer)


def dump_yaml(x, filename):
    y = Yaml()
    if isinstance(filename, str):
        with open(filename, 'w') as f:
            y.dump(x, f)
    else:
        y.dump(x, filename)

import logging.config
import re
import sys
import click
from murmuration import kms_wrapped

from .param_bunch import ParamBunch
from .yaml_base import KmsWrappedSecret
from . import version
from . import g_test_mode


def setup_logging():
    if g_test_mode:
        return
    logging.config.dictConfig({
        'version': 1,
        'root': {
            'handlers': ['me'],
            'level': 'INFO',
        },
        'handlers': {
            'me': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'formatter': 'me',
            }
        },
        'formatters': {
            'me': {
                'format': '[{asctime}.{msecs:03.0f}] {message}',
                'datefmt': '%H:%M:%S',
                'style': '{',
            },
        },
    })


@click.group(name='waddle')
@click.version_option(version)
def main():
    "cli for managing waddle config files"


def is_secret(key):
    matcher = re.compile('.*(key|secret|token|password).*')
    return matcher.match(key)


@main.command(name='add-secret')
@click.argument('key', metavar='db.password')
@click.option('-f', '--filename', metavar='/path/to/config_file.yml',
              type=click.Path(exists=True), required=True)
def add_secret(filename, key):
    """
    Adds an encrypted secret to the specified configuration file

    Example:
        waddle add-secret -f conf/dev.yml db.password
    """
    tty = sys.stdin.isatty()
    setup_logging()
    log = logging.getLogger(__name__)
    x = ParamBunch()
    x.from_file(filename=filename, decrypt=False, handle_tags=False)
    kms_key = x.get('meta.kms_key')
    if not kms_key:
        print(f'{filename} does not have a kms key specified.')
        return
    if tty:  # pragma: no-cover
        print(f'Enter value for [{key}]: ', end='', file=sys.stderr)
        sys.stderr.flush()
    # stdin = os.fdopen(sys.stdin.fileno(), 'rb', 0)
    plain_text = sys.stdin.readline().rstrip()
    # plain_text = plain_text.decode('utf-8').rstrip()
    log.info('encrypting secret')
    region = x.get('meta.region')
    profile = x.get('meta.profile')
    encrypted_value = kms_wrapped.encrypt(plain_text, kms_key, region, profile)
    x[key] = KmsWrappedSecret(encrypted_value)
    log.info('saving')
    x.save(filename)
    log.info('done')


@main.command(name='encrypt')
@click.option('-f', '--filename', metavar='/path/to/config_file.yml',
              type=click.Path(exists=True), required=True)
def encrypt(filename):
    """
    Encrypts values for any key that that has the following keywords in it:
      * key
      * password
      * token
      * secret

    Example:
        waddle encrypt -f conf/dev.yml
    """
    x = ParamBunch()
    x.load(filename=filename, decrypt=True)
    kms_key = x.get('meta.kms_key')
    if not kms_key:
        print(f'{filename} does not have a kms key specified.')
        return
    region = x.get('meta.region')
    profile = x.get('meta.profile')
    values = []
    for key, value in x.items():
        values.append([key, value])
    for key, value in values:
        if is_secret(key) and not key.startswith('meta.'):
            value = kms_wrapped.encrypt(
                value, kms_key, region=region, profile=profile)
            x[key] = value
    x.save(filename)


@main.command(name='deploy')
@click.option('-f', '--filename', metavar='/path/to/config_file.yml',
              type=click.Path(exists=True), required=True)
@click.option('-e', '--encrypted', is_flag=True)
def deploy(filename, encrypted):
    """
    Deploys a locally stored config file to aws:

    Example:
        waddle deploy -f conf/dev.yml

    Use the --encrypt flag to push all values as kms encrypted to
    parameter store.
    """
    x = ParamBunch(filename=filename)
    x.to_aws(force_encryption=encrypted)


@main.command(name='undeploy')
@click.option('-f', '--filename', metavar='/path/to/config_file.yml',
              type=click.Path(exists=True), required=True)
def undeploy(filename):
    """
    Deploys a locally stored config file to aws:

    Example:
        waddle deploy -f conf/dev.yml
    """
    x = ParamBunch(filename=filename)
    x.delete_from_aws()


if __name__ == "__main__":
    main()

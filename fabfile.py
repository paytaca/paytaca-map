from patchwork.transfers import rsync
from fabric import task
from fabric.connection import Connection


@task
def prod(ctx):
    user = 'root'
    host = '37.27.80.215'
    ctx.config.run.env['conn'] = Connection(
        host,
        user=user
    )


@task
def uname(ctx):
    conn = ctx.config.run.env['conn']
    conn.run('uname -a')


@task
def sync(ctx):
    conn = ctx.config.run.env['conn']
    rsync(
        conn,
        '.',
        '/root/paytaca-map',
        exclude=[
            '.git',
            '.venv',
            '.DS_Store',
            'dist',
            'node_modules',
            '/.env',
            '__pycache__',
            '/static',
            '/media',
            'postgres-data',
            'supervisord.pid'
        ]
    )


@task
def build(ctx):
    conn = ctx.config.run.env['conn']
    with conn.cd('/root/paytaca-map/deployment'):
        conn.run('docker-compose -p paytacamap -f prod.yml build')


@task
def up(ctx):
    conn = ctx.config.run.env['conn']
    with conn.cd('/root/paytaca-map/deployment'):
        conn.run('docker-compose -p paytacamap -f prod.yml up -d')


@task
def down(ctx):
    conn = ctx.config.run.env['conn']
    with conn.cd('/root/paytaca-map/deployment'):
        conn.run('docker-compose -p paytacamap -f prod.yml down')


@task
def deploy(ctx):
    sync(ctx)
    build(ctx)
    down(ctx)
    up(ctx)


@task
def logs(ctx):
    conn = ctx.config.run.env['conn']
    with conn.cd('/root/paytaca-map/deployment'):
        conn.run('docker-compose -f prod.yml -p paytacamap logs -f web')

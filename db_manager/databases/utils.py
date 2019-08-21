from subprocess import Popen, PIPE


def pg_dump(postgres_url, dump_path):
    cmd = [
        'pg_dump',
        postgres_url,
        '--file',
        dump_path,
        '--format',
        'custom',
        '--no-owner',
        '--no-privileges',
        '--verbose',
        '--compress',
        '0',
    ]

    p = Popen(cmd, stderr=PIPE, universal_newlines=True)
    log = p.communicate()[1]

    return {
        'log': log,
        'return_code': p.returncode
    }

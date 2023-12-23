import nox

from os import environ as envvar


PROJECT_NAME = 'checksignature'
VENV = f'{PROJECT_NAME}-venv'
TESTDIR = '.'
TESTNAME = envvar.get('TESTNAME', '')
USEVENV = envvar.get('USEVENV', False)

external = False if USEVENV else True
supported_python_versions = [
    '3.7',
    '3.8',
    '3.9',
    '3.10',
    '3.11',
    '3.12',
]

nox.options.default_venv_backend = 'none' if not USEVENV else USEVENV

def session_name(suffix: str):
    return f'{VENV}-{suffix}' if USEVENV else suffix


@nox.session(name=session_name('install'), python=supported_python_versions)
def install(session):
    session.run(
        'python', '-m',
        'pip', '--disable-pip-version-check', 'install', '.',
        external=external
    )
    session.run(
        'python', '-m',
        'pip', '--disable-pip-version-check', 'install', '-r', 'requirements.txt',
        external=external
    )


@nox.session(name=session_name('test'), python=supported_python_versions)
def test(session):
    if USEVENV:
        install(session)

    session.run(
        'python', '-m',
        'coverage', 'run', '--branch',
        '--omit', '.nox/*,noxfile.py,setup.py,test*',
        '--source', '.',
        '-m', 'unittest', TESTNAME if TESTNAME else f'discover',
        external=external
    )
    session.run('coverage', 'report', '-m', external=external)
    session.run('coverage', 'xml', external=external)


@nox.session(name=session_name('build'), python=supported_python_versions)
def build(session):
    session.run('python', 'setup.py', 'sdist')


# TODO (withtwoemms) -- leverage gitpython to show version on-demand


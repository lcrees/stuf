'''stuf fabfile'''

from fabric.api import prompt, local, settings, env


def _test(val):
    truth = val in ['py26', 'py27', 'py31', 'py32']
    if truth is False:
        raise KeyError(val)
    return val


def tox():
    '''test stuf'''
    local('tox')


def tox_recreate():
    '''recreate stuf test env'''
    prompt(
        'Enter testenv: [py26, py27, py32]',
        'testenv',
        validate=_test,
    )
    local('tox --recreate -e %(testenv)s' % env)


def release():
    '''release stuf'''
    local('hg update pu')
    local('hg update next')
    local('hg merge pu; hg ci -m automerge')
    local('hg update maint')
    local('hg merge default; hg ci -m automerge')
    local('hg update default')
    local('hg merge next; hg ci -m automerge')
    local('hg update pu')
    local('hg merge default; hg ci -m automerge')
    prompt('Enter tag: ', 'tag')
    with settings(warn_only=True):
        local('hg tag "%(tag)s"' % env)
        local('hg push ssh://hg@bitbucket.org/lcrees/stuf')
        local('hg push github')
    local('./setup.py register sdist --format=gztar,zip upload')

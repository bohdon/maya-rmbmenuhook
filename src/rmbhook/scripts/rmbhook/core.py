"""
Functions for installing and uninstalling the rmb hooks by sourcing
the appropriate mel scripts.

Installing and uninstalling has no effect on which menus are
currently registered.
"""


import pymel.core as pm
import os

__all__ = [
    'install',
    'uninstall',
]


# original scripts that can be sourced to uninstall the rmb hooks
ORIGINAL_SCRIPTS = [
    'buildObjectMenuItemsNow',
    'dagMenuProc'
]


def install():
    """
    Source the appropriate mel scripts
    """

    # ensure the overidden scripts have been sourced
    # at least once to prevent them sourcing later
    uninstall()

    # build list of mel scripts to source
    vers = pm.about(version=True).split(' ')[0]
    scripts = [
        'rmbhook.mel',
        'rmbhookOverrides{0}.mel'.format(vers),
    ]

    # source using full path for each script
    dir = os.path.dirname(__file__)
    for script in scripts:
        fullPath = os.path.join(dir, script).replace('\\', '/')
        print('Sourcing {0}'.format(fullPath))
        pm.mel.source(fullPath)


def uninstall():
    """
    Source the default mel scripts
    to uninstall any custom overrides
    """
    for script in ORIGINAL_SCRIPTS:
        pm.mel.source(script)




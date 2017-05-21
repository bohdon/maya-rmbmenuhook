"""
Provides a way to easily implement custom right click menus in Maya model view panels.
"""

import pymel.core as pm
import os

MEL_OVERRIDES = [
    'rmbhook.mel',
    'rmbhookOverrides{0}.mel',
]
MEL_OVERRIDDEN = [
    'buildObjectMenuItemsNow',
    'dagMenuProc'
]

def init():
    """
    Source the appropriate mel overrides,
    and perform other initializations
    """
    # ensure the overidden scripts have been sourced
    # at least once to prevent them sourcing later
    remove()
    # build paths for each custom override script
    dir = os.path.dirname(__file__)
    vers = pm.about(version=True).split(' ')[0]
    for script in MEL_OVERRIDES:
        path = os.path.join(dir, script.format(vers)).replace('\\', '/')
        print('Sourcing {0}'.format(path))
        pm.mel.source(path)

def remove():
    """
    Source the default mel scripts
    to remove any custom overrides
    """
    for script in MEL_OVERRIDDEN:
        pm.mel.source(script)


def buildCustomMenu(menu, obj=None):
    """
    Check for and build a custom right click menu

    This is called from the right click override mel scripts.
    Receives the name of the empty menu to build into, and an object if applicable.
    `obj` will not be None if an object is under the mouse,
    or a transform/shape is selected.
    """
    classes = getCustomMenus()
    for p, customCls in classes:
        i = customCls(menu, obj)
        if i._build():
            return True
    return False


def getCustomMenus():
    """
    Return a list of 2-tuples for each subclass of Menu.
    Each tuple contains (priority, class).
    """
    classes = Menu.__subclasses__()
    sortedClasses = reversed(sorted([(c.priority, c) for c in classes]))
    return list(sortedClasses)


class Menu(object):
    """
    The base class for any custom right click menus
    All subclasses are registered as custom menus, and should
    override the `build` method.

    `self.menu` - the name of the parent popup menu
    `self.object` - the name of the selected or hit object, if any
    `self.hit` - whether the mouse is currently over the object

    >>> # custom menu that shows when the mouse is over an object
    >>> class MyCustomMenu(Menu):    
    >>>     def build(self):
    >>>         if self.hit:
    >>>             pm.setParent(self.menu, m=True)
    >>>             pm.menuItem(l='Hit Object: {0}'.format(self.object))
    >>>             return True
    >>>     return False
    >>>
    >>> # deactivate the custom menu
    >>> MyCustomMenu.active = False
    >>>
    >>> # raise the priority
    >>> MyCustomMenu.priority = 1
    """

    active = True
    priority = 0

    def __init__(self, menu, obj=None):
        self.menu = pm.ui.Menu(menu)
        self.object = obj
        self.hit = pm.mel.dagObjectHit()

    def _build(self):
        if self.__class__.active:
            return self.build()
        return False

    def build(self):
        """
        Build a custom menu. Should set the parent menu to self.menu.
        self.object is the current selected or hit object
        self.hit is True if the object is under the mouse cursor
        """
        return False


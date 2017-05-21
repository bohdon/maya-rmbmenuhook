"""
A custom menu class that allows you to easily browse to
common project folders, such as the current workspace,
sourceimages, etc. It also provides menus for accessing
recent files, the reference editor, and other common file
related tools.


Simply import to use this custom menu:

>>> import rmbhook.customProjectMenu

To deactivate the menu, set the class to be inactive:

>>> rmbhook.customProjectMenu.Menu.active = false

"""

import pymel.core as pm
import os

import envtools

import mayaUtils

from rmbhook import Menu


class CustomProjectMenu(Menu):
    priority = -100

    rootPathPosition = 'NW'
    filePathPosition = 'NE'

    # custom paths to be listed in the menu
    # relative to the workspace root
    paths = {
        'W':'assets',
        'SW':'scenes',
    }

    # custom paths to be looked up in the
    # workspace fileEntry values
    workspacePaths = {
        'E':'images',
        'SE':'sourceImages',
    }

    def build(self):
        if self.object is None:
            pm.setParent(self.menu, m=True)
            self.buildDefaultItems()
            self.buildBrowseItems()
            self.buildFileMenuItems()
            self.buildRecentFilesMenu()
            return True
        return False

    def buildDefaultItems(self):
        """
        Build the default items for this menu,
        which are only in the N and S radial positions
        """
        pm.menuItem(rp='N', l=pm.mel.uiRes('m_buildObjectMenuItemsNow.kCompleteTool'), c=pm.Callback(pm.mel.CompleteCurrentTool))
        pm.menuItem(rp='S', l=pm.mel.uiRes('m_buildObjectMenuItemsNow.kSelectAll'), c=pm.Callback(pm.mel.SelectAll))

    def buildBrowseItems(self):
        """
        Build radial items that allow you to quickly browse
        to common workspace directories. These can be customized
        by changing the paths or workspacePaths dictionaries
        """
        projName = pm.workspace(q=True, act=True)
        root = pm.workspace(q=True, rd=True)
        # root path menu item
        if CustomProjectMenu.rootPathPosition:
            pm.menuItem(rp=CustomProjectMenu.rootPathPosition, l=self.title(projName), ann=root, c=pm.Callback(self.browse, root))
            pm.menuItem(ob=True, c=pm.Callback(pm.mel.SetProject))
        if CustomProjectMenu.filePathPosition:
            enabled = bool(pm.sceneName())
            path = pm.sceneName().dirname()
            pm.menuItem(rp=CustomProjectMenu.filePathPosition, l='Open File Directory', en=enabled, ann=path, c=pm.Callback(self.browse, path))
        # custom paths
        for rp, path in CustomProjectMenu.paths.items():
            fullpath = os.path.join(root, path)
            en = os.path.isdir(fullpath)
            pm.menuItem(rp=rp, l=self.title(path), en=en, ann=fullpath, c=pm.Callback(self.browse, fullpath))
        # custom workspace paths
        for rp, key in CustomProjectMenu.workspacePaths.items():
            path = pm.workspace(key, q=True, fre=True)
            fullpath = os.path.join(root, path)
            en = bool(path) and os.path.isdir(fullpath)
            pm.menuItem(rp=rp, l=self.title(key), en=en, ann=fullpath, c=pm.Callback(self.browse, fullpath))

    def buildFileMenuItems(self):
        # reference editor
        pm.menuItem(l='Reference Editor', c=pm.Callback(pm.mel.ReferenceEditor))
        # project window
        pm.menuItem(l='Project Window', c=pm.Callback(pm.mel.ProjectWindow))

    def buildRecentFilesMenu(self):
        pm.menuItem(d=True)
        pm.menuItem(l='Recent Files', en=False)
        if pm.optionVar(ex='RecentFilesList'):
            files = pm.optionVar(q='RecentFilesList')
            for f in reversed(files):
                pm.menuItem(l=os.path.basename(f), c=pm.Callback(self.openFile, f))

    def title(self, name):
        return envtools.title(name)

    def browse(self, path):
        envtools.open_dir(path)

    def openFile(self, filename):
        if not os.path.isfile(filename):
            pm.warning('file not found: {0}'.format(filename))
            return
        if mayaUtils.checkAndSaveScene(requireFileExists=False):
            mayaUtils.openScene(filename)



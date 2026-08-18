# -*- coding: utf-8 -*-
"""
ContourEase - Main plugin class
"""

from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsProject

import os.path

from .contour_ease_dialog import ContourEaseDialog


class ContourEase:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)

        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ContourEase_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        self.actions = []
        self.menu = self.tr(u'&ContourEase')
        self.toolbar = self.iface.addToolBar(u'ContourEase')
        self.toolbar.setObjectName(u'ContourEase')

        self.dlg = None

    def tr(self, message):
        return QCoreApplication.translate('ContourEase', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)
        return action

    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        if not os.path.exists(icon_path):
            icon_path = ':/images/themes/default/mActionAddRasterLayer.svg'

        self.add_action(
            icon_path,
            text=self.tr(u'ContourEase'),
            callback=self.run,
            parent=self.iface.mainWindow(),
            status_tip=self.tr(u'Create professional contours and DEM from XYZ data'))

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(self.tr(u'&ContourEase'), action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def run(self):
        if self.dlg is None:
            self.dlg = ContourEaseDialog(self.iface)
        self.dlg.show()
        result = self.dlg.exec()

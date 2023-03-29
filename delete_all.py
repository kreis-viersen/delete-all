"""
***************************************************************************
Delete all
QGIS plugin

        Date                 : March 2023
        Copyright            : (C) 2023 by Kreis Viersen
        Email                : open@kreis-viersen.de

***************************************************************************

***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

import os
from qgis.core import QgsProject
from qgis.PyQt.QtCore import QCoreApplication, QSettings, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMenu, QMessageBox


class DeleteAll:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))

        try:
            locale = QSettings().value("locale/userLocale")[0:2]
        except:
            locale = "en"
        locale_path = os.path.join(self.plugin_dir, "i18n", f"delete_all_{locale}.qm")

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

    def tr(self, text):
        return QCoreApplication.translate("DeleteAll", text)

    def initGui(self):
        self.toolbar = self.iface.addToolBar(self.tr("delete-all"))
        self.toolbar.setObjectName(self.tr("delete-all"))

        self.action = QAction(
            QIcon(os.path.join(self.plugin_dir, "delete_all.png")),
            self.tr("&delete-all"),
            self.iface.mainWindow(),
        )
        self.aboutAction = QAction(
            QIcon(os.path.join(self.plugin_dir, "info_icon.png")),
            self.tr("&About delete-all"),
            self.iface.mainWindow(),
        )
        self.action.triggered.connect(self.deleteAll)
        self.aboutAction.triggered.connect(self.about)

        self.menu = QMenu(self.tr("&delete-all"))
        self.menu.setIcon(QIcon(os.path.join(self.plugin_dir, "delete_all.png")))
        self.menu.addActions([self.action, self.aboutAction])

        self.iface.pluginMenu().addMenu(self.menu)
        self.toolbar.addAction(self.action)

    def unload(self):
        self.iface.removePluginMenu(self.tr("&delete-all"), self.action)
        self.iface.removePluginMenu(self.tr("&delete-all"), self.aboutAction)

        del self.action
        del self.toolbar

    def about(self):
        aboutString = (
            self.tr("delete-all")
            + "<br>"
            + self.tr(
                "QGIS plugin to delete all groups and layers from the layer widget"
            )
            + '<br>Author: Kreis Viersen<br>Mail: <a href="mailto:open@kreis-viersen.de?subject=delete&#8208;all">'
            + "open@kreis-viersen.de</a>"
        )
        QMessageBox.information(
            self.iface.mainWindow(), self.tr("About delete-all"), aboutString
        )

    def deleteAll(self):
        QgsProject.instance().removeAllMapLayers()

        root = QgsProject.instance().layerTreeRoot()
        for group in [child for child in root.children() if child.nodeType() == 0]:
            root.removeChildNode(group)

        self.iface.mapCanvas().refresh()

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

def classFactory(iface):
    from .delete_all import DeleteAll
    return DeleteAll(iface)
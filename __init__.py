# -*- coding: utf-8 -*-
"""
ContourEase QGIS Plugin
"""

def classFactory(iface):
    """Load ContourEase class from file contour_ease.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .contour_ease import ContourEase
    return ContourEase(iface)

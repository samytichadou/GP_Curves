'''
Copyright (C) 2018 Samy Tichadou (tonton)
samytichadou@gmail.com

Created by Samy Tichadou

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "GP Curves",
    "description": "Link 3D Curve to Grease Pencil animated datas",
    "author": "Samy Tichadou (tonton)",
    "version": (0, 2, 0),
    "blender": (3, 0, 0),
    "location": "",
    "wiki_url": "https://github.com/samytichadou/GP_Curves/blob/master/README.md",
    "tracker_url": "https://github.com/samytichadou/GP_Curves/issues/new",
    "category": "Animation" }

# IMPORT SPECIFICS
##################################

from . import   (
    properties,
    gui,
    curves_handler,
    layer_selector_operator,
    bake_operator,
)


# register
##################################

def register():
    properties.register()
    gui.register()
    curves_handler.register()
    layer_selector_operator.register()
    bake_operator.register()

def unregister():
    properties.unregister()
    gui.unregister()
    curves_handler.unregister()
    layer_selector_operator.unregister()
    bake_operator.unregister()
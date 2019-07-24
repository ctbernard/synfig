"""
Param.py
Will store the Parameters class for Synfig parameters 
"""

import sys
import copy
from lxml import etree
import settings
import common
from synfig.animation import print_animation, gen_dummy_waypoint
from properties.multiDimensionalKeyframed import gen_properties_multi_dimensional_keyframed
from properties.valueKeyframed import gen_value_Keyframed
sys.path.append("..")


class Param:
    """
    Class to keep Synfig format parameters
    """
    def __init__(self, param, parent):
        """
        This parent can be another parameter or a Layer
        """
        self.parent = parent
        self.param = param
        self.subparams = {}
        self.IS_ANIMATED = 0
        self.PATH_GENERATED = 0

    def get(self):
        """
        Returns the original param
        """
        return self.param

    def get_text(self):
        """
        Returns the text stored inside
        """
        return self.param.text

    def __getitem__(self, itr):
        """
        Returns the child corresponding to itr
        """
        return self.param[itr]

    def __setitem__(self, itr, val):
        """
        Sets the value of child corresponding to itr
        """
        self.param[itr] = val

    def get_layer_type(self):
        """
        Recursively go till the top until layer is not reached
        """
        if isinstance(self.parent, common.Layer.Layer):
            return self.parent.get_type()
        return self.parent.get_layer_type()

    def get_layer(self):
        """
        Recursively find the layer
        """
        if isinstance(self.parent, common.Layer.Layer):
            return self.parent
        return self.parent.get_layer()

    def getparent(self):
        """
        Returns the parent of this parameter
        """
        return self.parent

    def add_subparam(self, key, val):
        """
        Adds sub parameters
        """
        self.subparams[key] = val

    def get_subparam_dict(self):
        """
        Returns the address of the dict
        """
        return self.subparams

    def get_subparam(self, key):
        """
        Given a key, returns it's dictionary
        """
        return self.subparams[key]

    def animate(self, anim_type):
        """
        If this parameter is not animated, it generates dummy waypoints and
        animates this parameter
        """
        if self.IS_ANIMATED:
            return
        self.IS_ANIMATED = 1

        is_animate = common.misc.is_animated(self.param[0])
        if is_animate == 2:
            # If already animated, no need to add waypoints
            # Forcibly set it's animation type to the anim_type
            self.param[0].attrib["type"] = anim_type
            return
        elif is_animate == 0:
            st = '<animated type="{anim_type}"><waypoint time="0s" before="constant" after="constant"></waypoint></animated>'
            st = st.format(anim_type=anim_type)
            root = etree.fromstring(st)
            root[0].append(copy.deepcopy(self.param[0]))
            self.param[0] = root
        elif is_animate == 1:
            self.param[0].attrib["type"] = anim_type
            self.param[0][0].attrib["before"] = self.param[0][0].attrib["after"] = "constant"

        new_waypoint = copy.deepcopy(self.param[0][0])
        frame = common.misc.get_frame(self.param[0][0])
        frame += 1
        time = frame / settings.lottie_format["fr"]
        time = str(time) + 's'
        new_waypoint.attrib["time"] = time
        self.param[0].insert(1, new_waypoint)

    def gen_path(self, anim_type="real", idx=0):
        """
        Generates the path for this parameter over time depending on the
        animation type of this parameter
        """
        if self.PATH_GENERATED:
            return
        self.PATH_GENERATED = 1

        self.path = {}
        if anim_type == "real":
            gen_value_Keyframed(self.path, self.param[0], idx)
        else:
            gen_properties_multi_dimensional_keyframed(self.path, self.param[0], idx)

    def get_path(self):
        """
        Returns the dictionary which stores the path of this parameter
        """
        return self.path

    def gen_path_with_transform(self, anim_type="vector", idx=0):
        """
        Generates the path for this parameter over time with transform_axis
        being set true
        """
        self.path = {}
        # anim_type can not be real here
        self.param[0].attrib["transform_axis"] = "true"
        gen_properties_multi_dimensional_keyframed(self.path, self.param[0], idx)
        self.param[0].attrib["transform_axis"] = "false"

        # If a parameter is used at differnt places, then the path will need to
        # be generated again
        self.PATH_GENERATED = 0

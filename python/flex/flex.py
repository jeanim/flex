
""" flex.flex

Flex is the main module that allows you to run the update tool

:module: flex.flex
"""

# imports
from PySide2 import QtWidgets
from maya import OpenMayaUI
from shiboken2 import wrapInstance

from .query import get_transform_selection
from .query import is_maya_batch
from .query import is_valid_group
from .ui import FlexDialog
from .update import update_rig


class Flex(object):
    """ Flex is the mGear rig update tool

    Flex class object allows you to trigger updates on a given rig.
    You can use this object to execute the update with specific features
    """

    def __init__(self):
        super(Flex, self).__init__()

        # define properties
        self.__source_group = None
        self.__target_group = None
        self.__user_attributes = True

        # initialise Flex user interface
        self.ui = FlexDialog(self.__warp_maya_window())

        # connect user interface signals
        self.__setup_ui_signals()

    def __fill_line_edits(self, widget):

        selection = get_transform_selection()
        if not selection:
            return

        widget_name = widget.objectName()
        if widget_name == 'source_qpushbutton':
            self.ui.source_text.setText("{}".format(selection))

        else:
            self.ui.target_text.setText("{}".format(selection))

    def __property_check(self, value):
        """ Flex properties check

        :param value: value to check
        :type value: type
        """

        if not is_valid_group(value):
            raise ValueError("The given group ({}) is not a valid Maya "
                             "transform node or it simply doesn't exist on "
                             " your current Maya session".format(value))

    def __repr__(self):
        return "{}".format(self.__class__)

    def __setup_ui_signals(self):
        """ Setups how the UI interacts witht the API and the tool
        """

        # source button
        self.ui.add_source_button.clicked.connect(
            lambda: self.__fill_line_edits(self.ui.add_source_button))

        # target button
        self.ui.add_target_button.clicked.connect(
            lambda: self.__fill_line_edits(self.ui.add_target_button))

        # run button
        self.ui.run_button.clicked.connect(self.launch_rig_update)

    def __str__(self):
        return "mGear: Flex == > An awesome rig update tool"

    @staticmethod
    def __warp_maya_window():
        """ Returns a qt widget warp of the Maya window

        :return: Maya window on a qt widget. Returns None if Maya is on batch
        :rtype: PySide2.QtWidgets or None
        """

        if not is_maya_batch:
            return None

        # gets Maya main window object
        maya_window = OpenMayaUI.MQtUtil.mainWindow()
        return wrapInstance(long(maya_window), QtWidgets.QDialog)

    def launch_rig_update(self):
        """ Launches the rig update process
        """

        message = ("You need to provided a source and target group in order to"
                   " run the rig update.")

        if not self.source_group or not self.target_group:
            raise ValueError(message)

        update_rig(self.source_group, self.target_group)

    def show_ui(self):
        """ Displays the user interface
        """

        if not is_maya_batch():
            self.ui.show()

    @property
    def source_group(self):
        """ Flex source group name (property)
        """

        if self.ui.isVisible():
            self.__source_group = self.ui.source_text.text()
        return self.__source_group

    @source_group.setter
    def source_group(self, value):
        """ Setter for the source_group property

        :param value: Maya transform node name containing all the source shapes
        :type value: str
        """

        # property check
        self.__property_check(value)

        # set value
        self.__source_group = value

        # ui update
        if self.ui.isVisible():
            self.ui.source_text.setText(self.__source_group)

    @property
    def target_group(self):
        """ Flex target group name (property)
        """

        if self.ui.isVisible():
            self.__target_group = self.ui.target_text.text()
        return self.__target_group

    @target_group.setter
    def target_group(self, value):
        """ Setter for the target_group property

        :param value: Maya transform node name containing all the target shapes
        :type value: str
        """

        # property check
        self.__property_check(value)

        # set value
        self.__target_group = value

        # ui update
        if self.ui.isVisible():
            self.ui.target_text.setText(self.__source_group)


def run():
    """ Simply method allowing you to quickly run Flex
    """

    flex = Flex()
    flex.show_ui()
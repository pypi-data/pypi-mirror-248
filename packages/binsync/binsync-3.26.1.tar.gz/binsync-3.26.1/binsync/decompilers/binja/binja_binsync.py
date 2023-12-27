import re
import pkg_resources
from pathlib import Path

from PySide6.QtWidgets import QVBoxLayout
from binaryninjaui import (
    UIAction,
    UIActionHandler,
    Menu,
    SidebarWidget,
    SidebarWidgetType,
    Sidebar,
)
import binaryninja
from binaryninja.types import StructureType, EnumerationType
from binaryninja import SymbolType
from binaryninja.binaryview import BinaryDataNotification

from collections import defaultdict
import logging

from binsync.ui.version import set_ui_version
set_ui_version("PySide6")
from binsync.ui.config_dialog import ConfigureBSDialog
from binsync.ui.control_panel import ControlPanel
from binsync.ui.qt_objects import QImage
from .compat import bn_enum_to_bs, find_main_window, BinjaDockWidget, bn_struct_to_bs, bn_func_to_bs
from .controller import BinjaBSController
from binsync.data import FunctionHeader, GlobalVariable

l = logging.getLogger(__name__)

#
# Binja UI
#


class BinSyncSidebarWidget(SidebarWidget):
    def __init__(self, bv, bn_plugin, name="BinSync"):
        super().__init__(name)
        self._controller = bn_plugin.controllers[bv]
        self._controller.bv = bv
        self._widget = ControlPanel(self._controller)

        layout = QVBoxLayout()
        layout.addWidget(self._widget)
        self.setLayout(layout)


class BinSyncSidebarWidgetType(SidebarWidgetType):
    def __init__(self, bn_plugin):
        bs_img_path = Path(
            pkg_resources.resource_filename("binsync", "decompilers/binja/binsync_binja_logo.png")
        ).absolute()
        if not bs_img_path.exists():
            raise FileNotFoundError("Could not find BinSync logo image")

        self._bs_logo = QImage(str(bs_img_path))
        self.plugin = bn_plugin
        super().__init__(self._bs_logo, "BinSync")

    def createWidget(self, frame, data):
        return BinSyncSidebarWidget(data, self.plugin)


#
# Other
#

def instance():
    main_window = find_main_window()
    try:
        dock = [x for x in main_window.children() if isinstance(x, BinjaDockWidget)][0]
    except:
        dock = BinjaDockWidget("dummy")
    return dock

#
# Hooks (callbacks)
#


class DataMonitor(BinaryDataNotification):
    def __init__(self, view, controller):
        super().__init__()
        self._view = view
        self._controller = controller
        self._func_addr_requested = None
        self._func_before_change = None

    def function_updated(self, view, func_):
        if self._controller.sync_lock.locked() or self._func_before_change is None:
            # In the case of syncing, recording updates can cause infinite loops
            # In the case of None function before change, this means a function is being created
            # which is not supported as a change currently
            # TODO: add support for creating functions here
            return

        # service requested function only
        if self._func_addr_requested == func_.start:
            l.debug(f"Update on {hex(self._func_addr_requested)} being processed...")
            self._func_addr_requested = None

            # convert to binsync Function type for diffing
            bn_func = view.get_function_at(func_.start)
            bs_func = bn_func_to_bs(bn_func)

            #
            # header
            # NOTE: function name done inside symbol update hook
            #

            # check if the headers differ
            if self._func_before_change.header.diff(bs_func.header):
                self._controller.schedule_job(
                    self._controller.push_artifact,
                    bs_func.header
                )
                
            #
            # stack vars
            #

            for off, var in self._func_before_change.stack_vars.items():
                if off in bs_func.stack_vars and var != bs_func.stack_vars[off]:
                    new_var = bs_func.stack_vars[off]
                    if re.match(r"var_\d+[_\d+]{0,1}", new_var.name) \
                            or new_var.name in {'__saved_rbp', '__return_addr',}:
                        continue

                    self._controller.schedule_job(
                        self._controller.push_artifact,
                        new_var
                    )

            self._func_before_change = None

    def function_update_requested(self, view, func):
        if not self._controller.sync_lock.locked() and self._func_addr_requested is None:
            l.debug(f"Update on {func} requested...")
            self._func_addr_requested = func.start
            self._func_before_change = bn_func_to_bs(func)
    
    def symbol_updated(self, view, sym):
        if self._controller.sync_lock.locked():
            return

        l.debug(f"Symbol update Requested on {sym}...")
        if sym.type == SymbolType.FunctionSymbol:
            l.debug("   -> Function Symbol")
            func = view.get_function_at(sym.address)
            bs_func = bn_func_to_bs(func)
            self._controller.schedule_job(
                self._controller.push_artifact,
                FunctionHeader(sym.name, sym.address, type_=bs_func.header.type, args=bs_func.header.args)
            )
        elif sym.type == SymbolType.DataSymbol:
            l.debug("   -> Data Symbol")
            var: binaryninja.DataVariable = view.get_data_var_at(sym.address)
            
            self._controller.schedule_job(
                self._controller.push_artifact,
                GlobalVariable(var.address, var.name, type_=str(var.type), size=var.type.width)
            )
        else:
            l.debug(f"   -> Other Symbol: {sym.type}")
            pass

    def type_defined(self, view, name, type_):
        l.debug(f"Type Defined: {name} {type_}")
        name = str(name)
        if self._controller.sync_lock.locked():
            return 
        
        if isinstance(type_, StructureType):
            bs_struct = bn_struct_to_bs(name, type_)
            self._controller.schedule_job(
                self._controller.push_artifact,
                bs_struct
            )

        elif isinstance(type_, EnumerationType):
            bs_enum = bn_enum_to_bs(name, type_)
            self._controller.schedule_job(self._controller.push_artifact, bs_enum)


def start_data_monitor(view, controller):
    notification = DataMonitor(view, controller)
    view.register_notification(notification)


class BinjaPlugin:
    def __init__(self):
        # controller stored by a binary view
        self.controllers = defaultdict(BinjaBSController)
        self.sidebar_widget_type = None

        if binaryninja.core_ui_enabled():
            self._init_ui()

    def _init_ui(self):
        # config dialog
        configure_binsync_id = "BinSync: Configure..."
        UIAction.registerAction(configure_binsync_id)
        UIActionHandler.globalActions().bindAction(
            configure_binsync_id, UIAction(self._launch_config)
        )
        Menu.mainMenu("Plugins").addAction(configure_binsync_id, "BinSync")

        # control panel widget
        self.sidebar_widget_type = BinSyncSidebarWidgetType(self)
        Sidebar.addSidebarWidgetType(self.sidebar_widget_type)

    def _init_bv_dependencies(self, bv):
        l.debug("Starting data hook")
        start_data_monitor(bv, self.controllers[bv])

    def _launch_config(self, bn_context):
        bv = bn_context.binaryView
        controller_bv = self.controllers[bv]

        if bv is not None:
            controller_bv.bv = bv

        # exit early if we already configed
        if (controller_bv.bv is not None and controller_bv.check_client()) or bv is None:
            l.info("BinSync has already been configured! Restart if you want to reconfigure.")
            return

        # configure
        dialog = ConfigureBSDialog(controller_bv)
        dialog.exec_()

        # if the config was successful init a full client
        if controller_bv.check_client():
            self._init_bv_dependencies(bv)


BinjaPlugin()

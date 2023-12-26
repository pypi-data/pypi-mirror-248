# -*- coding: utf-8 -*-
"""A interface for maya."""

# Import built-in models
from __future__ import print_function
from __future__ import unicode_literals

import hashlib
import logging
import os

import sys
import time
from builtins import str
import threading

from rayvision_utils import constants
from rayvision_utils import utils
from rayvision_utils.cmd import Cmd
from rayvision_utils.exception import tips_code
from rayvision_utils.exception.exception import AnalyseFailError
from rayvision_utils.exception.exception import CGFileNotExistsError
from rayvision_utils.exception.exception import FileNameContainsChineseError
from rayvision_terragen.constants import PACKAGE_NAME


class AnalyzeTerragen(object):
    def __init__(self, cg_file,
                 software_version,
                 project_name=None,
                 plugin_config=None,
                 render_software="Terragen",
                 local_os=None,
                 workspace=None,
                 custom_exe_path=None,
                 platform="2",
                 custom_db_path=None,
                 logger=None,
                 log_folder=None,
                 log_name=None,
                 log_level="DEBUG"
                 ):
        """Initialize and examine the analysis information.

        Args:
            cg_file (str): Scene file path.
            software_version (str): Software version.
            project_name (str): The project name.
            plugin_config (dict): Plugin information.
            render_software (str): Software name, terragen by default.
            local_os (str): System name, linux or windows.
            workspace (str): Analysis out of the result file storage path.
            custom_exe_path (str): Customize the exe path for the analysis.
            platform (str): Platform no.
            custom_db_path (str): Custom database file location path.
            logger (object, optional): Custom log object.
            log_folder (str, optional): Custom log save location.
            log_name (str, optional): Custom log file name.
            log_level (string):  Set log level, example: "DEBUG","INFO","WARNING","ERROR".
        """
        self.logger = logger
        if not self.logger:
            from rayvision_log.core import init_logger
            init_logger(PACKAGE_NAME)
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(level=log_level.upper())

        self.check_path(cg_file)
        self.cg_file = cg_file
        self.custom_db_path = custom_db_path

        self.render_software = render_software
        self.software_version = software_version
        self.project_name = project_name
        self.plugin_config = plugin_config

        local_os = self.check_local_os(local_os)
        self.local_os = local_os
        self.tmp_mark = str(int(time.time())) + str(self.get_current_id())
        workspace = os.path.join(self.check_workspace(workspace),
                                 self.tmp_mark)
        if not os.path.exists(workspace):
            os.makedirs(workspace)
        self.workspace = workspace

        if custom_exe_path:
            self.check_path(custom_exe_path)
        self.custom_exe_path = custom_exe_path

        self.platform = platform

        self.task_json = os.path.join(workspace, "task.json")
        self.tips_json = os.path.join(workspace, "tips.json")
        self.asset_json = os.path.join(workspace, "asset.json")
        self.upload_json = os.path.join(workspace, "upload.json")
        self.tips_info = {}
        self.task_info = {}
        self.asset_info = {}
        self.upload_info = {}

        self.check_cg_name()

    @staticmethod
    def get_current_id():
        if isinstance(threading.current_thread(), threading._MainThread):
            return os.getpid()
        else:
            return threading.get_ident()

    @staticmethod
    def check_path(tmp_path):
        """Check if the path exists."""
        if not os.path.exists(tmp_path):
            raise CGFileNotExistsError("{} is not found".format(tmp_path))

    def check_cg_name(self):
        """Check if the scene file name has Chinese.

        Raises:
            FileNameContainsChineseError: Scene file name has Chinese.

        """
        if sys.version_info.major == "3":
            cg_file = self.cg_file
            if utils.check_contain_chinese(cg_file):
                self.add_tip(tips_code.CONTAIN_CHINESE, cg_file)
                self.save_tips()
                raise FileNameContainsChineseError

    def add_tip(self, code, info):
        """Add error message.

        Args:
            code (str): error code.
            info (str or list): Error message description.

        """
        if isinstance(info, list):
            self.tips_info[code] = info
        else:
            self.tips_info[code] = [info]

    def save_tips(self):
        """Write the error message to tips.json."""
        utils.json_save(self.tips_json, self.tips_info, ensure_ascii=False)

    @staticmethod
    def check_local_os(local_os):
        """Check the system name.

        Args:
            local_os (str): System name.

        Returns:
            str

        """
        if not local_os:
            if "win" in sys.platform.lower():
                local_os = "windows"
            else:
                local_os = "linux"
        return local_os

    def check_workspace(self, workspace):
        """Check the working environment.

        Args:
            workspace (str):  Workspace path.

        Returns:
            str: Workspace path.

        """
        if not workspace:
            if self.local_os == "windows":
                workspace = os.path.join(os.environ["USERPROFILE"],
                                         "renderfarm_sdk")
            else:
                workspace = os.path.join(os.environ["HOME"], "renderfarm_sdk")
        else:
            self.check_path(workspace)

        return workspace

    def write_task_json(self):
        """The initialization task.json."""
        constants.TASK_INFO["task_info"]["input_cg_file"] = self.cg_file.replace("\\", "/")
        constants.TASK_INFO["task_info"]["project_name"] = self.project_name
        constants.TASK_INFO["task_info"]["cg_id"] = constants.CG_SETTING.get(self.render_software.capitalize())
        constants.TASK_INFO["task_info"]["os_name"] = "1" if self.local_os == "windows" else "0"
        constants.TASK_INFO["task_info"]["platform"] = self.platform
        constants.TASK_INFO["software_config"] = {
            "plugins": self.plugin_config,
            "cg_version": self.software_version,
            "cg_name": self.render_software
        }
        utils.json_save(self.task_json, constants.TASK_INFO)

    def check_result(self):
        """Check that the analysis results file exists."""
        for json_path in [self.task_json, self.asset_json,
                          self.tips_json]:
            if not os.path.exists(json_path):
                msg = "Json file is not generated: {0}".format(json_path)
                return False, msg
        return True, None

    def get_file_md5(self, file_path):
        """Generate the md5 values for the scenario."""
        hash_md5 = hashlib.md5()
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file_path_f:
                while True:
                    data_flow = file_path_f.read(8096)
                    if not data_flow:
                        break
                    hash_md5.update(data_flow)
        return hash_md5.hexdigest()

    def write_upload_json(self):
        """Generate the upload.json."""
        assets = self.asset_info["asset"]
        upload_asset = []

        self.upload_info["scene"] = [
            {
                "local": self.cg_file.replace("\\", "/"),
                "server": utils.convert_path(self.cg_file),
                "hash": self.get_file_md5(self.cg_file)
            }
        ]

        for path in assets:
            resources = {}
            local = path.split("  (mtime")[0]
            server = utils.convert_path(local)
            resources["local"] = local.replace("\\", "/")
            resources["server"] = server
            upload_asset.append(resources)

        # Add the cg file to upload.json
        upload_asset.append({
            "local": self.cg_file.replace("\\", "/"),
            "server": utils.convert_path(self.cg_file)
        })

        self.upload_info["asset"] = upload_asset

        utils.json_save(self.upload_json, self.upload_info)

    def analyse(self, no_upload=False):
        """Build a cmd command to perform an analysis.

        Args:
            no_upload (bool): custom rendering software absolute path.

        Raises:
            AnalyseFailError: Analysis scenario failed.

        """
        self.write_task_json()
        exe_path = os.path.join(os.path.dirname(__file__), "Analyze.exe")
        cmd = '"{exe_path}" -user_id "{user_id}" -task_id "{task_id}" -cg_file "{cg_file}"' \
              ' -task_path "{task_path}" -tips_path "{tips_path}" -asset_path "{asset_path}"'.format(
            exe_path=exe_path,
            user_id = "",
            task_id = "",
            cg_file = self.cg_file,
            task_path = self.task_json,
            tips_path = self.tips_json,
            asset_path=self.asset_json,
        )

        self.logger.debug(cmd)
        code, _, _ = Cmd.run(cmd, shell=True)
        if code != 0:
            self.add_tip(tips_code.UNKNOW_ERR, "")
            self.save_tips()
            raise AnalyseFailError

        # Determine whether the analysis is successful by
        #  determining whether a json file is generated.
        status, msg = self.check_result()
        if status is False:
            self.add_tip(tips_code.UNKNOW_ERR, msg)
            self.save_tips()
            raise AnalyseFailError(msg)

        self.tips_info = utils.json_load(self.tips_json)
        self.asset_info = utils.json_load(self.asset_json)
        self.task_info = utils.json_load(self.task_json)
        if not no_upload:
            self.write_upload_json()
        return self

# -*- coding: utf-8 -*-

from rayvision_terragen.analyze_terragen import AnalyzeTerragen

analyze_info = {
    "cg_file": r"D:\terragen\CG file\muti_layer_test.tgd",
    "workspace": "c:/workspace",
    "software_version": "",
    "project_name": "Project1",
    "plugin_config": {}
}

AnalyzeTerragen(**analyze_info).analyse()

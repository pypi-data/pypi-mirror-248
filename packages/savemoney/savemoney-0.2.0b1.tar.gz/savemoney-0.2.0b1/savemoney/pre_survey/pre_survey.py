# -*- coding: utf-8 -*-

from pathlib import Path
from itertools import chain

from ..modules import my_classes as mc
from . import pre_survey_core as psc

__all__ = ["pre_survey"]

def pre_survey(plasmid_map_dir_paths: str, param_dict: dict, save_dir_base: str):
    # 0. Prepare files
    plasmid_map_paths = []
    for ext in mc.MyRefSeq.allowed_plasmid_map_extensions:
        plasmid_map_paths = chain(plasmid_map_paths, Path(plasmid_map_dir_paths).glob(f"*{ext}"))
    save_dir = mc.new_dir_path_wo_overlap(Path(save_dir_base) / "recommended_grouping", spacing="_")
    save_dir.mkdir()
    # 1. Prepare objects
    ref_seq_list = [mc.MyRefSeq(plasmid_map_path) for plasmid_map_path in plasmid_map_paths]
    # 2. execute
    recommended_grouping = psc.execute_grouping(ref_seq_list, param_dict, save_dir)
    # 3. save results
    psc.export_results(recommended_grouping, save_dir)
    # 4. display recommended_grouping in the std output
    print(f"\n{recommended_grouping.recommended_grouping_txt}")


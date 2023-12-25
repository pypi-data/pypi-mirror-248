# -*- coding: utf-8 -*-

import argparse

from . import *
from ..modules import my_classes as mc

error_rate = 0.0001
param_dict = {
    'gap_open_penalty': 3, 
    'gap_extend_penalty': 1, 
    'match_score': 1, 
    'mismatch_score': -2, 
    'score_threshold': 0.3, 
    'error_rate': error_rate, 
    'del_mut_rate': error_rate / 4, # e.g. "A -> T, C, G, del"
    'ins_rate': 0.0001, 
}


if __name__ == "__main__":
    """
    python -m savemoney.post_analysis path_to_sequence_data_dir save_dir_base
    """

    # パーサーの設定
    parser = argparse.ArgumentParser()
    parser.add_argument("sequence_dir_paths", help="sequence_dir_paths", type=str)
    parser.add_argument("save_dir_base", help="save directory path", type=str)
    for key, val in param_dict.items():
        parser.add_argument(f"-{mc.key2argkey(key)}", help=f"{key}, optional, default_value = {val}", type=int, default=val)

    # 取得した引数を適用
    args = parser.parse_args()
    args_dict =vars(args)
    for key in param_dict.keys():
        param_dict[key] = args_dict[mc.key2argkey(key)]

    post_analysis(args.sequence_dir_paths, param_dict, args.save_dir_base)


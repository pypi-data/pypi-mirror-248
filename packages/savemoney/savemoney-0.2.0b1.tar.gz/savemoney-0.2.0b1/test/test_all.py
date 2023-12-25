# -*- coding: utf-8 -*-

import savemoney
from pathlib import Path

if __name__ == "__main__":
    abs_path = Path(__file__).resolve()
    sequence_dir_paths = abs_path.parents[1] / "resources/demo_data/my_plasmid_maps_fa"
    save_dir_base = abs_path.parents[1] / "resources/demo_data"

    ##############
    # pre-survey #
    ##############
    param_dict = {
        'gap_open_penalty':     3, 
        'gap_extend_penalty':   1, 
        'match_score':          1, 
        'mismatch_score':       -2, 
        'distance_threshold':   5, 
        'number_of_groups':     1, 
    }
    savemoney.pre_survey(sequence_dir_paths, param_dict, save_dir_base)


    #################
    # post-anakysis #
    #################
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

    savemoney.post_analysis(sequence_dir_paths, param_dict, save_dir_base)





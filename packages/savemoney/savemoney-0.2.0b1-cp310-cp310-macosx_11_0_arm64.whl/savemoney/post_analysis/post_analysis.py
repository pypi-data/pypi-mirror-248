# -*- coding: utf-8 -*-

from pathlib import Path
from itertools import chain

# my modules
from ..modules import my_classes as mc
from . import post_analysis_core as pac

__all__ = ["post_analysis"]

def post_analysis(sequence_dir_paths, param_dict:dict, save_dir_base: Path):
    # 0. Prepare files
    plasmid_map_paths = []
    for ext in mc.MyRefSeq.allowed_plasmid_map_extensions:
        plasmid_map_paths = chain(plasmid_map_paths, Path(sequence_dir_paths).glob(f"*{ext}"))
    fastq_paths = Path(sequence_dir_paths).glob(f"*.fastq")
    # 1. Prepare files
    ref_seq_list = [mc.MyRefSeq(plasmid_map_path) for plasmid_map_path in plasmid_map_paths]
    my_fastq = mc.MyFastQ.combine([mc.MyFastQ(fastq_path) for fastq_path in fastq_paths])
    save_dir = mc.new_dir_path_wo_overlap(Path(save_dir_base) / my_fastq.combined_name_stem, spacing="_")
    save_dir.mkdir()
    # 2. Execute alignment: load if any previous score_matrix if possible
    result_dict = pac.execute_alignment(ref_seq_list, my_fastq, param_dict, save_dir)
    # 3. normalize alignment score and set threshold for assignment
    query_assignment = pac.normalize_scores_and_apply_threshold(ref_seq_list, my_fastq, result_dict, param_dict)
    pac.draw_and_save_query_assignment(query_assignment, save_dir, display_plot=False)
    # 4. MSA/consensus
    my_msa_dict = pac.execute_msa(result_dict, query_assignment, param_dict)
    # 5. EXPORT
    pac.export_results(my_msa_dict, save_dir)
    pac.export_log(ref_seq_list, my_fastq, param_dict, query_assignment, save_dir)


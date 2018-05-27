#! /usr/bin/env python

import utils
from Bio import SeqIO
import numpy
import seaborn
from matplotlib import pyplot
import os
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
import math

def main():
  (current_work_dir_path, asset_dir_path, program_dir_path, conda_program_dir_path) = utils.get_dir_paths()
  neofold_ss_dir_path = asset_dir_path + "/neofold"
  parasor_ss_dir_path = asset_dir_path + "/parasor"
  centroidhomfold_ss_dir_path = asset_dir_path + "/centroidhomfold"
  rna_fam_dir_path = asset_dir_path + "/sampled_rna_families"
  neofold_ppvs = []
  neofold_senss = []
  parasor_ppvs = []
  parasor_senss = []
  centroidhomfold_ppvs = []
  centroidhomfold_senss = []
  gammas = [2. ** i for i in range(-7, 11)]
  for gamma in gammas:
    gamma_str = str(gamma)
    neofold_tp = neofold_tn = neofold_fp = neofold_fn = 0.
    parasor_tp = parasor_tn = parasor_fp = parasor_fn = 0.
    centroidhomfold_tp = centroidhomfold_tn = centroidhomfold_fp = centroidhomfold_fn = 0.
    for rna_fam_file in os.listdir(rna_fam_dir_path):
      if not rna_fam_file.endswith(".fa"):
        continue
      rna_seq_file_path = os.path.join(rna_fam_dir_path, rna_fam_file)
      rna_seq_lens = [len(rna_seq.seq) for rna_seq in SeqIO.parse(rna_seq_file_path, "fasta")]
      (rna_fam_name, extension) = os.path.splitext(rna_fam_file)
      ref_ss_file_path = os.path.join(rna_fam_dir_path, "sss_of_" + rna_fam_name + ".dat")
      ref_sss = utils.get_sss(utils.get_ss_strings(ref_ss_file_path))
      neofold_estimated_ss_dir_path = os.path.join(neofold_ss_dir_path, "sss_of_" + rna_fam_name)
      if not os.path.isdir(neofold_estimated_ss_dir_path):
        continue
      parasor_estimated_ss_dir_path = os.path.join(parasor_ss_dir_path, "sss_of_" + rna_fam_name)
      if not os.path.isdir(parasor_estimated_ss_dir_path):
        continue
      centroidhomfold_estimated_ss_dir_path = os.path.join(centroidhomfold_ss_dir_path, "sss_of_" + rna_fam_name)
      if not os.path.isdir(centroidhomfold_estimated_ss_dir_path):
        continue
      neofold_estimated_ss_file_path = os.path.join(neofold_estimated_ss_dir_path, "gamma=" + gamma_str + ".dat")
      estimated_sss = utils.get_sss(utils.get_ss_strings(neofold_estimated_ss_file_path))
      for (estimated_ss, ref_ss, rna_seq_len) in zip(estimated_sss, ref_sss, rna_seq_lens):
        for i in range(0, rna_seq_len):
          for j in range(i + 1, rna_seq_len):
            estimated_bin = (i, j) in estimated_ss
            ref_bin = (i, j) in ref_ss
            if estimated_bin == ref_bin:
              if estimated_bin == True:
                neofold_tp += 1
              else:
                neofold_tn += 1
            else:
              if estimated_bin == True:
                neofold_fp += 1
              else:
                neofold_fn += 1
      parasor_estimated_ss_file_path = os.path.join(parasor_estimated_ss_dir_path, "gamma=" + gamma_str + ".dat")
      estimated_sss = utils.get_sss(utils.get_ss_strings(parasor_estimated_ss_file_path))
      for (estimated_ss, ref_ss, rna_seq_len) in zip(estimated_sss, ref_sss, rna_seq_lens):
        for i in range(0, rna_seq_len):
          for j in range(i + 1, rna_seq_len):
            estimated_bin = (i, j) in estimated_ss
            ref_bin = (i, j) in ref_ss
            if estimated_bin == ref_bin:
              if estimated_bin == True:
                parasor_tp += 1
              else:
                parasor_tn += 1
            else:
              if estimated_bin == True:
                parasor_fp += 1
              else:
                parasor_fn += 1
      centroidhomfold_estimated_ss_file_path = os.path.join(centroidhomfold_estimated_ss_dir_path, "gamma=" + gamma_str + ".dat")
      estimated_sss = utils.get_sss(utils.get_ss_strings(centroidhomfold_estimated_ss_file_path))
      for (estimated_ss, ref_ss, rna_seq_len) in zip(estimated_sss, ref_sss, rna_seq_lens):
        for i in range(0, rna_seq_len):
          for j in range(i + 1, rna_seq_len):
            estimated_bin = (i, j) in estimated_ss
            ref_bin = (i, j) in ref_ss
            if estimated_bin == ref_bin:
              if estimated_bin == True:
                centroidhomfold_tp += 1
              else:
                centroidhomfold_tn += 1
            else:
              if estimated_bin == True:
                centroidhomfold_fp += 1
              else:
                centroidhomfold_fn += 1
    ppv = neofold_tp / (neofold_tp + neofold_fp)
    sens = neofold_tp / (neofold_tp + neofold_fn)
    neofold_ppvs.insert(0, ppv)
    neofold_senss.insert(0, sens)
    ppv = parasor_tp / (parasor_tp + parasor_fp)
    sens = parasor_tp / (parasor_tp + parasor_fn)
    parasor_ppvs.insert(0, ppv)
    parasor_senss.insert(0, sens)
    ppv = centroidhomfold_tp / (centroidhomfold_tp + centroidhomfold_fp)
    sens = centroidhomfold_tp / (centroidhomfold_tp + centroidhomfold_fn)
    centroidhomfold_ppvs.insert(0, ppv)
    centroidhomfold_senss.insert(0, sens)
  neofold_ppvs = numpy.array(neofold_ppvs) 
  neofold_senss = numpy.array(neofold_senss)
  parasor_ppvs = numpy.array(parasor_ppvs) 
  parasor_senss = numpy.array(parasor_senss)
  centroidhomfold_ppvs = numpy.array(centroidhomfold_ppvs) 
  centroidhomfold_senss = numpy.array(centroidhomfold_senss)
  line_1, = pyplot.plot(neofold_ppvs, neofold_senss, label = "NeoFold", marker = "o", linestyle = "-")
  line_2, = pyplot.plot(parasor_ppvs, parasor_senss, label = "ParasoR", marker = "v", linestyle = "-")
  line_3, = pyplot.plot(centroidhomfold_ppvs, centroidhomfold_senss, label = "CentroidHomFold", marker = "s", linestyle = "-")
  pyplot.xlabel("A PPV")
  pyplot.ylabel("A sensitivity")
  pyplot.legend(handles = [line_1, line_2, line_3], loc = 1)
  neofold_mcc = (neofold_total_tp * neofold_total_tn - neofold_total_fp * neofold_total_fn) / math.sqrt((neofold_total_tp + neofold_total_fp) * (neofold_total_tp + neofold_total_fn) * (neofold_total_tn + neofold_total_fp) * (neofold_total_tn + neofold_total_fn))
  parasor_mcc = (parasor_total_tp * parasor_total_tn - parasor_total_fp * parasor_total_fn) / math.sqrt((parasor_total_tp + parasor_total_fp) * (parasor_total_tp + parasor_total_fn) * (parasor_total_tn + parasor_total_fp) * (parasor_total_tn + parasor_total_fn))
  centroidhomfold_mcc = (centroidhomfold_total_tp * centroidhomfold_total_tn - centroidhomfold_total_fp * centroidhomfold_total_fn) / math.sqrt((centroidhomfold_total_tp + centroidhomfold_total_fp) * (centroidhomfold_total_tp + centroidhomfold_total_fn) * (centroidhomfold_total_tn + centroidhomfold_total_fp) * (centroidhomfold_total_tn + centroidhomfold_total_fn))
  image_dir_path = asset_dir_path + "/images"
  if not os.path.exists(image_dir_path):
    os.mkdir(image_dir_path)
  pyplot.tight_layout()
  pyplot.savefig(image_dir_path + "/ppvs_vs_senss_on_ss_estimation.eps", bbox_inches = "tight")

if __name__ == "__main__":
  main()

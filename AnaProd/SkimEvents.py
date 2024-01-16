import ROOT
import os
import shutil
import sys
ROOT.gROOT.SetBatch(True)
ROOT.EnableThreadSafety()


if __name__ == "__main__":
    sys.path.append(os.environ['ANALYSIS_PATH'])

import Common.Utilities as Utilities



def ListToVector(list, type="string"):
	vec = ROOT.std.vector(type)()
	for item in list:
		vec.push_back(item)
	return vec

col_type_dict = {
  'Float_t':'float',
  'Bool_t':'bool',
  'Int_t' :'int',
  'ULong64_t' :'unsigned long long',
  'ULong_t' :'unsigned long',
  'Long_t' :'long',
  'UInt_t' :'unsigned int',
  'ROOT::VecOps::RVec<float>':'ROOT::VecOps::RVec<float>',
  'ROOT::VecOps::RVec<int>':'ROOT::VecOps::RVec<int>',
  'ROOT::VecOps::RVec<unsigned char>':'ROOT::VecOps::RVec<unsigned char>'
  }
def make_df(inputFileCentral,inputFileShifted,outDir,treeName,treeName_in='Events',treeName_central='Events'):
  df_out = ROOT.RDataFrame(treeName_in, inputFileShifted)
  colNames = [str(c) for c in df_out.GetColumnNames()]
  if len(colNames)==0:
    print(f"{treeName_in} has no columns")
    return
  entryIndexIdx = colNames.index("entryIndex")
  colNames[entryIndexIdx], colNames[0] = colNames[0], colNames[entryIndexIdx]
  col_types = [str(df_out.GetColumnType(c)) for c in colNames]
  tuple_maker = ROOT.analysis.TupleMaker(*col_types)(ROOT.RDataFrame(treeName_central,inputFileCentral), 4)
  print("tuplemaker created")
  df_out = tuple_maker.processOut(ROOT.RDF.AsRNode(df_out))
  print("tuplemaker processed")
  df_out = df_out.Define("isValid", "_entryCentral.use_count() > 0")
  df_unique = df_out.Filter("!isValid")
  df_out_valid = df_out.Filter('isValid')

  colToSave_diff= []
  colToNotToMakeDiff=  ["period","run", "sample_name", "sample_type", "channelId", "entryIndex", "event", "isData", "luminosityBlock", "X_mass", "X_spin"]
  colToSave_noDiff= [ "entryIndex"]

  condition_noDiff_list = []
  condition_Valid_list = []

  for var_idx,var_name in enumerate(colNames):
    if var_name in colToNotToMakeDiff: continue
    condition_noDiff_list.append(f"analysis::IsSame(_entryCentral->GetValue<{col_type_dict[col_types[var_idx]]}>({var_idx}),{var_name})")

  condition_noDiff = ' && '.join(condition_noDiff_list)
  df_out_valid = df_out_valid.Define("isSame", condition_noDiff)
  df_out_valid_noDiff = df_out_valid.Filter("isSame")
  df_out_valid_diff = df_out_valid.Filter("!isSame")
  for var_idx,var_name in enumerate(colNames):
    if var_name in colToNotToMakeDiff: continue
    df_out_valid_diff=df_out_valid_diff.Define(f"{var_name}Diff", f"""analysis::Delta(_entryCentral->GetValue<{col_type_dict[col_types[var_idx]]}>({var_idx}),{var_name})""")
    colToSave_diff.append(f"{var_name}Diff")

  snaps = []
  print("start making screenshot")
  snapshotOptions = ROOT.RDF.RSnapshotOptions()
  snapshotOptions.fOverwriteIfExists=False
  snapshotOptions.fLazy=True
  snapshotOptions.fMode="RECREATE"
  snapshotOptions.fCompressionAlgorithm = getattr(ROOT.ROOT, 'k' + 'ZLIB')
  snapshotOptions.fCompressionLevel = 4
  colToSave_noDiff_v = ListToVector(colToSave_noDiff)
  colToSave_diff_v = ListToVector(colToSave_diff+["entryIndex"])
  colNames_v = ListToVector(colNames)
  outFile_Valid = os.path.join(outDir, f"{treeName}_Valid.root")
  outFile_nonValid = os.path.join(outDir, f"{treeName}_nonValid.root")
  outFile_Valid_noDiff = os.path.join(outDir, f"{treeName}_noDiff.root")
  if os.path.exists(outFile_Valid):
    os.remove(outFile_Valid)
  if os.path.exists(outFile_nonValid):
    os.remove(outFile_nonValid)
  if os.path.exists(outFile_Valid_noDiff):
    os.remove(outFile_Valid_noDiff)
  snaps.append(df_out_valid_noDiff.Snapshot(f"{treeName}_noDiff", outFile_Valid_noDiff, colToSave_noDiff_v, snapshotOptions))
  snaps.append(df_out_valid_diff.Snapshot(f"{treeName}_Valid", outFile_Valid, colToSave_diff_v, snapshotOptions))
  snaps.append(df_unique.Snapshot(f"{treeName}_nonValid", outFile_nonValid, colNames_v, snapshotOptions))
  tuple_maker.processIn(colNames_v)
  ROOT.RDF.RunGraphs(snaps)


  tuple_maker.join()



if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('--inFileCentral', required=True, type=str)
  parser.add_argument('--inFileShifted', required=True, type=str)
  parser.add_argument('--outDir', required=True, type=str)
  parser.add_argument('--treeName_out', required=True, type=str)
  parser.add_argument('--treeName_in', required=False, type=str, default='Events')
  parser.add_argument('--treeName_central', required=False, type=str, default='Events')
  args = parser.parse_args()
  headers_dir = os.path.dirname(os.path.abspath(__file__))
  ROOT.gROOT.ProcessLine(f".include {os.environ['ANALYSIS_PATH']}")
  #header_path_Skimmer = os.path.join(headers_dir, "include/SystSkimmer.h")
  ROOT.gInterpreter.Declare(f'#include "include/SystSkimmer.h"')
  make_df(args.inFileCentral,args.inFileShifted,args.outDir,args.treeName_out,args.treeName_in,args.treeName_central)


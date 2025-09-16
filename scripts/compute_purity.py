import uproot
import awkward as ak

file_path = "/eos/user/e/emartinv/vbfjets_Training/training_skims_cclub/2022_VBFHHto2B2Tau_CV_1_C2V_1_C3_1.root"
tree_name = "Event"

with uproot.open(file_path)[tree_name] as tree:
    isCCLUB = tree["RecoJet_isCCLUBbjet"].arrays(library="ak")
    genMatched = tree["RecoJet_genMatched"].arrays(library="ak")

total_matches = 0
total_jets = 0
total_events = len(isCCLUB)
events_with_full_match = 0

for jets_isCCLUB, jets_genMatched in zip(isCCLUB["RecoJet_isCCLUBbjet"], genMatched["RecoJet_genMatched"]):

    for isCCLUB_val, genMatch_val in zip(jets_isCCLUB, jets_genMatched):
        if isCCLUB_val == genMatch_val:
            total_matches += 1
        total_jets += 1

    if jets_isCCLUB[0] == jets_genMatched[0] and jets_isCCLUB[1] == jets_genMatched[1]:
        events_with_full_match += 1

# Print results
print(f"Total number of events: {total_events}")
print(f"Total number of jets: {total_jets}")
print(f"Number of matching jets: {total_matches}")
print(f"Purity at least one(ratio): {total_matches / total_jets:.4f}")
print(f"Number of events: {len(isCCLUB)}")
print(f"Number of events with both jets matching: {events_with_full_match}")
print(f"Purity both matches(ratio): {events_with_full_match / total_events:.4f}")


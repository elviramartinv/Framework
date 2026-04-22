from Common.Utilities import *


channels = [ 'muMu', 'eMu', 'eE', 'muTau', 'eTau', 'tauTau' ] # in order of importance during the channel selection
leg_names = [ "Electron", "Muon", "Tau" ]

def getChannelLegs(channel):
    ch_str = channel.lower()
    legs = []
    while len(ch_str) > 0:
        name_idx = None
        obj_name = None
        for idx, obj in enumerate(['e', 'mu', 'tau']):
            if ch_str.startswith(obj):
                name_idx = idx
                obj_name = obj
                break
        if name_idx is None:
            raise RuntimeError(f"Invalid channel name {channel}")
        legs.append(leg_names[name_idx])
        ch_str = ch_str[len(obj_name):]
    return legs 

def PassGenAcceptance(df):
    df = df.Filter("genHttCandidate.get() != nullptr", "genHttCandidate present")
    return df.Filter("PassGenAcceptance(*genHttCandidate)", "genHttCandidate Acceptance")

# def GenJetSelection(df):
#     df = df.Define("GenJet_B1","GenJet_pt > 20 && abs(GenJet_eta) < 2.5 && GenJet_Hbb")
#     df = df.Define("GenJetAK8_B1","GenJetAK8_pt > 170 && abs(GenJetAK8_eta) < 2.5 && GenJetAK8_Hbb")
#     return df.Filter("GenJet_idx[GenJet_B1].size()==2 || (GenJetAK8_idx[GenJetAK8_B1].size()==1 && genHbb_isBoosted)", "(One)Two b-parton (Fat)jets at least")

def GenJetSelection(df):
    df = df.Define("GenJet_B1","GenJet_pt > 20 && abs(GenJet_eta) < 2.5 && GenJet_Hbb")
    return df.Filter("GenJet_idx[GenJet_B1].size()==2", "(One)Two b-parton jets at least")

def GenVBFJetSelection(df):
    df = df.Define("GenJet_VBF1", "GenJet_pt > 20 && abs(GenJet_eta) < 4.7 && GenVBFJetsMatch")
    return df.Filter("GenJet_idx[GenJet_VBF1].size()>=2", "Two different VBF jets at least")

# def GenJetHttOverlapRemoval(df):
#     for var in ["GenJet", "GenJetAK8"]:
#         df = df.Define(f"{var}_B2", f"RemoveOverlaps({var}_p4, {var}_B1,{{{{genHttCandidate->leg_p4[0], genHttCandidate->leg_p4[1]}},}}, 2, 0.5)" )
#     return df.Filter("GenJet_idx[GenJet_B2].size()==2 || (GenJetAK8_idx[GenJetAK8_B2].size()==1 && genHbb_isBoosted)", "No overlap between genJets and genHttCandidates")

def GenJetHttOverlapRemoval(df):
    """Remove overlap between b-jets from Hbb and taus from Htt.
    GenJet_B1 -> GenJet_B2 (after removing overlap with Htt taus)
    """
    for var in ["GenJet"]:
        df = df.Define(f"{var}_B2", f"RemoveOverlaps({var}_p4, {var}_B1,{{{{genHttCandidate->leg_p4[0], genHttCandidate->leg_p4[1]}},}}, 2, 0.5)" )
    return df.Filter("GenJet_idx[GenJet_B2].size()==2", "No overlap between genJets and genHttCandidates")

def GenAllOverlapRemoval(df):
    """Unified overlap removal: VBF jets vs (Hbb b-jets + Htt taus).
    This ensures VBF jets don't overlap with either b-jets (after tau cleaning) or taus.
    Uses GenJet_B2 (b-jets already cleaned from tau overlap) instead of genHbbCandidate.
    
    Note: GenJet_B2 are the indices of b-jets AFTER removing overlap with taus,
    so we extract their p4 vectors to use in the overlap removal.
    At this point we are guaranteed to have exactly 2 b-jets (enforced by GenJetHttOverlapRemoval filter).
    """
    # Extract the p4 of the two b-jets after tau overlap removal
    df = df.Define("GenJet_B2_indices", "GenJet_idx[GenJet_B2]")
    df = df.Define("GenJet_B2_p4_vec", """
        ROOT::VecOps::RVec<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>>> result;
        for (const auto& idx : GenJet_B2_indices) {
            result.push_back(GenJet_p4[idx]);
        }
        return result;
    """)
    
    # Remove VBF jet overlaps with both b-jets AND taus
    df = df.Define("GenJet_VBF2", """
        std::vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>>> objects_to_remove;
        // Add tau candidates
        objects_to_remove.push_back(genHttCandidate->leg_p4[0]);
        objects_to_remove.push_back(genHttCandidate->leg_p4[1]);
        // Add b-jets (already cleaned from tau overlap)
        for (const auto& bjet_p4 : GenJet_B2_p4_vec) {
            objects_to_remove.push_back(bjet_p4);
        }
        return RemoveOverlaps(GenJet_p4, GenJet_VBF1, {objects_to_remove}, 2, 0.5);
    """)
    return df.Filter("GenJet_idx[GenJet_VBF2].size()>=2", "No overlap between VBF jets and (Hbb+Htt)")

# Legacy functions - DEPRECATED: Use GenAllOverlapRemoval instead
# These are kept for backwards compatibility but should not be used together
def GenVBFHttOverlapRemoval(df):
    """DEPRECATED: Use GenAllOverlapRemoval for proper 3-way overlap removal"""
    for var in ["GenJet"]:
        df = df.Define(f"{var}_VBF", f"RemoveOverlaps({var}_p4, {var}_VBF1,{{{{genHttCandidate->leg_p4[0], genHttCandidate->leg_p4[1]}},}}, 2, 0.5)" )
    return df.Filter("GenJet_idx[GenJet_VBF].size()>=2", "No overlap between VBF jets and Htt jets")

def GenJetVBFOverlapRemoval(df):
    """DEPRECATED: Use GenAllOverlapRemoval for proper 3-way overlap removal
    WARNING: This uses genHbbCandidate.leg_p4 which are GenPart b-quarks, 
    NOT GenJets after tau overlap removal!
    """
    for var in ["GenJet"]:
        df = df.Define(f"{var}_VBF", f"RemoveOverlaps({var}_p4, {var}_VBF1,{{{{genHbbCandidate.leg_p4[0], genHbbCandidate.leg_p4[1]}},}}, 2, 0.5)" )
    return df.Filter("GenJet_idx[GenJet_VBF].size()>=2", "No overlap between VBF jets and Hbb jets")


# def GenJetHttOverlapRemoval_CCLUB(df):
#     for var in ["GenJet", "GenJetAK8"]:
#         df = df.Define(f"{var}_B2", f"RemoveOverlaps({var}_p4, {var}_B1,{{{{dau1_p4, dau2_p4}},}}, 2, 0.5)" )
#     return df.Filter("GenJet_idx[GenJet_B2].size()==2 || (GenJetAK8_idx[GenJetAK8_B2].size()==1 && genHbb_isBoosted)", "No overlap between genJets and genHttCandidates")

def RequestOnlyResolvedGenJets(df):
    return df.Filter("GenJet_idx[GenJet_B2].size()==2", "Resolved topology")

def RecoHttCandidateSelection(df, config):
    df = df.Define("Electron_B0", f"""
        v_ops::pt(Electron_p4) > 10 && abs(v_ops::eta(Electron_p4)) < 2.5 && abs(Electron_dz) < 0.2 && abs(Electron_dxy) < 0.045  """) # && (Electron_mvaIso_WP90 || (Electron_mvaNoIso_WP90 && Electron_pfRelIso03_all < 0.5))

    df = df.Define("Muon_B0", f"""
        v_ops::pt(Muon_p4) > 15 && abs(v_ops::eta(Muon_p4)) < 2.4 && abs(Muon_dz) < 0.2 && abs(Muon_dxy) < 0.045
        """) # && ( ((Muon_tightId || Muon_mediumId) && Muon_pfRelIso04_all < 0.5) || (Muon_highPtId && Muon_tkRelIso < 0.5) )

    eta_cut = 2.3 if config["deepTauVersion"] == '2p1' else 2.5
    df = df.Define("Tau_B0", f"""
        v_ops::pt(Tau_p4) > 20 && abs(v_ops::eta(Tau_p4)) < {eta_cut} && abs(Tau_dz) < 0.2 && Tau_decayMode != 5 && Tau_decayMode != 6 && ( Tau_idDeepTau{deepTauVersions[config["deepTauVersion"]]}v{config["deepTauVersion"]}VSjet >= {WorkingPointsTauVSjet.VVVLoose.value} )
    """)

    df = df.Define("Electron_iso", "Electron_pfRelIso03_all") \
           .Define("Muon_iso", "Muon_pfRelIso04_all") \
           .Define("Tau_iso", f"""-Tau_rawDeepTau{deepTauVersions[config["deepTauVersion"]]}v{config["deepTauVersion"]}VSjet""")

    df = df.Define("Electron_B2_eTau_1", f"Electron_B0 && Electron_mvaIso_WP80 ")
    #  Electron_mvaNoIso_WP80 && Electron_pfRelIso03_all < 0.3


    df = df.Define("Muon_B2_muTau_1", f"""
        Muon_B0 &&  ( (Muon_tightId && Muon_pfRelIso04_all < 0.15) || (Muon_highPtId && Muon_tkRelIso < 0.15) )
    """)
        #Muon_B0 &&  (Muon_tightId && Muon_pfRelIso04_all < 0.15)


    for ch in [ "eTau", "muTau", "tauTau" ]:
        cut_str = f'''Tau_B0
            && (Tau_idDeepTau{deepTauVersions[config["deepTauVersion"]]}v{config["deepTauVersion"]}VSe >= {getattr(WorkingPointsTauVSe, config["deepTauWPs"][ch]["VSe"]).value})
            && (Tau_idDeepTau{deepTauVersions[config["deepTauVersion"]]}v{config["deepTauVersion"]}VSmu >= {getattr(WorkingPointsTauVSmu, config["deepTauWPs"][ch]["VSmu"]).value})'''
        df = df.Define(f'Tau_B2_{ch}_2', cut_str)
        if ch == 'tauTau':
            cut_str_tt = cut_str + f' && (Tau_idDeepTau{deepTauVersions[config["deepTauVersion"]]}v{config["deepTauVersion"]}VSjet >= {getattr(WorkingPointsTauVSjet, config["deepTauWPs"]["tauTau"]["VSjet"]).value})'
            df = df.Define(f'Tau_B2_{ch}_1', cut_str_tt)


    df = df.Define("Muon_B2_muMu_1", f"""
        Muon_B0 && ( (Muon_tightId && Muon_pfRelIso04_all < 0.15) || (Muon_highPtId && Muon_tkRelIso < 0.15) )
    """)
    df = df.Define("Muon_B2_muMu_2", f"""
        Muon_B0 && ( (Muon_tightId && Muon_pfRelIso04_all < 0.3) || (Muon_highPtId && Muon_tkRelIso < 0.3) )
    """)

    df = df.Define("Electron_B2_eMu_1",f"Electron_B0 && Electron_mvaIso_WP80 ")
    #  Electron_mvaNoIso_WP80 && Electron_pfRelIso03_all < 0.3
    df = df.Define("Muon_B2_eMu_2", f"""
        Muon_B0 && ( (Muon_tightId && Muon_pfRelIso04_all < 0.3) || (Muon_highPtId && Muon_tkRelIso < 0.3) )
    """)

    df = df.Define("Electron_B2_eE_1",f"Electron_B0 && Electron_mvaIso_WP80 ")
    #  Electron_mvaNoIso_WP80 && Electron_pfRelIso03_all < 0.3
    df = df.Define("Electron_B2_eE_2", f""" Electron_B0 && Electron_mvaNoIso_WP80 && Electron_pfRelIso03_all < 0.3 """)

    cand_columns = []
    
    for ch in channels:
        leg1, leg2 = getChannelLegs(ch)
        cand_column = f"HttCandidates_{ch}"
        df = df.Define(cand_column, f"""
            GetHTTCandidates<2>(Channel::{ch}, 0.5, {leg1}_B2_{ch}_1, {leg1}_p4, {leg1}_iso, {leg1}_charge, {leg1}_genMatchIdx, {leg2}_B2_{ch}_2, {leg2}_p4, {leg2}_iso, {leg2}_charge, {leg2}_genMatchIdx)
        """)
        cand_columns.append(cand_column)
    cand_filters = [ f'{c}.size() > 0' for c in cand_columns ]
    df = df.Filter(" || ".join(cand_filters))
    cand_list_str = ', '.join([ '&' + c for c in cand_columns])
    return df.Define('HttCandidate', f'GetBestHTTCandidate<2>({{ {cand_list_str} }}, event)') 

def ThirdLeptonVeto(df):
    df = df.Define("Electron_vetoSel",
                   f"""v_ops::pt(Electron_p4) > 10 && abs(v_ops::eta(Electron_p4)) < 2.5 && abs(Electron_dz) < 0.2 && abs(Electron_dxy) < 0.045
                      && ( Electron_mvaIso_WP90 == true )
                     && (HttCandidate.isLeg(Electron_idx, Leg::e)== false)""") # || ( Electron_mvaNoIso_WP90 && Electron_pfRelIso03_all<0.3) --> removed
    df = df.Filter("Electron_idx[Electron_vetoSel].size() == 0", "No extra electrons")
    df = df.Define("Muon_vetoSel",
                   f"""v_ops::pt(Muon_p4) > 10 && abs(v_ops::eta(Muon_p4)) < 2.4 && abs(Muon_dz) < 0.2 && abs(Muon_dxy) < 0.045
                      && ( Muon_mediumId || Muon_tightId ) && Muon_pfRelIso04_all<0.3
                      && (HttCandidate.isLeg(Muon_idx, Leg::mu) == false)""")
    df = df.Filter("Muon_idx[Muon_vetoSel].size() == 0", "No extra muons")
    return df

def GenRecoTauMatching(df):
    df = df.Define("dau1_genTauIdx_matched", "GenRecoTauMatchingSingle(dau1_p4, *genHttCandidate, 0.3)")
    df = df.Define("dau2_genTauIdx_matched", "GenRecoTauMatchingSingle(dau2_p4, *genHttCandidate, 0.3)")
    df = df.Define("dau1_genMatched", "dau1_genTauIdx_matched >= 0")
    df = df.Define("dau2_genMatched", "dau2_genTauIdx_matched >= 0")
    df = df.Filter("dau1_genMatched && dau2_genMatched", "Both taus have gen match")
    return df

def RecoJetInvMass(df):
    df = df.Define("Jet_invMass", "GetInvMass(Jet_p4)")
    return df

def RecoJetSelection(df):
    df = df.Define("Jet_bIncl", f"v_ops::pt(Jet_p4)>20 && abs(v_ops::eta(Jet_p4)) < 2.5 && ( Jet_jetId >= 2 ) ")
    # df = df.Define("FatJet_bbIncl", "FatJet_msoftdrop > 30 && abs(v_ops::eta(FatJet_p4)) < 2.5")
    df = df.Define("Jet_bCand", "RemoveOverlaps(Jet_p4, Jet_bIncl,{{HttCandidate.leg_p4[0], HttCandidate.leg_p4[1]},}, 2, 0.5)")
    # df = df.Define("FatJet_bbCand", "RemoveOverlaps(FatJet_p4, FatJet_bbIncl, {{HttCandidate.leg_p4[0], HttCandidate.leg_p4[1]},}, 2, 0.5)")
    return df

def RecoJetSelection_CCLUB(df):
    df = df.Define("Jet_bIncl_CCLUB", f"v_ops::pt(Jet_p4)>20 && abs(v_ops::eta(Jet_p4)) < 2.5 && ( Jet_jetId >= 6 ) ")
    # df = df.Define("FatJet_bbIncl_CCLUB", "FatJet_msoftdrop > 30 && abs(v_ops::eta(FatJet_p4)) < 2.5")
    df = df.Define("Jet_bCand_CCLUB", "RemoveOverlaps(Jet_p4, Jet_bIncl_CCLUB,{{dau1_p4, dau2_p4},}, 2, 0.5)")
    # df = df.Define("FatJet_bbCand_CCLUB", "RemoveOverlaps(FatJet_p4, FatJet_bbIncl_CCLUB, {{dau1_p4, dau2_p4},}, 2, 0.5)")
    return df

def ExtraRecoJetSelection(df):
    df = df.Define("ExtraJet_B0", f"v_ops::pt(Jet_p4)>20 && abs(v_ops::eta(Jet_p4)) < 5 && ( Jet_jetId & 2 ) && (Jet_puId>0 || v_ops::pt(Jet_p4)>50)")
    df = df.Define(f"ObjectsToRemoveOverlap", "if(Hbb_isValid){return std::vector<RVecLV>({{HttCandidate.leg_p4[0], HttCandidate.leg_p4[1],HbbCandidate->leg_p4[0],HbbCandidate->leg_p4[1]}}); } return std::vector<RVecLV>({{HttCandidate.leg_p4[0], HttCandidate.leg_p4[1]}})")
    df = df.Define(f"ExtraJet_B1", """ RemoveOverlaps(Jet_p4, ExtraJet_B0,ObjectsToRemoveOverlap, 2, 0.5)""")
    return df

def RecoVBFJetSelection(df):
    df = df.Define("Jet_vbfIncl", f"v_ops::pt(Jet_p4)>20 && abs(v_ops::eta(Jet_p4)) < 4.7 && ( Jet_jetId >= 6 ) ")
    df = df.Define("Jet_vbfCand", "RemoveOverlaps(Jet_p4, Jet_vbfIncl,{{HttCandidate.leg_p4[0], HttCandidate.leg_p4[1], HbbCandidate->leg_p4[0], HbbCandidate->leg_p4[1]}}, 2, 0.5)")
    return df

def RecoVBFJetSelection_CCLUB(df, pt_threshold=20.0):
    df = df.Define("Jet_vbfIncl_CCLUB", f"v_ops::pt(Jet_p4)>{pt_threshold} && abs(v_ops::eta(Jet_p4)) < 4.7 && ( Jet_jetId >= 6 ) ")
    df = df.Define("Jet_vbfCand_CCLUB", "RemoveOverlaps(Jet_p4, Jet_vbfIncl_CCLUB,{{dau1_p4, dau2_p4, bjet1_p4, bjet2_p4}}, 2, 0.5)")
    return df

def RecoJetHornsRemoval(df):
    """Remove reconstructed jets in the detector 'Horns' region (bad reconstruction region).
    
    Horns region: 2.5 < |eta| < 3.0 with pT < 50 GeV
    These jets have poor reconstruction quality and should be removed from VBF jet candidates.
    
    Applies to Jet_vbfCand_CCLUB (VBF jets after overlap removal with taus and b-jets).
    Creates Jet_vbfCand_CCLUB_noHorns for further analysis.
    """
    df = df.Define("Jet_vbfCand_CCLUB_noHorns", """
        ROOT::VecOps::RVec<bool> result(Jet_p4.size(), false);
        for (size_t i = 0; i < Jet_p4.size(); ++i) {
            if (!Jet_vbfCand_CCLUB[i]) continue;  // Skip jets not in VBF candidate selection
            
            float pt = Jet_p4[i].Pt();
            float abs_eta = std::abs(Jet_p4[i].Eta());
            
            // Remove if in Horns region: pT < 50 && 2.5 < |eta| < 3.0
            bool in_horns_region = (pt < 50.0 && abs_eta > 2.5 && abs_eta < 3.0);
            
            if (!in_horns_region) {
                result[i] = true;
            }
        }
        return result;
    """)
    return df.Filter("Jet_idx[Jet_vbfCand_CCLUB_noHorns].size()>=2", "VBF reco jets after Horns removal")

# def ApplyJetSelection(df):
#     return df.Filter("Jet_idx[Jet_bCand].size()>=2 || FatJet_idx[FatJet_bbCand].size()>=1", "Reco bjet candidates")

def ApplyJetSelection(df):
    return df.Filter("Jet_idx[Jet_bCand].size()>=2", "Reco bjet candidates")

def GenRecoJetMatching(df):
    df = df.Define("Jet_genJetIdx_matched", "GenRecoJetMatching(event,Jet_idx, GenJet_idx, Jet_bCand, GenJet_B2, GenJet_p4, Jet_p4 , 0.3)")
    df = df.Define("Jet_genMatched", "Jet_genJetIdx_matched>=0")
    return df.Filter("Jet_genJetIdx_matched[Jet_genMatched].size()>=2", "Two different gen-reco jet matches at least")

def GenRecoJetMatching_CCLUB(df):
    df = df.Define("Jet_genJetIdx_matched", "GenRecoJetMatching(event,Jet_idx, GenJet_idx, Jet_bCand_CCLUB, GenJet_B2, GenJet_p4, Jet_p4 , 0.3)")
    df = df.Define("Jet_genMatched", "Jet_genJetIdx_matched>=0")
    return df.Filter("Jet_genJetIdx_matched[Jet_genMatched].size()>=2", "Two different gen-reco jet matches at least")

def GenJetMatchingForBjets(df):
    """Match reconstructed b-jets (from CCLUB preselection) to generator-level b-jets.
    
    IMPORTANT: Matching is done ONLY against cleaned GenJets (GenJet_B2_p4_vec).
    These are the b-jets after removing overlap with taus, ensuring consistent matching.
    
    The matching returns:
    - bjet{1,2}_genJetIdx_matched_local: Index in GenJet_B2_p4_vec (0, 1, or -1)
    - bjet{1,2}_genJetIdx_matched: Original GenJet index (to access GenJet_pt, GenJet_eta, etc.)
    """
    # Match against cleaned b-jets (returns local index: 0, 1, or -1)
    df = df.Define("bjet1_genJetIdx_matched_local", "GenRecoJetMatchingSingle(bjet1_p4, GenJet_B2_p4_vec, 0.3)")
    df = df.Define("bjet2_genJetIdx_matched_local", "GenRecoJetMatchingSingle(bjet2_p4, GenJet_B2_p4_vec, 0.3)")
    
    # Convert to original GenJet indices (for accessing GenJet branches)
    df = df.Define("bjet1_genJetIdx_matched", "bjet1_genJetIdx_matched_local >= 0 ? GenJet_B2_indices[bjet1_genJetIdx_matched_local] : -1")
    df = df.Define("bjet2_genJetIdx_matched", "bjet2_genJetIdx_matched_local >= 0 ? GenJet_B2_indices[bjet2_genJetIdx_matched_local] : -1")
    
    df = df.Define("bjet1_genMatched", "bjet1_genJetIdx_matched >= 0")
    df = df.Define("bjet2_genMatched", "bjet2_genJetIdx_matched >= 0")
    return df.Filter("bjet1_genMatched && bjet2_genMatched", "Both bjets have gen-reco match")

def DefineHbbCand(df):
    df = df.Define("Jet_HHBtagScore", "GetHHBtagScore(Jet_bCand, Jet_idx, Jet_p4,Jet_btagDeepFlavB, MET_pt,  MET_phi, HttCandidate, period, event)")
    df = df.Define("HbbCandidate", "GetHbbCandidate(Jet_HHBtagScore, Jet_bCand, Jet_p4, Jet_idx)")
    return df

def GenRecoVBFJetMatching(df):
    """Match reconstructed VBF jets to generator-level VBF jets.
    
    NOTE: This is the legacy version that uses GenJet_VBF (before unified overlap removal).
    For proper 3-way overlap removal, use GenRecoVBFJetMatching_CCLUB with GenAllOverlapRemoval.
    """
    df = df.Define("GenRecoVBFJetMatchIdx", """GenRecoVBFJetMatching(event, Jet_idx, GenJet_idx, Jet_vbfCand, GenJet_VBF, GenJet_p4, Jet_p4, 0.3)""")
    df = df.Define("Jet_vbfgenMatched", "GenRecoVBFJetMatchIdx>=0") 
    return df.Filter("GenRecoVBFJetMatchIdx[Jet_vbfgenMatched].size()>=2", "Two different gen-reco VBF matches") # 2 VBF jets at least

def GenRecoVBFJetMatching_CCLUB(df):
    """Match reconstructed VBF jets to generator-level VBF jets (after unified overlap removal).
    
    CRITICAL: Uses GenJet_VBF2 which is the result of GenAllOverlapRemoval.
    GenJet_VBF2 contains VBF jets after removing overlaps with BOTH taus and b-jets.
    This ensures consistency in the gen-reco matching process.
    
    NOTE: For reco jets, uses Jet_vbfCand_CCLUB_noHorns (after Horns removal) if RecoJetHornsRemoval
    was applied, otherwise uses Jet_vbfCand_CCLUB.
    """
    df = df.Define("GenRecoVBFJetMatchIdx", """GenRecoVBFJetMatching(event, Jet_idx, GenJet_idx, Jet_vbfCand_CCLUB_noHorns, GenJet_VBF2, GenJet_p4, Jet_p4, 0.3)""")
    df = df.Define("Jet_vbfgenMatched", "GenRecoVBFJetMatchIdx>=0") 
    return df.Filter("GenRecoVBFJetMatchIdx[Jet_vbfgenMatched].size()>=2", "Two different gen-reco VBF matches") # 2 VBF jets at least

def DefineVBFCand(df):
    df = df.Define("VBFCand", """GetVBFJetCandidate(Jet_vbfCand, Jet_p4, Jet_idx, GenRecoVBFJetMatchIdx)""")
    return df

def DefineVBFCand_CCLUB(df):
    """Define VBF candidate from matched VBF jets.
    
    Uses Jet_vbfCand_CCLUB_noHorns (after Horns removal) if RecoJetHornsRemoval was applied.
    """
    df = df.Define("VBFCand", """GetVBFJetCandidate(Jet_vbfCand_CCLUB_noHorns, Jet_p4, Jet_idx, GenRecoVBFJetMatchIdx)""")
    return df

def DefineisCCLUBjet(df):
    df = df.Define("Jet_isCCLUBbjet", """GetIsCCLUBbjet(Jet_p4, bjet1_p4, bjet2_p4, 0.3)""")
    return df

def DefineisCCLUBvbfjet(df):
    # Create LorentzVector objects for the preselected VBF jets from input branches
    df = df.Define("vbfjet1_p4", """ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>>(vbfjet1_pt_nom, vbfjet1_eta, vbfjet1_phi, vbfjet1_mass_nom)""")
    df = df.Define("vbfjet2_p4", """ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>>(vbfjet2_pt_nom, vbfjet2_eta, vbfjet2_phi, vbfjet2_mass_nom)""")
    df = df.Define("Jet_isCCLUBvbfjet", """GetIsCCLUBvbfjet(Jet_p4, vbfjet1_p4, vbfjet2_p4, 0.3)""")
    return df

def ApplyVBFTopologicalSelection_CCLUB(df, centralJet_ptThreshold=20.0):
    """Apply VBF topological cuts for pure samples (inspired by VBF trigger thresholds)"""
    return df.Filter(f"ApplyVBFTopologicalCuts(VBFCand, Jet_p4, Jet_idx, Jet_isCCLUBbjet, {centralJet_ptThreshold})", 
                     f"VBF topological cuts (mjj>500, |Δη|>2.5, central jet veto pT>{centralJet_ptThreshold})")

def VBFTopologicalVariables_CCLUB(df, centralJet_ptThreshold=20.0):
    """Define VBF topological variables for monitoring/analysis"""
    df = df.Define("VBF_mjj", "VBFCand ? (VBFCand->leg_p4[0] + VBFCand->leg_p4[1]).M() : -1")
    # Define both signed and unsigned eta differences for complete analysis
    df = df.Define("VBF_deltaEta_signed", "VBFCand ? VBFCand->leg_p4[0].Eta() - VBFCand->leg_p4[1].Eta() : -999")
    df = df.Define("VBF_deltaEta", "VBFCand ? VBFCand->leg_p4[0].Eta() - VBFCand->leg_p4[1].Eta() : -1")
    df = df.Define("VBF_deltaPhi", "VBFCand ? ROOT::Math::VectorUtil::DeltaPhi(VBFCand->leg_p4[0], VBFCand->leg_p4[1]) : -999")
    df = df.Define("VBF_centrality_htt", """VBFCand ? 
        (dau1_eta + dau2_eta) / 2.0 - (VBFCand->leg_p4[0].Eta() + VBFCand->leg_p4[1].Eta()) / 2.0 : -999""")
    df = df.Define("VBF_centrality_hbb", """VBFCand ? 
        (bjet1_eta + bjet2_eta) / 2.0 - (VBFCand->leg_p4[0].Eta() + VBFCand->leg_p4[1].Eta()) / 2.0 : -999""")
    df = df.Define("nJets_central", f"""VBFCand ? 
        GetCentralJetMultiplicity(Jet_p4, Jet_idx, Jet_isCCLUBbjet, VBFCand->leg_p4[0], VBFCand->leg_p4[1], {centralJet_ptThreshold}, 2.5) : -1""")
    return df
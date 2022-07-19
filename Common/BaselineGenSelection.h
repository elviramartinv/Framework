#pragma once

#include "AnalysisTools.h"
#include "GenTools.h"
#include "TextIO.h"
#include "HHCore.h"

HTTCand GetGenHTTCandidate(int evt, const RVecI& GenPart_pdgId,
                           const RVecVecI& GenPart_daughters, const RVecI& GenPart_statusFlags,
                           const RVecF& GenPart_pt, const RVecF& GenPart_eta,
                           const RVecF& GenPart_phi, const RVecF& GenPart_mass)
{
  try {
    std::set<int> htt_indices;
    for(int n = 0; n < GenPart_pdgId.size(); ++n) {
        const GenStatusFlags status(GenPart_statusFlags.at(n));
        if(!(GenPart_pdgId[n] == PdG::Higgs() && status.isLastCopy())) continue;
        const auto& daughters = GenPart_daughters.at(n);
        int n_tau_daughters = std::count_if(daughters.begin(), daughters.end(), [&](int idx) {
        return std::abs(GenPart_pdgId.at(idx)) == PdG::tau();
        });
        if(n_tau_daughters == 0) continue;
        if(n_tau_daughters != 2)
        throw analysis::exception("Invalid H->tautau decay. n_tau_daughters = %1%, higgs_idx = %2%")
            % n_tau_daughters % n;
        htt_indices.insert(n);
    }
    if(htt_indices.empty())
        throw analysis::exception("H->tautau not found.");
    if(htt_indices.size() != 1)
        throw analysis::exception("Multiple H->tautau candidates.");
    const int htt_index = *htt_indices.begin();
    HTTCand htt_cand;
    int leg_idx = 0;
    for(int tau_idx : GenPart_daughters.at(htt_index)) {
        if(std::abs(GenPart_pdgId.at(tau_idx)) != PdG::tau()) continue;
        tau_idx = GetLastCopy(tau_idx, GenPart_pdgId, GenPart_statusFlags, GenPart_daughters);

        int lepton_idx = tau_idx;
        size_t n_neutrinos = 0;
        for(int tau_daughter : GenPart_daughters.at(tau_idx)) {
            if(PdG::isNeutrino(GenPart_pdgId[tau_daughter]))
                ++n_neutrinos;
            const GenStatusFlags status(GenPart_statusFlags.at(tau_daughter));
            const int tau_daughter_pdg = std::abs(GenPart_pdgId[tau_daughter]);
            if(!((tau_daughter_pdg == PdG::e() || tau_daughter_pdg == PdG::mu())
                && status.isDirectPromptTauDecayProduct())) continue;
            if(lepton_idx != tau_idx)
                throw analysis::exception("Invalid tau decay. tau_idx = %1%") % tau_idx;
            lepton_idx = tau_daughter;
        }

        if(!((lepton_idx == tau_idx && n_neutrinos == 1) || (lepton_idx != tau_idx && n_neutrinos == 2)))
            throw analysis::exception("Invalid number of neutrinos = %1% in tau decay. tau_idx = %2%")
                % n_neutrinos % tau_idx;

        lepton_idx = GetLastCopy(lepton_idx, GenPart_pdgId, GenPart_statusFlags, GenPart_daughters);
        htt_cand.leg_index.at(leg_idx) = lepton_idx;
        ++leg_idx;
    }
    int leg0_pdg = std::abs(GenPart_pdgId.at(htt_cand.leg_index.at(0)));
    int leg1_pdg = std::abs(GenPart_pdgId.at(htt_cand.leg_index.at(1)));
    if(leg0_pdg > leg1_pdg || (leg0_pdg == leg1_pdg
            && GenPart_pt.at(htt_cand.leg_index.at(0)) < GenPart_pt.at(htt_cand.leg_index.at(1))))
        std::swap(htt_cand.leg_index.at(0), htt_cand.leg_index.at(1));

    for(leg_idx = 0; leg_idx < htt_cand.leg_index.size(); ++leg_idx) {
        const int genPart_index = htt_cand.leg_index.at(leg_idx);
        const int genPart_pdg = GenPart_pdgId.at(genPart_index);
        const auto& genPart_info = ParticleDB::GetParticleInfo(genPart_pdg);
        htt_cand.leg_type[leg_idx] = PdGToLeg(genPart_pdg);
        htt_cand.leg_charge[leg_idx] = genPart_info.charge;
        htt_cand.leg_p4[leg_idx] = GetVisibleP4(genPart_index, GenPart_pdgId, GenPart_daughters,
                                                GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass);
    }

    return htt_cand;
  } catch(analysis::exception& e) {
    throw analysis::exception("GetGenHTTCandidate (event=%1%): %2%") % evt % e.message();
  }
}

bool PassGenAcceptance(const HTTCand& HTT_Cand){
    for(size_t i = 0; i < HTT_Cand.leg_p4.size(); ++i){
        if(!(HTT_Cand.leg_p4.at(i).pt()>20 && std::abs(HTT_Cand.leg_p4.at(i).eta())<2.3 )){
            return false;
        }
    }
    return true;
}


RVecB FindTwoJetsClosestToMPV(float mpv, const RVecLV& GenPart_p4, const RVecB& pre_sel,const RVecI& GenPart_pdgId, bool WantOnlySpecificParticle, int ParticleType=5){
  RVecB result(pre_sel);
  int i_min, j_min;
  float delta_min = 10000;
  for(int i =0 ; i< GenPart_p4.size(); i++){
    for(int j=0; j<i; j++){
      RVecI temporary_indices;
      temporary_indices.push_back(i);
      temporary_indices.push_back(j);
      float inv_mass = InvMassByIndices(temporary_indices, GenPart_p4 ,GenPart_pdgId,  WantOnlySpecificParticle,  ParticleType);
      float delta_mass = abs(inv_mass-mpv);
      if(delta_mass<=delta_min){
        i_min=i;
        j_min=j;
        delta_min = delta_mass;
      }
    }
  }
   const auto isAGoodIndex = [&](const int& idx){
     if(idx==i_min || idx==j_min ) return true;
     return false;
   };
  for(size_t part_idx = 0; part_idx < GenPart_p4.size(); ++part_idx) {
    result[part_idx] = pre_sel[part_idx] && isAGoodIndex(part_idx);
  } 
  return result;
}

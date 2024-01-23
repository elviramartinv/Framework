#pragma once

#include "AnalysisTools.h"
#include "GenTools.h"

template<size_t N>
struct ZTTCand {
  static constexpr size_t n_legs = N;
  std::array<Leg, n_legs> leg_type;
  std::array<int, n_legs> leg_index;
  std::array<LorentzVectorM, n_legs> leg_p4;
  std::array<int, n_legs> leg_charge;
  std::array<float, n_legs> leg_rawIso;
  std::array<int, n_legs> leg_genMatchIdx;

  ZTTCand() { leg_type.fill(Leg::none); }

  Channel channel() const { return _channel(std::make_index_sequence<n_legs>{}); }

  bool operator==(const ZTTCand& other) const
  {
    for(size_t idx = 0; idx < n_legs; ++idx) {
      if(leg_type[idx] != other.leg_type[idx] || leg_index[idx] != other.leg_index[idx])
        return false;
    }
    return true;
  }
  bool isLeg(int obj_index, Leg leg) const {
    for(size_t idx = 0; idx < n_legs; idx++){
      if(leg_type[idx] == leg && leg_index[idx]==obj_index){
        return true;
      }
    }
    return false;
  }

  RVecB isLeg(const RVecI &obj_vec, Leg leg) const {
    RVecB isLeg_vector(obj_vec.size(), false);
    for(size_t obj_idx=0; obj_idx<obj_vec.size(); obj_idx++){
      isLeg_vector[obj_idx] = isLeg(obj_vec[obj_idx], leg);
    }
    return isLeg_vector;
  }

  std::vector<LorentzVectorM> getLegP4s() const {
    std::vector<LorentzVectorM> leg_p4s;
    for(size_t idx = 0; idx < n_legs; idx++){
      if(leg_type[idx] != Leg::none){
        leg_p4s.push_back(leg_p4[idx]);
      }
    }
    return leg_p4s;
  }

  size_t nValidLegs() const {
    size_t n_valid_legs = 0;
    for(size_t idx = 0; idx < n_legs; idx++){
      if(leg_type[idx] != Leg::none){
        ++n_valid_legs;
      }
    }
    return n_valid_legs;
  }

private:
  template<size_t ...Idx>
  Channel _channel(std::index_sequence<Idx...>) const
  {
    return LegsToChannel(leg_type[Idx]...);
  }
};

struct ZbbCand {
  static constexpr size_t n_legs = 2;
  std::array<int, n_legs> leg_index;
  std::array<LorentzVectorM, n_legs> leg_p4;
};

template<size_t N>
std::ostream& operator<<(std::ostream& os, const ZTTCand<N>& cand)
{
  for(size_t n = 0; n < ZTTCand<N>::n_legs; ++n) {
    if(cand.leg_type[n] == Leg::none) continue;
    os << "leg" << n+1 << ":"
       << " type=" << static_cast<int>(cand.leg_type[n])
       << " index=" << cand.leg_index[n]
       << " (pt,eta,phi,m)=" << cand.leg_p4[n]
       << " charge=" << cand.leg_charge[n]
       << " rawIso=" << cand.leg_rawIso[n] << "\n";
  }
  return os;
}

ALL_TOOLS      += alpaka-cuda
alpaka-cuda_EX_USE := alpaka cuda
alpaka-cuda_EX_FLAGS_CXXFLAGS  := -DALPAKA_ACC_GPU_CUDA_ENABLED

ALL_TOOLS      += alpaka-serial
alpaka-serial_EX_USE := alpaka
alpaka-serial_EX_FLAGS_CXXFLAGS  := -DALPAKA_ACC_CPU_B_SEQ_T_SEQ_ENABLED

ALL_TOOLS      += alpaka-tbb
alpaka-tbb_EX_USE := alpaka tbb
alpaka-tbb_EX_FLAGS_CXXFLAGS  := -DALPAKA_ACC_CPU_B_TBB_T_SEQ_ENABLED

ALL_TOOLS      += alpaka
alpaka_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/alpaka/0.6.0-ljfedo2/include
alpaka_EX_USE := boost

ALL_TOOLS      += alpgen

ALL_TOOLS      += blackhat
blackhat_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/blackhat/0.9.9-ghbfee/include
blackhat_EX_LIB := Ampl_eval BG BH BHcore CutPart Cut_wCI Cuteval Integrals Interface OLA RatPart Rateval Spinors assembly ratext
blackhat_EX_USE := qd

ALL_TOOLS      += boost
boost_EX_LIB := boost_thread boost_date_time
boost_EX_USE := boost_header

ALL_TOOLS      += boost_chrono
boost_chrono_EX_LIB := boost_chrono
boost_chrono_EX_USE := boost_system boost

ALL_TOOLS      += boost_filesystem
boost_filesystem_EX_LIB := boost_filesystem
boost_filesystem_EX_USE := boost_system boost

ALL_TOOLS      += boost_header
boost_header_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/boost/1.75.0-ljfedo/include
boost_header_EX_USE := sockets root_cxxdefaults
boost_header_EX_FLAGS_CPPDEFINES  := -DBOOST_SPIRIT_THREADSAFE -DPHOENIX_THREADSAFE -DBOOST_MATH_DISABLE_STD_FPCLASSIFY -DBOOST_UUID_RANDOM_PROVIDER_FORCE_POSIX
boost_header_EX_FLAGS_CXXFLAGS  := -Wno-error=unused-variable
boost_header_EX_FLAGS_SYSTEM_INCLUDE  := 1

ALL_TOOLS      += boost_iostreams
boost_iostreams_EX_USE := boost

ALL_TOOLS      += boost_mpi
boost_mpi_EX_LIB := boost_mpi
boost_mpi_EX_USE := boost boost_serialization

ALL_TOOLS      += boost_program_options
boost_program_options_EX_LIB := boost_program_options
boost_program_options_EX_USE := boost

ALL_TOOLS      += boost_python
boost_python_EX_LIB := boost_python27
boost_python_EX_USE := boost_header python

ALL_TOOLS      += boost_regex
boost_regex_EX_LIB := boost_regex
boost_regex_EX_USE := boost

ALL_TOOLS      += boost_serialization
boost_serialization_EX_LIB := boost_serialization
boost_serialization_EX_USE := boost

ALL_TOOLS      += boost_system
boost_system_EX_LIB := boost_system
boost_system_EX_USE := boost

ALL_TOOLS      += boost_test
boost_test_EX_LIB := boost_unit_test_framework
boost_test_EX_USE := boost

ALL_TOOLS      += bz2lib
bz2lib_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/bz2lib/1.0.6-bcolbf2/include
bz2lib_EX_LIB := bz2
bz2lib_EX_USE := root_cxxdefaults

ALL_TOOLS      += cascade
cascade_EX_LIB := cascade_merged
cascade_EX_USE := f77compiler cascade_headers

ALL_TOOLS      += cascade_headers
cascade_headers_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/cascade/2.2.04-ljfedo2/include
cascade_headers_EX_USE := root_cxxdefaults

ALL_TOOLS      += catch2
catch2_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/catch2/2.2.2-bcolbf/include

ALL_TOOLS      += ccache-ccompiler
ccache-ccompiler_EX_USE := gcc-ccompiler

ALL_TOOLS      += ccache-cxxcompiler
ccache-cxxcompiler_EX_USE := gcc-cxxcompiler

ALL_TOOLS      += ccache-f77compiler
ccache-f77compiler_EX_USE := gcc-f77compiler

ALL_TOOLS      += cgal
cgal_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/cgal/4.2-ljfedo4/include
cgal_EX_LIB := CGAL_Core CGAL
cgal_EX_USE := root_cxxdefaults zlib boost_system gmp mpfr

ALL_TOOLS      += cgalimageio
cgalimageio_EX_LIB := CGAL_ImageIO
cgalimageio_EX_USE := zlib boost_system cgal

ALL_TOOLS      += charybdis
charybdis_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/charybdis/1.003-ljfedo2/include
charybdis_EX_LIB := charybdis
charybdis_EX_USE := root_cxxdefaults f77compiler herwig pythia6

ALL_TOOLS      += classlib
classlib_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/classlib/3.1.3-ghbfee/include
classlib_EX_LIB := classlib
classlib_EX_USE := pcre root_cxxdefaults
classlib_EX_FLAGS_CPPDEFINES  := -D__STDC_LIMIT_MACROS -D__STDC_FORMAT_MACROS

ALL_TOOLS      += clhep
clhep_EX_LIB := CLHEP
clhep_EX_USE := clhepheader

ALL_TOOLS      += clhepheader
clhepheader_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/clhep/2.4.4.0-ljfedo/include
clhepheader_EX_USE := root_cxxdefaults
clhepheader_EX_FLAGS_ROOTCLING_ARGS  := -moduleMapFile=$(CLHEP_BASE)/include/module.modulemap
clhepheader_EX_FLAGS_SYSTEM_INCLUDE  := 1

ALL_TOOLS      += cmsswdata
cmsswdata_EX_FLAGS_CMSSW_DATA_PACKAGE  := Alignment/OfflineValidation=V00-01-00 CalibCalorimetry/CaloMiscalibTools=V01-00-00 CalibCalorimetry/EcalTrivialCondModules=V00-03-00 CalibPPS/ESProducers=V01-03-00 CalibTracker/SiPixelESProducers=V02-02-00 CalibTracker/SiStripDCS=V01-00-00 Calibration/Tools=V01-00-00 CondFormats/JetMETObjects=V01-00-03 CondTools/SiPhase2Tracker=V00-01-00 Configuration/Generator=V01-02-00 DQM/DTMonitorClient=V00-01-00 DQM/PhysicsHWW=V01-00-00 DQM/SiStripMonitorClient=V01-01-00 DataFormats/PatCandidates=V01-00-01 DetectorDescription/Schema=V02-02-01 EgammaAnalysis/ElectronTools=V00-03-01 EventFilter/L1TRawToDigi=V01-00-00 FWCore/Modules=V00-01-00 FastSimulation/MaterialEffects=V05-00-00 FastSimulation/TrackingRecHitProducer=V01-00-03 Fireworks/Geometry=V07-06-00 GeneratorInterface/EvtGenInterface=V02-03-00 GeneratorInterface/ReggeGribovPartonMCInterface=V00-00-02 Geometry/DTGeometryBuilder=V00-01-00 Geometry/TestReference=V00-08-00 HLTrigger/JetMET=V01-00-00 HeterogeneousCore/SonicTriton=V00-01-00 IOPool/Input=V00-01-00 L1Trigger/CSCTriggerPrimitives=V00-05-00 L1Trigger/DTTriggerPhase2=V00-01-00 L1Trigger/L1TCalorimeter=V01-01-00 L1Trigger/L1TGlobal=V00-00-07 L1Trigger/L1THGCal=V01-04-00 L1Trigger/L1TMuon=V01-05-00 L1Trigger/Phase2L1ParticleFlow=V00-03-00 L1Trigger/RPCTrigger=V00-15-00 L1Trigger/TrackFindingTMTT=V00-02-00 L1Trigger/TrackFindingTracklet=V00-01-00 L1Trigger/TrackTrigger=V00-01-00 MagneticField/Engine=V00-01-00 MagneticField/Interpolation=V01-01-00 PhysicsTools/NanoAOD=V01-01-00 PhysicsTools/PatUtils=V00-02-00 RecoBTag/CTagging=V01-00-03 RecoBTag/Combined=V01-10-00 RecoBTag/SecondaryVertex=V02-00-04 RecoBTag/SoftLepton=V01-00-01 RecoCTPPS/TotemRPLocal=V00-02-00 RecoEgamma/ElectronIdentification=V01-04-00 RecoEgamma/PhotonIdentification=V01-00-06 RecoHGCal/TICL=V00-02-01 RecoHI/HiJetAlgos=V01-00-01 RecoJets/JetProducers=V05-13-00 RecoLocalCalo/EcalDeadChannelRecoveryAlgos=V01-01-00 RecoMET/METPUSubtraction=V01-01-00 RecoMTD/TimingIDTools=V00-01-00 RecoMuon/MuonIdentification=V01-12-05 RecoMuon/TrackerSeedGenerator=V00-01-00 RecoParticleFlow/PFBlockProducer=V02-04-02 RecoParticleFlow/PFProducer=V16-01-00 RecoParticleFlow/PFTracking=V13-01-00 RecoTauTag/TrainingFiles=V00-02-00 RecoTracker/FinalTrackSelectors=V01-01-00 RecoTracker/TkSeedGenerator=V00-02-00 SLHCUpgradeSimulations/Geometry=V01-00-10 SimG4CMS/Calo=V03-01-00 SimG4CMS/Forward=V02-04-00 SimG4CMS/HGCalTestBeam=V01-00-00 SimPPS/PPSPixelDigiProducer=V00-00-02 SimTracker/SiStripDigitizer=V01-01-00 SimTransport/HectorProducer=V01-00-01 SimTransport/PPSProtonTransport=V00-02-00 SimTransport/TotemRPProtonTransportParametrization=V00-01-00 Validation/Geometry=V00-07-00

ALL_TOOLS      += coral
ALL_SCRAM_PROJECTS += coral
coral_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/coral/CORAL_2_3_21-ljfedo7/include/LCG
coral_EX_USE := root_cxxdefaults
coral_ORDER := 98000

ALL_TOOLS      += cppunit
cppunit_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/cppunit/1.15.x-bcolbf2/include
cppunit_EX_LIB := cppunit
cppunit_EX_USE := root_cxxdefaults sockets

ALL_TOOLS      += csctrackfinderemulation
csctrackfinderemulation_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/CSCTrackFinderEmulation/1.2-bcolbf/include
csctrackfinderemulation_EX_LIB := CSCTrackFinderEmulation

ALL_TOOLS      += cuda-cublas
cuda-cublas_EX_LIB := cublas cublasLt
cuda-cublas_EX_USE := cuda

ALL_TOOLS      += cuda-cufft
cuda-cufft_EX_LIB := cufft cufftw
cuda-cufft_EX_USE := cuda

ALL_TOOLS      += cuda-curand
cuda-curand_EX_LIB := curand
cuda-curand_EX_USE := cuda

ALL_TOOLS      += cuda-cusolver
cuda-cusolver_EX_LIB := cusolver cusolverMg
cuda-cusolver_EX_USE := cuda

ALL_TOOLS      += cuda-cusparse
cuda-cusparse_EX_LIB := cusparse
cuda-cusparse_EX_USE := cuda

ALL_TOOLS      += cuda-gcc-support

ALL_TOOLS      += cuda-npp
cuda-npp_EX_LIB := nppial nppicc nppidei nppif nppig nppim nppist nppisu nppitc npps nppc
cuda-npp_EX_USE := cuda

ALL_TOOLS      += cuda-nvgraph
cuda-nvgraph_EX_LIB := nvgraph
cuda-nvgraph_EX_USE := cuda

ALL_TOOLS      += cuda-nvjpeg
cuda-nvjpeg_EX_LIB := nvjpeg
cuda-nvjpeg_EX_USE := cuda

ALL_TOOLS      += cuda-nvml
cuda-nvml_EX_LIB := nvidia-ml
cuda-nvml_EX_USE := cuda-stubs

ALL_TOOLS      += cuda-nvrtc
cuda-nvrtc_EX_LIB := nvrtc
cuda-nvrtc_EX_USE := cuda

ALL_TOOLS      += cuda-stubs
cuda-stubs_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/cuda/11.2.2/include
cuda-stubs_EX_LIB := cuda
cuda-stubs_EX_LIBDIR := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/cuda/11.2.2/lib64/stubs
cuda-stubs_EX_FLAGS_SKIP_TOOL_SYMLINKS  := 1

ALL_TOOLS      += cuda
ALL_LIB_TYPES += CUDA_LIB
cuda_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/cuda/11.2.2/include
cuda_EX_LIB := cudart cudadevrt nvToolsExt
cuda_EX_CUDA_LIB := cudadevrt
cuda_EX_USE := cuda-stubs
cuda_EX_FLAGS_CUDA_FLAGS  := -std=c++17 -O3 --generate-line-info --source-in-ptx --display-error-number --expt-relaxed-constexpr --extended-lambda -gencode arch=compute_60,code=[sm_60,compute_60] -gencode arch=compute_70,code=[sm_70,compute_70] -gencode arch=compute_75,code=[sm_75,compute_75] -Wno-deprecated-gpu-targets -Xcudafe --diag_suppress=esa_on_defaulted_function_ignored --cudart shared
cuda_EX_FLAGS_CUDA_HOST_CXXFLAGS  := -std=c++17
cuda_EX_FLAGS_CUDA_HOST_REM_CXXFLAGS  := -std=% %potentially-evaluated-expression

ALL_TOOLS      += cudnn
cudnn_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/cudnn/8.1.1.33/include
cudnn_EX_LIB := cudnn
cudnn_EX_USE := cuda

ALL_TOOLS      += cupla-cuda
cupla-cuda_EX_LIB := cupla-cuda
cupla-cuda_EX_USE := cupla cuda
cupla-cuda_EX_FLAGS_CXXFLAGS  := -DALPAKA_ACC_GPU_CUDA_ENABLED -DCUPLA_STREAM_ASYNC_ENABLED=1

ALL_TOOLS      += cupla-serial
cupla-serial_EX_LIB := cupla-serial
cupla-serial_EX_USE := cupla
cupla-serial_EX_FLAGS_CXXFLAGS  := -DALPAKA_ACC_CPU_B_SEQ_T_SEQ_ENABLED -DCUPLA_STREAM_ASYNC_ENABLED=0

ALL_TOOLS      += cupla-tbb
cupla-tbb_EX_LIB := cupla-tbb
cupla-tbb_EX_USE := cupla tbb
cupla-tbb_EX_FLAGS_CXXFLAGS  := -DALPAKA_ACC_CPU_B_TBB_T_SEQ_ENABLED -DCUPLA_STREAM_ASYNC_ENABLED=1

ALL_TOOLS      += cupla
cupla_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/cupla/0.3.0-dev-ljfedo5/include
cupla_EX_USE := boost

ALL_TOOLS      += cupti
cupti_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/cuda/11.2.2/include
cupti_EX_LIB := cupti

ALL_TOOLS      += curl
curl_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/curl/7.70.0/include
curl_EX_LIB := curl
curl_EX_USE := root_cxxdefaults

ALL_TOOLS      += cvs2git

ALL_TOOLS      += dablooms
dablooms_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/dablooms/0.9.1-bcolbf/include
dablooms_EX_LIB := dablooms

ALL_TOOLS      += das_client
das_client_EX_USE := python

ALL_TOOLS      += davix
davix_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/davix/0.7.6/include/davix
davix_EX_LIB := davix
davix_EX_USE := boost_system openssl libxml2

ALL_TOOLS      += db6
db6_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/db6/6.2.32-bcolbf/include
db6_EX_LIB := db

ALL_TOOLS      += dcap
dcap_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/dcap/2.47.12-bcolbf2/include
dcap_EX_LIB := dcap
dcap_EX_USE := root_cxxdefaults

ALL_TOOLS      += dd4hep-core
dd4hep-core_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/dd4hep/v01-16-01-ljfedo/include
dd4hep-core_EX_LIB := DDCore DDParsers
dd4hep-core_EX_USE := root_cxxdefaults root boost xerces-c clhep
dd4hep-core_EX_FLAGS_CPPDEFINES  := -DDD4HEP_USE_GEANT4_UNITS=1
dd4hep-core_EX_FLAGS_LISTCOMPONENTS  := $(DD4HEP_CORE_BASE)/bin/listcomponents_dd4hep

ALL_TOOLS      += dd4hep-geant4
dd4hep-geant4_EX_LIB := DDG4-static
dd4hep-geant4_EX_USE := geant4core dd4hep-core

ALL_TOOLS      += dd4hep
dd4hep_EX_LIB := DDAlign DDCond
dd4hep_EX_USE := dd4hep-core

ALL_TOOLS      += dip-platform-dependent
dip-platform-dependent_EX_LIB := platform-dependent
dip-platform-dependent_EX_USE := dip_interface

ALL_TOOLS      += dip
dip_EX_LIB := dip
dip_EX_USE := dip-platform-dependent log4cplus

ALL_TOOLS      += dip_interface
dip_interface_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/dip/8693f00cc422b4a15858fcd84249acaeb07b6316-ljfedo/include

ALL_TOOLS      += distcc-ccompiler
distcc-ccompiler_EX_USE := gcc-ccompiler

ALL_TOOLS      += distcc-cxxcompiler
distcc-cxxcompiler_EX_USE := gcc-cxxcompiler

ALL_TOOLS      += distcc-f77compiler
distcc-f77compiler_EX_USE := gcc-f77compiler

ALL_TOOLS      += dmtcp

ALL_TOOLS      += doxygen

ALL_TOOLS      += dpm
dpm_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/dpm/1.8.0.1-ghbfee/include
dpm_EX_LIB := dpm
dpm_EX_LIBDIR := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/dpm/1.8.0.1-ghbfee/lib
dpm_EX_USE := root_cxxdefaults

ALL_TOOLS      += eigen
eigen_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/eigen/011e0db31d1bed8b7f73662be6d57d9f30fa457a/include/eigen3
eigen_EX_FLAGS_CPPDEFINES  := -DEIGEN_DONT_PARALLELIZE
eigen_EX_FLAGS_CUDA_FLAGS  := --diag-suppress 20014

ALL_TOOLS      += evtgen
evtgen_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/evtgen/2.0.0-ljfedo3/include
evtgen_EX_LIB := EvtGen EvtGenExternal
evtgen_EX_USE := hepmc pythia8 tauolapp photospp

ALL_TOOLS      += expat
expat_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/expat/2.1.0-bcolbf2/include
expat_EX_LIB := expat
expat_EX_USE := root_cxxdefaults

ALL_TOOLS      += fastjet-contrib-archive
fastjet-contrib-archive_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/fastjet-contrib/1.044-ljfedo/include
fastjet-contrib-archive_EX_LIB := EnergyCorrelator GenericSubtractor JetCleanser JetFFMoments Nsubjettiness ScJet SubjetCounting VariableR

ALL_TOOLS      += fastjet-contrib
fastjet-contrib_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/fastjet-contrib/1.044-ljfedo/include
fastjet-contrib_EX_LIB := fastjetcontribfragile

ALL_TOOLS      += fastjet
fastjet_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/fastjet/3.4.0-beta/include
fastjet_EX_LIB := fastjetplugins fastjettools siscone siscone_spherical fastjet
fastjet_EX_USE := root_cxxdefaults

ALL_TOOLS      += fftjet
fftjet_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/fftjet/1.5.0-bcolbf3/include
fftjet_EX_LIB := fftjet
fftjet_EX_USE := root_cxxdefaults

ALL_TOOLS      += fftw3
fftw3_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/fftw3/3.3.8-bcolbf/include
fftw3_EX_LIB := fftw3
fftw3_EX_USE := root_cxxdefaults

ALL_TOOLS      += flatbuffers
flatbuffers_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/flatbuffers/1.12.0/include
flatbuffers_EX_LIB := flatbuffers

ALL_TOOLS      += fmt
fmt_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/fmt/7.0.1/include
fmt_EX_LIB := fmt

ALL_TOOLS      += freetype
freetype_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/freetype/2.10.0-bcolbf3/include
freetype_EX_LIB := freetype-cms
freetype_EX_USE := root_cxxdefaults

ALL_TOOLS      += frontier_client
frontier_client_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/frontier_client/2.9.1-ghbfee/include
frontier_client_EX_LIB := frontier_client
frontier_client_EX_USE := root_cxxdefaults zlib openssl expat python

ALL_TOOLS      += gbl
gbl_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/gbl/V02-01-03-ljfedo/include
gbl_EX_LIB := GBL
gbl_EX_USE := eigen

ALL_TOOLS      += gcc-atomic
gcc-atomic_EX_LIB := atomic

ALL_TOOLS      += gcc-ccompiler
gcc-ccompiler_EX_FLAGS_CFLAGS  := -O2 -pthread
gcc-ccompiler_EX_FLAGS_CSHAREDOBJECTFLAGS  := -fPIC

ALL_TOOLS      += gcc-cxxcompiler
gcc-cxxcompiler_EX_FLAGS_CPPDEFINES  := -DGNU_GCC -D_GNU_SOURCE
gcc-cxxcompiler_EX_FLAGS_CXXFLAGS  := -O2 -pthread -pipe -Werror=main -Werror=pointer-arith -Werror=overlength-strings -Wno-vla -Werror=overflow -std=c++1z -ftree-vectorize -Wstrict-overflow -Werror=array-bounds -Werror=format-contains-nul -Werror=type-limits -fvisibility-inlines-hidden -fno-math-errno --param vect-max-version-for-alias-checks=50 -Xassembler --compress-debug-sections -msse3 -felide-constructors -fmessage-length=0 -Wall -Wno-non-template-friend -Wno-long-long -Wreturn-type -Wextra -Wpessimizing-move -Wclass-memaccess -Wno-cast-function-type -Wno-unused-but-set-parameter -Wno-ignored-qualifiers -Wno-deprecated-copy -Wno-unused-parameter -Wunused -Wparentheses -Wno-deprecated -Werror=return-type -Werror=missing-braces -Werror=unused-value -Werror=unused-label -Werror=address -Werror=format -Werror=sign-compare -Werror=write-strings -Werror=delete-non-virtual-dtor -Werror=strict-aliasing -Werror=narrowing -Werror=unused-but-set-variable -Werror=reorder -Werror=unused-variable -Werror=conversion-null -Werror=return-local-addr -Wnon-virtual-dtor -Werror=switch -fdiagnostics-show-option -Wno-unused-local-typedefs -Wno-attributes -Wno-psabi
gcc-cxxcompiler_EX_FLAGS_CXXSHAREDFLAGS  := -shared -Wl,-E
gcc-cxxcompiler_EX_FLAGS_CXXSHAREDOBJECTFLAGS  := -fPIC
gcc-cxxcompiler_EX_FLAGS_LDFLAGS  := -Wl,-E -Wl,--hash-style=gnu
gcc-cxxcompiler_EX_FLAGS_LD_UNIT  := -r -z muldefs

ALL_TOOLS      += gcc-f77compiler
gcc-f77compiler_EX_LIB := gfortran m
gcc-f77compiler_EX_FLAGS_FFLAGS  := -fno-second-underscore -Wunused -Wuninitialized -O2 -cpp -std=legacy
gcc-f77compiler_EX_FLAGS_FOPTIMISEDFLAGS  := -O2
gcc-f77compiler_EX_FLAGS_FSHAREDOBJECTFLAGS  := -fPIC

ALL_TOOLS      += gcc-plugin
gcc-plugin_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/gcc/9.3.0/lib/gcc/x86_64-unknown-linux-gnu/9.3.0/plugin/include
gcc-plugin_EX_LIB := cc1plugin cp1plugin

ALL_TOOLS      += gdb

ALL_TOOLS      += gdbm
gdbm_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/gdbm/1.10-bcolbf2/include
gdbm_EX_LIB := gdbm
gdbm_EX_USE := root_cxxdefaults

ALL_TOOLS      += gdrcopy
gdrcopy_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/gdrcopy/2.1-ljfedo2/include
gdrcopy_EX_LIB := gdrapi

ALL_TOOLS      += geant4-parfullcms

ALL_TOOLS      += geant4
geant4_EX_USE := geant4core geant4vis

ALL_TOOLS      += geant4core
geant4core_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/geant4/10.7.1-ljfedo2/include/Geant4 /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/geant4/10.7.1-ljfedo2/include
geant4core_EX_LIB := G4digits_hits G4error_propagation G4event G4geometry G4global G4graphics_reps G4intercoms G4interfaces G4materials G4parmodels G4particles G4persistency G4physicslists G4processes G4readout G4run G4tracking G4track G4analysis
geant4core_EX_USE := clhep vecgeom zlib expat xerces-c root_cxxdefaults
geant4core_EX_FLAGS_CPPDEFINES  := -DGNU_GCC -DG4V9
geant4core_EX_FLAGS_CXXFLAGS  := -ftls-model=global-dynamic -pthread

ALL_TOOLS      += geant4data

ALL_TOOLS      += geant4static
geant4static_EX_LIB := geant4-static
geant4static_EX_USE := clhep vecgeom zlib expat xerces-c
geant4static_EX_FLAGS_CXXFLAGS  := -ftls-model=global-dynamic -pthread

ALL_TOOLS      += geant4vis
geant4vis_EX_LIB := G4FR G4modeling G4RayTracer G4Tree G4visHepRep G4vis_management G4visXXX G4VRML G4GMocren
geant4vis_EX_USE := geant4core

ALL_TOOLS      += giflib
giflib_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/giflib/5.2.0-bcolbf2/include
giflib_EX_LIB := gif
giflib_EX_USE := root_cxxdefaults

ALL_TOOLS      += git

ALL_TOOLS      += glibc

ALL_TOOLS      += glimpse

ALL_TOOLS      += gmake

ALL_TOOLS      += gmp
gmp_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/gmp-static/6.2.0/include
gmp_EX_LIB := gmp
gmp_EX_USE := mpfr

ALL_TOOLS      += gnuplot

ALL_TOOLS      += google-benchmark-main
google-benchmark-main_EX_LIB := benchmark_main
google-benchmark-main_EX_USE := google-benchmark

ALL_TOOLS      += google-benchmark
google-benchmark_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/google-benchmark/1.4.x-ljfedo/include
google-benchmark_EX_LIB := benchmark
google-benchmark_EX_USE := sockets

ALL_TOOLS      += gosam

ALL_TOOLS      += gosamcontrib
gosamcontrib_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/gosamcontrib/2.0-20150803-bcolbf2/include

ALL_TOOLS      += graphviz
graphviz_EX_USE := expat zlib libjpeg-turbo libpng

ALL_TOOLS      += grpc
grpc_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/grpc/1.35.0-ljfedo2/include
grpc_EX_LIB := grpc grpc++ grpc++_reflection
grpc_EX_USE := protobuf openssl pcre
grpc_EX_FLAGS_SYSTEM_INCLUDE  := 1

ALL_TOOLS      += gsl
gsl_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/gsl/2.6-ljfedo/include
gsl_EX_LIB := gsl
gsl_EX_USE := openblas root_cxxdefaults

ALL_TOOLS      += hdf5
hdf5_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/hdf5/1.10.6-ljfedo3/include
hdf5_EX_LIB := hdf5 hdf5_hl
hdf5_EX_USE := openmpi

ALL_TOOLS      += hector
hector_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/hector/1.3.4_patch1-ljfedo5/include
hector_EX_LIB := Hector
hector_EX_USE := root_cxxdefaults

ALL_TOOLS      += hepmc
hepmc_EX_LIB := HepMCfio HepMC
hepmc_EX_USE := hepmc_headers

ALL_TOOLS      += hepmc_headers
hepmc_headers_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/hepmc/2.06.10-ljfedo/include
hepmc_headers_EX_USE := root_cxxdefaults

ALL_TOOLS      += heppdt
heppdt_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/heppdt/3.04.01-ljfedo/include
heppdt_EX_LIB := HepPDT HepPID
heppdt_EX_USE := root_cxxdefaults

ALL_TOOLS      += herwig
herwig_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/herwig/6.521-ljfedo2/include
herwig_EX_LIB := herwig herwig_dummy
herwig_EX_USE := root_cxxdefaults f77compiler lhapdf photos

ALL_TOOLS      += herwig7
herwig7_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/herwig7/7.2.2-ljfedo2/include
herwig7_EX_LIB := HerwigAPI
herwig7_EX_USE := root_cxxdefaults lhapdf thepeg madgraph5amcatnlo openloops

ALL_TOOLS      += highfive
highfive_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/highfive/2.0-ljfedo4/include
highfive_EX_USE := boost hdf5

ALL_TOOLS      += histfactory
histfactory_EX_LIB := HistFactory
histfactory_EX_USE := roofitcore roofit roostats rootcore roothistmatrix rootgpad rootxml rootfoam

ALL_TOOLS      += hls
hls_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/hls/2019.08-bcolbf/include
hls_EX_USE := root_cxxdefaults
hls_EX_FLAGS_SYSTEM_INCLUDE  := 1

ALL_TOOLS      += hwloc
hwloc_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/hwloc/2.4.0-ljfedo2/include/hwloc
hwloc_EX_LIB := hwloc

ALL_TOOLS      += hydjet
hydjet_EX_LIB := hydjet
hydjet_EX_USE := pyquen pythia6 lhapdf

ALL_TOOLS      += igprof

ALL_TOOLS      += intel-license

ALL_TOOLS      += ittnotify
ittnotify_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/ittnotify/16.06.18-ghbfee/include
ittnotify_EX_LIB := ittnotify

ALL_TOOLS      += iwyu-cxxcompiler
iwyu-cxxcompiler_EX_USE := llvm-cxxcompiler

ALL_TOOLS      += jemalloc
jemalloc_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/jemalloc/5.2.1-ghbfee3/include
jemalloc_EX_LIB := jemalloc
jemalloc_EX_USE := root_cxxdefaults

ALL_TOOLS      += jimmy
jimmy_EX_LIB := jimmy
jimmy_EX_USE := f77compiler herwig jimmy_headers

ALL_TOOLS      += jimmy_headers
jimmy_headers_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/jimmy/4.2-ljfedo2/include
jimmy_headers_EX_USE := root_cxxdefaults

ALL_TOOLS      += json
json_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/json/3.7.3/include

ALL_TOOLS      += ktjet
ktjet_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/ktjet/1.06-ljfedo/include
ktjet_EX_LIB := KtEvent
ktjet_EX_USE := root_cxxdefaults
ktjet_EX_FLAGS_CPPDEFINES  := -DKTDOUBLEPRECISION

ALL_TOOLS      += lcov

ALL_TOOLS      += lhapdf
lhapdf_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/lhapdf/6.2.3-ljfedo2/include
lhapdf_EX_LIB := LHAPDF
lhapdf_EX_USE := yaml-cpp root_cxxdefaults

ALL_TOOLS      += libffi
libffi_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/libffi/3.2.1-bcolbf/include
libffi_EX_LIB := ffi

ALL_TOOLS      += libjpeg-turbo
libjpeg-turbo_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/libjpeg-turbo/2.0.2-ghbfee/include
libjpeg-turbo_EX_LIB := jpeg turbojpeg
libjpeg-turbo_EX_USE := root_cxxdefaults

ALL_TOOLS      += libpciaccess
libpciaccess_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/libpciaccess/0.16/include
libpciaccess_EX_LIB := libpciaccess

ALL_TOOLS      += libpng
libpng_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/libpng/1.6.37-bcolbf2/include
libpng_EX_LIB := png
libpng_EX_USE := root_cxxdefaults zlib

ALL_TOOLS      += libtiff
libtiff_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/libtiff/4.0.10-ghbfee/include
libtiff_EX_LIB := tiff
libtiff_EX_USE := root_cxxdefaults libjpeg-turbo zlib

ALL_TOOLS      += libungif
libungif_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/libungif/4.1.4-bcolbf2/include
libungif_EX_LIB := ungif
libungif_EX_USE := root_cxxdefaults zlib

ALL_TOOLS      += libunwind
libunwind_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/libunwind/1.4.0/include
libunwind_EX_LIB := unwind
libunwind_EX_USE := root_cxxdefaults

ALL_TOOLS      += libuuid
libuuid_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/libuuid/2.34-bcolbf2/include
libuuid_EX_LIB := uuid
libuuid_EX_USE := root_cxxdefaults sockets

ALL_TOOLS      += libxml2
libxml2_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/libxml2/2.9.10/include/libxml2
libxml2_EX_LIB := xml2
libxml2_EX_USE := root_cxxdefaults

ALL_TOOLS      += libxslt
libxslt_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/libxslt/1.1.28-bcolbf2/include/libxslt
libxslt_EX_LIB := xslt

ALL_TOOLS      += llvm-analyzer-ccompiler
llvm-analyzer-ccompiler_EX_USE := llvm-ccompiler

ALL_TOOLS      += llvm-analyzer-cxxcompiler
llvm-analyzer-cxxcompiler_EX_USE := llvm-cxxcompiler

ALL_TOOLS      += llvm-ccompiler
llvm-ccompiler_EX_USE := gcc-ccompiler

ALL_TOOLS      += llvm-cxxcompiler
llvm-cxxcompiler_EX_USE := gcc-cxxcompiler
llvm-cxxcompiler_EX_FLAGS_CXXFLAGS  := -Wno-c99-extensions -Wno-c++11-narrowing -D__STRICT_ANSI__ -Wno-unused-private-field -Wno-unknown-pragmas -Wno-unused-command-line-argument -Wno-unknown-warning-option -ftemplate-depth=512 -Wno-error=potentially-evaluated-expression -Wno-tautological-type-limit-compare -fsized-deallocation
llvm-cxxcompiler_EX_FLAGS_REM_CXXFLAGS  := -Wno-non-template-friend -Werror=format-contains-nul -Werror=maybe-uninitialized -Werror=unused-but-set-variable -Werror=return-local-addr -fipa-pta -frounding-math -mrecip -fno-crossjumping -fno-aggressive-loop-optimizations -mlong-double-64 -funroll-all-loops

ALL_TOOLS      += llvm-f77compiler
llvm-f77compiler_EX_USE := gcc-f77compiler

ALL_TOOLS      += llvm
llvm_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/llvm/11.1.0-llifpc/include
llvm_EX_LIB := clang
llvm_EX_FLAGS_CXXFLAGS  := -D_DEBUG -D_GNU_SOURCE -D__STDC_CONSTANT_MACROS -D__STDC_FORMAT_MACROS -D__STDC_LIMIT_MACROS -O3 -fomit-frame-pointer -fPIC -Wno-enum-compare -Wno-strict-aliasing -fno-rtti
llvm_EX_FLAGS_LDFLAGS  := -Wl,-undefined -Wl,suppress

ALL_TOOLS      += log4cplus
log4cplus_EX_LIB := log4cplus
log4cplus_EX_USE := dip_interface

ALL_TOOLS      += lwtnn
lwtnn_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/lwtnn/2.10-ljfedo4/include
lwtnn_EX_LIB := lwtnn
lwtnn_EX_USE := root_cxxdefaults eigen boost_system

ALL_TOOLS      += lz4
lz4_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/lz4/1.9.2/include
lz4_EX_LIB := lz4
lz4_EX_USE := root_cxxdefaults

ALL_TOOLS      += madgraph5amcatnlo
madgraph5amcatnlo_EX_USE := root_cxxdefaults gosamcontrib

ALL_TOOLS      += mctester
mctester_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/mctester/1.25.0a-ljfedo5/include
mctester_EX_LIB := HEPEvent HepMCEvent MCTester
mctester_EX_USE := root_cxxdefaults root hepmc

ALL_TOOLS      += md5
md5_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/md5/1.0.0-bcolbf2/include
md5_EX_LIB := cms-md5

ALL_TOOLS      += meschach
meschach_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/meschach/1.2.pCMS1-bcolbf2/include
meschach_EX_LIB := meschach
meschach_EX_USE := root_cxxdefaults

ALL_TOOLS      += millepede
millepede_EX_USE := sockets pcre zlib

ALL_TOOLS      += mkfit
mkfit_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/mkfit/2.1.0-ljfedo/include
mkfit_EX_LIB := MicCore MkFit
mkfit_EX_USE := tbb

ALL_TOOLS      += mpfr
mpfr_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/mpfr-static/4.0.2-bcolbf2/include
mpfr_EX_LIB := mpfr

ALL_TOOLS      += mxnet-predict
mxnet-predict_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/mxnet-predict/1.6.0-ljfedo2/include
mxnet-predict_EX_LIB := mxnet
mxnet-predict_EX_USE := openblas
mxnet-predict_EX_FLAGS_SYSTEM_INCLUDE  := 1

ALL_TOOLS      += numactl
numactl_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/numactl/2.0.14/include
numactl_EX_LIB := numa

ALL_TOOLS      += numpy-c-api
numpy-c-api_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/py2-numpy/1.16.6-ljfedo2/c-api/core/include
numpy-c-api_EX_LIB := npymath
numpy-c-api_EX_USE := root_cxxdefaults

ALL_TOOLS      += nvperf
nvperf_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/cuda/11.2.2/include
nvperf_EX_LIB := nvperf_host nvperf_target

ALL_TOOLS      += ofast-flag
ofast-flag_EX_FLAGS_CXXFLAGS  := -Ofast
ofast-flag_EX_FLAGS_NO_RECURSIVE_EXPORT  := 1

ALL_TOOLS      += onnxruntime
onnxruntime_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/onnxruntime/1.7.2/include
onnxruntime_EX_LIB := onnxruntime
onnxruntime_EX_USE := protobuf cuda cudnn

ALL_TOOLS      += openblas
openblas_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/OpenBLAS/0.3.9-ljfedo/include
openblas_EX_LIB := openblas

ALL_TOOLS      += opencv
opencv_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/opencv/4.5.1/include
opencv_EX_LIB := opencv_core
opencv_EX_USE := libpng libjpeg-turbo zlib eigen openblas

ALL_TOOLS      += opengl
opengl_EX_LIB := GL GLU
opengl_EX_USE := x11

ALL_TOOLS      += openldap
openldap_EX_USE := openssl db6

ALL_TOOLS      += openloops

ALL_TOOLS      += openmpi
openmpi_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/openmpi/4.1.0-ljfedo2/include
openmpi_EX_LIB := mpi mpi_cxx

ALL_TOOLS      += openssl
openssl_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/openssl/1.0.2d-bcolbf/include
openssl_EX_LIB := ssl crypto
openssl_EX_USE := root_cxxdefaults

ALL_TOOLS      += oracle
oracle_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/oracle/12.1.0.2.0-bcolbf/include
oracle_EX_LIB := clntsh
oracle_EX_USE := root_cxxdefaults sockets

ALL_TOOLS      += oracleocci
oracleocci_EX_LIB := occi
oracleocci_EX_USE := oracle

ALL_TOOLS      += pacparser
pacparser_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/pacparser/1.3.5-bcolbf/include
pacparser_EX_LIB := pacparser
pacparser_EX_USE := root_cxxdefaults

ALL_TOOLS      += pcre
pcre_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/pcre/8.43-bcolbf/include
pcre_EX_LIB := pcre
pcre_EX_USE := root_cxxdefaults zlib bz2lib

ALL_TOOLS      += photos
photos_EX_LIB := photos
photos_EX_USE := photos_headers f77compiler

ALL_TOOLS      += photos_headers
photos_headers_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/photos/215.5-bcolbf/include
photos_headers_EX_USE := root_cxxdefaults

ALL_TOOLS      += photospp
photospp_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/photospp/3.64-ljfedo/include
photospp_EX_LIB := Photospp PhotosppHepMC PhotosppHEPEVT
photospp_EX_USE := hepmc

ALL_TOOLS      += professor

ALL_TOOLS      += professor2
professor2_EX_USE := py2-numpy py2-sympy root yoda eigen

ALL_TOOLS      += protobuf
protobuf_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/protobuf/3.15.1-ljfedo/include
protobuf_EX_LIB := protobuf
protobuf_EX_USE := root_cxxdefaults

ALL_TOOLS      += py2-absl-py

ALL_TOOLS      += py2-appdirs

ALL_TOOLS      += py2-argon2-cffi

ALL_TOOLS      += py2-argparse

ALL_TOOLS      += py2-asn1crypto

ALL_TOOLS      += py2-astor

ALL_TOOLS      += py2-astroid

ALL_TOOLS      += py2-astunparse

ALL_TOOLS      += py2-atomicwrites

ALL_TOOLS      += py2-attrs

ALL_TOOLS      += py2-autopep8

ALL_TOOLS      += py2-avro

ALL_TOOLS      += py2-awkward

ALL_TOOLS      += py2-awkward1

ALL_TOOLS      += py2-backports-functools_lru_cache

ALL_TOOLS      += py2-backports

ALL_TOOLS      += py2-backports_abc

ALL_TOOLS      += py2-beautifulsoup4

ALL_TOOLS      += py2-bleach

ALL_TOOLS      += py2-bokeh

ALL_TOOLS      += py2-bottleneck

ALL_TOOLS      += py2-cachetools

ALL_TOOLS      += py2-certifi

ALL_TOOLS      += py2-cffi

ALL_TOOLS      += py2-chardet

ALL_TOOLS      += py2-click

ALL_TOOLS      += py2-climate

ALL_TOOLS      += py2-cloudpickle

ALL_TOOLS      += py2-cmsml

ALL_TOOLS      += py2-colorama

ALL_TOOLS      += py2-configparser

ALL_TOOLS      += py2-contextlib2

ALL_TOOLS      += py2-coverage

ALL_TOOLS      += py2-cryptography

ALL_TOOLS      += py2-cx-oracle

ALL_TOOLS      += py2-cycler

ALL_TOOLS      += py2-cython

ALL_TOOLS      += py2-decorator

ALL_TOOLS      += py2-defusedxml

ALL_TOOLS      += py2-distlib

ALL_TOOLS      += py2-docopt

ALL_TOOLS      += py2-docutils

ALL_TOOLS      += py2-downhill

ALL_TOOLS      += py2-dxr

ALL_TOOLS      += py2-entrypoints

ALL_TOOLS      += py2-enum34

ALL_TOOLS      += py2-filelock

ALL_TOOLS      += py2-fire

ALL_TOOLS      += py2-flake8

ALL_TOOLS      += py2-flawfinder

ALL_TOOLS      += py2-fs

ALL_TOOLS      += py2-funcsigs

ALL_TOOLS      += py2-functools32

ALL_TOOLS      += py2-future

ALL_TOOLS      += py2-futures

ALL_TOOLS      += py2-gast

ALL_TOOLS      += py2-gitdb2

ALL_TOOLS      += py2-gitpython

ALL_TOOLS      += py2-google-common

ALL_TOOLS      += py2-google-pasta

ALL_TOOLS      += py2-googlepackages

ALL_TOOLS      += py2-grpcio-tools

ALL_TOOLS      += py2-grpcio

ALL_TOOLS      += py2-h5py-cache

ALL_TOOLS      += py2-h5py

ALL_TOOLS      += py2-hep_ml

ALL_TOOLS      += py2-hepdata-lib

ALL_TOOLS      += py2-histbook

ALL_TOOLS      += py2-histogrammar

ALL_TOOLS      += py2-html5lib

ALL_TOOLS      += py2-hyperas

ALL_TOOLS      += py2-hyperopt

ALL_TOOLS      += py2-idna

ALL_TOOLS      += py2-importlib-metadata

ALL_TOOLS      += py2-importlib-resources

ALL_TOOLS      += py2-iniconfig

ALL_TOOLS      += py2-ipaddress

ALL_TOOLS      += py2-ipykernel

ALL_TOOLS      += py2-ipython

ALL_TOOLS      += py2-ipython_genutils

ALL_TOOLS      += py2-ipywidgets

ALL_TOOLS      += py2-isort

ALL_TOOLS      += py2-jedi

ALL_TOOLS      += py2-jinja2

ALL_TOOLS      += py2-joblib

ALL_TOOLS      += py2-jsonpickle

ALL_TOOLS      += py2-jsonschema

ALL_TOOLS      += py2-jupyter

ALL_TOOLS      += py2-jupyter_client

ALL_TOOLS      += py2-jupyter_console

ALL_TOOLS      += py2-jupyter_core

ALL_TOOLS      += py2-keras-applications

ALL_TOOLS      += py2-keras-preprocessing

ALL_TOOLS      += py2-keras

ALL_TOOLS      += py2-kiwisolver

ALL_TOOLS      += py2-law

ALL_TOOLS      += py2-lazy-object-proxy

ALL_TOOLS      += py2-lizard

ALL_TOOLS      += py2-lockfile

ALL_TOOLS      += py2-luigi

ALL_TOOLS      += py2-lxml

ALL_TOOLS      += py2-lz4

ALL_TOOLS      += py2-mako

ALL_TOOLS      += py2-markdown

ALL_TOOLS      += py2-markupsafe

ALL_TOOLS      += py2-matplotlib

ALL_TOOLS      += py2-mccabe

ALL_TOOLS      += py2-mistune

ALL_TOOLS      += py2-mock

ALL_TOOLS      += py2-more-itertools

ALL_TOOLS      += py2-mpld3

ALL_TOOLS      += py2-mpmath

ALL_TOOLS      += py2-nbconvert

ALL_TOOLS      += py2-nbdime

ALL_TOOLS      += py2-nbformat

ALL_TOOLS      += py2-networkx

ALL_TOOLS      += py2-neurolab

ALL_TOOLS      += py2-nose-parameterized

ALL_TOOLS      += py2-nose

ALL_TOOLS      += py2-notebook

ALL_TOOLS      += py2-numexpr

ALL_TOOLS      += py2-numpy

ALL_TOOLS      += py2-onnx

ALL_TOOLS      += py2-opt-einsum

ALL_TOOLS      += py2-ordereddict

ALL_TOOLS      += py2-packaging

ALL_TOOLS      += py2-pandas

ALL_TOOLS      += py2-pandocfilters

ALL_TOOLS      += py2-parsimonious

ALL_TOOLS      += py2-parso

ALL_TOOLS      += py2-pathlib2

ALL_TOOLS      += py2-pbr

ALL_TOOLS      += py2-pexpect

ALL_TOOLS      += py2-pickleshare

ALL_TOOLS      += py2-pillow

ALL_TOOLS      += py2-pip

ALL_TOOLS      += py2-pkgconfig

ALL_TOOLS      += py2-plac

ALL_TOOLS      += py2-pluggy

ALL_TOOLS      += py2-ply

ALL_TOOLS      += py2-prettytable

ALL_TOOLS      += py2-prometheus_client

ALL_TOOLS      += py2-prompt_toolkit

ALL_TOOLS      += py2-protobuf

ALL_TOOLS      += py2-prwlock

ALL_TOOLS      += py2-psutil

ALL_TOOLS      += py2-ptyprocess

ALL_TOOLS      += py2-py

ALL_TOOLS      += py2-pyasn1-modules

ALL_TOOLS      += py2-pyasn1

ALL_TOOLS      += py2-pybind11
py2-pybind11_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/py2-pybind11/2.6.2/lib/python2.7/site-packages/pybind11/include

ALL_TOOLS      += py2-pybrain

ALL_TOOLS      += py2-pycodestyle

ALL_TOOLS      += py2-pycparser

ALL_TOOLS      += py2-pycuda

ALL_TOOLS      += py2-pycurl

ALL_TOOLS      += py2-pydot

ALL_TOOLS      += py2-pyflakes

ALL_TOOLS      += py2-pygithub

ALL_TOOLS      += py2-pygments

ALL_TOOLS      += py2-pylint

ALL_TOOLS      += py2-pymongo

ALL_TOOLS      += py2-pyopenssl

ALL_TOOLS      += py2-pyparsing

ALL_TOOLS      += py2-pyrsistent

ALL_TOOLS      += py2-pysqlite

ALL_TOOLS      += py2-pytest-cov

ALL_TOOLS      += py2-pytest-runner

ALL_TOOLS      += py2-pytest

ALL_TOOLS      += py2-python-cjson

ALL_TOOLS      += py2-python-daemon

ALL_TOOLS      += py2-python-dateutil

ALL_TOOLS      += py2-python-ldap

ALL_TOOLS      += py2-pytools

ALL_TOOLS      += py2-pytz

ALL_TOOLS      += py2-pyyaml

ALL_TOOLS      += py2-pyzmq

ALL_TOOLS      += py2-qtconsole

ALL_TOOLS      += py2-qtpy

ALL_TOOLS      += py2-rep

ALL_TOOLS      += py2-repoze-lru

ALL_TOOLS      += py2-requests

ALL_TOOLS      += py2-root_numpy

ALL_TOOLS      += py2-root_pandas

ALL_TOOLS      += py2-scandir

ALL_TOOLS      += py2-schema

ALL_TOOLS      += py2-scikit-learn

ALL_TOOLS      += py2-scinum

ALL_TOOLS      += py2-scipy

ALL_TOOLS      += py2-seaborn

ALL_TOOLS      += py2-send2trash

ALL_TOOLS      += py2-setuptools-scm

ALL_TOOLS      += py2-setuptools

ALL_TOOLS      += py2-simplegeneric

ALL_TOOLS      += py2-singledispatch

ALL_TOOLS      += py2-six

ALL_TOOLS      += py2-smmap

ALL_TOOLS      += py2-smmap2

ALL_TOOLS      += py2-soupsieve

ALL_TOOLS      += py2-sqlalchemy

ALL_TOOLS      += py2-stevedore

ALL_TOOLS      += py2-subprocess32

ALL_TOOLS      += py2-sympy

ALL_TOOLS      += py2-tables

ALL_TOOLS      += py2-tensorflow-estimator

ALL_TOOLS      += py2-termcolor

ALL_TOOLS      += py2-terminado

ALL_TOOLS      += py2-testpath

ALL_TOOLS      += py2-theanets

ALL_TOOLS      += py2-theano

ALL_TOOLS      += py2-toml

ALL_TOOLS      += py2-tornado

ALL_TOOLS      += py2-tqdm

ALL_TOOLS      += py2-traitlets

ALL_TOOLS      += py2-typing

ALL_TOOLS      += py2-typing_extensions

ALL_TOOLS      += py2-uncertainties

ALL_TOOLS      += py2-uproot-methods

ALL_TOOLS      += py2-uproot

ALL_TOOLS      += py2-uproot4

ALL_TOOLS      += py2-urllib3

ALL_TOOLS      += py2-virtualenv-clone

ALL_TOOLS      += py2-virtualenv

ALL_TOOLS      += py2-virtualenvwrapper

ALL_TOOLS      += py2-wcwidth

ALL_TOOLS      += py2-webencodings

ALL_TOOLS      += py2-werkzeug

ALL_TOOLS      += py2-wheel

ALL_TOOLS      += py2-widgetsnbextension

ALL_TOOLS      += py2-wrapt

ALL_TOOLS      += py2-xgboost

ALL_TOOLS      += py2-xrootdpyfs

ALL_TOOLS      += py2-zipp

ALL_TOOLS      += py3-astroid

ALL_TOOLS      += py3-backcall

ALL_TOOLS      += py3-bokeh

ALL_TOOLS      += py3-boost-histogram

ALL_TOOLS      += py3-cachetools

ALL_TOOLS      += py3-correctionlib

ALL_TOOLS      += py3-flatbuffers

ALL_TOOLS      += py3-flit-core

ALL_TOOLS      += py3-flit

ALL_TOOLS      += py3-gitdb

ALL_TOOLS      += py3-gitpython

ALL_TOOLS      += py3-google-auth-oauthlib

ALL_TOOLS      += py3-google-auth

ALL_TOOLS      += py3-hist

ALL_TOOLS      += py3-histogrammar

ALL_TOOLS      += py3-histoprint

ALL_TOOLS      += py3-ipykernel

ALL_TOOLS      += py3-ipython

ALL_TOOLS      += py3-joblib

ALL_TOOLS      += py3-jupyter_client

ALL_TOOLS      += py3-jupyter_console

ALL_TOOLS      += py3-keras2onnx

ALL_TOOLS      += py3-llvmlite

ALL_TOOLS      += py3-luigi

ALL_TOOLS      += py3-matplotlib

ALL_TOOLS      += py3-more-itertools

ALL_TOOLS      += py3-mplhep

ALL_TOOLS      += py3-nbformat

ALL_TOOLS      += py3-networkx

ALL_TOOLS      += py3-notebook

ALL_TOOLS      += py3-numba

ALL_TOOLS      += py3-numpy

ALL_TOOLS      += py3-oauthlib

ALL_TOOLS      += py3-onnxconverter-common

ALL_TOOLS      += py3-onnxmltools

ALL_TOOLS      += py3-opt-einsum

ALL_TOOLS      += py3-pandas

ALL_TOOLS      += py3-pillow

ALL_TOOLS      += py3-pip

ALL_TOOLS      += py3-prompt_toolkit

ALL_TOOLS      += py3-pyasn1-modules

ALL_TOOLS      += py3-pydantic

ALL_TOOLS      += py3-pylint

ALL_TOOLS      += py3-pyrsistent

ALL_TOOLS      += py3-pytest

ALL_TOOLS      += py3-python-rapidjson

ALL_TOOLS      += py3-pytoml

ALL_TOOLS      += py3-requests-oauthlib

ALL_TOOLS      += py3-rsa

ALL_TOOLS      += py3-scikit-learn

ALL_TOOLS      += py3-scipy

ALL_TOOLS      += py3-setuptools

ALL_TOOLS      += py3-skl2onnx

ALL_TOOLS      += py3-sympy

ALL_TOOLS      += py3-tables

ALL_TOOLS      += py3-tensorboard-plugin-wit

ALL_TOOLS      += py3-tensorboard

ALL_TOOLS      += py3-tensorflow

ALL_TOOLS      += py3-testpath

ALL_TOOLS      += py3-threadpoolctl

ALL_TOOLS      += py3-tornado

ALL_TOOLS      += py3-typed-ast

ALL_TOOLS      += py3-xgboost

ALL_TOOLS      += py3-zipp

ALL_TOOLS      += pyclang
pyclang_EX_USE := python

ALL_TOOLS      += pydata
pydata_EX_FLAGS_LDFLAGS  := $(PYDATA_BASE)/lib/pydata.o
pydata_EX_FLAGS_NO_RECURSIVE_EXPORT  := 1

ALL_TOOLS      += pyminuit2

ALL_TOOLS      += pyquen
pyquen_EX_LIB := pyquen
pyquen_EX_USE := pythia6 lhapdf

ALL_TOOLS      += pythia6
pythia6_EX_LIB := pythia6 pythia6_dummy pythia6_pdfdummy
pythia6_EX_USE := pythia6_headers f77compiler

ALL_TOOLS      += pythia6_headers
pythia6_headers_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/pythia6/426-ghbfee/include
pythia6_headers_EX_USE := root_cxxdefaults

ALL_TOOLS      += pythia8
pythia8_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/pythia8/303-ljfedo3/include
pythia8_EX_LIB := pythia8
pythia8_EX_USE := root_cxxdefaults cxxcompiler hepmc lhapdf
pythia8_EX_FLAGS_SYSTEM_INCLUDE  := 1

ALL_TOOLS      += python-paths

ALL_TOOLS      += python
python_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/python/2.7.15-bcolbf2/include/python2.7
python_EX_LIB := python2.7
python_EX_USE := root_cxxdefaults sockets

ALL_TOOLS      += python3
python3_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/python3/3.8.2-bcolbf/include/python3.8
python3_EX_LIB := python3.8
python3_EX_USE := sockets

ALL_TOOLS      += python_tools

ALL_TOOLS      += qd
qd_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/qd/2.3.13-bcolbf2/include
qd_EX_LIB := qdmod qd

ALL_TOOLS      += qd_f_main
qd_f_main_EX_LIB := qd_f_main
qd_f_main_EX_USE := qd

ALL_TOOLS      += rivet
rivet_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/rivet/3.1.3-ljfedo5/include
rivet_EX_LIB := Rivet
rivet_EX_USE := hepmc fastjet fastjet-contrib gsl yoda

ALL_TOOLS      += roofit
roofit_EX_LIB := RooFit
roofit_EX_USE := roofitcore rootcore rootmath roothistmatrix

ALL_TOOLS      += roofitcore
roofitcore_EX_LIB := RooFitCore
roofitcore_EX_USE := rootcore roothistmatrix rootgpad rootminuit root_cxxdefaults

ALL_TOOLS      += roostats
roostats_EX_LIB := RooStats
roostats_EX_USE := roofitcore roofit rootcore roothistmatrix rootgpad

ALL_TOOLS      += root
root_EX_USE := rootphysics
root_EX_FLAGS_CXXMODULES  := 0
root_EX_FLAGS_GENREFLEX_FAILES_ON_WARNS  := --fail_on_warnings

ALL_TOOLS      += root_cxxdefaults

ALL_TOOLS      += root_interface
root_interface_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/lcg/root/6.22.08-ljfedo/include
root_interface_EX_USE := root_cxxdefaults
root_interface_EX_FLAGS_SYSTEM_INCLUDE  := 1

ALL_TOOLS      += rootcling
rootcling_EX_LIB := Core
rootcling_EX_USE := root_interface sockets pcre zlib xz
TOOLS_OVERRIDABLE_FLAGS  +=ROOTCLING_ARGS

ALL_TOOLS      += rootcore
rootcore_EX_LIB := Tree Net
rootcore_EX_USE := rootmathcore rootthread

ALL_TOOLS      += rootdataframe
rootdataframe_EX_LIB := ROOTDataFrame
rootdataframe_EX_USE := rootcore rootgraphics roothistmatrix rootrio rootvecops

ALL_TOOLS      += rooteg
rooteg_EX_LIB := EG
rooteg_EX_USE := rootgraphics

ALL_TOOLS      += rooteve
rooteve_EX_LIB := Eve
rooteve_EX_USE := rootgeompainter rootrgl rootged

ALL_TOOLS      += rootfoam
rootfoam_EX_LIB := Foam
rootfoam_EX_USE := roothistmatrix

ALL_TOOLS      += rootged
rootged_EX_LIB := Ged
rootged_EX_USE := rootgui

ALL_TOOLS      += rootgeom
rootgeom_EX_LIB := Geom
rootgeom_EX_USE := rootrio rootmathcore

ALL_TOOLS      += rootgeompainter
rootgeompainter_EX_LIB := GeomPainter
rootgeompainter_EX_USE := rootgeom rootgraphics

ALL_TOOLS      += rootglew
rootglew_EX_LIB := GLEW

ALL_TOOLS      += rootgpad
rootgpad_EX_LIB := Gpad Graf
rootgpad_EX_USE := roothistmatrix

ALL_TOOLS      += rootgraphics
rootgraphics_EX_LIB := TreePlayer Graf3d Postscript
rootgraphics_EX_USE := rootgpad

ALL_TOOLS      += rootgui
rootgui_EX_LIB := Gui
rootgui_EX_USE := rootgpad

ALL_TOOLS      += rootguihtml
rootguihtml_EX_LIB := GuiHtml
rootguihtml_EX_USE := rootgui rootinteractive

ALL_TOOLS      += roothistmatrix
roothistmatrix_EX_LIB := Hist Matrix
roothistmatrix_EX_USE := rootcore

ALL_TOOLS      += roothistpainter
roothistpainter_EX_LIB := HistPainter
roothistpainter_EX_USE := roothistmatrix rootgpad rootimt

ALL_TOOLS      += roothtml
roothtml_EX_LIB := Html
roothtml_EX_USE := rootgpad

ALL_TOOLS      += rootimt
rootimt_EX_LIB := Imt
rootimt_EX_USE := rootthread tbb

ALL_TOOLS      += rootinteractive
rootinteractive_EX_LIB := Gui
rootinteractive_EX_USE := libjpeg-turbo libpng rootgpad rootrint

ALL_TOOLS      += rootmath
rootmath_EX_LIB := GenVector MathMore
rootmath_EX_USE := rootcore gsl

ALL_TOOLS      += rootmathcore
rootmathcore_EX_LIB := MathCore
rootmathcore_EX_USE := rootcling

ALL_TOOLS      += rootminuit
rootminuit_EX_LIB := Minuit
rootminuit_EX_USE := rootgpad

ALL_TOOLS      += rootminuit2
rootminuit2_EX_LIB := Minuit2
rootminuit2_EX_USE := rootgpad

ALL_TOOLS      += rootmlp
rootmlp_EX_LIB := MLP
rootmlp_EX_USE := rootgraphics

ALL_TOOLS      += rootphysics
rootphysics_EX_LIB := Physics
rootphysics_EX_USE := roothistmatrix

ALL_TOOLS      += rootpy
rootpy_EX_USE := rootgraphics

ALL_TOOLS      += rootpymva
rootpymva_EX_LIB := PyMVA
rootpymva_EX_USE := roottmva numpy-c-api

ALL_TOOLS      += rootrflx
rootrflx_EX_USE := root_interface rootcling
rootrflx_EX_FLAGS_GENREFLEX_CPPFLAGS  := -DCMS_DICT_IMPL -D_REENTRANT -DGNUSOURCE -D__STRICT_ANSI__
rootrflx_EX_FLAGS_GENREFLEX_GCCXMLOPT  := -m64

ALL_TOOLS      += rootrgl
rootrgl_EX_LIB := RGL
rootrgl_EX_USE := rootglew rootgui rootinteractive rootgraphics

ALL_TOOLS      += rootrint
rootrint_EX_LIB := Rint
rootrint_EX_USE := rootcling

ALL_TOOLS      += rootrio
rootrio_EX_LIB := RIO
rootrio_EX_USE := rootcling

ALL_TOOLS      += rootsmatrix
rootsmatrix_EX_LIB := Smatrix
rootsmatrix_EX_USE := rootcling

ALL_TOOLS      += rootspectrum
rootspectrum_EX_LIB := Spectrum
rootspectrum_EX_USE := roothistmatrix

ALL_TOOLS      += rootthread
rootthread_EX_LIB := Thread
rootthread_EX_USE := rootrio

ALL_TOOLS      += roottmva
roottmva_EX_LIB := TMVA
roottmva_EX_USE := rootmlp rootminuit

ALL_TOOLS      += rootvecops
rootvecops_EX_LIB := ROOTVecOps
rootvecops_EX_USE := rootcore

ALL_TOOLS      += rootx11
rootx11_EX_LIB := GX11
rootx11_EX_USE := rootcling

ALL_TOOLS      += rootxml
rootxml_EX_LIB := XMLParser
rootxml_EX_USE := rootcore libxml2

ALL_TOOLS      += rootxmlio
rootxmlio_EX_LIB := XMLIO
rootxmlio_EX_USE := rootrio

ALL_TOOLS      += scons

ALL_TOOLS      += self
self_EX_INCLUDE := /afs/cern.ch/user/e/emartinv/public/Ntuple_prod/soft/CMSSW_11_3_4/src /afs/cern.ch/user/e/emartinv/public/Ntuple_prod/soft/CMSSW_11_3_4/include/slc7_amd64_gcc900/src /afs/cern.ch/user/e/emartinv/public/Ntuple_prod/soft/CMSSW_11_3_4/include/LCG /cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_11_3_4/src /cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_11_3_4/include/slc7_amd64_gcc900/src /cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_11_3_4/include/LCG
self_EX_LIBDIR := /afs/cern.ch/user/e/emartinv/public/Ntuple_prod/soft/CMSSW_11_3_4/biglib/slc7_amd64_gcc900 /afs/cern.ch/user/e/emartinv/public/Ntuple_prod/soft/CMSSW_11_3_4/lib/slc7_amd64_gcc900 /afs/cern.ch/user/e/emartinv/public/Ntuple_prod/soft/CMSSW_11_3_4/external/slc7_amd64_gcc900/lib /cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_11_3_4/biglib/slc7_amd64_gcc900 /cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_11_3_4/lib/slc7_amd64_gcc900 /cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_11_3_4/external/slc7_amd64_gcc900/lib
self_EX_FLAGS_DEFAULT_COMPILER  := gcc
self_EX_FLAGS_EXTERNAL_SYMLINK  := PATH LIBDIR CMSSW_SEARCH_PATH
self_EX_FLAGS_LLVM_ANALYZER  := llvm-analyzer
self_EX_FLAGS_NO_EXTERNAL_RUNTIME  := LD_LIBRARY_PATH PATH CMSSW_SEARCH_PATH
TOOLS_OVERRIDABLE_FLAGS  +=CPPDEFINES CXXFLAGS FFLAGS CFLAGS CPPFLAGS LDFLAGS CUDA_FLAGS CUDA_LDFLAGS
self_EX_FLAGS_SCRAM_TARGETS  := haswell sandybridge nehalem
self_EX_FLAGS_SKIP_TOOLS_SYMLINK  := cxxcompiler ccompiler f77compiler gcc-cxxcompiler gcc-ccompiler gcc-f77compiler llvm-cxxcompiler llvm-ccompiler llvm-f77compiler llvm-analyzer-cxxcompiler llvm-analyzer-ccompiler icc-cxxcompiler icc-ccompiler icc-f77compiler x11 dpm
self_EX_FLAGS_SYMLINK_DEPTH_CMSSW_SEARCH_PATH  := 2
self_ORDER := 20000
IS_PATCH:=

ALL_TOOLS      += sherpa
sherpa_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/sherpa/2.2.11-ljfedo3/include/SHERPA-MC
sherpa_EX_LIB := SherpaMain ToolsMath ToolsOrg
sherpa_EX_USE := root_cxxdefaults hepmc lhapdf qd blackhat fastjet sqlite openmpi openloops

ALL_TOOLS      += sigcpp
sigcpp_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/sigcpp/2.6.2-bcolbf2/include/sigc++-2.0
sigcpp_EX_LIB := sigc-2.0
sigcpp_EX_USE := root_cxxdefaults

ALL_TOOLS      += sip
sip_EX_USE := python

ALL_TOOLS      += sloccount

ALL_TOOLS      += sockets
sockets_EX_LIB := nsl crypt dl rt

ALL_TOOLS      += sqlite
sqlite_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/sqlite/3.22.0-bcolbf/include
sqlite_EX_LIB := sqlite3
sqlite_EX_USE := root_cxxdefaults

ALL_TOOLS      += starlight
starlight_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/starlight/r193-ljfedo/include
starlight_EX_LIB := Starlib
starlight_EX_USE := root_cxxdefaults clhep

ALL_TOOLS      += stdcxx-fs
stdcxx-fs_EX_LIB := stdc++fs

ALL_TOOLS      += tauola
tauola_EX_LIB := pretauola tauola
tauola_EX_USE := f77compiler tauola_headers

ALL_TOOLS      += tauola_headers
tauola_headers_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/tauola/27.121.5-ghbfee/include
tauola_headers_EX_USE := root_cxxdefaults

ALL_TOOLS      += tauolapp
tauolapp_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/tauolapp/1.1.8-ljfedo2/include
tauolapp_EX_LIB := TauolaCxxInterface TauolaFortran TauolaTauSpinner TauolaHepMC TauolaHEPEVT
tauolapp_EX_USE := root_cxxdefaults hepmc f77compiler pythia8 lhapdf

ALL_TOOLS      += tbb
tbb_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/tbb/2020_U3-ljfedo/include
tbb_EX_LIB := tbb
tbb_EX_USE := root_cxxdefaults
tbb_EX_FLAGS_CPPDEFINES  := -DTBB_USE_GLIBCXX_VERSION=90300 -DTBB_SUPPRESS_DEPRECATED_MESSAGES -DTBB_PREVIEW_RESUMABLE_TASKS=1
tbb_EX_FLAGS_SYSTEM_INCLUDE  := 1

ALL_TOOLS      += tcmalloc
tcmalloc_EX_LIB := tcmalloc

ALL_TOOLS      += tcmalloc_minimal
tcmalloc_minimal_EX_LIB := tcmalloc_minimal

ALL_TOOLS      += tensorflow-c
tensorflow-c_EX_LIB := tensorflow
tensorflow-c_EX_USE := tensorflow-framework eigen libpng sqlite

ALL_TOOLS      += tensorflow-cc
tensorflow-cc_EX_LIB := tensorflow_cc
tensorflow-cc_EX_USE := tensorflow-framework eigen libpng sqlite

ALL_TOOLS      += tensorflow-executable_run_options
tensorflow-executable_run_options_EX_LIB := executable_run_options
tensorflow-executable_run_options_EX_USE := tensorflow

ALL_TOOLS      += tensorflow-framework
tensorflow-framework_EX_LIB := tensorflow_framework
tensorflow-framework_EX_USE := tensorflow giflib zlib libjpeg-turbo protobuf

ALL_TOOLS      += tensorflow-runtime
tensorflow-runtime_EX_LIB := cpu_function_runtime
tensorflow-runtime_EX_USE := tensorflow

ALL_TOOLS      += tensorflow-tf2xla
tensorflow-tf2xla_EX_LIB := tf2xla
tensorflow-tf2xla_EX_USE := tensorflow

ALL_TOOLS      += tensorflow-xla_compiled_cpu_function
tensorflow-xla_compiled_cpu_function_EX_LIB := xla_compiled_cpu_function
tensorflow-xla_compiled_cpu_function_EX_USE := tensorflow

ALL_TOOLS      += tensorflow
tensorflow_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/tensorflow/2.4.1-ljfedo/include
tensorflow_EX_FLAGS_SYSTEM_INCLUDE  := 1

ALL_TOOLS      += thepeg
thepeg_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/thepeg/2.2.2/include
thepeg_EX_LIB := ThePEG LesHouches
thepeg_EX_USE := root_cxxdefaults lhapdf gsl

ALL_TOOLS      += tinyxml2
tinyxml2_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/tinyxml2/6.2.0-ghbfee/include
tinyxml2_EX_LIB := tinyxml2

ALL_TOOLS      += tkonlinesw
tkonlinesw_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/tkonlinesw/4.2.0-1_gcc7-ljfedo5/include
tkonlinesw_EX_LIB := ICUtils Fed9UUtils
tkonlinesw_EX_USE := root_cxxdefaults xerces-c
tkonlinesw_EX_FLAGS_CXXFLAGS  := -DCMS_TK_64BITS

ALL_TOOLS      += tkonlineswdb
tkonlineswdb_EX_LIB := DeviceDescriptions Fed9UDeviceFactory
tkonlineswdb_EX_USE := tkonlinesw oracle oracleocci

ALL_TOOLS      += toprex
toprex_EX_LIB := toprex
toprex_EX_USE := toprex_headers f77compiler

ALL_TOOLS      += toprex_headers
toprex_headers_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/toprex/4.23-ghbfee/include
toprex_headers_EX_USE := root_cxxdefaults

ALL_TOOLS      += triton-inference-server
triton-inference-server_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/triton-inference-server/2.3.0-ljfedo5/include
triton-inference-server_EX_LIB := grpcclient
triton-inference-server_EX_USE := protobuf opencv grpc

ALL_TOOLS      += ucx
ucx_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/ucx/1.9.0-ljfedo2/include
ucx_EX_LIB := ucp uct ucs ucm

ALL_TOOLS      += utm
utm_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/utm/utm_0.8.1-ljfedo4/include
utm_EX_LIB := tmeventsetup tmtable tmxsd tmgrammar tmutil
utm_EX_USE := root_cxxdefaults

ALL_TOOLS      += valgrind
valgrind_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/valgrind/3.15.0-bcolbf2/include
valgrind_EX_USE := root_cxxdefaults

ALL_TOOLS      += vdt
vdt_EX_LIB := vdt
vdt_EX_USE := vdt_headers

ALL_TOOLS      += vdt_headers
vdt_headers_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/vdt/0.4.0-ghbfee/include
vdt_headers_EX_USE := root_cxxdefaults

ALL_TOOLS      += vecgeom
vecgeom_EX_LIB := vecgeom
vecgeom_EX_USE := vecgeom_interface

ALL_TOOLS      += vecgeom_interface
vecgeom_interface_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/vecgeom/v1.1.8-ljfedo2/include /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/vecgeom/v1.1.8-ljfedo2/include/VecGeom
vecgeom_interface_EX_USE := root_cxxdefaults

ALL_TOOLS      += x11
x11_EX_USE := sockets

ALL_TOOLS      += xerces-c
xerces-c_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/xerces-c/3.1.3-bcolbf2/include
xerces-c_EX_LIB := xerces-c
xerces-c_EX_USE := root_cxxdefaults

ALL_TOOLS      += xgboost
xgboost_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/xgboost/1.3.3/include
xgboost_EX_LIB := xgboost

ALL_TOOLS      += xrootd
xrootd_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/xrootd/4.12.3/include/xrootd /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/xrootd/4.12.3/include/xrootd/private
xrootd_EX_LIB := XrdUtils XrdClient
xrootd_EX_USE := root_cxxdefaults

ALL_TOOLS      += xtensor
xtensor_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/xtensor/0.20.1-ghbfee/include
xtensor_EX_USE := xtl

ALL_TOOLS      += xtl
xtl_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/xtl/0.6.3-ghbfee/include

ALL_TOOLS      += xz
xz_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/xz/5.2.4-bcolbf2/include
xz_EX_LIB := lzma
xz_EX_USE := root_cxxdefaults

ALL_TOOLS      += yaml-cpp
yaml-cpp_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/yaml-cpp/0.6.2-ljfedo4/include
yaml-cpp_EX_LIB := yaml-cpp
yaml-cpp_EX_USE := boost

ALL_TOOLS      += yoda
yoda_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/yoda/1.8.5-ljfedo5/include
yoda_EX_LIB := YODA
yoda_EX_USE := root_cxxdefaults

ALL_TOOLS      += zlib
zlib_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/zlib/1.2.11-bcolbf/include
zlib_EX_LIB := z
zlib_EX_USE := root_cxxdefaults

ALL_TOOLS      += zstd
zstd_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/zstd/1.4.5/include
zstd_EX_LIB := zstd
zstd_EX_USE := root_cxxdefaults


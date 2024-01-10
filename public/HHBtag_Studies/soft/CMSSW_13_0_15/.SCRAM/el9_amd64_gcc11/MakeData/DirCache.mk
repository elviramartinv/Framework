ifeq ($(strip $(HHTools/HHbtag)),)
ALL_COMMONRULES += src_HHTools_HHbtag_src
src_HHTools_HHbtag_src_parent := HHTools/HHbtag
src_HHTools_HHbtag_src_INIT_FUNC := $$(eval $$(call CommonProductRules,src_HHTools_HHbtag_src,src/HHTools/HHbtag/src,LIBRARY))
HHToolsHHbtag := self/HHTools/HHbtag
HHTools/HHbtag := HHToolsHHbtag
HHToolsHHbtag_files := $(patsubst src/HHTools/HHbtag/src/%,%,$(wildcard $(foreach dir,src/HHTools/HHbtag/src ,$(foreach ext,$(SRC_FILES_SUFFIXES),$(dir)/*.$(ext)))))
HHToolsHHbtag_BuildFile    := $(WORKINGDIR)/cache/bf/src/HHTools/HHbtag/BuildFile
HHToolsHHbtag_LOC_USE := self   PhysicsTools/TensorFlow tensorflow tensorflow-cc 
HHToolsHHbtag_EX_LIB   := HHToolsHHbtag
HHToolsHHbtag_EX_USE   := $(foreach d,$(HHToolsHHbtag_LOC_USE),$(if $($(d)_EX_FLAGS_NO_RECURSIVE_EXPORT),,$d))
HHToolsHHbtag_PACKAGE := self/src/HHTools/HHbtag/src
ALL_PRODS += HHToolsHHbtag
HHToolsHHbtag_CLASS := LIBRARY
HHTools/HHbtag_forbigobj+=HHToolsHHbtag
HHToolsHHbtag_INIT_FUNC        += $$(eval $$(call Library,HHToolsHHbtag,src/HHTools/HHbtag/src,src_HHTools_HHbtag_src,$(SCRAMSTORENAME_BIN),,$(SCRAMSTORENAME_LIB),$(SCRAMSTORENAME_LOGS),))
endif
ifeq ($(strip $(TauAnalysis/ClassicSVfit)),)
ALL_COMMONRULES += src_TauAnalysis_ClassicSVfit_src
src_TauAnalysis_ClassicSVfit_src_parent := TauAnalysis/ClassicSVfit
src_TauAnalysis_ClassicSVfit_src_INIT_FUNC := $$(eval $$(call CommonProductRules,src_TauAnalysis_ClassicSVfit_src,src/TauAnalysis/ClassicSVfit/src,LIBRARY))
TauAnalysisClassicSVfit := self/TauAnalysis/ClassicSVfit
TauAnalysis/ClassicSVfit := TauAnalysisClassicSVfit
TauAnalysisClassicSVfit_files := $(patsubst src/TauAnalysis/ClassicSVfit/src/%,%,$(wildcard $(foreach dir,src/TauAnalysis/ClassicSVfit/src ,$(foreach ext,$(SRC_FILES_SUFFIXES),$(dir)/*.$(ext)))))
TauAnalysisClassicSVfit_BuildFile    := $(WORKINGDIR)/cache/bf/src/TauAnalysis/ClassicSVfit/BuildFile
TauAnalysisClassicSVfit_LOC_FLAGS_CPPDEFINES   := -DUSE_SVFITTF
TauAnalysisClassicSVfit_LOC_FLAGS_LDFLAGS   := -rdynamic
TauAnalysisClassicSVfit_LOC_USE := self   TauAnalysis/SVfitTF boost root roofit 
TauAnalysisClassicSVfit_EX_LIB   := TauAnalysisClassicSVfit
TauAnalysisClassicSVfit_EX_USE   := $(foreach d,$(TauAnalysisClassicSVfit_LOC_USE),$(if $($(d)_EX_FLAGS_NO_RECURSIVE_EXPORT),,$d))
TauAnalysisClassicSVfit_PACKAGE := self/src/TauAnalysis/ClassicSVfit/src
ALL_PRODS += TauAnalysisClassicSVfit
TauAnalysisClassicSVfit_CLASS := LIBRARY
TauAnalysis/ClassicSVfit_forbigobj+=TauAnalysisClassicSVfit
TauAnalysisClassicSVfit_INIT_FUNC        += $$(eval $$(call Library,TauAnalysisClassicSVfit,src/TauAnalysis/ClassicSVfit/src,src_TauAnalysis_ClassicSVfit_src,$(SCRAMSTORENAME_BIN),,$(SCRAMSTORENAME_LIB),$(SCRAMSTORENAME_LOGS),))
endif
ifeq ($(strip $(TauAnalysis/SVfitTF)),)
ALL_COMMONRULES += src_TauAnalysis_SVfitTF_src
src_TauAnalysis_SVfitTF_src_parent := TauAnalysis/SVfitTF
src_TauAnalysis_SVfitTF_src_INIT_FUNC := $$(eval $$(call CommonProductRules,src_TauAnalysis_SVfitTF_src,src/TauAnalysis/SVfitTF/src,LIBRARY))
TauAnalysisSVfitTF := self/TauAnalysis/SVfitTF
TauAnalysis/SVfitTF := TauAnalysisSVfitTF
TauAnalysisSVfitTF_files := $(patsubst src/TauAnalysis/SVfitTF/src/%,%,$(wildcard $(foreach dir,src/TauAnalysis/SVfitTF/src ,$(foreach ext,$(SRC_FILES_SUFFIXES),$(dir)/*.$(ext)))))
TauAnalysisSVfitTF_BuildFile    := $(WORKINGDIR)/cache/bf/src/TauAnalysis/SVfitTF/BuildFile
TauAnalysisSVfitTF_LOC_FLAGS_LDFLAGS   := -rdynamic
TauAnalysisSVfitTF_LOC_USE := self   CondFormats/JetMETObjects DataFormats/TauReco FWCore/ParameterSet root roofit 
TauAnalysisSVfitTF_EX_LIB   := TauAnalysisSVfitTF
TauAnalysisSVfitTF_EX_USE   := $(foreach d,$(TauAnalysisSVfitTF_LOC_USE),$(if $($(d)_EX_FLAGS_NO_RECURSIVE_EXPORT),,$d))
TauAnalysisSVfitTF_PACKAGE := self/src/TauAnalysis/SVfitTF/src
ALL_PRODS += TauAnalysisSVfitTF
TauAnalysisSVfitTF_CLASS := LIBRARY
TauAnalysis/SVfitTF_forbigobj+=TauAnalysisSVfitTF
TauAnalysisSVfitTF_INIT_FUNC        += $$(eval $$(call Library,TauAnalysisSVfitTF,src/TauAnalysis/SVfitTF/src,src_TauAnalysis_SVfitTF_src,$(SCRAMSTORENAME_BIN),,$(SCRAMSTORENAME_LIB),$(SCRAMSTORENAME_LOGS),))
endif
ifeq ($(strip $(HHKinFit2/HHKinFit2)),)
ALL_COMMONRULES += src_HHKinFit2_HHKinFit2_src
src_HHKinFit2_HHKinFit2_src_parent := HHKinFit2/HHKinFit2
src_HHKinFit2_HHKinFit2_src_INIT_FUNC := $$(eval $$(call CommonProductRules,src_HHKinFit2_HHKinFit2_src,src/HHKinFit2/HHKinFit2/src,LIBRARY))
HHKinFit2HHKinFit2 := self/HHKinFit2/HHKinFit2
HHKinFit2/HHKinFit2 := HHKinFit2HHKinFit2
HHKinFit2HHKinFit2_files := $(patsubst src/HHKinFit2/HHKinFit2/src/%,%,$(wildcard $(foreach dir,src/HHKinFit2/HHKinFit2/src ,$(foreach ext,$(SRC_FILES_SUFFIXES),$(dir)/*.$(ext)))))
HHKinFit2HHKinFit2_BuildFile    := $(WORKINGDIR)/cache/bf/src/HHKinFit2/HHKinFit2/BuildFile
HHKinFit2HHKinFit2_LOC_USE := self   root histfactory 
HHKinFit2HHKinFit2_EX_LIB   := HHKinFit2HHKinFit2
HHKinFit2HHKinFit2_EX_USE   := $(foreach d,$(HHKinFit2HHKinFit2_LOC_USE),$(if $($(d)_EX_FLAGS_NO_RECURSIVE_EXPORT),,$d))
HHKinFit2HHKinFit2_PACKAGE := self/src/HHKinFit2/HHKinFit2/src
ALL_PRODS += HHKinFit2HHKinFit2
HHKinFit2HHKinFit2_CLASS := LIBRARY
HHKinFit2/HHKinFit2_forbigobj+=HHKinFit2HHKinFit2
HHKinFit2HHKinFit2_INIT_FUNC        += $$(eval $$(call Library,HHKinFit2HHKinFit2,src/HHKinFit2/HHKinFit2/src,src_HHKinFit2_HHKinFit2_src,$(SCRAMSTORENAME_BIN),,$(SCRAMSTORENAME_LIB),$(SCRAMSTORENAME_LOGS),))
endif

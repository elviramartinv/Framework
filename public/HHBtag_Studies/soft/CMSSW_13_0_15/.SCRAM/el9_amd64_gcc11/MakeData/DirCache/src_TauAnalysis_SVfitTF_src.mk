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

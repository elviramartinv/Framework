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

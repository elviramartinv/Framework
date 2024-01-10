ifeq ($(strip $(testClassicSVfit)),)
testClassicSVfit := self/src/TauAnalysis/ClassicSVfit/bin
testClassicSVfit_files := $(patsubst src/TauAnalysis/ClassicSVfit/bin/%,%,$(foreach file,testClassicSVfit.cc,$(eval xfile:=$(wildcard src/TauAnalysis/ClassicSVfit/bin/$(file)))$(if $(xfile),$(xfile),$(warning No such file exists: src/TauAnalysis/ClassicSVfit/bin/$(file). Please fix src/TauAnalysis/ClassicSVfit/bin/BuildFile.))))
testClassicSVfit_BuildFile    := $(WORKINGDIR)/cache/bf/src/TauAnalysis/ClassicSVfit/bin/BuildFile
testClassicSVfit_LOC_FLAGS_CPPDEFINES   := -DUSE_SVFITTF
testClassicSVfit_LOC_USE := self   TauAnalysis/ClassicSVfit TauAnalysis/SVfitTF root 
testClassicSVfit_PACKAGE := self/src/TauAnalysis/ClassicSVfit/bin
ALL_PRODS += testClassicSVfit
testClassicSVfit_INIT_FUNC        += $$(eval $$(call Binary,testClassicSVfit,src/TauAnalysis/ClassicSVfit/bin,src_TauAnalysis_ClassicSVfit_bin,$(SCRAMSTORENAME_BIN),,$(SCRAMSTORENAME_BIN),bin,$(SCRAMSTORENAME_LOGS)))
testClassicSVfit_CLASS := BINARY
else
$(eval $(call MultipleWarningMsg,testClassicSVfit,src/TauAnalysis/ClassicSVfit/bin))
endif
ALL_COMMONRULES += src_TauAnalysis_ClassicSVfit_bin
src_TauAnalysis_ClassicSVfit_bin_parent := TauAnalysis/ClassicSVfit
src_TauAnalysis_ClassicSVfit_bin_INIT_FUNC += $$(eval $$(call CommonProductRules,src_TauAnalysis_ClassicSVfit_bin,src/TauAnalysis/ClassicSVfit/bin,BINARY))

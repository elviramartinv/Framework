ifeq ($(strip $(PyFrameworkNanoProd)),)
PyFrameworkNanoProd := self/src/Framework/NanoProd/python
src_Framework_NanoProd_python_parent := src/Framework/NanoProd
ALL_PYTHON_DIRS += $(patsubst src/%,%,src/Framework/NanoProd/python)
PyFrameworkNanoProd_files := $(patsubst src/Framework/NanoProd/python/%,%,$(wildcard $(foreach dir,src/Framework/NanoProd/python ,$(foreach ext,$(SRC_FILES_SUFFIXES),$(dir)/*.$(ext)))))
PyFrameworkNanoProd_LOC_USE := self   
PyFrameworkNanoProd_PACKAGE := self/src/Framework/NanoProd/python
ALL_PRODS += PyFrameworkNanoProd
PyFrameworkNanoProd_INIT_FUNC        += $$(eval $$(call PythonProduct,PyFrameworkNanoProd,src/Framework/NanoProd/python,src_Framework_NanoProd_python))
else
$(eval $(call MultipleWarningMsg,PyFrameworkNanoProd,src/Framework/NanoProd/python))
endif
ALL_COMMONRULES += src_Framework_NanoProd_python
src_Framework_NanoProd_python_INIT_FUNC += $$(eval $$(call CommonProductRules,src_Framework_NanoProd_python,src/Framework/NanoProd/python,PYTHON))
ALL_PACKAGES += HHTools/HHbtag
subdirs_src_HHTools_HHbtag := src_HHTools_HHbtag_bin src_HHTools_HHbtag_src
ALL_SUBSYSTEMS+=Framework
subdirs_src_Framework = src_Framework_NanoProd
subdirs_src += src_Framework
ALL_PACKAGES += Framework/NanoProd
subdirs_src_Framework_NanoProd := src_Framework_NanoProd_python
ALL_SUBSYSTEMS+=HHTools
subdirs_src_HHTools = src_HHTools_HHbtag
subdirs_src += src_HHTools
ALL_SUBSYSTEMS+=TauAnalysis
subdirs_src_TauAnalysis = src_TauAnalysis_ClassicSVfit src_TauAnalysis_SVfitTF
subdirs_src += src_TauAnalysis
ALL_PACKAGES += TauAnalysis/ClassicSVfit
subdirs_src_TauAnalysis_ClassicSVfit := src_TauAnalysis_ClassicSVfit_bin src_TauAnalysis_ClassicSVfit_src
ALL_PACKAGES += TauAnalysis/SVfitTF
subdirs_src_TauAnalysis_SVfitTF := src_TauAnalysis_SVfitTF_src
ALL_SUBSYSTEMS+=HHKinFit2
subdirs_src_HHKinFit2 = src_HHKinFit2_HHKinFit2
subdirs_src += src_HHKinFit2
ALL_PACKAGES += HHKinFit2/HHKinFit2
subdirs_src_HHKinFit2_HHKinFit2 := src_HHKinFit2_HHKinFit2_src
ifeq ($(strip $(hhBtagTest)),)
hhBtagTest := self/src/HHTools/HHbtag/bin
hhBtagTest_files := $(patsubst src/HHTools/HHbtag/bin/%,%,$(foreach file,hhBtagTest.cc,$(eval xfile:=$(wildcard src/HHTools/HHbtag/bin/$(file)))$(if $(xfile),$(xfile),$(warning No such file exists: src/HHTools/HHbtag/bin/$(file). Please fix src/HHTools/HHbtag/bin/BuildFile.))))
hhBtagTest_BuildFile    := $(WORKINGDIR)/cache/bf/src/HHTools/HHbtag/bin/BuildFile
hhBtagTest_LOC_USE := self   HHTools/HHbtag PhysicsTools/TensorFlow tensorflow tensorflow-cc 
hhBtagTest_PACKAGE := self/src/HHTools/HHbtag/bin
ALL_PRODS += hhBtagTest
hhBtagTest_INIT_FUNC        += $$(eval $$(call Binary,hhBtagTest,src/HHTools/HHbtag/bin,src_HHTools_HHbtag_bin,$(SCRAMSTORENAME_BIN),,$(SCRAMSTORENAME_BIN),bin,$(SCRAMSTORENAME_LOGS)))
hhBtagTest_CLASS := BINARY
else
$(eval $(call MultipleWarningMsg,hhBtagTest,src/HHTools/HHbtag/bin))
endif
ALL_COMMONRULES += src_HHTools_HHbtag_bin
src_HHTools_HHbtag_bin_parent := HHTools/HHbtag
src_HHTools_HHbtag_bin_INIT_FUNC += $$(eval $$(call CommonProductRules,src_HHTools_HHbtag_bin,src/HHTools/HHbtag/bin,BINARY))
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

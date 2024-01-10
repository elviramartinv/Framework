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

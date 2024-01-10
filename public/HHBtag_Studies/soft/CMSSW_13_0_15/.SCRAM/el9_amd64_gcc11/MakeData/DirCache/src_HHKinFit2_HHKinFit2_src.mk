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

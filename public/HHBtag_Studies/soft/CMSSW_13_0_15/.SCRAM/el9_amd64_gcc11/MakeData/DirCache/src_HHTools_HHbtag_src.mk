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

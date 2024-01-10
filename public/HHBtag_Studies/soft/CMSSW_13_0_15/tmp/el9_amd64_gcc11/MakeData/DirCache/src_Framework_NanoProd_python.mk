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

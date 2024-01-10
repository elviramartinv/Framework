ALL_TOOLS      += cupla-tbb
cupla-tbb_EX_LIB := cupla-tbb
cupla-tbb_EX_USE := cupla tbb
cupla-tbb_EX_FLAGS_CXXFLAGS  := -DALPAKA_ACC_CPU_B_TBB_T_SEQ_ENABLED -DCUPLA_STREAM_ASYNC_ENABLED=1


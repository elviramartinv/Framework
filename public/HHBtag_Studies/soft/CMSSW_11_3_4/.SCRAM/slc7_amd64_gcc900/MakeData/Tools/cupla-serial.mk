ALL_TOOLS      += cupla-serial
cupla-serial_EX_LIB := cupla-serial
cupla-serial_EX_USE := cupla
cupla-serial_EX_FLAGS_CXXFLAGS  := -DALPAKA_ACC_CPU_B_SEQ_T_SEQ_ENABLED -DCUPLA_STREAM_ASYNC_ENABLED=0


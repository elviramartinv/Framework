ALL_TOOLS      += cupla-cuda
cupla-cuda_EX_LIB := cupla-cuda
cupla-cuda_EX_USE := cupla cuda
cupla-cuda_EX_FLAGS_CXXFLAGS  := -DALPAKA_ACC_GPU_CUDA_ENABLED -DCUPLA_STREAM_ASYNC_ENABLED=1


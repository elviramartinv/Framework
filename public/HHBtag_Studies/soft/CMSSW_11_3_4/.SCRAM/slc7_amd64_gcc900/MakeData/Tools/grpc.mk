ALL_TOOLS      += grpc
grpc_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/grpc/1.35.0-ljfedo2/include
grpc_EX_LIB := grpc grpc++ grpc++_reflection
grpc_EX_USE := protobuf openssl pcre
grpc_EX_FLAGS_SYSTEM_INCLUDE  := 1


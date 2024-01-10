ALL_TOOLS      += geant4core
geant4core_EX_INCLUDE := /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/geant4/10.7.1-ljfedo2/include/Geant4 /cvmfs/cms.cern.ch/slc7_amd64_gcc900/external/geant4/10.7.1-ljfedo2/include
geant4core_EX_LIB := G4digits_hits G4error_propagation G4event G4geometry G4global G4graphics_reps G4intercoms G4interfaces G4materials G4parmodels G4particles G4persistency G4physicslists G4processes G4readout G4run G4tracking G4track G4analysis
geant4core_EX_USE := clhep vecgeom zlib expat xerces-c root_cxxdefaults
geant4core_EX_FLAGS_CPPDEFINES  := -DGNU_GCC -DG4V9
geant4core_EX_FLAGS_CXXFLAGS  := -ftls-model=global-dynamic -pthread


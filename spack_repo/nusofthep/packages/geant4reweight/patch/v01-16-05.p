diff --git a/CMakeLists.txt b/CMakeLists.txt
index 5787ded..bc6aca2 100644
--- a/CMakeLists.txt
+++ b/CMakeLists.txt
@@ -13,8 +13,8 @@
 # ======================================================================
 
 
-# use cmake 3.11 or later
-cmake_minimum_required (VERSION 3.11)
+# use cmake 3.20 or later
+cmake_minimum_required (VERSION 3.20 FATAL_ERROR)
 
 project(geant4reweight VERSION 01.16.05)
 
@@ -84,44 +84,27 @@ project(geant4reweight VERSION 01.16.05)
 #else()
   #message( FATAL_ERROR "NOT USING ART" )
 
-  find_package(cetbuildtools REQUIRED)
+  find_package(cetmodules REQUIRED)
 
-  #LG if(NOT "${CMAKE_CXX_STANDARD}")
-  #LG   set(CMAKE_CXX_STANDARD 17)
-  #LG endif()
-  
-  #LG set(CMAKE_CXX_STANDARD_REQUIRED ON)
-  #LG set(CMAKE_CXX_EXTENSIONS OFF)
-  
   include(CetCMakeEnv)
   cet_cmake_env()
   
   cet_set_compiler_flags(DIAGS CAUTIOUS
     WERROR
     NO_UNDEFINED
-    EXTRA_FLAGS -pedantic
-    EXTRA_CXX_FLAGS -Wno-unused-local-typedefs
+    EXTRA_FLAGS -pedantic -Wno-unused-local-typedefs
   )
   
-  cet_report_compiler_flags()
-  
-  #new
-  find_package(cetlib REQUIRED)
-  find_package(cetlib_except REQUIRED)
-  find_package(CLHEP REQUIRED)
-  find_package(fhiclcpp REQUIRED PUBLIC)
+  cet_report_compiler_flags(REPORT_THRESHOLD VERBOSE)
 
-  find_ups_geant4( )
-  find_ups_root()
-  #find_package(ROOT REQUIRED COMPONENTS RIO Net)
+  find_package(Geant4 REQUIRED EXPORT)
+  find_package(ROOT COMPONENTS Gpad Hist MathCore Matrix RIO Tree REQUIRED EXPORT)
+  find_package(cetlib REQUIRED EXPORT)
+  find_package(cetlib_except REQUIRED EXPORT)
+  find_package(fhiclcpp REQUIRED EXPORT)
 
-  # ADD SOURCE CODE SUBDIRECTORIES HERE
   add_subdirectory(geant4reweight)
-  # tests
   add_subdirectory(test)
-  # ups - table and config files
-  # must be AFTER all other subdirectories
-  add_subdirectory(ups)
   
-  include(UseCPack) 
+  cet_cmake_config()
 #endif()
diff --git a/geant4reweight/app/FitterBase/CMakeLists.txt b/geant4reweight/app/FitterBase/CMakeLists.txt
index e31efdb..d6cc287 100644
--- a/geant4reweight/app/FitterBase/CMakeLists.txt
+++ b/geant4reweight/app/FitterBase/CMakeLists.txt
@@ -3,14 +3,13 @@ SET(FITTER_APPS
 )
 
 foreach(appname ${FITTER_APPS})
-  cet_make_exec( ${appname} 
+  cet_make_exec(NAME ${appname}
     SOURCE 
       ${appname}.cc
     LIBRARIES
       fhiclcpp::fhiclcpp
       cetlib::cetlib
       cetlib_except::cetlib_except
-      ${ROOT_BASIC_LIB_LIST}
       FitterBaseLib
       ReweightBaseLib
       PropBaseLib    
diff --git a/geant4reweight/app/PredictionBase/CMakeLists.txt b/geant4reweight/app/PredictionBase/CMakeLists.txt
index 7c846f7..12dd848 100644
--- a/geant4reweight/app/PredictionBase/CMakeLists.txt
+++ b/geant4reweight/app/PredictionBase/CMakeLists.txt
@@ -6,7 +6,7 @@ SET(PREDICTION_APPS
 
 
 foreach(appname ${PREDICTION_APPS})
-  cet_make_exec( ${appname} 
+  cet_make_exec(NAME ${appname}
     SOURCE 
       ${appname}.cc
     LIBRARIES
@@ -27,7 +27,7 @@ foreach(appname ${PREDICTION_APPS})
       Geant4::G4global
       Geant4::G4persistency
       Geant4::G4physicslists
-      ${ROOT_BASIC_LIB_LIST}
+      ROOT::Tree
       PredictionBaseLib
   )
 
diff --git a/geant4reweight/app/PropBase/CMakeLists.txt b/geant4reweight/app/PropBase/CMakeLists.txt
index 614e501..0113ca5 100644
--- a/geant4reweight/app/PropBase/CMakeLists.txt
+++ b/geant4reweight/app/PropBase/CMakeLists.txt
@@ -4,15 +4,14 @@ SET(PROP_APPS
 
 
 foreach(appname ${PROP_APPS})
-  cet_make_exec( ${appname} 
+  cet_make_exec(NAME ${appname}
     SOURCE 
       ${appname}.cc
     LIBRARIES
       fhiclcpp::fhiclcpp
       cetlib::cetlib
       cetlib_except::cetlib_except
-      ${ROOT_BASIC_LIB_LIST}
-      PropBaseLib    
+      PropBaseLib
   )
 
 endforeach()
diff --git a/geant4reweight/src/FitterBase/CMakeLists.txt b/geant4reweight/src/FitterBase/CMakeLists.txt
index f8ea5ab..1aafa8b 100644
--- a/geant4reweight/src/FitterBase/CMakeLists.txt
+++ b/geant4reweight/src/FitterBase/CMakeLists.txt
@@ -8,7 +8,8 @@ cet_make_library( LIBRARY_NAME FitterBaseLib
     fhiclcpp::fhiclcpp
     cetlib::cetlib
     cetlib_except::cetlib_except
-    ${ROOT_BASIC_LIB_LIST}
+    ROOT::Gpad
+    ROOT::Tree
     PropBaseLib
     ReweightBaseLib
 )
diff --git a/geant4reweight/src/PredictionBase/CMakeLists.txt b/geant4reweight/src/PredictionBase/CMakeLists.txt
index 1e0f07b..5ad6645 100644
--- a/geant4reweight/src/PredictionBase/CMakeLists.txt
+++ b/geant4reweight/src/PredictionBase/CMakeLists.txt
@@ -18,7 +18,7 @@ cet_make_library( LIBRARY_NAME PredictionBaseLib
     Geant4::G4global
     Geant4::G4persistency
     Geant4::G4physicslists
-    ${ROOT_BASIC_LIB_LIST}
+    ROOT::Hist
 )
 install_headers()
 install_source()
diff --git a/geant4reweight/src/PropBase/CMakeLists.txt b/geant4reweight/src/PropBase/CMakeLists.txt
index 313775f..346acaf 100644
--- a/geant4reweight/src/PropBase/CMakeLists.txt
+++ b/geant4reweight/src/PropBase/CMakeLists.txt
@@ -6,7 +6,7 @@ cet_make_library( LIBRARY_NAME PropBaseLib
     fhiclcpp::fhiclcpp
     cetlib::cetlib
     cetlib_except::cetlib_except
-    ${ROOT_BASIC_LIB_LIST}
+    ROOT::Hist
 )
 install_headers()
 install_source()
diff --git a/geant4reweight/src/ReweightBase/CMakeLists.txt b/geant4reweight/src/ReweightBase/CMakeLists.txt
index 0dd5695..08b4785 100644
--- a/geant4reweight/src/ReweightBase/CMakeLists.txt
+++ b/geant4reweight/src/ReweightBase/CMakeLists.txt
@@ -30,7 +30,6 @@ cet_make_library( LIBRARY_NAME ReweightBaseLib
     Geant4::G4global
     Geant4::G4persistency
     Geant4::G4physicslists
-    ${ROOT_BASIC_LIB_LIST}
     PropBaseLib
     PredictionBaseLib    
 )

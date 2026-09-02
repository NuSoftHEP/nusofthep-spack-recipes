# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
from spack import *
from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Dk2nugenie(CMakePackage, FnalGithubPackage):
    """This package consolidates the disparate formats of neutrino beam simulation "flux" files."""

    repo = "NuSoftHEP/dk2nu"
    git = "https://github.com/%s" % repo
    version_patterns = ["v0_10_01"]

    version("01.12.00", sha256="720e75befd8f725be090eaf0dee9b4533043e7959f2c43945e580933db7eda6c")
    version("01.11.00", sha256="5b5f8993c230b10c2354fd428bfa51e1e7d2c8477a3ee0ecb0dd5d8bc3429dbe")
    version("01.10.02", sha256="6186a03cc778e93ebe86be82b31becaf205d0e6eb2ca2de1cfe48d1e98df809f")
    version("01.10.01", sha256="8680ffae5182dc1c0a04a3410cf687c4b7c0d9420e2aabc5c3c4bb42c69c3dd0")

    cxxstd_variant("17", "20", default="17")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake", type="build")

    depends_on("dk2nudata")
    depends_on("genie")
    depends_on("libxml2")
    depends_on("log4cpp")
    depends_on("root")
    depends_on("tbb")

    def patch(self):
        patch("dk2nu.patch", when="^genie@3.00.00:", working_dir=f"v{self.version}")
        cmakelists = FileFilter(f"genie/CMakeLists.txt")
        cmakelists.filter(r"\$\{GENIE\}/src", "${GENIE}/include/GENIE")
        cmakelists.filter(r"\$ENV", "$")
        cmakelists.filter("execute_process", "#execute_process")
        cmakelists.filter("ENV GENIE_LIB", "${GENIE_LIB}")
        cmakelists.filter("ENV LOG4CPP_LIB", "${LOG4CPP_LIB}")

    # dk2nugenie cannot support parallel builds
    parallel = False

    def cmake_args(self):
        if os.path.exists(self.spec["tbb"].prefix.lib64):
            tbblib = self.spec["tbb"].prefix.lib64
        if os.path.exists(self.spec["tbb"].prefix.lib):
            tbblib = self.spec["tbb"].prefix.lib
        if os.path.exists(self.spec["tbb"].prefix.tbb.latest.lib):
            tbblib = self.spec["tbb"].prefix.tbb.latest.lib
        genie = self.spec["genie"]
        if os.path.exists(self.spec["libxml2"].prefix.include.libxml2):
            libxml2inc = self.spec["libxml2"].prefix.include.libxml2
        else:
            libxml2inc = self.spec["libxml2"].prefix.include
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("CMAKE_INSTALL_PREFIX", self.prefix),
            self.define("GENIE_ONLY", True),
            self.define("TBB_LIBRARY", os.path.join(tbblib, "libtbb.so")),
            self.define("GENIE_INC", genie.prefix.include.GENIE),
            self.define("GENIE_LIB", genie.prefix.lib),
            self.define("GENIE", genie.prefix),
            self.define("GENIE_VERSION", genie.version),
            self.define("DK2NUDATA_DIR", self.spec["dk2nudata"].prefix.lib),
            self.define("LIBXML2_INC", libxml2inc),
            # genie/CMakeLists.txt does `find_library(XML2 xml2 PATHS
            # ${LIBXML2_FQ_DIR}/lib NO_DEFAULT_PATH)`; without LIBXML2_FQ_DIR it
            # searches "/lib" and XML2 -> NOTFOUND when libxml2 is a Spack build
            # (non-OS prefix).  Point it at libxml2's prefix (multispack fix).
            self.define("LIBXML2_FQ_DIR", self.spec["libxml2"].prefix),
            self.define("LOG4CPP_INC", self.spec["log4cpp"].prefix.include),
            self.define("LOG4CPP_LIB", self.spec["log4cpp"].prefix.lib),
        ]

    def setup_build_environment(self, env):
        env.set("DK2NUGENIE_LIB", self.prefix.lib)
        env.set("DK2NUGENIE_INC", self.prefix.include)

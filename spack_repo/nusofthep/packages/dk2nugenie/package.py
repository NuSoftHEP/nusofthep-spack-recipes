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
    version_patterns = ["v0_10_01"]

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
            self.define("GENIE", genie.prefix),
            self.define("GENIE_VERSION", genie.version),
            self.define("DK2NUDATA_DIR", self.spec["dk2nudata"].prefix.lib),
            self.define("LIBXML2_INC", libxml2inc),
            self.define("LOG4CPP_INC", self.spec["log4cpp"].prefix.include),
        ]

    def setup_build_environment(self, env):
        env.set("DK2NUGENIE_LIB", self.prefix.lib)
        env.set("DK2NUGENIE_INC", self.prefix.include)

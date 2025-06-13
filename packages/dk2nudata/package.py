# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class Dk2nudata(CMakePackage, FnalGithubPackage):
    """This package consolidates the disparate formats of neutrino beam simulation "flux" files."""

    repo = "NuSoftHEP/dk2nu"
    version_patterns = ["v0_10_01"]

    version("01.10.01", sha256="8680ffae5182dc1c0a04a3410cf687c4b7c0d9420e2aabc5c3c4bb42c69c3dd0")

    cxxstd_variant("17", "20", default="17")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake", type="build")

    depends_on("libxml2")
    depends_on("log4cpp")
    depends_on("root")
    depends_on("tbb")

    # dk2nudata cannot support parallel builds
    parallel = False

    def cmake_args(self):
        if os.path.exists(self.spec["tbb"].prefix.lib64):
            tbblib = self.spec["tbb"].prefix.lib64
        if os.path.exists(self.spec["tbb"].prefix.lib):
            tbblib = self.spec["tbb"].prefix.lib
        if os.path.exists(self.spec["tbb"].prefix.tbb.latest.lib):
            tbblib = self.spec["tbb"].prefix.tbb.latest.lib
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("WITH_GENIE", False),
            self.define("TBB_LIBRARY", os.path.join(tbblib, "libtbb.so")),
        ]

    def setup_build_environment(self, env):
        env.set("DK2NUDATA_LIB", self.prefix.lib)
        env.set("DK2NUDATA_INC", self.prefix.include)

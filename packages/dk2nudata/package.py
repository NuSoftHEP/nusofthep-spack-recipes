# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *
from spack.pkg.fnal_art.utilities import *


class Dk2nudata(CMakePackage):
    """This package consolidates the disparate formats of neutrino beam simulation "flux" files."""

    homepage = "https://github.com/NuSoftHEP/dk2nu.git"
    git = homepage
    url = "https://github.com/NuSoftHEP/dk2nu/archive/refs/tags/v01_10_01.tar.gz"
    list_url = "https://github.com/NuSoftHEP/dk2nu/tags"

    version("01.10.01", sha256="8680ffae5182dc1c0a04a3410cf687c4b7c0d9420e2aabc5c3c4bb42c69c3dd0")

    def url_for_version(self, version):
        return github_version_url("NuSoftHEP", "dk2nu", f"v{version.underscored}")

    variant(
        "cxxstd",
        default="17",
        values=("17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cmake", type="build")

    depends_on("root")
    depends_on("tbb")
    depends_on("libxml2")
    depends_on("log4cpp")

    # dk2nudata cannot support parallel builds
    parallel = False

    def cmake_args(self):
        if os.path.exists(self.spec["tbb"].prefix.lib64):
            tbblib = self.spec["tbb"].prefix.lib64
        else:
            tbblib = self.spec["tbb"].prefix.lib
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("WITH_GENIE", False),
            self.define("TBB_LIBRARY", os.path.join(tbblib, "libtbb.so")),
        ]

    def setup_build_environment(self, env):
        env.set("DK2NUDATA_LIB", self.prefix.lib)
        env.set("DK2NUDATA_INC", self.prefix.include)

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
from spack import *
from spack.pkg.fnal_art.utilities import *


class Dk2nugenie(CMakePackage):
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
    depends_on("libxml2")
    depends_on("log4cpp")
    depends_on("genie")
    depends_on("dk2nudata")
    depends_on("tbb")

    def patch(self):
        patch("dk2nu.patch", when="^genie@3.00.00:", working_dir="v{0}".format(self.version))
        cmakelists = FileFilter("{0}/dk2nu/genie/CMakeLists.txt".format(self.stage.source_path))
        cmakelists.filter(r"\$\{GENIE\}/src", "${GENIE}/include/GENIE")
        cmakelists.filter(r"\$ENV", "$")
        cmakelists.filter("execute_process", "#execute_process")

    # dk2nugenie cannot support parallel builds
    parallel = False

    def cmake_args(self):
        if os.path.exists(self.spec["tbb"].prefix.lib64):
            tbblib = self.spec["tbb"].prefix.lib64
        else:
            tbblib = self.spec["tbb"].prefix.lib
        genie = self.spec["genie"]
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("CMAKE_INSTALL_PREFIX", self.prefix),
            self.define("GENIE_ONLY", True),
            self.define("TBB_LIBRARY", os.path.join(tbblib, "libtbb.so")),
            self.define("GENIE_INC", os.path.join(genie.prefix.include, "GENIE")),
            self.define("GENIE", genie.prefix),
            self.define("GENIE_VERSION", genie.version),
            self.define("DK2NUDATA_DIR", self.spec["dk2nudata"].prefix.lib),
            self.define("LIBXML2_INC", self.spec["libxml2"].prefix.include),
            self.define("LOG4CPP_INC", self.spec["log4cpp"].prefix.include),
        ]

    def setup_build_environment(self, env):
        env.set("DK2NUGENIE_LIB", self.prefix.lib)
        env.set("DK2NUGENIE_INC", self.prefix.include)

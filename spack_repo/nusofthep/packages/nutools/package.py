# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Nutools(CMakePackage, FnalGithubPackage):
    """Nutools"""

    repo = "NuSoftHEP/nutools"
    license("Apache-2.0")
    version_patterns = ["v3_15_04", "3.16.03"]

    version("3.17.00", sha256="48b6be64291411d27878da5010415564fd658ecffc72e617fb8a11579ecaed0b")
    version("3.16.06", sha256="f540be7b30eec357c5f65260be6da3ce6988e5b193c58770baaa36a913a513ac")
                
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("art-root-io")
    depends_on("cry")
    depends_on("nusimdata")
    depends_on("perl")

    @cmake_preset
    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
        ]

    @sanitize_paths
    def setup_run_environment(self, run_env):
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)

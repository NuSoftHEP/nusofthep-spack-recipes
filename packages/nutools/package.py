# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.fnal_art.fnal_github_package import *


class Nutools(CMakePackage, FnalGithubPackage):
    """Nutools"""

    repo = "NuSoftHEP/nutools"
    license("Apache-2.0")
    version_patterns = ["v3_15_04", "3.16.03"]

    version("3.16.06", sha256="4ad2b05bcbed59a34d7723b864df39e1efc114666fe11dd3383737922c1d7d30")
    version("3.16.05", sha256="030cad7d6b7d8c079543203ef5c60292c961d5cc8f6acfd16e360209adda6a0c")
    version("3.15.04", sha256="9f145338854ae1bbcfbbbd7f56fd518663cfd0e2279520c31649ad1b71d4d028")
    version("develop", branch="develop", get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cetmodules", type="build")

    depends_on("art")
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

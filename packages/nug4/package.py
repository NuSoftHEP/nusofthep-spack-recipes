# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *
from spack.pkg.fnal_art.utilities import *


def sanitize_environments(*args):
    for env in args:
        for var in (
            "PATH",
            "CET_PLUGIN_PATH",
            "LDSHARED",
            "LD_LIBRARY_PATH",
            "DYLD_LIBRARY_PATH",
            "LIBRARY_PATH",
            "CMAKE_PREFIX_PATH",
            "ROOT_INCLUDE_PATH",
        ):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Nug4(CMakePackage):
    """Generator interfaces to art for GENIE and GiBUU."""

    git = "https://github.com/NuSoftHEP/nug4.git"
    homepage = git
    url = "https://github.com/NuSoftHEP/nug4/archive/refs/tags/1.16.05.tar.gz"
    list_url = "https://github.com/NuSoftHEP/nug4/tags"

    version("1.16.05", sha256="91d5cf3bfed7206e92193582b4dca48e9089042b959c088666c5c83cedbf0e56")
    version("1.15.02", sha256="53dcc4998a9e4841739cfbc7ee2e5cb312321cb1be2591af891f39ff7d306ed7")
    version("develop", branch="develop", get_full_repo=True)

    def url_for_version(self, version):
        if version < Version("1.16.03"):
            return github_version_url("NuSoftHEP", "nug4", f"v{version.underscored}")
        else:
            return super().url_for_version(version)

    variant(
        "cxxstd",
        default="17",
        values=("17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    # Build-only dependencies.
    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("boost")
    depends_on("nusimdata")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("geant4 cxxstd=20", when="cxxstd=20")
    depends_on("geant4 cxxstd=17", when="cxxstd=17")
    depends_on("messagefacility")
    depends_on("pythia8")
    depends_on("root")

    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
        ]

    def setup_build_environment(self, spack_env):
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Cleanup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        run_env.prepend_path("FHICL_FILE_PATH", self.prefix.fcl)
        # Cleanup.
        sanitize_environments(run_env)

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


class Nurandom(CMakePackage):
    """Random number generator interfaces to art."""

    git = "https://github.com/NuSoftHEP/nurandom.git"
    homepage = git
    url = "https://github.com/NuSoftHEP/nurandom/archive/refs/tags/1.11.04.tar.gz"
    list_url = "https://github.com/NuSoftHEP/nurandom/tags"

    version("1.11.04", sha256="bbd9b5b8773e640d84ce7e92b40812221f6419a0a5eead9da1d93eebbe54d6b4")
    version("1.10.02", sha256="9010dc663d08ee3c7451a7c423f2350a77fe98f3de8bfd4cbd9a5bdcb67c6114")
    version("develop", branch="develop", get_full_repo=True)

    def url_for_version(self, version):
        if version < Version("1.11.03"):
            return github_version_url("NuSoftHEP", "nurandom", f"v{version.underscored}")
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
    depends_on("canvas")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("clhep")
    depends_on("fhicl-cpp")
    depends_on("root")

    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    def setup_build_environment(self, spack_env):
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))
        spack_env.prepend_path("ROOT_INCLUDE_PATH", str(self.prefix.include))
        # Cleanup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        run_env.prepend_path("FHICL_FILE_PATH", self.prefix.fcl)
        # Cleanup.
        sanitize_environments(run_env)

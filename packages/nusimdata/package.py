# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.fnal_art.fnal_github_package import *


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


class Nusimdata(CMakePackage, FnalGithubPackage):
    """Nusimdata"""

    repo = "NuSoftHEP/nusimdata"
    license("Apache-2.0")
    version_patterns = ["v1_24_05", "1.27.02"]

    version("develop", branch="develop", get_full_repo=True)
    version("1.27.02", sha256="ed61e94ef931ed6383299db281c54df82136dfe5331492072ac1a3f08770b6a8")

    variant(
        "cxxstd",
        default="17",
        values=("17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    # Build and link dependencies.
    depends_on("cetmodules", type="build")

    depends_on("canvas")
    depends_on("canvas-root-io")
    depends_on("cetlib-except")
    depends_on("dk2nudata")
    depends_on("nufinder", when="@1.27.02:")
    depends_on("root")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    def setup_build_environment(self, build_env):
        build_env.prepend_path("LD_LIBRARY_PATH", self.spec["root"].prefix.lib)
        build_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Cleanup.
        sanitize_environments(build_env)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Cleanup.
        sanitize_environments(run_env)

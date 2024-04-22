# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


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


class Nugen(CMakePackage, FnalGithubPackage):
    """Generator interfaces to art for GENIE and GiBUU."""

    repo = "NuSoftHEP/nugen"
    license("Apache-2.0")
    version_patterns = ["v1_19_06", "1.20.03"]

    version("1.20.06", sha256="ae2ebc347c2e3f6f44c6e43dab3c5f74752c20396824f2fbc0d6a4d55b614df3")
    version("1.19.06", sha256="718c2fb406fbebefd18d8906ca313513dfdd9d0ff4bda7cf6aff842c84f1ca2d")
    version("develop", branch="develop", get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    # Build-only dependencies.
    depends_on("cmake@3.12:", type="build")
    depends_on("cetmodules", type="build")
    depends_on("nufinder", type="build")

    # Build and link dependencies.
    depends_on("art")
    depends_on("art-root-io")
    depends_on("blas")
    depends_on("canvas")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("clhep")
    depends_on("dk2nudata")
    depends_on("dk2nugenie")
    depends_on("fhicl-cpp")
    depends_on("genie")
    depends_on("ifdh-art")
    depends_on("ifdhc")
    depends_on("libxml2")
    depends_on("log4cpp")
    depends_on("messagefacility")
    depends_on("nusimdata")
    depends_on("pythia6")
    depends_on("root+fftw")

    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
            self.define("GENIE_INC", self.spec["genie"].prefix.include),
        ]

    def setup_build_environment(self, build_env):
        build_env.prepend_path("CET_PLUGIN_PATH", Prefix(self.build_directory).lib)
        # Cleanup.
        sanitize_environments(build_env)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Cleanup.
        sanitize_environments(run_env)

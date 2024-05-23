# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


class Nurandom(CMakePackage, FnalGithubPackage):
    """Random number generator interfaces to art."""

    repo = "NuSoftHEP/nurandom"
    license("Apache-2.0")
    version_patterns = ["v1_10_02", "1.11.03"]

    version("1.11.05", sha256="752d3b27073915e8e609d7a50821285359f3f4a5082786955f8c7d7a134396e9")
    version("1.11.04", sha256="0535d786322ee87c203b722726e50ee48a1ee8f5d110bb1afd28ac1cfb2c5b4b")
    version("1.11.03", sha256="a2e12f8c9a205ede46ce9152f80bbbd50d3393531b8a752434222d52052cc282")
    version("1.10.02", sha256="9010dc663d08ee3c7451a7c423f2350a77fe98f3de8bfd4cbd9a5bdcb67c6114")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    # Build-only dependencies.
    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("canvas")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("clhep")
    depends_on("fhicl-cpp")
    depends_on("messagefacility")
    depends_on("root")

    with when("@:1.11.04"):
        depends_on("boost +filesystem")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @sanitize_paths
    def setup_build_environment(self, build_env):
        build_env.prepend_path("CET_PLUGIN_PATH", Prefix(self.build_directory).lib)

    @sanitize_paths
    def setup_run_environment(self, run_env):
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        run_env.prepend_path("FHICL_FILE_PATH", self.prefix.fcl)

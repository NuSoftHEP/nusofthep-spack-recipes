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

    version("1.11.05", sha256="547b4843ad2e0106a33d138f6312e1c6d087b556697e059bb5d12893896ff9a7")
    version("1.11.04", sha256="bbd9b5b8773e640d84ce7e92b40812221f6419a0a5eead9da1d93eebbe54d6b4")
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
        build_env.prepend_path("ROOT_INCLUDE_PATH", str(self.prefix.include))

    @sanitize_paths
    def setup_run_environment(self, run_env):
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        run_env.prepend_path("FHICL_FILE_PATH", self.prefix.fcl)

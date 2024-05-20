# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.fnal_art.fnal_github_package import *


class Nusimdata(CMakePackage, FnalGithubPackage):
    """Nusimdata"""

    repo = "NuSoftHEP/nusimdata"
    license("Apache-2.0")
    version_patterns = ["v1_24_05", "1.27.02"]

    version("develop", branch="develop", get_full_repo=True)
    version("1.28.06", sha256="da5c30b230b37f546612429688e3b4195bdd7b49beccf1f5001ed49cab8717c5")
    version("1.28.05", sha256="edfc013a790e6f8633088931cd54b7a60adeb4197c87849c3cad124c3dfade9c")
    version("1.28.04", sha256="43b2e51708a295c7a8a4c4cf7ad4cb86741e1f086470b6ed15659ce4c5fb02e1")
    version("1.28.03", sha256="b81590e2822421fc3f9a8849e57107f90a3f254334da25b1db03140ec2a2701d")
    version("1.27.02", sha256="ed61e94ef931ed6383299db281c54df82136dfe5331492072ac1a3f08770b6a8")

    cxxstd_variant("17", "20", default="17")

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

    @sanitize_paths
    def setup_build_environment(self, build_env):
        build_env.prepend_path("LD_LIBRARY_PATH", self.spec["root"].prefix.lib)
        build_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)

    @sanitize_paths
    def setup_run_environment(self, run_env):
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)

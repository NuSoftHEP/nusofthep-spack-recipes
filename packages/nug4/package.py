# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class Nug4(CMakePackage, FnalGithubPackage):
    """Geant4 interface from NuTools"""

    repo = "NuSoftHEP/nug4"
    license("Apache-2.0")
    version_patterns = ["v1_15_02", "1.16.03"]

    version("1.16.06", sha256="afee7472150df82121992db3f5b549f05a013e40debb491bff54c123e1944c37")
    version("1.16.05", sha256="91d5cf3bfed7206e92193582b4dca48e9089042b959c088666c5c83cedbf0e56")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    # Build-only dependencies.
    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("boost")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("clhep")
    depends_on("geant4 cxxstd=17", when="cxxstd=17")
    depends_on("geant4 cxxstd=20", when="cxxstd=20")
    depends_on("messagefacility")
    depends_on("nusimdata")
    depends_on("pythia8")
    depends_on("root")

    with when("@:1.16.05"):
        depends_on("art-root-io")
        depends_on("canvas-root-io")

    @cmake_preset
    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
        ]

    @sanitize_paths
    def setup_run_environment(self, run_env):
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        run_env.prepend_path("FHICL_FILE_PATH", self.prefix.fcl)

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Nug4(CMakePackage, FnalGithubPackage):
    """Geant4 interface from NuTools"""

    repo = "NuSoftHEP/nug4"
    git = "https://github.com/%s" % repo
    license("Apache-2.0")
    version_patterns = ["v1_15_02", "1.16.03"]

    version("1.19.02", sha256="b952d7c3ce3d1c0672c9f3317f80a77fe59c35a13ec20f29f136c71f94b91e3a")
    version("1.19.01", sha256="1855630ae8959de0d37c3177d3eed14fc44216af34ea8e14732acf91762537df")
    version("1.19.00", sha256="c76ba8e5023e141387c6c1ed5cb8184c1b78ee6159a66fcd00419bbbf88dad45")
    version("1.18.03", sha256="3953c2b415771842194ffc6c6300a7b3bd58a04ffceb2f941bdc7247c700e1cd")
    version("1.18.00", sha256="4f8cdc22a303040156274b7e603d8edcda57ce6362bb9778fdda6092b65bc4ce")
    version("1.17.04", sha256="440e7c0e1adcd1da33d532d01307d73e4730506a6dca6a443b4c5491cb4b9918")
    version("1.17.03", sha256="20eab958a46d7ba0ee75ec05142090185abff2eb5e988568c1a12112acb8629a")
    version("1.17.02", sha256="357ecb889fa67de6270918c05845dcef3c85f9b99a21ea2345c91fb1a851d625")
    version("1.16.09", sha256="e12e817ea81fc933e2cff68d05020e9ec081bc0e7decda67533bcb18655ebea7")
    version("1.16.08", sha256="f19d4b170c0f5b2a36ee315d6681b6faa8500b513a91f5ba3f06d1ad7925745d")
    version("1.16.06", sha256="afee7472150df82121992db3f5b549f05a013e40debb491bff54c123e1944c37")
    version("1.16.05", sha256="91d5cf3bfed7206e92193582b4dca48e9089042b959c088666c5c83cedbf0e56")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # Build-only dependencies.
    depends_on("cetmodules", type="build")
    depends_on("nufinder", type="build")

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

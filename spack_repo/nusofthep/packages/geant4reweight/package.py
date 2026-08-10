# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Geant4reweight(CMakePackage, FnalGithubPackage):
    """Repository for implementing reweighting of Pion Scattering as simulated by Geant4"""

    repo = "NuSoftHEP/Geant4Reweight"
    git = "https://github.com/%s" % repo
    version_patterns = ["v01_20_00", "01.20.05"]

    version("develop", branch="develop")
    version("01.23.02", sha256="464db519e27ae7d8b7d82ce4808dcdde883fe4278cb095fa5e61a9d48e28e262")
    version("01.23.01", sha256="a5eb94eab7ebf90b7f31ad485fafafa77a55b9719054c4c7417f9f7e9fb8ffbb")
    version("01.23.00", sha256="40d6c2f06bfb21c4885751b9f4678f5ee5048007c8fab9d23f7b68545435b5af")
    version("01.22.03", sha256="5da0ad74bc24452a63faca64443bd8fde8634504d17c599b25578c5731d93b42")
    version("01.22.02", sha256="c7426cc44bd04e304310432cd1432c5da4e5d9ce8bb80b2fb088b3018920ffa4")
    version("01.21.04", sha256="18254bb1dfa0e31efc9fc5a15f9b17d5a91ae3ac4cc4951f0a2413007c90653a")
    version("01.21.03", sha256="65b6511339ef341b52cd6ff81dc9eb5c65c4bba73a91c048a633d382ed660770")
    version("01.21.02", sha256="674751cd303df72c1e5f9a6ab14362782ec911773053c74d0f5a29298eef14dd")
    version("01.20.13", sha256="a9357ebd25c0ad396730ea19ab4a913bd7ed7447160354479e8c600431d96932")
    version("01.20.12", sha256="966125455c62e37ba9f226ff7b6b326a7d41c02b35b39ca4f49ba5570c6b9f81")
    version("01.20.11", sha256="b807985685d5cb6c1df3cc3e9a9dcadd8589515fcb88b22891f9546cb457478b")
    version("01.20.05", sha256="338aecfa71483a1a22c403f63f143ad08721ad4679d64bf1e7c058ba0cf92414")
    version("01.20.00", sha256="f8d30f2a1426ee9e100694d4d19d58a7b98af93c8e71ff0a52cb0a1e7a6d3d96")
    version("01.16.05", sha256="23417293c2bb5663bbe26398c622c08052563febf396fd7513e9c8536687c6e8")

    # experiment versions
    variant("experiment", default="lar", description="Experiment variants",
            values=("lar", "nova"), multi=False)
    requires("experiment=nova", when="@01.22.02")
    requires("experiment=lar", when="@01.21.02")
    requires("experiment=lar", when="@01.20.00")
    requires("experiment=nova", when="@01.16.05")

    # patches
    patch("patch/v01-16-05.p", when="@01.16.05")

    cxxstd_variant("17", "20", default="17")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cetmodules")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("fhicl-cpp")
    depends_on("geant4")
    depends_on("root")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

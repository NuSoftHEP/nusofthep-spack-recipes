# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class Geant4reweight(CMakePackage, FnalGithubPackage):
    """Repository for implementing reweighting of Pion Scattering as simulated by Geant4"""

    repo = "NuSoftHEP/Geant4Reweight"
    version_patterns = ["v01_20_00", "01.20.05"]

    version("01.20.00", sha256="f8d30f2a1426ee9e100694d4d19d58a7b98af93c8e71ff0a52cb0a1e7a6d3d96")

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("fhicl-cpp")
    depends_on("geant4")
    depends_on("root")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

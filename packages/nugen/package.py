# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


class Nugen(CMakePackage, FnalGithubPackage):
    """Generator interfaces to art for GENIE and GiBUU."""

    repo = "NuSoftHEP/nugen"
    license("Apache-2.0")
    version_patterns = ["v1_19_06", "1.20.03"]

    version("1.21.02", sha256="11dfa220c53c7d6c7593a84e3e37f3af44964e3461c111667c40a341095a6e80")
    version("1.21.00", sha256="84fab7eabe96a408c5927d6d948021866a8fcc7a1b6e342bce6ea5aaad9570f4")
    version("1.20.07", sha256="d8de1e474189e8030f00f0b1c35dc11625d45e9cd902b048bf46b0956fc52f83")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    # Build-only dependencies.
    depends_on("cmake@3.19:", type="build")
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
    depends_on("gsl")
    depends_on("ifdh-art")
    depends_on("lhapdf")
    depends_on("libxml2")
    depends_on("log4cpp")
    depends_on("messagefacility")
    depends_on("nusimdata")
    depends_on("pythia6")
    depends_on("root+fftw")

    # Conditional dependencies.
    depends_on("canvas-root-io", when="@:1.20.06")
    depends_on("postgresql", when="@:1.19.06")

    @cmake_preset
    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
            self.define("GENIE_INC", self.spec["genie"].prefix.include),
        ]

    @sanitize_paths
    def setup_run_environment(self, run_env):
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)

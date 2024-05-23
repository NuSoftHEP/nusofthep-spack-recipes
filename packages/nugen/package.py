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

    version("1.21.00", sha256="84fab7eabe96a408c5927d6d948021866a8fcc7a1b6e342bce6ea5aaad9570f4")
    version("1.20.07", sha256="d8de1e474189e8030f00f0b1c35dc11625d45e9cd902b048bf46b0956fc52f83")
    version("1.20.06", sha256="ae2ebc347c2e3f6f44c6e43dab3c5f74752c20396824f2fbc0d6a4d55b614df3")
    version("1.20.04", sha256="a9a54cb89cb216b7c10cac69c3c184c0d43aec06742788df021d0840c3adc0fc")
    version("1.20.03", sha256="0866f147f56090c6eb5033007be38cdc696e60679294c2941612b647e1131f30")
    version("1.19.06", sha256="718c2fb406fbebefd18d8906ca313513dfdd9d0ff4bda7cf6aff842c84f1ca2d")
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

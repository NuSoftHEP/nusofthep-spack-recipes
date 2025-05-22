# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class Nuevdb(CMakePackage, FnalGithubPackage):
    """Nuevdb"""

    repo = "NuSoftHEP/nuevdb"
    license("Apache-2.0")
    version_patterns = ["v1_08_01", "1.09.03"]

    version("develop", branch="develop", get_full_repo=True)
    version("1.09.08", sha256="bc949e57ecc9a1658606decd884dc736fa130539d746211231d9b9a60a18a745")

    cxxstd_variant("17", "20", default="17")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("art-root-io")
    depends_on("boost+date_time")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("libwda")
    depends_on("nusimdata")
    depends_on("postgresql")
    depends_on("root")

    with when("@:1.09.07"):
        depends_on("canvas-root-io")
        depends_on("boost +filesystem +regex +thread")

    @cmake_preset
    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
            self.define("libwda_DIR:PATH", self.spec["libwda"].prefix),
        ]

    @sanitize_paths
    def setup_run_environment(self, run_env):
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)

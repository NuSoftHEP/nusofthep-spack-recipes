# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Nuevdb(CMakePackage, FnalGithubPackage):
    """Nuevdb"""

    repo = "NuSoftHEP/nuevdb"
    git = "https://github.com/%s" % repo
    license("Apache-2.0")
    version_patterns = ["v1_08_01", "1.09.03"]

    version("develop", branch="develop", get_full_repo=True)
    version("1.09.10", sha256="ea6daafd2faaa5160b7b85253fec422408c0a37c1fef6cc408b273df1fb28ff7")
    version("1.09.09", sha256="cd9d87f2dbb050e5f8fc0d23a6b955763003a58d78a50e036a0b73072934064d")
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

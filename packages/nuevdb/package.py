# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


def sanitize_environments(*args):
    for env in args:
        for var in (
            "PATH",
            "CET_PLUGIN_PATH",
            "LDSHARED",
            "LD_LIBRARY_PATH",
            "DYLD_LIBRARY_PATH",
            "LIBRARY_PATH",
            "CMAKE_PREFIX_PATH",
            "ROOT_INCLUDE_PATH",
        ):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Nuevdb(CMakePackage, FnalGithubPackage):
    """Nuevdb"""

    repo = "NuSoftHEP/nuevdb"
    license("Apache-2.0")
    version_patterns = ["v1_08_01", "1.09.03"]

    version("develop", branch="develop", get_full_repo=True)
    version("1.09.07", sha256="f4ff8c0fb3b9d909af4bb99f68d01b7b3448661825f448adf4afe85517e62507")
    version("1.08.01", sha256="5bbf54e6c772e8f73e8ad2f7629f47e8b15731dd7af80c51b2060976c8c7a013")

    variant(
        "cxxstd",
        default="17",
        values=("17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

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
        # Dependencies removed from @develop
        depends_on("canvas-root-io")
        depends_on("boost +filesystem +regex +thread")

    @cmake_preset
    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
            self.define("libwda_DIR:PATH", self.spec["libwda"].prefix),
        ]

    def setup_build_environment(self, build_env):
        build_env.prepend_path("PATH", Prefix(self.build_directory).bin)
        build_env.prepend_path("CET_PLUGIN_PATH", Prefix(self.build_directory).lib)
        # Cleanup.
        sanitize_environments(env)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Cleanup.
        sanitize_environments(run_env)

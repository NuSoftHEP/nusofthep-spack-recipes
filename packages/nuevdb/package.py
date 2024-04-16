# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *
from spack.pkg.fnal_art.utilities import *


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


class Nuevdb(CMakePackage):
    """Nuevdb"""

    git = "https://github.com/NuSoftHEP/nuevdb.git"
    homepage = git
    url = "https://github.com/NuSoftHEP/nuevdb/archive/refs/tags/1.09.07.tar.gz"
    list_url = "https://github.com/NuSoftHEP/nuevdb/tags"

    version("1.09.07", sha256="f4ff8c0fb3b9d909af4bb99f68d01b7b3448661825f448adf4afe85517e62507")
    version("1.08.01", sha256="5bbf54e6c772e8f73e8ad2f7629f47e8b15731dd7af80c51b2060976c8c7a013")
    version("develop", branch="develop", get_full_repo=True)

    def url_for_version(self, version):
        if version < Version("1.09.03"):
            return github_version_url("NuSoftHEP", "nuevdb", f"v{version.underscored}")
        else:
            return super().url_for_version(version)

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

    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
            self.define("libwda_DIR:PATH", self.spec["libwda"].prefix),
        ]

    def setup_build_environment(self, spack_env):
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))
        # Cleanup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PATH", os.path.join(self.prefix, "bin"))
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Cleanup.
        sanitize_environments(run_env)

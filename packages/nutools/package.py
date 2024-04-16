# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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


class Nutools(CMakePackage):
    """Nutools"""

    git = "https://github.com/NuSoftHEP/nutools.git"
    homepage = git
    url = "https://github.com/NuSoftHEP/nutools/archive/refs/tags/3.15.04.tar.gz"
    list_url = "https://github.com/NuSoftHEP/nutools/tags"

    version("3.16.05", sha256="030cad7d6b7d8c079543203ef5c60292c961d5cc8f6acfd16e360209adda6a0c")
    version("3.15.04", sha256="9f145338854ae1bbcfbbbd7f56fd518663cfd0e2279520c31649ad1b71d4d028")
    version("develop", branch="develop", get_full_repo=True)

    def url_for_version(self, version):
        if version < Version("3.16.03"):
            return github_version_url("NuSoftHEP", "nutools", f"v{version.underscored}")
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
    depends_on("cry")
    depends_on("nusimdata")
    depends_on("perl")

    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
        ]

    def setup_build_environment(self, spack_env):
        # Cleaup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PATH", self.prefix.bin)
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Cleaup.
        sanitize_environments(run_env)

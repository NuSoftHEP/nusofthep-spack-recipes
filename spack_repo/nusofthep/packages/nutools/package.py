# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Nutools(CMakePackage, FnalGithubPackage):
    """Nutools"""

    repo = "NuSoftHEP/nutools"
    git = "https://github.com/%s" % repo
    license("Apache-2.0")
    version_patterns = ["v3_15_04", "3.16.03"]

    version("3.22.01", sha256="8313e85790fb998874d3f4b3eaefe6dd34a30e2b8cc839fc15a0d3e975c21157")
    version("3.22.00", sha256="5f74fa96d4164eec4db8e0eb5e873da2fff6db49689b1d4e097c4d1c41c18095")
    version("3.20.01", sha256="ab7276c58eb17911719af7948ee6304dcd7668314f1e943bf5949f57f99767ed")
    version("3.19.02", sha256="a1429623215a64b2db74f573b5e12f6488a71a9b0bd5eb5eceb4a2da27e6ca88")
    version("3.19.01", sha256="db412e148b90731903ea6458775f072488f1fbab70a94ce8ae5921c0b75bbc97")
    version("3.17.01", sha256="6f517b7436690ce8b1d43cc9929d59bba061e993ac0ae3274712be3978366bd3")
    version("3.17.00", sha256="48b6be64291411d27878da5010415564fd658ecffc72e617fb8a11579ecaed0b")
    version("3.16.06", sha256="f540be7b30eec357c5f65260be6da3ce6988e5b193c58770baaa36a913a513ac")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("art-root-io")
    depends_on("cry")
    depends_on("nusimdata")
    depends_on("perl")

    @cmake_preset
    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
        ]

    @sanitize_paths
    def setup_run_environment(self, run_env):
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)

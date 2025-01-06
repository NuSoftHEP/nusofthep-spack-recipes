# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class Nufinder(CMakePackage, FnalGithubPackage):
    """CMake package finding macros for nutools suite"""

    repo = "NuSoftHEP/nufinder"
    version_patterns = ["v1_00_00", "1.02.01"]

    maintainers = ["marcmengel", "nusense"]
    depends_on("cetmodules", type="build")

    version("1.02.01", sha256="e20cd0c5e23b70f4889b79fca01fed91cff532d66dfbeb9e25f4c93a2fdda8e2")
    version("develop", branch="develop", get_full_repo=True)

# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nufinder(CMakePackage):
    """CMake package finding macros for nutools suite"""

    homepage = "https://github.com/NuSoftHEP/nufinder"
    git = "https://github.com/NuSoftHEP/nufinder.git"
    url = "https://github.com/NuSoftHEP/nufinder/archive/refs/tags/v1_01_02.tar.gz"

    maintainers = ["marcmengel", "nusense"]
    depends_on("cetmodules", type="build")

    version("1_01_02", sha256="07cb659967012399bbde27ac5cdf4188d71edfb685d7b6f6bc1d24ff4a7bd987")
    version("develop", branch="develop", get_full_repo=True)

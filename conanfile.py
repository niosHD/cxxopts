from conans import ConanFile, CMake, tools
import os
import re
import sys

# parse the version from the cxxopts.hpp file
def get_version():
    header_path = os.path.join(os.path.dirname(__file__), "include", "cxxopts.hpp")
    if not os.path.isfile(header_path):
        return None
    with open(header_path, 'r') as myfile:
        data = myfile.read()
    version = []
    for x in ['MAJOR', 'MINOR', 'PATCH']:
        component = re.search("#define CXXOPTS__VERSION_%s\s+([^\s]+)" % x, data)
        if component:
            version.append(component.group(1))
    if len(version) > 0:
        return ".".join(version)
    return None

class Cxxopts(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'
    name = 'cxxopts'
    url = 'https://github.com/jarro2783/cxxopts'
    license = 'MIT'
    version = get_version()
    no_copy_source = True
    scm = {
        "type": "git",
        "url": "auto",
        "revision": "auto"
    }

    def build(self):
        run_tests = not tools.cross_building(self.settings)

        cmake = CMake(self)
        cmake.definitions["CXXOPTS_BUILD_EXAMPLES"] = False
        cmake.definitions["CXXOPTS_BUILD_TESTS"] = run_tests
        cmake.configure()
        cmake.build()
        if run_tests:
            cmake.test()
        cmake.install()

    def package_id(self):
        self.info.header_only()

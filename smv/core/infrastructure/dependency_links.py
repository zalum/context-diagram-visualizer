import setuptools
import setup


class download(setuptools.Command):
    description = "A custom command to load the Model Schema."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("loading schema {}".format(self))
        print("downloading following dependencies {}", setup.dependency_links)
from unittest import TestCase

from smv.core.infrastructure.system_model_output import PlantUmlLocalRenderer


class Test(TestCase):

    def test_trim_png(self):
        #given
        untrimmed_image = self.read_image("untrimmed.png")

        #when
        result = PlantUmlLocalRenderer._trim_left_png(untrimmed_image)

        #then
        self.assertIsNotNone(result)
        self.assertEqual(result,self.read_image("trimmed.png"))

    def read_image(self, path):
        file = open(path, "rb")
        return file.read()

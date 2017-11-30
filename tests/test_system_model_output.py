import smv.system_model_output as smo
from unittest import TestCase
import io


class Test(TestCase):

    def test_trim_png(self):
        #given
        untrimmed_image = self.read_image("untrimmed.png")

        #when
        result = smo.trim_left_png(untrimmed_image)

        #then
        self.assertIsNotNone(result)
        self.assertEqual(result,self.read_image("trimmed.png"))


    def read_image(self,path):
        file = open(path, "rb")
        return file.read()

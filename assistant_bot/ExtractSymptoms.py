from PIL import Image
import pandas as pd
import logging
from OCR.ocr import pyTesseractOCR
from entity_extraction.extractor_medcat import SymptomExtractor

get_ocr_data = pyTesseractOCR()
symp_extr = SymptomExtractor()

FILE_TYPE = ["jpg", "jpeg"]

class Extract:

    def __init__(self) -> None:
        pass

    def _validatefile(self):
        """
        Validate Filetype as jpeg or jpg
        """
        return all(
            [
                str(infilepath).lower().split(".")[-1] in FILE_TYPE
                for infilepath in self.images
            ]
        )
    
    def get_symptoms(self, img):
        self.img = img
        self.img = Image.open(self.img)

        ocr_data = get_ocr_data.extract(self.img)

        ents = symp_extr.extractSymptom(ocr_data)


        return ents

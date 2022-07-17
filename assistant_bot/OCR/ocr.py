#####################################################################
# Copyright(C), 2022 IHX Private Limited. All Rights Reserved
# Unauthorized copying of this file, via any medium is
# strictly prohibited
#
# Proprietary and confidential
# email: care@ihx.in
#####################################################################

import json
import traceback
import pytesseract
from PIL import Image
from pytesseract import Output
import pandas as pd
import logging

class pyTesseractOCR:
    def __init__(self):
        
        self.client = None
        self.form_path = None
        self.text = None
        self._config()

    def _config(self) -> None:
        self.custom_config = r"--oem 1 --psm 6"

    def extract(
        self, imageBytes, postprocess: bool = True, outfilepath: str = None
    ) -> str:
        """
        Main function that performs OCR extraction
        """
        # print("Running local pyTesseract OCR")
        try:
            # tesseract needs the right channel order
            # cropped_rgb = cv2.cvtColor(imageBytes, cv2.COLOR_BGR2RGB)

            # give the numpy array directly to pytesseract, no PIL or other acrobatics necessary
            # Results = pytesseract.image_to_string(cropped_rgb, lang="eng")
            # img_tesseract = Image.fromarray(imageBytes)
            self.img_width, self.img_height = imageBytes.size
            response = pytesseract.image_to_string(
                imageBytes, config=self.custom_config
            )
            # save the response json as file
            if outfilepath:
                with open(outfilepath, "w") as f:
                    json.dump(response, f)
            else:
                pass
        except:
            logging.info("TESSERACT_OCR_FAILURE")
        return response.lower()

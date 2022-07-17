from medcat.cat import CAT
import logging
import os


class SymptomExtractor:
    def __init__(self):
        self.cat = CAT.load_model_pack(
            os.path.join(os.getcwd(), "models", "medmen_wstatus_2021_oct.zip")
        )

    def validate(self, text):
        self.text = text
        return isinstance(self.text, str) and len(self.text) > 0

    def extractSymptom(self, text):
        self.text = text

        resp = []

        if not self.validate(self.text):
            logging.warning("Please enter valid text...")
        else:
            entities = self.cat.get_entities(text)

            prev_ent_type = ""
            prev_ent = ""
            prev_ent_ind = 0

            for i in entities["entities"]:

                ent = entities["entities"][i]
                if ent["types"][0] == "Sign or Symptom":
                    if prev_ent_type == "Qualitative Concept" and prev_ent_ind == i - 1:
                        resp.append({"Symptom": prev_ent + " " + ent["detected_name"]})
                    else:
                        resp.append({"Symptom": ent["source_value"]})

                elif ent["types"][0] == "Temporal Concept":
                    if prev_ent_type == "Sign or Symptom" and prev_ent_ind == i - 1:
                        resp[-1]["Duration"] = ent["source_value"]

                prev_ent_type = ent["types"][0]
                prev_ent = ent["detected_name"]
                prev_ent_ind = i

            return resp

import pandas as pd
import os

class GetICD:
    def __init__(self) -> None:
        
        self.df_vocab = pd.read_csv(
            os.path.join(os.getcwd(), 'artifacts',"CONCEPT.csv")
        )

        self.df_SNOMED_to_ICD_mapping = pd.read_csv(
            os.path.join(os.getcwd(), "artifacts", "tls_Icd10cmHumanReadableMap_US1000124_20200901.tsv"),
            sep="\t",
        )

        # select the mapCategoryName only if "MAP SOURCE CONCEPT IS PROPERLY CLASSIFIED"
        self.df_SNOMED_to_ICD_mapping = self.df_SNOMED_to_ICD_mapping[
            (
                self.df_SNOMED_to_ICD_mapping["mapCategoryName"]
                == "MAP SOURCE CONCEPT IS PROPERLY CLASSIFIED"
            )
        ].reset_index(drop=True)

        # select only two columns
        self.df_SNOMED_to_ICD_mapping = self.df_SNOMED_to_ICD_mapping[
            ["referencedComponentId", "mapTarget"]
        ]

        # replace . with empty and ? with A
        self.df_SNOMED_to_ICD_mapping["ICD_10_Dx"] = self.df_SNOMED_to_ICD_mapping[
            "mapTarget"
        ].str.replace("\?", "A")

        # drop nan
        self.df_SNOMED_to_ICD_mapping = self.df_SNOMED_to_ICD_mapping.dropna(
            subset=["ICD_10_Dx"]
        )

        # merge multiple rows into single row
        self.df_SNOMED_to_ICD_mapping = (
            self.df_SNOMED_to_ICD_mapping.groupby("referencedComponentId")
            .agg(lambda x: tuple(x))
            .applymap(list)
            .reset_index()
        )

        # convert to 'str' and assign columns name as "concept_code_Dx" (SNOMED code)
        self.df_SNOMED_to_ICD_mapping[
            "concept_code_Dx"
        ] = self.df_SNOMED_to_ICD_mapping["referencedComponentId"].apply(
            lambda x: str(x)
        )

        # select columns "concept_code_Dx" and "ICD_10_Dx"
        self.df_SNOMED_to_ICD_mapping = self.df_SNOMED_to_ICD_mapping[
            ["concept_code_Dx", "ICD_10_Dx"]
        ]

    def get(self, entity):
        try:
            
            self.entity = entity

            concept_code = self.df_vocab_snomed[
                (self.df_vocab_snomed["concept_name"] == self.entity)
            ]["concept_code"].values[0]

            icd = self.df_SNOMED_to_ICD_mapping[
                self.df_SNOMED_to_ICD_mapping["concept_code_Dx"] == concept_code
            ]["ICD_10_Dx"].values[0]

            return icd
        except:
            return ''

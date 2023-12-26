import pandas as pd

from process_nitta.csv_config import CSVConfig
from process_nitta.models import Base


class IRNICOLETSample(Base):
    def get_result_df(self) -> pd.DataFrame:
        df: pd.DataFrame = pd.read_csv(
            self.file_path,
            **CSVConfig().IR_NICOLET().to_dict(),
        )
        return df

import pandas as pd
from pybaselines import Baseline

from .csv_config import ColumnStrEnum as col
from .csv_config import CSVConfig
from .models import Base


class RamanSample(Base):
    def baseline_correction(
        self, df: pd.DataFrame, lam: float = 1e7, p: float = 0.02
    ) -> pd.DataFrame:
        df = df.copy()
        baseline_fitter = Baseline(df[col.RAMAN_SHIFT].values, check_finite=False)
        bkg = baseline_fitter.asls(df[col.INTENSITY], lam=lam, p=p)[0]
        df[col.INTENSITY] = df[col.INTENSITY] - bkg
        return df

    def get_result_df(self, lam: float = 1e7, p: float = 0.02) -> pd.DataFrame:
        return self.baseline_correction(
            pd.read_csv(self.file_path, **CSVConfig().Raman().to_dict()),
            lam=lam,
            p=p,
        )

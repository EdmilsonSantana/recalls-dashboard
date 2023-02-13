import pandas as pd
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'

class Recalls(object):
    def __init__(self) -> None:
        self.df = pd.read_csv('data/recalls.csv', parse_dates=['REPORTED_DATE'])
        self.filtered = None

    def recalls_count(self) -> int:
        return self.get_data()['RECALL_ID'].unique().shape[0]

    def vehicle_models_count(self) -> int:
        return self.get_data()[['VEHICLE_MODEL', 'VEHICLE_YEAR']].drop_duplicates().shape[0]

    def affected_units_count(self) -> str:
        df_affected_units = self.get_data()[['RECALL_ID', 'AFFECTED_UNITS']].drop_duplicates()
        affected_units = df_affected_units['AFFECTED_UNITS'].sum()
        return f'{affected_units:,}'

    def manufacturers(self) -> list:
        return ['-'] + self.get_data()['MANUFACTURER'].unique().tolist()

    def filter_by(self, time_range: tuple, manufacturer: str) -> None:
        start_date = datetime.strptime(time_range[0], DATE_FORMAT)
        end_date = datetime.strptime(time_range[1], DATE_FORMAT)

        self.filtered = self.df[self.df['REPORTED_DATE'].between(start_date, end_date)]

        if (manufacturer != '-'):
            self.filtered = self.filtered[self.filtered['MANUFACTURER'] == manufacturer]

    def get_data(self) -> pd.DataFrame:
        return self.filtered if self.filtered is not None else self.df
    
    def get_component_category_count(self) -> pd.Series:
        return self.get_data()[['RECALL_ID', 'COMPONENT_CATEGORY']].drop_duplicates()['COMPONENT_CATEGORY'].value_counts()

    def get_recalls_grouped_by_month_and_year(self) -> pd.Series:
        reported_recalls = self.get_data()[['RECALL_ID', 'REPORTED_DATE']].drop_duplicates()
        reported_period = reported_recalls['REPORTED_DATE'].dt.to_period("M")
        return reported_recalls.groupby(reported_period).count()['RECALL_ID']
    
    def get_affected_units_grouped_by_month_and_year(self):
        reported_recalls = self.get_data()[['RECALL_ID', 'REPORTED_DATE', 'AFFECTED_UNITS']].drop_duplicates()
        reported_period = reported_recalls['REPORTED_DATE'].dt.to_period("M")
        return reported_recalls[['AFFECTED_UNITS', 'REPORTED_DATE']].groupby(reported_period).sum()['AFFECTED_UNITS']

    def get_recalls_by_manufacturers(self, reported_date: datetime, limit: int, ) -> pd.DataFrame:
        return self.get_recalls_by('MANUFACTURER', reported_date, limit)

    def get_recalls_by_vehicles(self, reported_date: datetime, limit: int) -> pd.DataFrame:
        return self.get_recalls_by('VEHICLE_MODEL', reported_date, limit)
    
    def get_recalls_by_components(self, reported_date: datetime, limit: int) -> pd.DataFrame:
        return self.get_recalls_by('COMPONENT_NAME', reported_date, limit)
    
    def get_recalls_by(self, by: str, reported_date: datetime, limit: int):
        recalls = self.filter_recalls_by_reported_date(reported_date)[[by, 'RECALL_ID']].drop_duplicates()
        recalls_by = recalls[by].value_counts()
        return recalls_by.head(limit)

    def filter_recalls_by_reported_date(self, reported_date: datetime) -> pd.DataFrame:
        return self.df[self.df['REPORTED_DATE'] >= reported_date]
    
    def get_date_range(self) -> tuple:
        return self.df['REPORTED_DATE'].min().date(), self.df['REPORTED_DATE'].max().date()


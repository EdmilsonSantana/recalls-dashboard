import pandas as pd
from datetime import datetime


class Recalls(object):
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def recalls_count(self) -> int:
        return self.df['RECALL_ID'].unique().shape[0]

    def vehicle_models_count(self) -> int:
        return self.df[['VEHICLE_MODEL', 'VEHICLE_YEAR']].drop_duplicates().shape[0]

    def affected_units_count(self) -> str:
        df_affected_units = self.df[['RECALL_ID',
                                     'AFFECTED_UNITS']].drop_duplicates()
        affected_units = df_affected_units['AFFECTED_UNITS'].sum()
        return f'{affected_units:,}'

    def get_manufacturers(self) -> list:
        return ['-'] + self.df['MANUFACTURER'].unique().tolist()

    def get_vehicle_models(self, manufacturer: str) -> list:
        if (manufacturer == '-'):
            return []
        return ['-'] + self.df[self.df['MANUFACTURER'] == manufacturer]['VEHICLE_MODEL'].unique().tolist()

    def filter_by(self, time_range: tuple, manufacturer: str, vehicle_model: str) -> None:
        date_format = '%Y-%m-%d'
        start_date = datetime.strptime(time_range[0], date_format)
        end_date = datetime.strptime(time_range[1], date_format)

        self.df = self.df[self.df['REPORTED_DATE'].between(
            start_date, end_date)]

        if (manufacturer != '-'):
            self.df = self.df[self.df['MANUFACTURER'] == manufacturer]

        if (vehicle_model != '-'):
            self.df = self.df[self.df['VEHICLE_MODEL'] == vehicle_model]

    def get_recalls_and_affected_units_by_reported_period(self) -> pd.DataFrame:
        reported_recalls = self.get_reported_recalls_and_affected_units()
        reported_period = reported_recalls['REPORTED_DATE'].dt.to_period("M")

        by_affected_units = reported_recalls[['AFFECTED_UNITS', 'REPORTED_DATE']].groupby(
            reported_period).sum(numeric_only=True)['AFFECTED_UNITS']
        by_recalls_count = reported_recalls[['RECALL_ID', 'REPORTED_DATE']].groupby(
            reported_period).count()['RECALL_ID']

        return pd.merge(by_recalls_count, by_affected_units, left_index=True, right_index=True)

    def get_recalls_and_affected_units_by_component(self) -> pd.DataFrame:
        recalls = self.df[['RECALL_ID', 'COMPONENT_CATEGORY',
                           'COMPONENT_NAME', 'AFFECTED_UNITS']].drop_duplicates()

        recalls_by_component = recalls.groupby(
            ['COMPONENT_CATEGORY', 'COMPONENT_NAME']).count().reset_index()

        affected_units_by_component = recalls.groupby(
            ['COMPONENT_CATEGORY', 'COMPONENT_NAME']).sum(numeric_only=True).reset_index()

        recalls_by_component.rename(
            {'RECALL_ID': 'VALUE'}, axis=1, inplace=True)
        recalls_by_component['CHART_TYPE'] = 'A'

        affected_units_by_component.rename(
            {'AFFECTED_UNITS': 'VALUE'}, axis=1, inplace=True)
        affected_units_by_component['CHART_TYPE'] = 'B'

        return pd.concat([recalls_by_component, affected_units_by_component])

    def get_recalls_and_affected_units_by_vehicle(self) -> pd.DataFrame:
        selected_columns = ['RECALL_ID', 'MANUFACTURER',
                            'VEHICLE_MODEL', 'VEHICLE_YEAR', 'AFFECTED_UNITS']
        recalls = self.df[selected_columns].drop_duplicates()

        affected_units_by_vehicle = recalls.groupby(
            ['VEHICLE_MODEL', 'VEHICLE_YEAR']).sum(numeric_only=True)
        recalls_by_vehicle = recalls.groupby(
            ['VEHICLE_MODEL', 'VEHICLE_YEAR']).count()

        recalls_by_vehicle.drop(columns=['AFFECTED_UNITS'], inplace=True)

        return pd.merge(affected_units_by_vehicle, recalls_by_vehicle, left_index=True, right_index=True).reset_index()

    def get_recalls_distribution(self) -> pd.DataFrame:
        selected_columns = ['RECALL_ID', 'MANUFACTURER', 'REPORTED_DATE',
                            'VEHICLE_MODEL', 'VEHICLE_YEAR', 'AFFECTED_UNITS']
        recalls = self.df[selected_columns].drop_duplicates()

        return recalls.groupby(
            ['RECALL_ID', 'MANUFACTURER', 'AFFECTED_UNITS', 'REPORTED_DATE']).count().reset_index()

    def get_reported_recalls_and_affected_units(self) -> pd.DataFrame:
        return self.df[['RECALL_ID', 'REPORTED_DATE', 'AFFECTED_UNITS']].drop_duplicates()

    def get_date_range(self) -> tuple:
        return self.df['REPORTED_DATE'].min().date(), self.df['REPORTED_DATE'].max().date()

    def get_recalls_and_affected_units_by_manufacturer(self):
        vehicles_by_manufacturer = (self.df[['MANUFACTURER', 'VEHICLE_MODEL', 'VEHICLE_YEAR']]
                                    .drop_duplicates()).groupby('MANUFACTURER').count()

        recalls_by_manufacturer = (self.df[['MANUFACTURER', 'RECALL_ID']]
                                   .drop_duplicates()).groupby('MANUFACTURER').count()

        affected_units_by_manufacturer = (self.df[['RECALL_ID', 'MANUFACTURER', 'AFFECTED_UNITS']]
                                          .drop_duplicates()).groupby('MANUFACTURER').sum(numeric_only=True)[['AFFECTED_UNITS']]

        by_manufacturer = pd.merge(
            vehicles_by_manufacturer, recalls_by_manufacturer, left_index=True, right_index=True)
        by_manufacturer = pd.merge(
            by_manufacturer, affected_units_by_manufacturer, left_index=True, right_index=True)

        by_manufacturer.reset_index(inplace=True)
        by_manufacturer.drop(columns='VEHICLE_YEAR', inplace=True)
        by_manufacturer.rename(columns={'MANUFACTURER': 'Manufacturer',
                                        'VEHICLE_MODEL': 'Recalled vehicles',
                                        'RECALL_ID': 'Recalls',
                                        'AFFECTED_UNITS': 'Affected vehicle units'},
                               inplace=True)

        return by_manufacturer.to_dict('records')

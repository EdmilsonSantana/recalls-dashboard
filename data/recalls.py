import pandas as pd
from data.constants import *


class Recalls(object):
    def __init__(self, uploaded_file):
        self.df = pd.read_csv(
            uploaded_file, sep='\t', names=RECALLS_DATASET_COLUMNS, on_bad_lines='warn')

        self.fill_affected_columns()
        self.drop_invalid_recall_ids()
        self.drop_invalid_models()
        self.drop_invalid_recall_type()
        self.parse_component_name()
        self.convert_report_received_date()
        self.drop_invalid_vehicle_year()
        self.upper_case_columns()
        self.create_component_category()
        self.concat_make_and_model()

        self.df = self.df[REQUIRED_DATASET_COLUMNS].drop_duplicates()
        self.df.dropna(inplace=True)
        self.filtered_df = self.df

        nan_count = self.df.isna().sum().sum()
        if nan_count > 0:
            raise Exception(
                "We couldn't clean the uploaded data. Please review the uploaded file")

    def fill_affected_columns(self):
        self.df['POTAFF'].fillna(0, inplace=True)

    def drop_invalid_recall_ids(self):
        invalid_ids = self.df[~self.df['CAMPNO'].str.match(
            VALID_RECALL_ID_PATTERN)].index
        print('Found %d rows with an invalid recall id' % len(invalid_ids))
        self.df.drop(invalid_ids, axis=0, inplace=True)

    def drop_invalid_models(self):
        self.df.drop(self.df[self.df['MODELTXT'] ==
                     'TBD'].index, axis=0, inplace=True)

    def drop_invalid_recall_type(self):
        self.df.drop(self.df[self.df['RCLTYPECD'] !=
                     'V'].index, axis=0, inplace=True)

    def parse_component_name(self):
        self.df['COMPNAME'] = self.df['COMPNAME'].str.split(':').str[0]
        self.df['COMPNAME'] = self.df['COMPNAME'].replace(
            DUPLICATED_COMPONENTS_TYPE)

    def create_component_category(self):
        self.df['COMPNAME_GROUP'] = self.df['COMPNAME'].apply(
            get_component_category)

    def convert_report_received_date(self):
        self.df['RCDATE'] = pd.to_datetime(
            self.df['RCDATE'], format=REPORT_RECEIVED_DATE_FORMAT)

    def drop_invalid_vehicle_year(self):
        self.df['YEARTXT'] = self.df['YEARTXT'].astype(int)
        self.df.drop(self.df[self.df['YEARTXT'] ==
                     UNKNOWN_MODEL_YEAR].index, axis=0, inplace=True)

    def concat_make_and_model(self):
        self.df['VEHICLE'] = self.df[['MAKETXT', 'MODELTXT']].apply(
            lambda row: ' '.join(row.values.astype(str)), axis=1)

    def upper_case_columns(self):
        # self.df['MFGNAME'] = self.df['MFGNAME'].str.upper()
        self.df['MFGTXT'] = self.df['MFGTXT'].str.upper()

    def get_manufacturers(self):
        return self.df['MFGTXT'].unique()

    def get_vehicles_by_manufacturer(self, manufacturer):
        return self.df[self.df['MFGTXT'] == manufacturer]['VEHICLE'].unique()

    def get_date_range(self):
        df_received_date = pd.to_datetime(self.df['RCDATE'])

        first_report_year = int(df_received_date.min().strftime('%Y'))
        last_report_year = int(df_received_date.max().strftime('%Y'))
        return first_report_year, last_report_year

    def filter_by(self, time_range, manufacturer, vehicle):
        query = f'RCDATE.dt.year >= {time_range[0]} & RCDATE.dt.year <= {time_range[1]}'

        if manufacturer is not None:
            query += f' & MFGTXT == "{manufacturer}"'
        
        if vehicle != '-':
            query += f' & VEHICLE == "{vehicle}"'

        self.filtered_df = self.df.query(query)
        return self.filtered_df
    

    # def filter_by(self, manufacturer, vehicle):
    #     self.filtered_df = self.df.query(
    #         '(MFGTXT == @manufacturer) & (VEHICLE == @vehicle)'
    #     )

    #     return self.filtered_df

    def get_data(self):
        return self.filtered_df

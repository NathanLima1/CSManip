"""
import cdsapi

class EcmwfProcessing:
    def __init__(self):
        pass

    def init_dates(self, start_year, start_month, start_day, 
                   end_year, end_month, end_day):
        self.start_year = start_year
        self.start_month = start_month
        self.start_day = start_day
        self.end_year = end_year
        self.end_month = end_month
        self.end_day = end_day
        self.years = [y for y in range(int(start_year), int(end_year))]

    def define_date(self, pattern="yyyy-mm-dd", range=("2001-10-01", "2001-10-03")):
        
        start_date = [range[0].split('-')]
        end_date = [range[1].split('-')]

        if pattern == "yyyy-mm-dd":
            self.init_dates(start_date[0], start_date[1], start_date[2], 
                            end_date[0], end_date[1], end_date[2])
        elif pattern == "dd-mm-yyyy":
            self.init_dates(start_date[2], start_date[1], start_date[0], 
                            end_date[2], end_date[1], end_date[0])
        elif pattern == "mm-dd-yyyy":
            self.init_dates(start_date[2], start_date[0], start_date[1], 
                            end_date[2], end_date[0], end_date[1])
        else:
            print("Error! Pattern of date not supported. Please utilize one of these: " \
            "'yyyy-mm-dd', 'dd-mm-yyyy', 'mm-dd-yyyy'.")

    def download_data(self, range:tuple):
        c = cdsapi.Client()

        for year in self.years:
            print(f"Baixando ano {year}...")
            c.retrieve(
                'era5-land',
                {
                    'format': 'netcdf',
                    'variable': ['2m_temperature'],
                    'year': year,
                    'month': [f'{i:02d}' for i in range(1, 13)] # Arrumar para ir só até a data desejada
                    'day': [f'{i:02d}' for i in range(1, 32)],
                    'time':['00:00'],
                },
                f'era5_land_2m_temp_{year}.nc'
            )
"""
from cdsutils import *
import logging

logger = logging.getLogger(__name__)


# def download():
# 	predicted_dates = p.dates_mapped_to_hours(
# 		upper_bound=datetime(2023, 12, 31, 6)
# 	)


# 	logger.info('dates to download', predicted_dates)
	
# 	all_ds = []
# 	for date, hours in predicted_dates:

# 		all_ds.append(ds)

# 	filename = 'cruft/era5/-20231220-era5.nc'
# 	os.makedirs(os.path.dirname(filename), exist_ok=True)

# 	ds = xarray.concat([d.to_xarray() for d in all_ds], dim='time')
# 	ds.to_netcdf(filename)



if __name__ == '__main__':
	logger.debug('what a good time')

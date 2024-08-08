# # Compute daily transports along contour and save


import cosima_cookbook as cc
import numpy as np
import netCDF4 as nc
import xarray as xr
from gsw import SA_from_SP, p_from_z, sigma1
import sys,os
from pathlib import Path

import logging
logging.captureWarnings(True)
logging.getLogger('py.warnings').setLevel(logging.ERROR)

from dask.distributed import Client
import climtas.nci

if __name__ == '__main__':

	# Start a dask cluster with multiple cores
	climtas.nci.GadiClient()
	#dask_dir = '/scratch/x77/cy8964/dask_dump/dask_dump_'+str(sys.argv[2])+'_'+str(int(sys.argv[1]))+'/'
	#Path(dask_dir).mkdir(parents=True, exist_ok=True)
	#client = Client(local_directory=dask_dir)

	#session = cc.database.create_session('/g/data/e14/pc5520/model_data/access-om2/basal_melt_MOM5/basal_melt_MOM5.db')
	session = cc.database.create_session('/g/data/ik11/databases/basal_melt_MOM5.db')
        #session = cc.database.create_session('/g/data/v45/wf4500/databases/gdata_01deg_jra55v13_ryf9091_DSW.db')
	#session = cc.database.create_session('/g/data/ik11/databases/cosima_master.db')
	#expt = '01deg_jra55v13_ryf9091_DSW_BasalNoGade_NoIcb'
	expt = '01deg_jra55v13_ryf9091_DSW_BasalGade_NoIcb_Brine'
	#expt = '01deg_jra55v13_ryf9091_DSW'
	###############################
	#### get run count argument that was passed to python script ####
	
	month = str(int(sys.argv[1]))
	month = month.zfill(2)

	year = str(sys.argv[2])

	first_year = year
	last_year = year

	start_time=first_year+'-'+month    
	end_time=last_year+'-'+month

	# reference density value:
	rho_0 = 1035.0
	lat_range = slice(-90,-59)
	
	###############################
	# ### Open grid cell width data for domain

	## some grid data is required, a little complicated because these variables don't behave well with some 
	dyt = cc.querying.getvar(expt, 'dyt',session, n=1, ncfile = 'ocean_grid.nc')
	dxu = cc.querying.getvar(expt, 'dxu',session, n=1, ncfile = 'ocean_grid.nc')

	# select latitude range:
	dxu = dxu.sel(yu_ocean=lat_range)
	dyt = dyt.sel(yt_ocean=lat_range)

	###############################
	# ### Open contour data

	isobath_depth = 1000
	outfile = '/g/data/g40/akm157/model_data/access-om2/Antarctic_slope_contour_'+str(isobath_depth)+'m.npz'
	data = np.load(outfile)
	mask_y_transport = data['mask_y_transport']
	mask_x_transport = data['mask_x_transport']
	mask_y_transport_numbered = data['mask_y_transport_numbered']
	mask_x_transport_numbered = data['mask_x_transport_numbered']

	yt_ocean = cc.querying.getvar(expt,'yt_ocean',session,n=1)
	yt_ocean = yt_ocean.sel(yt_ocean=lat_range)
	yu_ocean = cc.querying.getvar(expt,'yu_ocean',session,n=1)
	yu_ocean = yu_ocean.sel(yu_ocean=lat_range)
	xt_ocean = cc.querying.getvar(expt,'xt_ocean',session,n=1)
	xu_ocean = cc.querying.getvar(expt,'xu_ocean',session,n=1)

	# Convert contour masks to data arrays, so we can multiply them later.
	# We need to ensure the lat lon coordinates correspond to the actual data location:
	#       The y masks are used for vhrho, so like vhrho this should have dimensions (yu_ocean, xt_ocean).
	#       The x masks are used for uhrho, so like uhrho this should have dimensions (yt_ocean, xu_ocean).
	#       However the actual name will always be simply y_ocean/x_ocean irrespective of the variable
	#       to make concatenation of transports in both direction and sorting possible.

	mask_x_transport = xr.DataArray(mask_x_transport, coords = [yt_ocean, xu_ocean], dims=['y_ocean', 'x_ocean'])
	mask_y_transport = xr.DataArray(mask_y_transport, coords = [yu_ocean, xt_ocean], dims=['y_ocean', 'x_ocean'])
	mask_x_transport_numbered = xr.DataArray(mask_x_transport_numbered, coords = [yt_ocean, xu_ocean], dims=['y_ocean', 'x_ocean'])
	mask_y_transport_numbered = xr.DataArray(mask_y_transport_numbered, coords = [yu_ocean, xt_ocean], dims=['y_ocean', 'x_ocean'])

	# ### Stack contour data into 1D

	# Create the contour order data-array. Note that in this procedure the x-grid counts have x-grid
	#   dimensions and the y-grid counts have y-grid dimensions, but these are implicit, the dimension 
	#   *names* are kept general across the counts, the generic y_ocean, x_ocean, so that concatening works
	#   but we dont double up with numerous counts for one lat/lon point.

	# stack contour data into 1d:
	mask_x_numbered_1d = mask_x_transport_numbered.stack(contour_index = ['y_ocean', 'x_ocean'])
	mask_x_numbered_1d = mask_x_numbered_1d.where(mask_x_numbered_1d > 0, drop = True)
	mask_y_numbered_1d = mask_y_transport_numbered.stack(contour_index = ['y_ocean', 'x_ocean'])
	mask_y_numbered_1d = mask_y_numbered_1d.where(mask_y_numbered_1d > 0, drop = True)
	contour_ordering = xr.concat((mask_x_numbered_1d,mask_y_numbered_1d), dim = 'contour_index')
	contour_ordering = contour_ordering.sortby(contour_ordering)
	contour_index_array = np.arange(1,len(contour_ordering)+1)
	
	# get lat and lon along contour, useful for plotting later:
	lat_along_contour = contour_ordering.y_ocean
	lon_along_contour = contour_ordering.x_ocean
	# don't need the multi-index anymore, replace with contour count
	lat_along_contour.coords['contour_index'] = contour_index_array
	lon_along_contour.coords['contour_index'] = contour_index_array

	###############################
	# ### Open uhrho, vhrho from daily data

	# Note vhrho_nt is v*dz*1035 and is positioned on north centre edge of t-cell.
	vhrho = cc.querying.getvar(expt,'vhrho_nt',session,ncfile='%daily%')
	uhrho = cc.querying.getvar(expt,'uhrho_et',session,ncfile='%daily%')

	# the coords on regional variables might be wacky, in which case need to do:
	vhrho = vhrho.rename({'yt_ocean_sub01':'yt_ocean', 'xt_ocean_sub01':'xt_ocean'})
	uhrho = uhrho.rename({'yt_ocean_sub01':'yt_ocean', 'xt_ocean_sub01':'xt_ocean'})
	# if meridional length is too long, cut to match:
	vhrho = vhrho[:,:,:len(yt_ocean),:]
	uhrho = uhrho[:,:,:len(yt_ocean),:]
	vhrho.coords['yt_ocean'] = yt_ocean
	uhrho.coords['yt_ocean'] = yt_ocean

	# select latitude range and this month:
	vhrho = vhrho.sel(yt_ocean=lat_range).sel(time=slice(start_time,end_time))
	uhrho = uhrho.sel(yt_ocean=lat_range).sel(time=slice(start_time,end_time))

	# Note that vhrho is defined as the transport across the northern edge of a tracer cell so its coordinates 
	#       should be (yu_ocean, xt_ocean).
	#  uhrho is defined as the transport across the eastern edge of a tracer cell so its coordinates should 
	#       be (yt_ocean, xu_ocean).
	#  However we will keep the actual name as simply y_ocean/x_ocean irrespective of the variable
	#       to make concatenation and sorting possible.
	yt_ocean = dyt.yt_ocean.values
	yu_ocean = dxu.yu_ocean.values
	xu_ocean = dxu.xu_ocean.values
	xt_ocean = dyt.xt_ocean.values
	vhrho.coords['yt_ocean'] = yu_ocean
	uhrho.coords['xt_ocean'] = xu_ocean
	vhrho = vhrho.rename({'yt_ocean':'y_ocean', 'xt_ocean':'x_ocean'})
	uhrho = uhrho.rename({'yt_ocean':'y_ocean', 'xt_ocean':'x_ocean'})

	# ### Convert to transports 

	# First we also need to change coords on dxu, dyt, so we can multiply the transports:
	dyt = dyt.reset_coords().dyt # remove geolon_t/geolat_t coordinates
	dxu = dxu.reset_coords().dxu # remove geolon_t/geolat_t coordinates
	dxu.coords['xu_ocean'] = xt_ocean
	dxu = dxu.rename({'yu_ocean':'y_ocean', 'xu_ocean':'x_ocean'}) 
	dyt.coords['xt_ocean'] = xu_ocean
	dyt = dyt.rename({'yt_ocean':'y_ocean','xt_ocean':'x_ocean'})

	# convert to transports and multiply by contour masks:
	vhrho = vhrho*dxu*mask_y_transport/rho_0
	uhrho = uhrho*dyt*mask_x_transport/rho_0
	
	###############################
	# ### Extract transport values along contour:

	## initiate a empty dataarray
	vol_trans_across_contour = xr.DataArray(np.zeros((len(uhrho.time),len(uhrho.st_ocean),len(contour_index_array))),
											coords = [uhrho.time,uhrho.st_ocean, contour_index_array],
											dims = ['time','st_ocean', 'contour_index'],
											name = 'vol_trans_across_contour')

	# stack transports into 1d and drop any points not on contour:
	x_transport_1d = uhrho.stack(contour_index = ['y_ocean', 'x_ocean'])
	x_transport_1d = x_transport_1d.where(mask_x_numbered_1d>0, drop = True)
	y_transport_1d = vhrho.stack(contour_index = ['y_ocean', 'x_ocean'])
	y_transport_1d = y_transport_1d.where(mask_y_numbered_1d>0, drop = True)

	# combine all points on contour:
	vol_trans_across_contour = xr.concat((x_transport_1d, y_transport_1d), dim = 'contour_index')
	vol_trans_across_contour = vol_trans_across_contour.sortby(contour_ordering)
	vol_trans_across_contour.coords['contour_index'] = contour_index_array
	vol_trans_across_contour = vol_trans_across_contour.load()

	del uhrho, vhrho, x_transport_1d, y_transport_1d

	###############################
	# ### Extract potrho0 along contour:
	potrho0 = cc.querying.getvar(expt,'pot_rho_0',session,ncfile='%daily%')
	
	# # the coords on regional variables might be wacky, in which case need to do:
	# potrho0 = potrho0.rename({'yt_ocean_sub01':'yt_ocean', 'xt_ocean_sub01':'xt_ocean'})
	# if meridional length is too long, cut to match:
	potrho0 = potrho0[:,:,:len(yt_ocean),:]
	potrho0.coords['yt_ocean'] = yt_ocean
	
	potrho0 = potrho0.sel(yt_ocean=lat_range).sel(time=slice(start_time,end_time))
	
	# interpolate to correct grid:
	potrho0 = potrho0.rename({'yt_ocean':'y_ocean', 'xt_ocean':'x_ocean'}) 
	potrho0_w = potrho0.copy()
	potrho0_w.coords['x_ocean'] = xu_ocean
	potrho0_e = potrho0.roll(x_ocean=-1)
	potrho0_e.coords['x_ocean'] = xu_ocean
	# potrho0_xgrid will be on the uhrho grid:
	potrho0_xgrid = (potrho0_e + potrho0_w)/2
	
	potrho0_s = potrho0.copy()
	potrho0_s.coords['y_ocean'] = yu_ocean
	potrho0_n = potrho0.roll(y_ocean=-1)
	potrho0_n.coords['y_ocean'] = yu_ocean
	# potrho0_ygrid will be on the vhrho grid:
	potrho0_ygrid = (potrho0_s + potrho0_n)/2
	
	# stack transports into 1d and drop any points not on contour:
	potrho0_xgrid = potrho0_xgrid.where(mask_x_transport_numbered>0)
	potrho0_ygrid = potrho0_ygrid.where(mask_y_transport_numbered>0)
	x_potrho0_1d = potrho0_xgrid.stack(contour_index = ['y_ocean', 'x_ocean'])
	y_potrho0_1d = potrho0_ygrid.stack(contour_index = ['y_ocean', 'x_ocean'])
	x_potrho0_1d = x_potrho0_1d.where(mask_x_numbered_1d>0,drop=True)
	y_potrho0_1d = y_potrho0_1d.where(mask_y_numbered_1d>0,drop=True)
	
	# combine all points on contour:
	potrho0_along_contour = xr.concat((x_potrho0_1d, y_potrho0_1d), dim = 'contour_index')
	potrho0_along_contour = potrho0_along_contour.sortby(contour_ordering)
	potrho0_along_contour.coords['contour_index'] = contour_index_array
	potrho0_along_contour = potrho0_along_contour.load()
	
	###############################
	# ### Bin into density:
	## define isopycnal bins   
	#isopycnal_bins_sigma0 = np.append(np.append(np.append(1,np.arange(27,32,.1)),np.arange(32,32.8,.01)),40)
	isopycnal_bins_sigma0 = np.append(np.append(np.append(1000,np.arange(1024,1027.5,.1)),np.arange(1027.5,1028.4,.01)),1040)

	## intialise empty transport along contour in density bins array
	vol_trans_across_contour_binned = xr.DataArray(np.zeros((len(isopycnal_bins_sigma0),len(contour_ordering))), 
	                                                   coords = [isopycnal_bins_sigma0, contour_index_array], 
	                                                   dims = ['isopycnal_bins', 'contour_index'], 
	                                                   name = 'vol_trans_across_contour_binned')
	
	# loop through density bins:
	for i in range(len(isopycnal_bins_sigma0)-1):
	    print(i)
	    bin_mask = potrho0_along_contour.where(potrho0_along_contour<=isopycnal_bins_sigma0[i+1]).where(potrho0_along_contour>isopycnal_bins_sigma0[i])*0+1
	    bin_fractions = (isopycnal_bins_sigma0[i+1]-potrho0_along_contour * bin_mask)/(isopycnal_bins_sigma0[i+1]-isopycnal_bins_sigma0[i])
	    ## transport
	    transport_across_contour_in_sigmalower_bin = (vol_trans_across_contour * bin_mask * bin_fractions).sum(dim = 'st_ocean')
	    vol_trans_across_contour_binned[i,:] += transport_across_contour_in_sigmalower_bin.fillna(0).mean('time')
	    del transport_across_contour_in_sigmalower_bin
	    transport_across_contour_in_sigmaupper_bin = (vol_trans_across_contour * bin_mask * (1-bin_fractions)).sum(dim = 'st_ocean')
	    vol_trans_across_contour_binned[i+1,:] += transport_across_contour_in_sigmaupper_bin.fillna(0).mean('time')
	    del bin_mask, bin_fractions, transport_across_contour_in_sigmaupper_bin
	
	days_in_month = len(vol_trans_across_contour.time)
	
	###############################
	
	### Save:
	save_dir = '/g/data/x77/cy8964/Post_Process/access-om2/'+expt+'/Antarctic_cross_slope/'
	# make sure dir exists:
	if not os.path.lexists(save_dir):
	    os.mkdir(save_dir)
	ds_vol_trans_across_contour = xr.Dataset({'vol_trans_across_contour_binned': vol_trans_across_contour_binned, 'ndays': days_in_month})
	ds_vol_trans_across_contour.to_netcdf(save_dir+'vol_trans_across_contour_'+year+'_'+month+'.nc')

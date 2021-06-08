# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import math
import numpy as np

from metdig.io import get_model_points
from metdig.io.cassandra import get_obs_stations_multitime

from metdig.onestep.lib.utility import date_init

from metdig.products import observation_station as draw_obsstation

import metdig.cal as mdgcal
import metdig.utl as mdgstda

__all__ = [
    'obs_uv_tmp_rh_rain',
]


@date_init('obs_times', method=date_init.series_1_36_set)
def obs_uv_tmp_rh_rain(data_source='cassandra', data_name='sfc_chn_hor', obs_times=None, id_selected=54511,
                       is_return_data=False, is_draw=True, **products_kwargs):
    ret = {}

    rain01 = get_obs_stations_multitime(obs_times=obs_times, data_name=data_name, var_name='rain01', id_selected=id_selected)
    tmp = get_obs_stations_multitime(obs_times=obs_times, data_name=data_name, var_name='tmp', id_selected=id_selected)
    rh = get_obs_stations_multitime(obs_times=obs_times, data_name=data_name,  var_name='rh', id_selected=id_selected)
    wsp = get_obs_stations_multitime(obs_times=obs_times, data_name=data_name, var_name='wsp', id_selected=id_selected)
    wdir = get_obs_stations_multitime(obs_times=obs_times, data_name=data_name, var_name='wdir', id_selected=id_selected)

    # calcu
    u, v = mdgcal.wind_components(wsp, wdir)

    if is_return_data:
        dataret = {'tmp': tmp, 'u': u, 'v': v, 'rh': rh, 'rain01': rain01, 'wsp': wsp}
        ret.update({'data': dataret})

    if is_draw:
        drawret = draw_obsstation.draw_obs_uv_tmp_rh_rain(tmp, u, v, rh, rain01, wsp, **products_kwargs)
        ret.update(drawret)

    if ret:
        return ret


'''
def station_synthetical_forecast_from_cassandra(init_time=None,  fhours=np.arange(3, 36, 3), points={'lon': [110], 'lat': [20]}, **products_kwargs):

    t2m = get_model_points(data_source='cassandra', init_time=init_time, fhours=fhours, data_name='ecmwf', var_name='t2m', points=points)
    rh2m = get_model_points(data_source='cassandra', init_time=init_time, fhours=fhours, data_name='ecmwf', var_name='rh2m', points=points)
    td2m = mdgcal.dewpoint_from_relative_humidity(t2m, rh2m)

    p_vapor = mdgcal.cal_p_vapor(t2m, rh2m)  # 计算水汽压

    u10m = get_model_points(data_source='cassandra', init_time=init_time, fhours=fhours, data_name='ecmwf', var_name='u10m', points=points)
    v10m = get_model_points(data_source='cassandra', init_time=init_time, fhours=fhours, data_name='ecmwf', var_name='v10m', points=points)
    wsp10m = mdgcal.wind_speed(u10m, v10m)  # 计算10m风

    at = mdgcal.apparent_temperature(t2m, wsp10m, p_vapor)  # 计算体感温度

    rain03 = get_model_points(data_source='cassandra', init_time=init_time, fhours=fhours, data_name='ecmwf', var_name='rain03', points=points)

    tcdc = get_model_points(data_source='cassandra', init_time=init_time, fhours=fhours, data_name='ecmwf', var_name='tcdc', points=points)
    lcdc = get_model_points(data_source='cassandra', init_time=init_time, fhours=fhours, data_name='ecmwf', var_name='lcdc', points=points)
    u100m = get_model_points(data_source='cassandra', init_time=init_time, fhours=fhours, data_name='ecmwf', var_name='u100m', points=points)
    v100m = get_model_points(data_source='cassandra', init_time=init_time, fhours=fhours, data_name='ecmwf', var_name='v100m', points=points)
    wsp100m = mdgcal.wind_speed(u100m, v100m)  # 计算100m风

    vis = get_model_points(data_source='cassandra', init_time=init_time, fhours=fhours, data_name='ecmwf', var_name='vis', points=points)

    gust10m_3h = get_model_points(data_source='cassandra', init_time=init_time, fhours=fhours,
                                  data_name='ecmwf', var_name='gust10m_3h', points=points)
    gust10m_6h = get_model_points(data_source='cassandra', init_time=init_time, fhours=fhours,
                                  data_name='ecmwf', var_name='gust10m_6h', points=points)

    # draw_vis = True
    # drw_thr = True
    # draw_station_synthetical_forecast_from_cassandra(
    #     t2m, td2m, at, u10m, v10m, u100m, v100m,
    #     gust10m, wsp10m, wsp100m, rain03, tcdc, lcdc,
    #     draw_vis=draw_vis, vis=vis, drw_thr=drw_thr,
    #     output_dir=output_dir)


def station_snow_synthetical_forecast_from_cassandra():
    pass
'''

# -*- coding: utf-8 -*-

import numpy as np

from metdig.metdig_io import get_model_grid

from metdig.metdig_onestep.lib.utility import get_map_area
from metdig.metdig_onestep.lib.utility import mask_terrian
from metdig.metdig_onestep.lib.utility import date_init

from metdig.metdig_onestep.complexgrid_var.pv_div_uv import read_pv_div_uv
from metdig.metdig_onestep.complexgrid_var.rain06 import read_rain06
from metdig.metdig_onestep.complexgrid_var.vort_uv import read_vort_uv
from metdig.metdig_onestep.complexgrid_var.wsp import read_wsp

from metdig.metdig_products.diag_synoptic import draw_hgt_uv_prmsl
from metdig.metdig_products.diag_synoptic import draw_hgt_uv_rain06
from metdig.metdig_products.diag_synoptic import draw_hgt_uv_wsp
from metdig.metdig_products.diag_synoptic import draw_pv_div_uv
from metdig.metdig_products.diag_synoptic import draw_syn_composite

import metdig.metdig_utl.utl_stda_grid as utl_stda_grid

import metdig.metdig_cal as mdgcal

@date_init('init_time')
def syn_composite(data_source='cassandra', data_name='ecmwf', init_time=None, fhour=24,
                 hgt_lev=500, uv_lev=850, is_mask_terrain=True,
                 area='全国',  is_return_data=False, is_draw=True,add_city=False,add_background=False,
                 **products_kwargs):
    ret = {}
    # get area
    map_extent = get_map_area(area)

    # get data
    vort500, u500, v500 = read_vort_uv(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name,level=500, extent=map_extent)    
    wsp200, u200, v200 = read_wsp(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name,level=200, extent=map_extent)
    hgt500 = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='hgt', level=500, extent=map_extent, x_percent=0.2, y_percent=0.1)
    u850 = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='u', level=850, extent=map_extent, x_percent=0.2, y_percent=0.1)
    v850 = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='v', level=850, extent=map_extent, x_percent=0.2, y_percent=0.1)    
    prmsl = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='prmsl', extent=map_extent, x_percent=0.2, y_percent=0.1)
    tcwv = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='tcwv', extent=map_extent, x_percent=0.2, y_percent=0.1)

    if is_return_data:
        dataret = {'hgt': hgt500, 'u850': u850, 'v850': v850,'wsp200': wsp200, 'prmsl': prmsl}
        ret.update({'data': dataret})

    # 隐藏被地形遮挡地区
    if is_mask_terrain:
        psfc = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='psfc', extent=map_extent, x_percent=0.2, y_percent=0.1)
        hgt500 = mask_terrian(psfc, 500, hgt500)
        vort500 = mask_terrian(psfc,500,vort500)
        u850 = mask_terrian(psfc, 850, u850)
        v850 = mask_terrian(psfc, 850, v850)

    prmsl_attrs=prmsl.attrs
    prmsl = prmsl.rolling(lon=10,lat=10,min_periods=1,center=True).mean()
    prmsl.attrs=prmsl_attrs

    vort500_attrs=vort500.attrs
    vort500 = vort500.rolling(lon=10,lat=10,min_periods=1,center=True).mean()
    vort500.attrs=vort500_attrs
    
    # plot
    if is_draw:
        drawret = draw_syn_composite(hgt500, vort500, u850, v850, wsp200, prmsl, tcwv, 
                                    map_extent=map_extent, add_city=add_city,add_background=add_background,
                                    **products_kwargs)

        ret.update(drawret)

    return ret

@date_init('init_time')
def hgt_uv_prmsl(data_source='cassandra', data_name='ecmwf', init_time=None, fhour=24,
                 hgt_lev=500, uv_lev=850, is_mask_terrain=True,
                 area='全国',  is_return_data=False, is_draw=True, **products_kwargs):
    ret = {}
    # get area
    map_extent = get_map_area(area)

    # get data
    hgt = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='hgt', level=hgt_lev, extent=map_extent, x_percent=0.2, y_percent=0.1)
    u = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='u', level=uv_lev, extent=map_extent, x_percent=0.2, y_percent=0.1)
    v = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='v', level=uv_lev, extent=map_extent, x_percent=0.2, y_percent=0.1)
    prmsl = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='prmsl', extent=map_extent, x_percent=0.2, y_percent=0.1)

    if is_return_data:
        dataret = {'hgt': hgt, 'u': u, 'v': v, 'prmsl': prmsl}
        ret.update({'data': dataret})

    # 隐藏被地形遮挡地区
    if is_mask_terrain:
        psfc = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='psfc', extent=map_extent, x_percent=0.2, y_percent=0.1)
        hgt = mask_terrian(psfc, hgt_lev, hgt)
        u = mask_terrian(psfc, uv_lev, u)
        v = mask_terrian(psfc, uv_lev, v)

    # plot
    if is_draw:
        drawret = draw_hgt_uv_prmsl(hgt, u, v, prmsl, map_extent=map_extent, **products_kwargs)

        ret.update(drawret)

    return ret

@date_init('init_time')
def hgt_uv_rain06(data_source='cassandra', data_name='ecmwf', init_time=None, fhour=24,
                  hgt_lev=500, uv_lev=850, is_mask_terrain=True,
                  area='全国',  is_return_data=False, is_draw=True, **products_kwargs):
    ret = {}

    # get area
    map_extent = get_map_area(area)

    # get data
    hgt = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='hgt', level=hgt_lev, extent=map_extent, x_percent=0.2, y_percent=0.1)
    u = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='u', level=uv_lev, extent=map_extent, x_percent=0.2, y_percent=0.1)
    v = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='v', level=uv_lev, extent=map_extent, x_percent=0.2, y_percent=0.1)
    rain06 = read_rain06(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, extent=map_extent)
    
    if is_return_data:
        dataret = {'hgt': hgt, 'u': u, 'v': v, 'rain06': rain06}
        ret.update({'data': dataret})


    # 隐藏被地形遮挡地区
    if is_mask_terrain:
        psfc = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='psfc', extent=map_extent, x_percent=0.2, y_percent=0.1)
        hgt = mask_terrian(psfc, hgt_lev, hgt)
        u = mask_terrian(psfc, uv_lev, u)
        v = mask_terrian(psfc, uv_lev, v)

    # plot
    if is_draw:
        drawret = draw_hgt_uv_rain06(hgt, u, v, rain06, map_extent=map_extent, **products_kwargs)
        ret.update(drawret)

    return ret


@date_init('init_time')
def hgt_uv_wsp(data_source='cassandra', data_name='ecmwf', init_time=None, fhour=24,
               hgt_lev=500, uv_lev=850, is_mask_terrain=True,
               area='全国',  is_return_data=False, is_draw=True, **products_kwargs):
    ret = {}
    
    # get area
    map_extent = get_map_area(area)

    # get data
    hgt = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='hgt', level=hgt_lev, extent=map_extent, x_percent=0.2, y_percent=0.1)
    u = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='u', level=uv_lev, extent=map_extent, x_percent=0.2, y_percent=0.1)
    v = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='v', level=uv_lev, extent=map_extent, x_percent=0.2, y_percent=0.1)

    # calculate
    wsp = mdgcal.wind_speed(u, v)

    if is_return_data:
        dataret = {'hgt': hgt, 'u': u, 'v': v, 'wsp': wsp}
        ret.update({'data': dataret})

    # 隐藏被地形遮挡地区
    if is_mask_terrain:
        psfc = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='psfc', extent=map_extent, x_percent=0.2, y_percent=0.1)
        hgt = mask_terrian(psfc, hgt_lev, hgt)
        u = mask_terrian(psfc, uv_lev, u)
        v = mask_terrian(psfc, uv_lev, v)
        wsp = mask_terrian(psfc, uv_lev, wsp)

    # plot
    if is_draw:
        drawret = draw_hgt_uv_wsp(hgt, u, v, wsp, map_extent=map_extent, **products_kwargs)
        ret.update(drawret)

    return ret



@date_init('init_time')
def pv_div_uv(data_source='cassandra', data_name='ecmwf', init_time=None, fhour=24,
              lvl_ana=250, levels=[1000, 950, 925, 900, 850, 800, 700, 600, 500, 400, 300, 250, 200, 100], is_mask_terrain=True,
              area='全国',  is_return_data=False, is_draw=True, **products_kwargs):
    ret = {}

    # get area
    map_extent = get_map_area(area)

    # get data
    pv, div, u, v = read_pv_div_uv(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, lvl_ana=lvl_ana, levels=levels, extent=map_extent)

    if is_return_data:
        dataret = {'pv': pv, 'u': u, 'v': v, 'div': div}
        ret.update({'data': dataret})

    # 隐藏被地形遮挡地区
    if is_mask_terrain:
        psfc = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='psfc', extent=map_extent, x_percent=0.2, y_percent=0.1)
        pv = mask_terrian(psfc, lvl_ana, pv)
        div = mask_terrian(psfc, lvl_ana, div)
        u = mask_terrian(psfc, lvl_ana, u)
        v = mask_terrian(psfc, lvl_ana, v)

    # smooth
    pv = mdgcal.smooth_n_point(pv, 9, 2)
    div = mdgcal.smooth_n_point(div, 9, 2)
    
    # plot
    if is_draw:
        drawret = draw_pv_div_uv(pv, div, u, v, map_extent=map_extent, **products_kwargs)
        ret.update(drawret)

    return ret

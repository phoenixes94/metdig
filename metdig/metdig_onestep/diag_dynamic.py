# -*- coding: utf-8 -*-

from metdig.metdig_io import get_model_grid

from metdig.metdig_onestep.lib.utility import get_map_area
from metdig.metdig_onestep.lib.utility import mask_terrian

from metdig.metdig_products.diag_dynamic import draw_hgt_uv_vvel

import metdig.metdig_cal as mdgcal


def hgt_uv_vvel(data_source='cassandra', data_name='ecmwf', init_time=None, fhour=24,
                hgt_lev=500, uv_lev=850, vvel_lev=850, is_mask_terrain=True,
                area='全国', is_return_data=False, is_draw=True, **products_kwargs):
    ret = {}

    # get area
    map_extent = get_map_area(area)

    # get data
    hgt = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='hgt', level=hgt_lev, extent=map_extent, x_percent=0.2, y_percent=0.1)
    u = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='u', level=uv_lev, extent=map_extent, x_percent=0.2, y_percent=0.1)
    v = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='v', level=uv_lev, extent=map_extent, x_percent=0.2, y_percent=0.1)
    vvel = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='vvel', level=vvel_lev, extent=map_extent, x_percent=0.2, y_percent=0.1)
    

    if is_return_data:
        dataret = {'hgt': hgt, 'u': u, 'v': v, 'vvel': vvel}
        ret.update({'data': dataret})

    vvel = mdgcal.gaussian_filter(vvel, 5)

    # 隐藏被地形遮挡地区
    if is_mask_terrain:
        psfc = get_model_grid(data_source=data_source, init_time=init_time, fhour=fhour, data_name=data_name, var_name='psfc', extent=map_extent, x_percent=0.2, y_percent=0.1)
        hgt = mask_terrian(psfc, hgt_lev, hgt)
        u = mask_terrian(psfc, uv_lev, u)
        v = mask_terrian(psfc, uv_lev, v)
        vvel = mask_terrian(psfc, vvel_lev, vvel)

    # plot
    if is_draw:
        drawret = draw_hgt_uv_vvel(hgt, u, v, vvel, map_extent=map_extent, **products_kwargs)
        ret.update(drawret)

    return ret

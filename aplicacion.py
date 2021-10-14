#############################################################################
#############################################################################
#############################################################################
########### MODULOS #########################################################
#############################################################################
#############################################################################

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, State
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame
from funciones import *

#############################################################################
#############################################################################
#############################################################################
########### LOADING DATABASES ####################################################
#############################################################################
#############################################################################

#path datos NCEP/NCAR
tmax_ncep=('./assets/databases/air_temperature_max/tmax.air.sig995.1981-2010.nc','air')
tmean_ncep=('./assets/databases/air_temperature_mean/tmean.air.sig995.1981-2010.nc','air')
tmin_ncep=('./assets/databases/air_temperature_min/tmin.air.sig995.1981-2010.nc','air')
vwnd_ncep=('./assets/databases/meridional_wind_surface/vwnd.sfc.mon.ltm.nc','vwnd')
uwnd_ncep=('./assets/databases/zonal_wind_surface/uwnd.sfc.mon.ltm.nc','uwnd')
vwnd200_ncep=('./assets/databases/meridional_wind_200/vwnd200.mon.ltm.nc','vwnd')
uwnd200_ncep=('./assets/databases/zonal_wind_200/uwnd200.mon.ltm.nc','uwnd')
slp_ncep=('./assets/databases/sea_level_pressure/slp.mon.ltm.nc','slp')
land_ncep=('./assets/databases/etopo_NCEP.nc','elev')
precip_ncep=('./assets/databases/precipitation/prate.mmmes.sfc.mon.ltm.nc','prate')

#path datos GHCN
tmax_ghcn=('./assets/databases/air_temperature_max/ghcnm_tmax_ltm1981-2010.csv')
tmean_ghcn=('./assets/databases/air_temperature_mean/ghcnm_tavg_ltm1981-2010.csv')
tmin_ghcn=('./assets/databases/air_temperature_min/ghcnm_tmin_ltm1981-2010.csv')
precip_ghcn=('./assets/databases/precipitation/ghcnm_precip_ltm1981-2010.csv')

precip_ghcn_climo=('./assets/databases/climograma/ghcnm_precip_ltm1981-2010_comun.csv')
tmean_ghcn_climo=('./assets/databases/climograma/ghcnm_tavg_ltm1981-2010_comun.csv')

#path datos ICOADS
slp_icoads=('./assets/databases/sea_level_pressure/ICOADS_slp.ltm.nc','slp')
sst_icoads=('./assets/databases/sea_surface_temperature/ICOADS_sst.ltm.nc','sst')

#path datos OISST
sst_oisst=('./assets/databases/sea_surface_temperature/OISSTv2_sst.1981-2010.ltm.nc','sst')

#path datos CMAP
precip_cmap=('./assets/databases/precipitation/CMAP_enhanced_precip.mon.ltm.nc','precip')


#CARGA DATOS NCEP/NCAR
lon,lat,tmax=load_netcdf(tmax_ncep[0],tmax_ncep[1])
tmax=tmax-273.15 #a Celsius
lon,lat,tmean=load_netcdf(tmean_ncep[0],tmean_ncep[1])
tmean=tmean-273.15 #a Celsius
lon,lat,tmin=load_netcdf(tmin_ncep[0],tmin_ncep[1])
tmin=tmin-273.15 #a Celsius
lon,lat,vwnd=load_netcdf(vwnd_ncep[0],vwnd_ncep[1]) #en m/s
lon,lat,uwnd=load_netcdf(uwnd_ncep[0],uwnd_ncep[1]) #en m/s
lon,lat,vwnd200=load_netcdf(vwnd200_ncep[0],vwnd200_ncep[1]) #en m/s
lon,lat,uwnd200=load_netcdf(uwnd200_ncep[0],uwnd200_ncep[1]) #en m/s
lon,lat,slp=load_netcdf(slp_ncep[0],slp_ncep[1]) #en hPa
lon,lat,precip=load_netcdf(precip_ncep[0],precip_ncep[1]) #land

lon,lat,land=load_netcdf(land_ncep[0],land_ncep[1]) #land

#CARGA DATOS GHCN
lonGHtmax,latGHtmax,tmaxGH,name_GHtmax,elev_GHtmax=load_ghcn(tmax_ghcn) #en Celsius
lonGHtmean,latGHtmean,tmeanGH,name_GHtmean,elev_GHtmean=load_ghcn(tmean_ghcn) #en Celsius
lonGHtmin,latGHtmin,tminGH,name_GHtmin,elev_GHtmin=load_ghcn(tmin_ghcn) #en Celsius
lonGHprecip,latGHprecip,precipGH,name_GHprecip,elev_GHprecip=load_ghcn(precip_ghcn) #en mm/mes

lonGHclimo,latGHclimo,tmeanGHclimo,name_GHclimo,elev_GHclimo=load_ghcn(tmean_ghcn_climo) #en celsius
lonGHclimo,latGHclimo,precipGHclimo,name_GHclimo,elev_GHclimo=load_ghcn(precip_ghcn_climo) #en mm/mes

#CARGA DATOS COADS
lonCO,latCO,sstCO=load_netcdf(sst_icoads[0],sst_icoads[1]) #en Celsius
lonCO,latCO,slpCO=load_netcdf(slp_icoads[0],slp_icoads[1]) #en hPa

#CARGA DATOS OISST
lonOI,latOI,sstOI=load_netcdf(sst_oisst[0],sst_oisst[1]) #en Celsius

#CARGA DATOS CMAP
lonCM,latCM,precipCM=load_netcdf(precip_cmap[0],precip_cmap[1])
precipCM=precipCM*30# pasamos de mm/dia a mm/mes

#PERCENTIES LIMITES COLORES
perinf=2.5
persup=97.5
#############################################################################
#############################################################################
#############################################################################
########### OPTIONS ########################################################
#############################################################################
#############################################################################

options_disabled=[
    {'label': 'Diciembre', 'value': 11, 'disabled':True},
    {'label': 'Enero', 'value': 0, 'disabled':True},
    {'label': 'Febrero', 'value': 1, 'disabled':True},
    {'label': 'Marzo', 'value': 2, 'disabled':True},
    {'label': 'Abril', 'value': 3, 'disabled':True},
    {'label': 'Mayo', 'value': 4, 'disabled':True},
    {'label': 'Junio', 'value': 5, 'disabled':True},
    {'label': 'Julio', 'value': 6, 'disabled':True},
    {'label': 'Agosto', 'value': 7, 'disabled':True},
    {'label': 'Septiembre', 'value': 8, 'disabled':True},
    {'label': 'Octubre', 'value': 9, 'disabled':True},
    {'label': 'Noviembre', 'value': 10, 'disabled':True}]

options_enabled=[
    {'label': 'Diciembre', 'value': 11, 'disabled':False},
    {'label': 'Enero', 'value': 0, 'disabled':False},
    {'label': 'Febrero', 'value': 1, 'disabled':False},
    {'label': 'Marzo', 'value': 2, 'disabled':False},
    {'label': 'Abril', 'value': 3, 'disabled':False},
    {'label': 'Mayo', 'value': 4, 'disabled':False},
    {'label': 'Junio', 'value': 5, 'disabled':False},
    {'label': 'Julio', 'value': 6, 'disabled':False},
    {'label': 'Agosto', 'value': 7, 'disabled':False},
    {'label': 'Septiembre', 'value': 8, 'disabled':False},
    {'label': 'Octubre', 'value': 9, 'disabled':False},
    {'label': 'Noviembre', 'value': 10, 'disabled':False}]

variables=[
    {'label': 'Climograma (ciclo medio anual de temperatura y precipitación en la estación seleccionada)', 'value': 'climo', 'disabled':False},
    {'label': 'Mapa de temperatura media', 'value': 'tmean', 'disabled':False},
    {'label': 'Mapa de temperatura maxima', 'value': 'tmax', 'disabled':False},
    {'label': 'Mapa de temperatura mínima', 'value': 'tmin', 'disabled':False},
    {'label': 'Mapa de precipitación', 'value': 'pp', 'disabled':False},
    {'label': 'Mapa de presión a nivel del mar', 'value': 'slp', 'disabled':False},
    {'label': 'Mapa de viento zonal a 10m', 'value': 'uwnd10', 'disabled':False},
    {'label': 'Mapara de viento meridional a 10m', 'value': 'vwnd10', 'disabled':False},
    {'label': 'Mapra de viento zonal a 200 hPa', 'value': 'uwnd200', 'disabled':False},
    {'label': 'Mapa de viento meridional a 200 hPa', 'value': 'vwnd200', 'disabled':False},
    {'label': 'Mapa de temperatura superficial del mar', 'value': 'sst', 'disabled':False}]

variables_pp=[
    {'label': 'Climograma (ciclo medio anual de temperatura y precipitación en la estación seleccionada)  ', 'value': 'climo', 'disabled':True},
    {'label': 'Temperatura media', 'value': 'tmean', 'disabled':True},
    {'label': 'Temperatura maxima', 'value': 'tmax', 'disabled':True},
    {'label': 'Temperatura mínima', 'value': 'tmin', 'disabled':True},
    {'label': 'Precipitación', 'value': 'pp', 'disabled':False},
    {'label': 'Presión a nivel del mar', 'value': 'slp', 'disabled':True},
    {'label': 'Viento zonal a 10m', 'value': 'uwnd10', 'disabled':True},
    {'label': 'Viento meridional a 10m', 'value': 'vwnd10', 'disabled':True},
    {'label': 'Viento zonal a 200 hPa', 'value': 'uwnd200', 'disabled':True},
    {'label': 'Viento meridional a 200 hPa', 'value': 'vwnd200', 'disabled':True},
    {'label': 'Temperatura superficial del mar', 'value': 'sst', 'disabled':True}]


#############################################################################
#############################################################################
#############################################################################
#############################################################################
################## DASH APP #################################################
#############################################################################
#############################################################################
#############################################################################
texto='''# ClimaWeb (versión Web)
---------------
ClimaWeb es una aplicación que permite visualizar mapas globales de los promedios históricos de diversas variables climáticas a nivel mensual. También permite calcular el mapa de diferencia de ese promedio entre distintos meses junto con el ciclo medio anual en cada punto del planeta donde existe información. Las variables disponibles son la temperatura (media, máxima y mínima), precipitación, presión a nivel del mar y viento en varios niveles. Dependiendo de la variable, hay diversas bases desde donde se obtuvieron los datos, que incluyen registros en estaciones de medición y reanálisis atmosféricos.

Esta aplicación está pensada como un apoyo a la docencia en distintos niveles. La misma está inspirada en el software GeoClima desarrollado el año 2002 por Bernhard Lopez bajo la supervisión del Profesor Patricio Aceituno Gutiérrez, del Departamento de Geofísica de la Universidad de Chile.  ClimaWeb fue desarrollado el año 2020 por Piero Mardones, Geofísico y Magíster en Meteorología y Climatología (U. Chile), y socio fundador de geoatlas.cl, con la supervisión de René Garreaud, académico del Departamento de Geofísica de la U. Chile y subdirector del Centro de Ciencia del Clima y la Resiliencia (CR)2. El proyecto recibió el apoyo del Departamento de Geofísica y del (CR)2, a través del soporte de datos y computo por Francisca Muñoz y Camilo Menares. El diseño fue revisado por Giselle Ogaz. Si necesitas información sobre cómo usar esta plataforma, puedes revisar el Tutorial de Uso.


Data Scientist: 

Piero Mardones, pieromardonesb@gmail.com

Camilo Menares, camilo.menares@uchile.cl

Soporte       : 

Datos y Cómputos Cr2, cr2sysadmin@dgf.cl




---------------
'''
modal=html.Div(
    children=[html.Div([html.Div(
        className='modal-content',style={'text-align': 'justify'},children=[dcc.Markdown(texto)]),html.Button('Cerrar', id='modal-close-button')],id='modal',className='modal',style={"display": "none"})])

app = dash.Dash(update_title='Actualizando...')
#app.scripts.append_script({"external_url": "https://cdn.plot.ly/plotly-locale-es-latest.js"})
app.title = 'ClimaWEB - CR2'
# App Layout
app.layout = html.Div(
    children=[
        # Mensaje de error
        html.Div(id="error-message"),
        # Banner superior
        html.Div(
            className="study-browser-banner row",
            children=[
                html.Div(className="h2-title", children=[html.A([html.Img(className="logoclima", src=app.get_asset_url("logo_climaweb_blanco.png"))], href="http://climaweb.cr2.cl/")]),
                html.Div(
                    className="div-logo",
                    children=[html.A(id='instructions-button',className='links',children=[html.H6('Acerca de', style={'display':'inline-block','float':'left','margin-top':'40px','margin-right':'10px'})]),
                     html.A(className='links',children=[html.H6('Tutorial de uso', style={'display':'inline-block','float':'left','padding-left':'5px','margin-top':'40px','margin-right':'15px'})],href=app.get_asset_url("tutorial_geoclima.pdf"),target='_blank'),

                    html.A([
                     html.Img(
                        className="logoCr2", src=app.get_asset_url("logo_transparente.png")
                    )
                    ], href="http://www.cr2.cl/")
                    ]
                ),modal,
                html.Div(className="h2-title-mobile", children=[html.A([html.Img(className="logoclimamobile", src=app.get_asset_url("logo_climaweb_blanco.png"))], href="http://climaweb.cr2.cl/")]),
            ],
        ),
        # Cuerpo de la app
        html.Div(
            className="row app-body",
            children=[
                ######################################
                ######################################
                ##### Controles de usuario ###########
                ######################################
                ######################################
                html.Div(
                    className="four columns card",
                    children=[
                        html.Div(id='div-control',
                            className="bg-white user-control",
                            children=[
                                #Control 1: Seleccione una variable
                                html.Div(  style={'color': '#0071BC'} ,
                                    className="padding-top-bot",
                                    children=[
                                        html.H6("1) Seleccione producto:"),
                                        dcc.Dropdown(id="lista-variables",options=variables,placeholder='Seleccione ...',value='tmean',searchable=False,clearable=False),
                                    ],
                                ),
                                #Control 2: Seleccione la base de datos (se activa dependiendo del control 1)
                                html.Div( style={'color': '#0071BC'} , id='control2',
                                    className="padding-top-bot",
                                    children=[
                                        html.H6("2) Seleccione la base de datos:"),
                                        dcc.Dropdown(id="lista-basedatos",value='ncep',placeholder='Seleccione ...',searchable=False,clearable=False),
                                    ],
                                ),
                                #Control 3: Seleccione los meses
                                html.Div( style={'color': '#0071BC'} , id='control3',
                                    className="padding-top-bot",
                                    children=[
                                        html.H6("3) Seleccione el/los mes/es:", style={'color': '#0071BC'} ),
                                        daq.BooleanSwitch(
                                            id='boton-todos',
                                            label="Marcar todos/ninguno",
                                            labelPosition="top",
                                            style={'display': 'inline-block','float':'right','color': '#0071BC'}),                                        
                                        dcc.Checklist(id='checklist-meses',
                                            options=options_enabled,
                                            value=[0],
                                            labelStyle={'display': 'inline-block','color': '#0071BC'}
                                        ),                                       
                                    ],
                                ),
                                html.Div(id='control3clon',
                                    className="padding-top-bot",
                                    children=[                                    
                                        dcc.Checklist(id='checklist-mesesclon',
                                            options=options_enabled,
                                            value=[0],
                                            labelStyle={'display': 'inline-block','color': '#0071BC'}
                                        ),                                       
                                    ],style={'display':'none','color': '#0071BC'}
                                ),
                                #Control 4: Seleccionar operacion (promedio,suma,resta)
                                html.Div( id='control4',
                                    className="padding-top-bot",
                                    children=[
                                        html.H6("4) Elija la operación (Suma solo se activa al seleccionar Precipitación):",
                                                style={'color': '#0071BC'}),
                                        dcc.RadioItems(
                                            id="operacion",
                                            options=[
                                                {"label": "Promedio", "value": "promediar"},
                                                {"label": "Suma","value": "suma","disabled":True},
                                                {"label": "Diferencia", "value": "resta"},
                                            ],
                                            value="promediar",
                                            labelStyle={
                                                "display": "inline-block",
                                                "padding": "0px 12px 0px 0px",
                                            },
                                        ),
                                    ],
                                ),
                                #Control 5 : Seleccionar meses a restar (Enero a Diciembre)
                                html.Div(id='div-resta',
                                    className="padding-top-bot",
                                    children=[
                                        html.H6("5) Seleccione el/los mes/es a restar. Por defecto se restan los promedios de los meses seleccionados (excepto para la precipitación donde se restan las sumas):"),
                                        daq.BooleanSwitch(
                                            id='boton-todos-resta',
                                            label="Marcar todos/ninguno",
                                            labelPosition="top",
                                            style={'display': 'inline-block','float':'right'}),
                                        dcc.Checklist(
                                            id="checklist-resta",
                                            options=options_disabled,
                                            value=[6],
                                            labelStyle={'display': 'inline-block'}
                                        )                                            
                                    ],style={'color': '#0071BC', 'display':'none'}
                                ),
                                                                #botones retroceder/adelantar
                                html.Div(id='controlmap',className="buttons",children=[
                                    html.H6("Retroceder/Adelantar mes:"),
                                    html.Button('<<', id='btn-nclicks-1', n_clicks=0),
                                    " ",
                                    html.Button('>>', id='btn-nclicks-2', n_clicks=0),
                                    #modificar barra de colores
                                    html.H6("Modificar escala de colores:"),
                                    dcc.RangeSlider(
                                        id='color-slider',
                                        step=1,
                                        min=np.floor(np.percentile(tmean,perinf)),
                                        max=np.floor(np.percentile(tmean,persup)),
                                        value=[np.floor(np.percentile(tmean,perinf)),np.floor(np.percentile(tmean,persup))],
                                        updatemode='drag'
                                    ),
                                html.Div(id='controlmapclon',className="buttons",children=[
                                    dcc.RangeSlider(
                                        id='color-sliderclon',
                                        step=1,
                                        min=np.floor(np.percentile(tmean,perinf)),
                                        max=np.floor(np.percentile(tmean,persup)),
                                        value=[np.floor(np.percentile(tmean,perinf)),np.floor(np.percentile(tmean,persup))],
                                        updatemode='drag'
                                    ),
                                    ],style={'display':'none'}),
                                    html.Div(id='output-container-range-slider'),
                                    html.Div(id='mesaux',style={'display':'none'}), #quitar display none si quiero revisar los meses seleccionados
                                    html.Div([], id='previously-selected')
                                ]),
                            ],
                        )
                    ],
                ),
                ######################################
                ######################################
                ### Mapa global ######################
                ######################################
                html.Div(
                    className="eight columns card-left",
                    children=[
                        html.Div(id='div-mapa',
                            className="bg-white",
                            children=[
                                #html.H5("Mapa con variable"),
                                #mapa
                                dcc.Graph(id="mapaglobal",style={'height':'610px'},config={'displayModeBar': True ,'modeBarButtonsToRemove': [ "zoom2d" , 'lasso2d', 'select2d', 'toggleSpikelines','autoScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian'], "locale":"es",'displaylogo':False, 'toImageButtonOptions': { 'filename': 'figura_cr2','format': 'png','height': 350*2, 'width': 700*2,'scale':6} }),
                                #html.Div(id = 'earth_div'),,
                            ],
                        ),
                    ],
                ),
                ######################################
                ######################################
                ## Grafico climatologia en un punto ###
                ######################################
                ######################################
                html.Div(id='divgraficoclim',
                    className="eight columns card-left",
                    children=[
                        html.Div(
                            className="bg-white2",
                            children=[
                                html.Div(id='salida_prueba'),
                                dcc.Graph(id="graficoclim",style={'height':'500px'},responsive=True,config={'displayModeBar': True, 'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d', 'toggleSpikelines','autoScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian'],"locale":"es", 'displaylogo':False}),
                                html.Div(className="botones-download",children=[
                                    html.Button("Exportar a CSV", id="boton-exportarCsv", n_clicks=None),
                                    Download(id="exportarCsv")
                                ])
                            ],
                        )
                    ]
                )
                ######################################
                ######################################
                ######################################
                ######################################
            ],
        ),
    ]
)

#############################################################################
#############################################################################
#############################################################################
########### CALLBACKS #######################################################
#############################################################################
#############################################################################
from callbacks import *

#############################################################################
#############################################################################
#############################################################################
########### RUN APP #######################################################
#############################################################################
#############################################################################

app.scripts.config.serve_locally = False
app.scripts.append_script({
    'external_url':  'https://cdn.jsdelivr.net/gh/lppier/lppier.github.io/async_src.js'
})
app.scripts.append_script({
    'external_url': 'https://cdn.jsdelivr.net/gh//cr2uchile/Plataforma_Geoclima/gtag.js'
})


if __name__ == '__main__':
	#app.run_server()
    app.run_server(debug=False,port='8052',host='0.0.0.0')


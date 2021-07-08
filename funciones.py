from netCDF4 import Dataset
import numpy as np
import pandas as pd
from scipy.io import loadmat
import plotly.graph_objs as go
from scipy.io import loadmat

############################################################################
#############################################################################
#############################################################################
########### LOADING DATA ####################################################
#############################################################################
#############################################################################

### FUNCION PARA CARGAR NETCDF ####
def load_netcdf(filepath,name):
    file = Dataset(filepath, mode='r') 
    
    lon= file.variables['lon'][:]
    lat = file.variables['lat'][:]
    datos = file.variables[name][:]
    datos= np.transpose(datos,(1,2,0))
    
    #Pasamos longitudes to -180 to 180
    tmp_lon = np.array([lon[n]-360 if l>=180 else lon[n] 
                       for n,l in enumerate(lon)])  # => [0,180]U[-180,2.5]
    
    i_east, = np.where(tmp_lon>=0)  # indices of east lon
    i_west, = np.where(tmp_lon<0)   # indices of west lon
    lonnew = np.hstack((tmp_lon[i_west], tmp_lon[i_east], np.abs(tmp_lon[i_west[0]])))  # stack the 2 halves
    
    # Correspondingly, shift the 'datos' array
    datos_center = np.hstack((datos[:,i_west,:], datos[:,i_east,:], datos[:,i_east[-1:],:]))
    datos_center[np.abs(datos_center)>32000]=None;
    return lonnew,lat,datos_center

### FUNCION PARA CARGAR CSV DE GHCN ###
def load_ghcn(filepath):
    df = pd.read_csv(filepath)
    name_ghcn=df.iloc[:,0]
    lat_ghcn=np.around(df['Latitud'],5)
    lon_ghcn=np.around(df['Longitud'],5)
    elev_ghcn=np.around(df['Elevación'])
    elev_ghcn[elev_ghcn<0]=np.nan
    datos=np.around(df.iloc[:,5:],2)
    lat_ghcn[abs(lat_ghcn)>1000]=lat_ghcn[abs(lat_ghcn)>1000]/1000 #arreglamos ciertas latitudes y longitudes erróneas
    lon_ghcn[abs(lon_ghcn)>1000]=lon_ghcn[abs(lon_ghcn)>1000]/1000
    datos[abs(datos)>1000]=datos[abs(datos)>1000]/1000
    return lon_ghcn,lat_ghcn,datos,name_ghcn,elev_ghcn

#############################################################################
#############################################################################
#############################################################################
#############################################################################
################## FUNCIONES PARA GRAFICAR ##################################
#############################################################################
#############################################################################
#############################################################################
coastline=loadmat('./assets/databases/coastline_pieropaises.mat')
lat_coast=coastline['lat_coast'].squeeze()
lon_coast=coastline['lon_coast'].squeeze()

### FUNCION PARA HACER CONTOURF ####
def contourf(lons,lats,variable,mes,colorbar_label,minimo,maximo,colormap,coastcolor,titulo): #Funcion para crear gráfico de contornos
    if len(mes)==1:
        textmes=' mes'
        nombremeses=('Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre')
    elif len(mes)==12:
        textmes=''
        nombremeses=('Año completo','','','','','','','','','','','')
    elif len(mes)>1 and len(mes)<6:
        textmes=' meses'
        nombremeses=('Ene/','Feb/','Mar/','Abr/','May/','Jun/','Jul/','Ago/','Sep/','Oct/','Nov/','Dic')
    else:
        textmes=''
        nombremeses=('E','F','M','A','M','J','J','A','S','O','N','D')

    
    mesesletra=''
    for i in mes:
        mesesletra=mesesletra+nombremeses[i]
        
    figura = {'data': 
            [go.Heatmap(x=lons.squeeze(), 
                    y=lats.squeeze(),
                    z=np.around(variable.squeeze(),decimals=2),
                    colorscale=colormap,
                    zsmooth=False,
                    zmin=minimo,
                    zmax=maximo,
                    name='contourf',
                    hovertemplate='Longitud: %{x}<br>Latitud: %{y}<br>Valor: %{z}<extra></extra>',
                    colorbar=dict(
                            title=colorbar_label, # title here
                            titleside='right',
                            titlefont=dict(
                                size=14,
                                #family='Arial, sans-serif'
                                )
                            )
                    )] + 
            [go.Scatter(x=lon_coast, #Agrega linea de costa
                        y=lat_coast, 
                        mode='lines', 
                        name='',
                        marker_color=coastcolor,
                        line=dict(width=2),
                        hoverinfo='skip')],
            
            'layout':go.Layout(
                    title=titulo + textmes + ' ' + mesesletra,
                    margin=dict(t=40),
                    xaxis=go.layout.XAxis(
                        title=go.layout.xaxis.Title(
                            text='Longitud',
                        ),range=[-180,180],uirevision='mapaglobal',
                        zeroline=False,showgrid=False),
                    yaxis=go.layout.YAxis(
                        title=go.layout.yaxis.Title(
                            text='Latitud',
                        ),range=[-90,90],uirevision='mapaglobal',
                        zeroline=False,showgrid=False))
            }
    
    return figura

### FUNCION PARA HACER CONTOURF MESESRESTA ####
def contourf_resta(lons,lats,variable,mes,mesesresta,colorbar_label,minimo,maximo,colormap,coastcolor): #Funcion para crear gráfico de contornos
    if colormap=='GnBu':
        textope='suma climatológica (1981-2010) '
    else:
        textope='promedio climatológico (1981-2010) '
        
    if len(mes)==1:
        textmes=' mes '
        nombremeses=('Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre')
    elif len(mes)==12:
        textmes=''
        nombremeses=(' Año completo','','','','','','','','','','','')
    elif len(mes)>1 and len(mes)<6:
        textmes=' meses '
        nombremeses=('Ene/','Feb/','Mar/','Abr/','May/','Jun/','Jul/','Ago/','Sep/','Oct/','Nov/','Dic')
    else:
        textmes=''
        nombremeses=('E','F','M','A','M','J','J','A','S','O','N','D')

    
    mesesletra=''
    for i in mes:
        mesesletra=mesesletra+nombremeses[i]

    if len(mesesresta)==1:
        nombremeses=('Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre')
    elif len(mesesresta)==12:
        nombremeses=('Año completo','','','','','','','','','','','')
    elif len(mesesresta)>1 and len(mes)<6:
        nombremeses=('Ene/','Feb/','Mar/','Abr/','May/','Jun/','Jul/','Ago/','Sep/','Oct/','Nov/','Dic')
    else:
        nombremeses=('E','F','M','A','M','J','J','A','S','O','N','D')

    
    mesesletraresta=''
    for i in mesesresta:
        mesesletraresta=mesesletraresta+nombremeses[i]
        
    figura = {'data': 
            [go.Heatmap(x=lons.squeeze(), 
                    y=lats.squeeze(),
                    z=np.around(variable.squeeze(),decimals=2),
                    colorscale=colormap,
                    zsmooth=False,
                    zmin=minimo,
                    zmax=maximo,
                    name='',
                    hovertemplate='Longitud: %{x}<br>Latitud: %{y}<br>Valor: %{z}<extra></extra>',
                    colorbar=dict(
                            title=colorbar_label, # title here
                            titleside='right',
                            titlefont=dict(
                                size=14,
                                #family='Arial, sans-serif'
                                )
                            )
                    )] + 
            [go.Scatter(x=lon_coast, #Agrega linea de costa
                        y=lat_coast, 
                        mode='lines', 
                        name='',
                        marker_color=coastcolor,
                        line=dict(width=2),
                        hoverinfo='skip')],
            
            'layout':go.Layout(
                    title='Diferencia '  + textope + textmes + mesesletra + ' menos ' + mesesletraresta,
                    margin=dict(t=40),
                    xaxis=go.layout.XAxis(
                        title=go.layout.xaxis.Title(
                            text='Longitud',
                        ),range=[-180,180],uirevision='mapaglobal',
                        zeroline=False,showgrid=False),
                    yaxis=go.layout.YAxis(
                        title=go.layout.yaxis.Title(
                            text='Latitud',
                        ),range=[-90,90],uirevision='mapaglobal',
                        zeroline=False,showgrid=False))
            }
    
    return figura


### FUNCION PARA HACER SCATTER DE GHCN ###
def scattermap(lons,lats,name,variable,mes,colorbar_label,minimo,maximo,colormap,coastcolor,titulo): #Funcion para crear gráfico de contornos
    if len(mes)==1:
        textmes=' mes'
        nombremeses=('Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre')
    elif len(mes)==12:
        textmes=''
        nombremeses=('Año completo','','','','','','','','','','','')
    elif len(mes)>1 and len(mes)<6:
        textmes=' meses'
        nombremeses=('Ene/','Feb/','Mar/','Abr/','May/','Jun/','Jul/','Ago/','Sep/','Oct/','Nov/','Dic')
    else:
        textmes=''
        nombremeses=('E','F','M','A','M','J','J','A','S','O','N','D')

    
    mesesletra=''
    for i in mes:
        mesesletra=mesesletra+nombremeses[i]
        
        
    figura = {'data': 
            [go.Scatter(x=lons, 
                    y=lats,
                    mode='markers',
                    showlegend=False,
                    text=name.apply(str.strip),
                    #hoverinfo='none',
                    hovertemplate='Nombre/País: %{text}<br>Longitud: %{x}<br>Latitud: %{y}<br>Valor: %{marker.color}<extra></extra>',
                    marker=dict(
                            size=12,
                            color=np.around(variable,decimals=2), #set color equal to a variable
                            colorscale=colormap, # one of plotly colorscales
                            cmin=minimo,
                            cmax=maximo,                            
                            showscale=True,
                            colorbar=dict(
                            title=colorbar_label, # title here
                            titleside='right',
                            titlefont=dict(
                                size=14,
                                #family='Arial, sans-serif'
                                )
                            )
                    )
                    )] + 
            [go.Scatter(x=lon_coast, #Agrega linea de costa
                        y=lat_coast, 
                        mode='lines', 
                        name='',
                        showlegend=False,                        
                        marker_color=coastcolor,
                        line=dict(width=2),
                        hoverinfo='skip')],
            
            'layout':go.Layout(
                    title=titulo + textmes + ' ' + mesesletra,
                    margin=dict(t=40),
                    xaxis=go.layout.XAxis(
                        title=go.layout.xaxis.Title(
                            text='Longitud',
                        ),range=[-180,180],uirevision='mapaglobal',
                        zeroline=False,
                        showgrid=False),
                    yaxis=go.layout.YAxis(
                        title=go.layout.yaxis.Title(
                            text='Latitud',
                        ),range=[-90,90],uirevision='mapaglobal',
                        zeroline=False,showgrid=False),hovermode='closest',clickmode='event+select')
            }
    
    return figura


### FUNCION PARA HACER SCATTER DE GHCN PARA LAS RESTAS ###
def scattermap_resta(lons,lats,name,variable,mes,mesesresta,colorbar_label,minimo,maximo,colormap,coastcolor): #Funcion para crear gráfico de contornos
    if colormap=='GnBu':
        textope='suma climatológica (1981-2010)'
    else:
        textope='promedio climatológico (1981-2010)'

    if len(mes)==1:
        textmes=' mes '
        nombremeses=('Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre')
    elif len(mes)==12:
        textmes=''
        nombremeses=(' Año completo','','','','','','','','','','','')
    elif len(mes)>1 and len(mes)<6:
        textmes=' meses '
        nombremeses=('Ene/','Feb/','Mar/','Abr/','May/','Jun/','Jul/','Ago/','Sep/','Oct/','Nov/','Dic')
    else:
        textmes=''
        nombremeses=('E','F','M','A','M','J','J','A','S','O','N','D')

    
    mesesletra=''
    for i in mes:
        mesesletra=mesesletra+nombremeses[i]

    if len(mesesresta)==1:
        nombremeses=('Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre')
    elif len(mesesresta)==12:
        nombremeses=('Año completo','','','','','','','','','','','')
    elif len(mesesresta)>1 and len(mes)<6:
        nombremeses=('Ene/','Feb/','Mar/','Abr/','May/','Jun/','Jul/','Ago/','Sep/','Oct/','Nov/','Dic')
    else:
        nombremeses=('E','F','M','A','M','J','J','A','S','O','N','D')

    
    mesesletraresta=''
    for i in mesesresta:
        mesesletraresta=mesesletraresta+nombremeses[i]
                
    figura = {'data': 
            [go.Scatter(x=lons, 
                    y=lats,
                    mode='markers',
                    showlegend=False,
                    text=name.apply(str.strip),
                    #hoverinfo='none',
                    hovertemplate='Nombre/País: %{text}<br>Longitud: %{x}<br>Latitud: %{y}<br>Valor: %{marker.color}<extra></extra>',
                    marker=dict(
                            size=12,
                            color=np.around(variable,decimals=2), #set color equal to a variable
                            colorscale=colormap, # one of plotly colorscales
                            cmin=minimo,
                            cmax=maximo,                            
                            showscale=True,
                            colorbar=dict(
                            title=colorbar_label, # title here
                            titleside='right',
                            titlefont=dict(
                                size=14,
                                #family='Arial, sans-serif'
                                )
                            )
                    )
                    )] + 
            [go.Scatter(x=lon_coast, #Agrega linea de costa
                        y=lat_coast, 
                        mode='lines', 
                        name='',
                        showlegend=False,                        
                        marker_color=coastcolor,
                        line=dict(width=2),
                        hoverinfo='skip')],
            
            'layout':go.Layout(
                    title='Diferencia '  + textope + textmes + mesesletra + ' menos ' + mesesletraresta,
                    margin=dict(t=40),
                    xaxis=go.layout.XAxis(
                        title=go.layout.xaxis.Title(
                            text='Longitud',
                        ),range=[-180,180],uirevision='mapaglobal',
                        zeroline=False,
                        showgrid=False),
                    yaxis=go.layout.YAxis(
                        title=go.layout.yaxis.Title(
                            text='Latitud',
                        ),range=[-90,90],uirevision='mapaglobal',
                        zeroline=False,showgrid=False),hovermode='closest',clickmode='event+select')
            }
    
    return figura

### FUNCION PARA HACER SCATTER DE GHCN ###
def scattermap_climo(lons,lats,name,elev,colorbar_label,minimo,maximo,colormap,coastcolor,titulo): #Funcion para crear gráfico de contornos


    figura = {'data': 
            [go.Scatter(x=lons, 
                    y=lats,
                    mode='markers',
                    showlegend=False,
                    text=name.apply(str.strip),
                    #hoverinfo='none',
                    hovertemplate='Nombre/País: %{text}<br>Longitud: %{x}<br>Latitud: %{y}<br>Valor: %{marker.color}<extra></extra>',
                    marker=dict(
                            size=12,
                            color=np.around(elev,decimals=2), #set color equal to a variable
                            colorscale=colormap, # one of plotly colorscales
                            cmin=minimo,
                            cmax=maximo,                            
                            showscale=True,
                            colorbar=dict(
                            title=colorbar_label, # title here
                            titleside='right',
                            titlefont=dict(
                                size=14,
                                #family='Arial, sans-serif'
                                )
                            )
                    )
                    )] + 
            [go.Scatter(x=lon_coast, #Agrega linea de costa
                        y=lat_coast, 
                        mode='lines', 
                        name='',
                        showlegend=False,                        
                        marker_color=coastcolor,
                        line=dict(width=2),
                        hoverinfo='skip')],
            
            'layout':go.Layout(
                    title=titulo,
                    margin=dict(t=40),
                    xaxis=go.layout.XAxis(
                        title=go.layout.xaxis.Title(
                            text='Longitud',
                        ),range=[-180,180],uirevision='mapaglobal',
                        zeroline=False,
                        showgrid=False),
                    yaxis=go.layout.YAxis(
                        title=go.layout.yaxis.Title(
                            text='Latitud',
                        ),range=[-90,90],uirevision='mapaglobal',
                        zeroline=False,showgrid=False),hovermode='closest',clickmode='event+select')
            }
    
    return figura


### GRAFICO AL HACER CLICK
def grafico_punto(lons,lats,variable,clickData,tipografico,colorlinea,titulo,ylabel):
    if len(variable.shape)==3:
        lat_mapa=clickData['points'][0]['y']
        lon_mapa=clickData['points'][0]['x']
        coords=str(lat_mapa) + ',' + str(lon_mapa)
        idx_lon= (np.abs(lons-lon_mapa)).argmin()
        idx_lat= (np.abs(lats-lat_mapa)).argmin()
        
        coords_real='Latitud: ' + str(lats[idx_lat]) + ', Longitud: ' + str(lons[idx_lon])
        xdata = 'Ene Feb Mar Abr May Jun Jul Ago Sep Oct Nov Dic'.split()
        ydata = variable[idx_lat,idx_lon,:] 
    else:
        if 'pointIndex' in clickData['points'][0].keys():
            lat_mapa=clickData['points'][0]['y']
            lon_mapa=clickData['points'][0]['x']
            coords=str(lat_mapa) + ',' + str(lon_mapa)
            idx=clickData['points'][0]['pointIndex']
            coords_real='Latitud: ' + str(lats.iloc[idx]) + ', Longitud: ' + str(lons.iloc[idx])
            xdata = 'Ene Feb Mar Abr May Jun Jul Ago Sep Oct Nov Dic'.split()
            ydata = variable.iloc[idx,:] 
        else:
            lat_mapa=clickData['points'][0]['y']
            lon_mapa=clickData['points'][0]['x']
            coords=str(lat_mapa) + ',' + str(lon_mapa)
            idx_lon= (np.abs(lons-lon_mapa)).argmin()
            idx_lat= (np.abs(lats-lat_mapa)).argmin()
            
            coords_real='Latitud: ' + str(lats[idx_lat]) + ', Longitud: ' + str(lons[idx_lat])
            xdata = 'Ene Feb Mar Abr May Jun Jul Ago Sep Oct Nov Dic'.split()
            ydata = variable.iloc[idx_lat,:]  

    
    if tipografico=='barras':
        plotclim = {'data':[go.Bar(
        x = list(xdata),
        y = np.around(list(ydata),decimals=2),        
        marker={'color':colorlinea}
        )],
        'layout':go.Layout(title={'text':titulo + ' en ' + coords_real,'font':{'size':14}} ,yaxis = {'title':ylabel,'fixedrange':True,'zeroline':False},xaxis = {'title':'Mes','showgrid': False,'fixedrange':True})
        }
        return plotclim
    else:
        plotclim = {'data':[go.Scatter(
        x = list(xdata),
        y = np.around(list(ydata),decimals=2),
        mode='lines+markers',
        marker={'color':colorlinea}
        )],
        'layout':go.Layout(title={'text':titulo + ' en ' + coords_real,'font':{'size':14}} ,yaxis = {'title':ylabel,'fixedrange':True,'zeroline':False},xaxis = {'title':'Mes','showgrid': False,'fixedrange':True})
        }        
        return plotclim

### GRAFICO AL HACER CLICK PARA GHCN (lo repeti nomás, que elegancia la de francia jajaja)
def grafico_puntoGHCN(lons,lats,name,elev,variable,clickData,tipografico,colorlinea,titulo,ylabel):
    if len(variable.shape)==3:
        lat_mapa=clickData['points'][0]['y']
        lon_mapa=clickData['points'][0]['x']
        coords=str(lat_mapa) + ',' + str(lon_mapa)
        idx_lon= (np.abs(lons-lon_mapa)).argmin()
        idx_lat= (np.abs(lats-lat_mapa)).argmin()
        
        coords_real='Latitud: ' + str(lats[idx_lat]) + ', Longitud: ' + str(lons[idx_lon])
        xdata = 'Ene Feb Mar Abr May Jun Jul Ago Sep Oct Nov Dic'.split()
        ydata = variable[idx_lat,idx_lon,:] 
    else:
        if 'pointIndex' in clickData['points'][0].keys():
            lat_mapa=clickData['points'][0]['y']
            lon_mapa=clickData['points'][0]['x']
            coords=str(lat_mapa) + ',' + str(lon_mapa)
            idx=clickData['points'][0]['pointIndex']
            if idx<=len(lons):
                namest=str(name.iloc[idx]).strip()
                eleva=elev.iloc[idx]
                coords_real=namest + ' Latitud: ' + str(lats.iloc[idx]) + ', Longitud: ' + str(lons.iloc[idx]) + ' Elevación: ' + str(eleva)  + ' m.s.n.m.' 
                xdata = 'Ene Feb Mar Abr May Jun Jul Ago Sep Oct Nov Dic'.split()
                ydata = variable.iloc[idx,:]
                
            else:
                idx= (np.abs(lats-lat_mapa)).argmin()
                namest=str(name.iloc[idx]).strip()
                eleva=elev.iloc[idx]
                coords_real=namest + ' Latitud: ' + str(lats.iloc[idx]) + ', Longitud: ' + str(lons.iloc[idx]) + ' Elevación: ' + str(eleva)  + ' m.s.n.m.' 
                xdata = 'Ene Feb Mar Abr May Jun Jul Ago Sep Oct Nov Dic'.split()
                ydata = variable.iloc[idx,:]
                
        else:
            lat_mapa=clickData['points'][0]['y']
            lon_mapa=clickData['points'][0]['x']
            coords=str(lat_mapa) + ',' + str(lon_mapa)
            idx_lon= (np.abs(lons-lon_mapa)).argmin()
            idx_lat= (np.abs(lats-lat_mapa)).argmin()
            coords_real='Latitud: ' + str(lats[idx_lat]) + ', Longitud: ' + str(lons[idx_lat])
            xdata = 'Ene Feb Mar Abr May Jun Jul Ago Sep Oct Nov Dic'.split()
            ydata = variable.iloc[idx_lat,:]  

    
    if tipografico=='barras':
        plotclim = {'data':[go.Bar(
        x = list(xdata),
        y = np.around(list(ydata),decimals=2),        
        marker={'color':colorlinea}
        )],
        'layout':go.Layout(title={'text':titulo + ' en ' + coords_real,'font':{'size':14}},yaxis = {'title':ylabel,'fixedrange':True,'zeroline':False},xaxis = {'title':'Mes','showgrid': False,'fixedrange':True})
        }
        return plotclim
    else:
        plotclim = {'data':[go.Scatter(
        x = list(xdata),
        y = np.around(list(ydata),decimals=2),
        mode='lines+markers',
        marker={'color':colorlinea}
        )],
        'layout':go.Layout(title={'text':titulo + ' en ' + coords_real,'font':{'size':14}},yaxis = {'title':ylabel,'fixedrange':True,'zeroline':False},xaxis = {'title':'Mes','showgrid': False,'fixedrange':True})
        }        
        return plotclim
    
 ### GRAFICO AL HACER CLICK PARA GHCN en climo (lo repeti nomás, que elegancia la de francia jajaja)
def grafico_puntoGHCNclimo(lons,lats,name,elev,variable,variable2,clickData,tipografico,colorlinea,titulo):
    if len(variable.shape)==3:
        lat_mapa=clickData['points'][0]['y']
        lon_mapa=clickData['points'][0]['x']
        coords=str(lat_mapa) + ',' + str(lon_mapa)
        idx_lon= (np.abs(lons-lon_mapa)).argmin()
        idx_lat= (np.abs(lats-lat_mapa)).argmin()
        
        coords_real='Latitud: ' + str(lats[idx_lat]) + ', Longitud: ' + str(lons[idx_lon])
        xdata = 'Ene Feb Mar Abr May Jun Jul Ago Sep Oct Nov Dic'.split()
        ydata = variable[idx_lat,idx_lon,:] 
    else:
        if 'pointIndex' in clickData['points'][0].keys():
            lat_mapa=clickData['points'][0]['y']
            lon_mapa=clickData['points'][0]['x']
            coords=str(lat_mapa) + ',' + str(lon_mapa)
            idx=clickData['points'][0]['pointIndex']
            if idx<=len(lons):
                namest=str(name.iloc[idx]).strip()
                eleva=elev.iloc[idx]
                coords_real=namest + ' Latitud: ' + str(lats.iloc[idx]) + ', Longitud: ' + str(lons.iloc[idx]) + ' Elevación: ' + str(eleva)  + ' m.s.n.m.' 
                xdata = 'Ene Feb Mar Abr May Jun Jul Ago Sep Oct Nov Dic'.split()
                ydata1 = variable.iloc[idx,:]
                ydata2= variable2.iloc[idx,:]
                
            else:
                idx= (np.abs(lats-lat_mapa)).argmin()
                namest=str(name.iloc[idx]).strip()
                eleva=elev.iloc[idx]
                coords_real=namest + ' Latitud: ' + str(lats.iloc[idx]) + ', Longitud: ' + str(lons.iloc[idx]) + ' Elevación: ' + str(eleva)  + ' m.s.n.m.' 
                xdata = 'Ene Feb Mar Abr May Jun Jul Ago Sep Oct Nov Dic'.split()
                ydata1 = variable.iloc[idx,:]
                ydata2= variable2.iloc[idx,:]
                
        else:
            lat_mapa=clickData['points'][0]['y']
            lon_mapa=clickData['points'][0]['x']
            coords=str(lat_mapa) + ',' + str(lon_mapa)
            idx_lon= (np.abs(lons-lon_mapa)).argmin()
            idx_lat= (np.abs(lats-lat_mapa)).argmin()
            coords_real='Latitud: ' + str(lats[idx_lat]) + ', Longitud: ' + str(lons[idx_lat])
            xdata = 'Ene Feb Mar Abr May Jun Jul Ago Sep Oct Nov Dic'.split()
            ydata = variable.iloc[idx_lat,:]  
    
    suma_pp=np.round(np.sum(ydata2),0)        
    traces=[go.Bar(
    x = list(xdata),
    y = np.around(list(ydata2),decimals=2),        
    marker={'color':'lightblue'},name='Precipitación'
    ),go.Scatter(
    x = list(xdata),
    y = np.around(list(ydata1),decimals=2),
    mode='lines+markers',
    marker={'color':'red'},yaxis='y2',name='Temperatura'
    )]
    plotclim={'data': traces,
                    'layout': {
                        'title': {'text':titulo + ' en ' + coords_real + ' (Precip. total ' + str(suma_pp) + ' mm)','font':{'size':12}},
                        'showlegend': False,
                        'legend': {'x': 0,
                                   'y': 1,
                                   'y2': 2,
                                   'traceorder': 'normal'
                                   },
                        'xaxis': {'title': 'Mes',
                                  'showline': True,
                                  'fixedrange':True,
                                  'showgrid': False},
                        'yaxis': {'title': 'Precipitación [mm/mes]',                                 
                                  'side': 'left',
                                  'showline': True,
                                  'showgrid': False,
                                  'zeroline':False,
                                  'titlefont':dict(color='steelblue'),
                                  'tickfont':dict(color='steelblue'),
                                  'fixedrange':True},
                        'yaxis2': {'title': 'Temperatura [⁰C]',
                                   'overlaying':'y',
                                   'showline': True,
                                   'zeroline':False,
                                   'titlefont':dict(color='red'),
                                   'tickfont':dict(color='red'),                   
                                   'side': 'right',
                                   'fixedrange':True}
                        },
                    }     
    return plotclim
#GRAFICO CLIMOGRAMA
def grafico_climo(lons,lats,variable1,variable2,clickData,tipografico,colorlinea,titulo):

    lat_mapa=clickData['points'][0]['y']
    lon_mapa=clickData['points'][0]['x']
    coords=str(lat_mapa) + ',' + str(lon_mapa)
    idx_lon= (np.abs(lons-lon_mapa)).argmin()
    idx_lat= (np.abs(lats-lat_mapa)).argmin()

    coords_real='Latitud: ' + str(lats[idx_lat]) + ', Longitud: ' + str(lons[idx_lon])
    xdata = 'Ene Feb Mar Abr May Jun Jul Ago Sep Oct Nov Dic'.split()
    ydata1 = variable1[idx_lat,idx_lon,:] 
    ydata2 = variable2[idx_lat,idx_lon,:] 

    
    # plotclim = {'data':[go.Bar(
    # x = list(xdata),
    # y = np.around(list(ydata2),decimals=2),        
    # marker={'color':'lightblue'}
    # )] +
    # [go.Scatter(
    # x = list(xdata),
    # y = np.around(list(ydata1),decimals=2),
    # mode='lines+markers',
    # marker={'color':'red'}
    # )],    
    # 'layout':go.Layout(title=titulo + ' en ' + coords_real ,yaxis = {'title':ylabel,'fixedrange':True},xaxis = {'title':'Mes','showgrid': False,'fixedrange':True})
    # }
    suma_pp=np.round(np.sum(ydata2),0)  
    traces=[go.Bar(
    x = list(xdata),
    y = np.around(list(ydata2),decimals=2),        
    marker={'color':'lightblue'},name='Precipitación'
    ),go.Scatter(
    x = list(xdata),
    y = np.around(list(ydata1),decimals=2),
    mode='lines+markers',
    marker={'color':'red'},yaxis='y2',name='Temperatura'
    )]
    plotclim={'data': traces,
                    'layout': {
                        'title': {'text':titulo + ' en ' + coords_real + ' (Precip. total ' + str(suma_pp) + ' mm)','font':{'size':14}},
                        'showlegend': False,
                        'legend': {'x': 0,
                                   'y': 1,
                                   'y2': 2,
                                   'traceorder': 'normal'
                                   },
                        'xaxis': {'title': 'Mes',
                                  'showline': True,
                                  'fixedrange':True,
                                  'showgrid': False},
                        'yaxis': {'title': 'Precipitación [mm/mes]',                                 
                                  'side': 'left',
                                  'showline': True,
                                  'showgrid': False,
                                  'zeroline':False,
                                  'titlefont':dict(color='steelblue'),
                                  'tickfont':dict(color='steelblue'),
                                  'fixedrange':True},
                        'yaxis2': {'title': 'Temperatura [⁰C]',
                                   'overlaying':'y',
                                   'showline': True,
                                   'zeroline':False,
                                   'titlefont':dict(color='red'),
                                   'tickfont':dict(color='red'),                   
                                   'side': 'right',
                                   'fixedrange':True}
                        },
                    }     
    return plotclim


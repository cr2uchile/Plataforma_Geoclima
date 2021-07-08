from aplicacion import *
from funciones import *
#############################################################################
#############################################################################
#############################################################################
########### CALLBACKS #######################################################
#############################################################################
#############################################################################
# hide/show modal
@app.callback(Output('modal', 'style'),
              [Input('instructions-button', 'n_clicks'),
               Input('modal', 'n_clicks')])
def show_modal(n,n2):
    if n > 0:
        return {"display": "block"}
    return {"display": "none"}

# Close modal by resetting info_button click to 0
@app.callback(Output('instructions-button', 'n_clicks'),
              [Input('modal-close-button', 'n_clicks')])
def close_modal(n):
    return 0



options=[{"label": "Promedio", "value": "promediar"},{"label": "Suma","value": "suma","disabled":True},{"label": "Diferencia", "value": "resta"}]
options_pp=[{"label": "Promedio", "value": "promediar"},{"label": "Suma","value": "suma","disabled":False},{"label": "Diferencia", "value": "resta"}]
##### INTERACCION LISTA DE VARIABLES CON LISTA BASE DE DATOS
@app.callback([
    dash.dependencies.Output('lista-basedatos', 'options'),
    dash.dependencies.Output('lista-basedatos', 'disabled'),
    dash.dependencies.Output('lista-basedatos', 'value'),
    dash.dependencies.Output('operacion', 'options')],
    [dash.dependencies.Input('lista-variables', 'value')])
def update_output(value):
    if value==None:
        return [],True,[]
    elif value=='climo':
        options_datos=[{'label':'GHCN','value':'ghcn'},{'label': 'NCEP/NCAR', 'value': 'ncep'}]
        return options_datos,False,'ghcn',options
    elif value=='tmean':
        options_datos=[{'label': 'NCEP/NCAR', 'value': 'ncep'},{'label': 'GHCN', 'value': 'ghcn'}]
        return options_datos,False,'ncep',options
    elif value=='tmax':
        options_datos=[{'label': 'NCEP/NCAR', 'value': 'ncep'},{'label': 'GHCN', 'value': 'ghcn'}]
        return options_datos,False,'ncep',options
    elif value=='tmin':
        options_datos=[{'label': 'NCEP/NCAR', 'value': 'ncep'},{'label': 'GHCN', 'value': 'ghcn'}]
        return options_datos,False,'ncep',options
    elif value=='pp':
        options_datos=[{'label': 'CMAP', 'value': 'cmap'},{'label': 'NCEP/NCAR', 'value': 'ncep'},{'label': 'GHCN', 'value': 'ghcn'}]
        return options_datos,False,'cmap',options_pp
    elif value=='slp':
        options_datos=[{'label': 'NCEP/NCAR', 'value': 'ncep'},{'label': 'COADS', 'value': 'coads'}]
        return options_datos,False,'ncep',options
    elif value=='uwnd10':
        options_datos=[{'label': 'NCEP/NCAR', 'value': 'ncep'}]
        return options_datos,False,'ncep',options
    elif value=='vwnd10':
        options_datos=[{'label': 'NCEP/NCAR', 'value': 'ncep'}]
        return options_datos,False,'ncep',options
    elif value=='uwnd200':
        options_datos=[{'label': 'NCEP/NCAR', 'value': 'ncep'}]
        return options_datos,False,'ncep',options
    elif value=='vwnd200':
        options_datos=[{'label': 'NCEP/NCAR', 'value': 'ncep'}]
        return options_datos,False,'ncep',options
    elif value=='sst':
        options_datos=[{'label': 'OISSTv2', 'value': 'oisstv2'},{'label': 'COADS', 'value': 'coads'}]
        return options_datos,False,'oisstv2',options

## INTERACCION DISABLE TODAS MENOS PP CUANDO ES SUMA
@app.callback(dash.dependencies.Output('lista-variables', 'options'),
    [dash.dependencies.Input('operacion', 'value')])
def update_output(operacion):
    if operacion=='suma':
        return variables_pp
    else:
        return variables

###INTERACCION PARA CLONAR COMPORTAMIENTO DE CHECKLIST (SALTAR DEPENDENCIA CIRCULAR)
@app.callback(
    [Output('control3clon', 'children'), Output('mesaux', 'children')],
    [Input('checklist-meses', 'value'),
     dash.dependencies.Input('boton-todos', 'on')])
def update_via_children(value,on):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'boton-todos' in changed_id and on==True:
        value=[0,1,2,3,4,5,6,7,8,9,10,11]
    elif 'boton-todos' in changed_id and on==False:
        value=[]

    return dcc.Checklist(id='checklist-mesesclon',options=options_enabled,value=value,labelStyle={'display': 'inline-block'}), value

##INTERACCION DE TODOS LOS BOTONES CON CHECKLIST MESES
@app.callback(
    Output('checklist-meses', 'value'),
    [Input('checklist-mesesclon', 'value'),
     dash.dependencies.Input('boton-todos', 'on'),
     Input('btn-nclicks-1', 'n_clicks'),
     Input('btn-nclicks-2', 'n_clicks')])
def update_directly(value,on,btn1,btn2):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'boton-todos' in changed_id and on==True:
        value=[0,1,2,3,4,5,6,7,8,9,10,11]
    elif 'boton-todos' in changed_id and on==False:
        value=[]
        
    if 'btn-nclicks-1' in changed_id:
        for idx,val in enumerate(value):
            value[idx]=value[idx]-1 
            if value[idx]==-1:
                value[idx]=11
                 
    elif 'btn-nclicks-2' in changed_id:
        for idx,val in enumerate(value):
            value[idx]=value[idx]+1 
            if value[idx]==12:
                value[idx]=0
    else:
        value=value
    return value

################################
#INTERACCION CHECKLIST RESTA MESES
@app.callback([
    dash.dependencies.Output('checklist-resta', 'options'),
    dash.dependencies.Output('div-resta', 'style')],
    [dash.dependencies.Input('operacion', 'value'),
     dash.dependencies.Input('lista-variables', 'value')])
def update_output2(value,variable):
    if value=='resta' and not variable=='climo':
        return options_enabled,{'display':'block','className': "padding-top-bot"}
    else:
        return options_disabled,{'display':'none'}


#INTERACCION BOTON MARCAR TODOS RESTA
@app.callback(
    dash.dependencies.Output('checklist-resta', 'value'),
    [dash.dependencies.Input('boton-todos-resta', 'on')])
def update_output3(value):
    if value==True:
        return [0,1,2,3,4,5,6,7,8,9,10,11]
    else:
        return []



##INTERACCION CUANDO SELECCIONO CLIMO
@app.callback([
    dash.dependencies.Output('control3', 'style'),
    dash.dependencies.Output('control4', 'style'),
    dash.dependencies.Output('controlmap', 'style'),
    dash.dependencies.Output('div-mapa', 'style'),
    dash.dependencies.Output('div-control', 'style')],
    [dash.dependencies.Input('lista-variables', 'value')])
def update_map(variable):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'lista-variables' in changed_id and variable=='climo':
        return {'display':'none'},{'display':'none'},{'display':'none'},{'height':'auto'},{'height':'auto'}
    else:
        return {},{},{},{},{}

### INTERACCION PARA CLONAR COMPORTAMIENTO DE RANGE SLIDER (SALTAR DEPENDENCIA CIRCULAR) #######
@app.callback(
    [Output('controlmapclon', 'children'), Output('output-container-range-slider', 'children')],
    [Input('color-slider', 'value'),
     Input('color-slider', 'min'),
     Input('color-slider', 'max')])
def update_slider(value,mini,maxi):

    return dcc.RangeSlider(id='color-sliderclon',step=1,min=mini,max=maxi,value=value,updatemode='drag'),'Rango de colores actual: {}'.format(value)


#############################################################################
####### INTERACCION CON EL MAPA GLOBAL ######################################
#############################################################################

@app.callback([
    dash.dependencies.Output('mapaglobal', 'figure'),
    dash.dependencies.Output('color-slider', 'min'),
    dash.dependencies.Output('color-slider', 'max'),
    dash.dependencies.Output('color-slider', 'value')],
    [dash.dependencies.Input('lista-variables', 'value'),
     dash.dependencies.Input('lista-basedatos', 'value'),
     dash.dependencies.Input('checklist-meses', 'value'),
     dash.dependencies.Input('operacion', 'value'),
     dash.dependencies.Input('checklist-resta', 'value'),
     dash.dependencies.Input('color-sliderclon', 'value')])

def update_mapa(variable,basedatos,mes,operacion,mesesresta,rangocolor):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

##########################################################################################  
########################## OPERACION PROMEDIAR ###########################################
##########################################################################################              
    if operacion=='promediar':
        if len(mes)>0:
            mes=np.sort(mes)
            if variable==None or basedatos==None:
                figura=contourf(lon,lat,tmean[:,:,0]*np.nan,'','',rangocolor[0],rangocolor[1],'Jet','rgba(50, 50, 50, .8)', '')
                return figura,-10000,10000,[-10000,10000]
            else:
                if variable=='climo':
                    if basedatos=='ghcn':
                        minimo=0
                        maximo=1000                  
                        figura=scattermap_climo(lonGHclimo,latGHclimo,name_GHclimo,elev_GHclimo,'Altura estación [m]',0,1000,'Cividis','rgba(50, 50, 50, .8)', 'Seleccione una estación haciendo click sobre ella')                          
                    else:
                        minimo=-5000
                        maximo=5000                   
                        figura=contourf(lon,lat,land[:,:,0],'','Elevación del terreno [m]',-5000,5000,'delta','rgba(50, 50, 50, .8)', '')                        
################ Temperatura media PROMEDIAR #############    
                elif variable=='tmean':
                    minimo=np.floor(np.nanpercentile(tmean,perinf))
                    maximo=np.floor(np.nanpercentile(tmean,persup))                    
                    #### CASO NCEP ####
                    if basedatos=='ncep':

                        if 'lista-variables' in changed_id or 'operacion' in changed_id:                 
                            figura=contourf(lon,lat,np.mean(tmean[:,:,mes],2),mes,'Temperatura media [⁰C]',minimo,maximo,'Jet','rgba(250, 250, 250, .8)', 'Promedio climatológico (1981-2010)')
                            rangocolor=[minimo,maximo]
                        else:
                            figura=contourf(lon,lat,np.mean(tmean[:,:,mes],2),mes,'Temperatura media [⁰C]',rangocolor[0],rangocolor[1],'Jet','rgba(250, 250, 250, .8)', 'Promedio climatológico (1981-2010)')
                            
                    ### CASO GHCN #####       
                    else:
                        if 'operacion' in changed_id:
                            figura=scattermap(lonGHtmean,latGHtmean,name_GHtmean,np.mean(tmeanGH.iloc[:,mes],1),mes,'Temperatura media [⁰C]',minimo,maximo,'Jet','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')
                            rangocolor=[minimo,maximo]
                        else:
                            figura=scattermap(lonGHtmean,latGHtmean,name_GHtmean,np.mean(tmeanGH.iloc[:,mes],1),mes,'Temperatura media [⁰C]',rangocolor[0],rangocolor[1],'Jet','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')
################ Temperatura máxima PROMEDIAR #############  
                elif variable=='tmax':
                    minimo=np.floor(np.nanpercentile(tmax,perinf))
                    maximo=np.floor(np.nanpercentile(tmax,persup))   
                    #### CASO NCEP ####
                    if basedatos=='ncep':
                      
                        if 'lista-variables' in changed_id or 'operacion' in changed_id:
                            figura=contourf(lon,lat,np.mean(tmax[:,:,mes],2),mes,'Temperatura máxima [⁰C]',minimo,maximo,'Jet','rgba(250, 250, 250, .8)', 'Promedio climatológico (1981-2010)')
                            rangocolor=[minimo,maximo]
                        else:
                            figura=contourf(lon,lat,np.mean(tmax[:,:,mes],2),mes,'Temperatura máxima [⁰C]',rangocolor[0],rangocolor[1],'Jet','rgba(250, 250, 250, .8)', 'Promedio climatológico (1981-2010)')
                            
                    #### CASO GHCN ####
                    else:
                        if 'operacion' in changed_id:
                            figura=scattermap(lonGHtmax,latGHtmax,name_GHtmax,np.mean(tmaxGH.iloc[:,mes],1),mes,'Temperatura máxima [⁰C]',minimo,maximo,'Jet','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')
                            rangocolor=[minimo,maximo]
                        else:
                            figura=scattermap(lonGHtmax,latGHtmax,name_GHtmax,np.mean(tmaxGH.iloc[:,mes],1),mes,'Temperatura máxima [⁰C]',rangocolor[0],rangocolor[1],'Jet','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')
  
################ Temperatura mínima PROMEDIAR #############
                elif variable=='tmin':
                    minimo=np.floor(np.nanpercentile(tmin,perinf))
                    maximo=np.floor(np.nanpercentile(tmin,persup))                       
                    ### CASO NCEP ####
                    if basedatos=='ncep':

                        if 'lista-variables' in changed_id or 'operacion' in changed_id:
                            figura=contourf(lon,lat,np.mean(tmin[:,:,mes],2),mes,'Temperatura mínima [⁰C]',minimo,maximo,'Jet','rgba(250, 250, 250, .8)', 'Promedio climatológico (1981-2010)')
                            rangocolor=[minimo,maximo]
                        else:
                            figura=contourf(lon,lat,np.mean(tmin[:,:,mes],2),mes,'Temperatura mínima [⁰C]',rangocolor[0],rangocolor[1],'Jet','rgba(250, 250, 250, .8)', 'Promedio climatológico (1981-2010)')
                    ### CASO GHCN ###
                    else:
                        if 'operacion' in changed_id:
                            figura=scattermap(lonGHtmin,latGHtmin,name_GHtmin,np.mean(tminGH.iloc[:,mes],1),mes,'Temperatura mínima [⁰C]',minimo,maximo,'Jet','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')
                            rangocolor=[minimo,maximo]
                        else:
                            figura=scattermap(lonGHtmin,latGHtmin,name_GHtmin,np.mean(tminGH.iloc[:,mes],1),mes,'Temperatura mínima [⁰C]',rangocolor[0],rangocolor[1],'Jet','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')

################ Precipitación PROMEDIAR #############
                elif variable=='pp':
                    minimo=np.floor(np.nanpercentile(precipCM,perinf))
                    maximo=np.floor(np.nanpercentile(precipCM,persup))                      
                    ### CASO CMAP ###
                    if basedatos=='cmap':
                        if 'lista-variables' in changed_id or 'operacion' in changed_id:
                            figura=contourf(lonCM,latCM,np.mean(precipCM[:,:,mes],2),mes,'Precipitación [mm/mes]',minimo,maximo,'GnBu','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')
                            rangocolor=[minimo,maximo]
                        else:
                            figura=contourf(lonCM,latCM,np.mean(precipCM[:,:,mes],2),mes,'Precipitación [mm/mes]',rangocolor[0],rangocolor[1],'GnBu','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')
                    ### CASO NCEP ####
                    elif basedatos=='ncep':
                        figura=contourf(lon,lat,np.mean(precip[:,:,mes],2),mes,'Precipitación [mm/mes]',rangocolor[0],rangocolor[1],'GnBu','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')
                        
                    ### CASO GHCN ###
                    else:
                        if 'operacion' in changed_id:
                            figura=scattermap(lonGHprecip,latGHprecip,name_GHprecip,np.mean(precipGH.iloc[:,mes],1),mes,'Precipitación [mm/mes]',minimo,maximo,'GnBu','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')
                            rangocolor=[minimo,maximo]
                        else:
                            figura=scattermap(lonGHprecip,latGHprecip,name_GHprecip,np.mean(precipGH.iloc[:,mes],1),mes,'Precipitación [mm/mes]',rangocolor[0],rangocolor[1],'GnBu','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')

################ Presión a nivel del mar PROMEDIAR #############
                elif variable=='slp':
                    minimo=np.floor(np.nanpercentile(slp,perinf))
                    maximo=np.floor(np.nanpercentile(slp,persup))                     
                    ### CASO NCEP ###
                    if basedatos=='ncep':
                        if 'lista-variables' in changed_id or 'operacion' in changed_id:
                            figura=contourf(lon,lat,np.mean(slp[:,:,mes],2),mes,'Presión a nivel del mar [hPa]',minimo,maximo,'Geyser','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')
                            rangocolor=[minimo,maximo]
                        else:
                            figura=contourf(lon,lat,np.mean(slp[:,:,mes],2),mes,'Presión a nivel del mar [hPa]',rangocolor[0],rangocolor[1],'Geyser','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')
                    ### CASO ICOADS ###
                    else:
                        figura=contourf(lonCO,latCO,np.nanmean(slpCO[:,:,mes],2),mes,'Presión a nivel del mar [hPa]',rangocolor[0],rangocolor[1],'Geyser','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')
                        
################ Viento zonal 10m PROMEDIAR #############                        
                elif variable=='uwnd10':
                    minimo=-np.floor(np.nanpercentile(uwnd,persup))
                    maximo=np.floor(np.nanpercentile(uwnd,persup))                   
                    ### CASO NCEP ###
                    if 'lista-variables' in changed_id or 'operacion' in changed_id:
                        figura=contourf(lon,lat,np.mean(uwnd[:,:,mes],2),mes,'Viento zonal [m/s]',minimo,maximo,'balance','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')
                        rangocolor=[minimo,maximo]
                    else:
                        figura=contourf(lon,lat,np.mean(uwnd[:,:,mes],2),mes,'Viento zonal [m/s]',rangocolor[0],rangocolor[1],'balance','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')
                        
################ Viento meridional 10m PROMEDIAR #############    
                elif variable=='vwnd10':
                    ### CASO NCEP ###
                    minimo=-np.floor(np.nanpercentile(vwnd,persup))
                    maximo=np.floor(np.nanpercentile(vwnd,persup)) 
                    if 'lista-variables' in changed_id or 'operacion' in changed_id:
                        figura=contourf(lon,lat,np.mean(vwnd[:,:,mes],2),mes,'Viento meridional [m/s]',minimo,maximo,'balance','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')
                        rangocolor=[minimo,maximo]
                    else:
                        figura=contourf(lon,lat,np.mean(vwnd[:,:,mes],2),mes,'Viento meridional [m/s]',rangocolor[0],rangocolor[1],'balance','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')

################ Viento zonal 200 hPa PROMEDIAR #############                     
                elif variable=='uwnd200':
                    ### CASO NCEP ###
                    minimo=-np.floor(np.nanpercentile(uwnd200,persup))
                    maximo=np.floor(np.nanpercentile(uwnd200,persup)) 
                    if 'lista-variables' in changed_id or 'operacion' in changed_id:
                        figura=contourf(lon,lat,np.mean(uwnd200[:,:,mes],2),mes,'Viento zonal en 200 hPa [m/s]',minimo,maximo,'balance','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')
                        rangocolor=[minimo,maximo]
                    else:
                        figura=contourf(lon,lat,np.mean(uwnd200[:,:,mes],2),mes,'Viento zonal en 200 hPa [m/s]',rangocolor[0],rangocolor[1],'balance','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')

                        
################ Viento meridional 200hPa PROMEDIAR ############# 
                elif variable=='vwnd200':
                    ### CASO NCEP ###
                    minimo=-np.floor(np.nanpercentile(vwnd200,persup))
                    maximo=np.floor(np.nanpercentile(vwnd200,persup)) 
                    if 'lista-variables' in changed_id or 'operacion' in changed_id:
                        figura=contourf(lon,lat,np.mean(vwnd200[:,:,mes],2),mes,'Viento meridional en 200 hPa [m/s]',minimo,maximo,'balance','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')
                        rangocolor=[minimo,maximo]
                    else:
                        figura=contourf(lon,lat,np.mean(vwnd200[:,:,mes],2),mes,'Viento meridional en 200 hPa [m/s]',rangocolor[0],rangocolor[1],'balance','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')

################ Temperatura superficial del mar PROMEDIAR ############# 
                elif variable=='sst':
                    minimo=np.floor(np.nanpercentile(sstOI,perinf))
                    maximo=np.floor(np.nanpercentile(sstOI,persup)) 
                    ### CASO OISSTv2 ###
                    if basedatos=='oisstv2':
                        if 'lista-variables' in changed_id or 'operacion' in changed_id:
                            figura=contourf(lonOI,latOI,np.nanmean(sstOI[:,:,mes],2),mes,'Temperatura superficial del mar [⁰C]',minimo,maximo,'Jet','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')
                            rangocolor=[minimo,maximo]
                        else:
                            figura=contourf(lonOI,latOI,np.nanmean(sstOI[:,:,mes],2),mes,'Temperatura superficial del mar [⁰C]',rangocolor[0],rangocolor[1],'Jet','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')
                    ### CASO ICOADS ###
                    else:
                        #minimo=np.floor(np.nanmin(np.nanmean(sstCO[:,:,mes],2)))
                        #maximo=np.floor(np.nanmax(np.nanmean(sstCO[:,:,mes],2)))
                        figura=contourf(lonCO,latCO,np.nanmean(sstCO[:,:,mes],2),mes,'Temperatura superficial del mar [⁰C]',rangocolor[0],rangocolor[1],'Jet','rgba(50, 50, 50, .8)', 'Promedio climatológico (1981-2010)')
                else:
                    figura=contourf(lon,lat,tmean[:,:,0]*np.nan,' ',rangocolor[0],rangocolor[1],'Jet','rgba(50, 50, 50, .8)', '')
                return figura,minimo,maximo,[rangocolor[0],rangocolor[1]]    
            
        else: ################ ELSE NO SE SELECCIONA NINGUN MES #############
            if variable=='climo':
                if basedatos=='ghcn':
                    minimo=0
                    maximo=1000                  
                    figura=scattermap_climo(lonGHclimo,latGHclimo,name_GHclimo,elev_GHclimo,'Altura estación [m]',0,1000,'Cividis','rgba(50, 50, 50, .8)', 'Seleccione una estación haciendo click sobre ella')                          
                else:
                    minimo=-5000
                    maximo=5000                   
                    figura=contourf(lon,lat,land[:,:,0],'','Elevación del terreno [m]',-5000,5000,'delta','rgba(50, 50, 50, .8)', '')  
                return figura,minimo,maximo,[minimo,maximo]
            else:
                figura=contourf(lon,lat,tmean[:,:,0]*np.nan,'',' ',rangocolor[0],rangocolor[1],'Jet','rgba(50, 50, 50, .8)', '')
                return figura,-10000,10000,[-10000,10000]
        
##########################################################################################  
########################## OPERACION SUMA ################################################
##########################################################################################

    elif operacion=='suma':
        if len(mes)>0:
            mes=np.sort(mes)
            if variable==None or basedatos==None:
                figura=contourf(lon,lat,tmean[:,:,0]*np.nan,'',' ',rangocolor[0],rangocolor[1],'Jet','rgba(50, 50, 50, .8)','')
                return figura,-10000,10000,[-10000,10000]
            else:
                if variable=='climo':
                    if basedatos=='ghcn':
                        minimo=0
                        maximo=1000                  
                        figura=scattermap_climo(lonGHclimo,latGHclimo,name_GHclimo,elev_GHclimo,'Altura estación [m]',0,1000,'Cividis','rgba(50, 50, 50, .8)', 'Seleccione una estación haciendo click sobre ella')                          
                    else:
                        minimo=-5000
                        maximo=5000                   
                        figura=contourf(lon,lat,land[:,:,0],'','Elevación del terreno [m]',-5000,5000,'delta','rgba(50, 50, 50, .8)', '')
                    return figura,minimo,maximo,[minimo,maximo]
################ Precipitación SUMAR #############
                elif variable=='pp':
                    ### CASO CMAP ###
                    minimo=np.floor(np.nanpercentile(np.sum(precipCM[:,:,:],2),perinf))
                    maximo=np.floor(np.nanpercentile(np.sum(precipCM[:,:,:],2),persup))
                    if basedatos=='cmap':
                        #minimo=np.floor(np.min(np.sum(precipCM[:,:,mes],2)))
                        #maximo=np.floor(np.max(np.sum(precipCM[:,:,mes],2)))
                        if 'lista-variables' in changed_id:
                            figura=contourf(lonCM,latCM,np.sum(precipCM[:,:,mes],2),mes,'Precipitación [mm/mes]',minimo,maximo,'GnBu','rgba(50, 50, 50, .8)', 'Suma climatológica (1981-2010)')
                            rangocolor=[minimo,maximo]
                        else:
                            figura=contourf(lonCM,latCM,np.sum(precipCM[:,:,mes],2),mes,'Precipitación [mm/mes]',rangocolor[0],rangocolor[1],'GnBu','rgba(50, 50, 50, .8)', 'Suma climatológica (1981-2010)')
                    ### CASO NCEP ####
                    elif basedatos=='ncep':
                        figura=contourf(lon,lat,np.sum(precip[:,:,mes],2),mes,'Precipitación [mm/mes]',rangocolor[0],rangocolor[1],'GnBu','rgba(50, 50, 50, .8)', 'Suma climatológica (1981-2010)')
                                                    
                    ### CASO GHCN ###
                    else:
                        figura=scattermap(lonGHprecip,latGHprecip,name_GHprecip,np.sum(precipGH.iloc[:,mes],1),mes,'Precipitación [mm/mes]',rangocolor[0],rangocolor[1],'GnBu','rgba(50, 50, 50, .8)', 'Suma climatológica (1981-2010)')
                    return figura,minimo,maximo,[rangocolor[0],rangocolor[1]] 
        else: ################ ELSE NO SE SELECCIONA NINGUN MES ############# 
            if variable=='climo':
                if basedatos=='ghcn':
                    minimo=0
                    maximo=1000                  
                    figura=scattermap_climo(lonGHclimo,latGHclimo,name_GHclimo,elev_GHclimo,'Altura estación [m]',0,1000,'Cividis','rgba(50, 50, 50, .8)', 'Seleccione una estación haciendo click sobre ella')                          
                else:
                    minimo=-5000
                    maximo=5000                   
                    figura=contourf(lon,lat,land[:,:,0],'','Elevación del terreno [m]',-5000,5000,'delta','rgba(50, 50, 50, .8)', '')  
                return figura,minimo,maximo,[minimo,maximo]
            else:
                figura=contourf(lon,lat,tmean[:,:,0]*np.nan,'',' ',rangocolor[0],rangocolor[1],'Jet','rgba(50, 50, 50, .8)', '')
                return figura,-10000,10000,[-10000,10000]
        
##########################################################################################  
########################## OPERACION DIFERENCIA ############################################
##########################################################################################

    else:
        if len(mes)>0 and len(mesesresta)>0:
            mes=np.sort(mes)
            mesesresta=np.sort(mesesresta)
            if variable==None or basedatos==None:
                figura=contourf(lon,lat,tmean[:,:,0]*np.nan,'',' ',rangocolor[0],rangocolor[1],'Jet','rgba(50, 50, 50, .8)', '')
                return figura,-10000,10000,[-10000,10000]
            else:
                if variable=='climo':
                    if basedatos=='ghcn':
                        minimo=0
                        maximo=1000                  
                        figura=scattermap_climo(lonGHclimo,latGHclimo,name_GHclimo,elev_GHclimo,'Altura estación [m]',0,1000,'Cividis','rgba(50, 50, 50, .8)', 'Seleccione una estación haciendo click sobre ella')                          
                    else:
                        minimo=-5000
                        maximo=5000                   
                        figura=contourf(lon,lat,land[:,:,0],'','Elevación del terreno [m]',-5000,5000,'delta','rgba(50, 50, 50, .8)', '')  
                    
################ Temperatura media RESTA #############    
                elif variable=='tmean':
                    #### CASO NCEP ####
                    minimo=np.floor(np.nanpercentile(np.mean(tmean[:,:,mes],2)-np.mean(tmean[:,:,mesesresta],2),perinf))
                    maximo=np.floor(np.nanpercentile(np.mean(tmean[:,:,mes],2)-np.mean(tmean[:,:,mesesresta],2),persup))                    
                    if basedatos=='ncep':
                        if 'lista-variables' in changed_id:                 
                            figura=contourf_resta(lon,lat,np.mean(tmean[:,:,mes],2)-np.mean(tmean[:,:,mesesresta],2),mes,mesesresta,'Temperatura media [⁰C]',minimo,maximo,'Jet','rgba(250, 250, 250, .8)')
                            rangocolor=[minimo,maximo]
                        else:
                            figura=contourf_resta(lon,lat,np.mean(tmean[:,:,mes],2)-np.mean(tmean[:,:,mesesresta],2),mes,mesesresta,'Temperatura media [⁰C]',rangocolor[0],rangocolor[1],'Jet','rgba(250, 250, 250, .8)')
                            
                    ### CASO GHCN #####       
                    else:
                        figura=scattermap_resta(lonGHtmean,latGHtmean,name_GHtmean,np.mean(tmeanGH.iloc[:,mes],1)-np.mean(tmeanGH.iloc[:,mesesresta],1),mes,mesesresta,'Temperatura media [⁰C]',rangocolor[0],rangocolor[1],'Jet','rgba(50, 50, 50, .8)')
            
                        
################ Temperatura máxima RESTA #############  
                elif variable=='tmax':
                    #### CASO NCEP ####
                    minimo=np.floor(np.nanpercentile(np.mean(tmax[:,:,mes],2)-np.mean(tmax[:,:,mesesresta],2),perinf))
                    maximo=np.floor(np.nanpercentile(np.mean(tmax[:,:,mes],2)-np.mean(tmax[:,:,mesesresta],2),persup))   
                    if basedatos=='ncep':
                    
                        if 'lista-variables' in changed_id:
                            figura=contourf_resta(lon,lat,np.mean(tmax[:,:,mes],2)-np.mean(tmax[:,:,mesesresta],2),mes,mesesresta,'Temperatura máxima [⁰C]',minimo,maximo,'Jet','rgba(250, 250, 250, .8)')
                            rangocolor=[minimo,maximo]
                        else:
                            figura=contourf_resta(lon,lat,np.mean(tmax[:,:,mes],2)-np.mean(tmax[:,:,mesesresta],2),mes,mesesresta,'Temperatura máxima [⁰C]',rangocolor[0],rangocolor[1],'Jet','rgba(250, 250, 250, .8)')
                            
                    #### CASO GHCN ####
                    else:
                        figura=scattermap_resta(lonGHtmax,latGHtmax,name_GHtmax,np.mean(tmaxGH.iloc[:,mes],1)-np.mean(tmaxGH.iloc[:,mesesresta],1),mes,mesesresta,'Temperatura máxima [⁰C]',rangocolor[0],rangocolor[1],'Jet','rgba(50, 50, 50, .8)')
                        
################ Temperatura mínima RESTA #############
                elif variable=='tmin':
                    ### CASO NCEP ####
                    minimo=np.floor(np.nanpercentile(np.mean(tmin[:,:,mes],2)-np.mean(tmin[:,:,mesesresta],2),perinf))
                    maximo=np.floor(np.nanpercentile(np.mean(tmin[:,:,mes],2)-np.mean(tmin[:,:,mesesresta],2),persup))                   
                    if basedatos=='ncep':
                        if 'lista-variables' in changed_id:
                            figura=contourf_resta(lon,lat,np.mean(tmin[:,:,mes],2)-np.mean(tmin[:,:,mesesresta],2),mes,mesesresta,'Temperatura mínima [⁰C]',minimo,maximo,'Jet','rgba(250, 250, 250, .8)')
                            rangocolor=[minimo,maximo]
                        else:
                            figura=contourf_resta(lon,lat,np.mean(tmin[:,:,mes],2)-np.mean(tmin[:,:,mesesresta],2),mes,mesesresta,'Temperatura mínima [⁰C]',rangocolor[0],rangocolor[1],'Jet','rgba(250, 250, 250, .8)')
                    
                    ### CASO GHCN ###
                    else:
                        figura=scattermap_resta(lonGHtmin,latGHtmin,name_GHtmin,np.mean(tminGH.iloc[:,mes],1)-np.mean(tminGH.iloc[:,mesesresta],1),mes,mesesresta,'Temperatura mínima [⁰C]',rangocolor[0],rangocolor[1],'Jet','rgba(50, 50, 50, .8)')
                        
################ Precipitación RESTA #############
                elif variable=='pp':
                    ### CASO CMAP ###
                    minimo=np.floor(np.nanpercentile(np.sum(precipCM[:,:,mes],2)-np.sum(precipCM[:,:,mesesresta],2),perinf))
                    maximo=np.floor(np.nanpercentile(np.sum(precipCM[:,:,mes],2)-np.sum(precipCM[:,:,mesesresta],2),persup))                    
                    if basedatos=='cmap':

                        if 'lista-variables' in changed_id:
                            figura=contourf_resta(lonCM,latCM,np.sum(precipCM[:,:,mes],2)-np.sum(precipCM[:,:,mesesresta],2),mes,mesesresta,'Precipitación [mm/mes]',minimo,maximo,'GnBu','rgba(50, 50, 50, .8)')
                            rangocolor=[minimo,maximo]
                        else:
                            figura=contourf_resta(lonCM,latCM,np.sum(precipCM[:,:,mes],2)-np.sum(precipCM[:,:,mesesresta],2),mes,mesesresta,'Precipitación [mm/mes]',rangocolor[0],rangocolor[1],'GnBu','rgba(50, 50, 50, .8)')
                    ### CASO NCEP ####
                    elif basedatos=='ncep':
                        figura=contourf_resta(lonCM,latCM,np.sum(precip[:,:,mes],2)-np.sum(precip[:,:,mesesresta],2),mes,mesesresta,'Precipitación [mm/mes]',minimo,maximo,'GnBu','rgba(50, 50, 50, .8)')
                                            
                    ### CASO GHCN ###
                    else:
                        figura=scattermap_resta(lonGHprecip,latGHprecip,name_GHprecip,np.sum(precipGH.iloc[:,mes],1)-np.sum(precipGH.iloc[:,mesesresta],1),mes,mesesresta,'Precipitación [mm/mes]',rangocolor[0],rangocolor[1],'GnBu','rgba(50, 50, 50, .8)')

################ Presión a nivel del mar RESTA #############
                elif variable=='slp':
                    ### CASO NCEP ###
                    minimo=np.floor(np.nanpercentile(np.mean(slp[:,:,mes],2)-np.mean(slp[:,:,mesesresta],2),perinf))
                    maximo=np.floor(np.nanpercentile(np.mean(slp[:,:,mes],2)-np.mean(slp[:,:,mesesresta],2),persup))
                    if basedatos=='ncep':
                        if 'lista-variables' in changed_id:
                            figura=contourf_resta(lon,lat,np.mean(slp[:,:,mes],2)-np.mean(slp[:,:,mesesresta],2),mes,mesesresta,'Presión a nivel del mar [hPa]',minimo,maximo,'Geyser','rgba(50, 50, 50, .8)')
                            rangocolor=[minimo,maximo]
                        else:
                            figura=contourf_resta(lon,lat,np.mean(slp[:,:,mes],2)-np.mean(slp[:,:,mesesresta],2),mes,mesesresta,'Presión a nivel del mar [hPa]',rangocolor[0],rangocolor[1],'Geyser','rgba(50, 50, 50, .8)')
                    ### CASO ICOADS ###
                    else:
                        figura=contourf_resta(lonCO,latCO,np.nanmean(slpCO[:,:,mes],2)-np.nanmean(slpCO[:,:,mesesresta],2),mes,mesesresta,'Presión a nivel del mar [hPa]',rangocolor[0],rangocolor[1],'Geyser','rgba(50, 50, 50, .8)')
                        
################ Viento zonal 10m RESTA #############                        
                elif variable=='uwnd10':
                    ### CASO NCEP ###
                    minimo=np.floor(np.nanpercentile(np.mean(uwnd[:,:,mes],2)-np.mean(uwnd[:,:,mesesresta],2),perinf))
                    maximo=np.floor(np.nanpercentile(np.mean(uwnd[:,:,mes],2)-np.mean(uwnd[:,:,mesesresta],2),persup))
                    if 'lista-variables' in changed_id:
                        figura=contourf_resta(lon,lat,np.mean(uwnd[:,:,mes],2)-np.mean(uwnd[:,:,mesesresta],2),mes,mesesresta,'Viento zonal [m/s]',minimo,maximo,'balance','rgba(50, 50, 50, .8)')
                        rangocolor=[minimo,maximo]
                    else:
                        figura=contourf_resta(lon,lat,np.mean(uwnd[:,:,mes],2)-np.mean(uwnd[:,:,mesesresta],2),mes,mesesresta,'Viento zonal [m/s]',rangocolor[0],rangocolor[1],'balance','rgba(50, 50, 50, .8)')
                        
################ Viento meridional 10m RESTA #############    
                elif variable=='vwnd10':
                    ### CASO NCEP ###
                    minimo=np.floor(np.percentile(np.mean(vwnd[:,:,mes],2)-np.mean(vwnd[:,:,mesesresta],2),perinf))
                    maximo=np.floor(np.percentile(np.mean(vwnd[:,:,mes],2)-np.mean(vwnd[:,:,mesesresta],2),persup))
                    if 'lista-variables' in changed_id:
                        figura=contourf_resta(lon,lat,np.mean(vwnd[:,:,mes],2)-np.mean(vwnd[:,:,mesesresta],2),mes,mesesresta,'Viento meridional [m/s]',minimo,maximo,'balance','rgba(50, 50, 50, .8)')
                        rangocolor=[minimo,maximo]
                    else:
                        figura=contourf_resta(lon,lat,np.mean(vwnd[:,:,mes],2)-np.mean(vwnd[:,:,mesesresta],2),mes,mesesresta,'Viento meridional [m/s]',rangocolor[0],rangocolor[1],'balance','rgba(50, 50, 50, .8)')

################ Viento zonal 200 hPa RESTA #############                     
                elif variable=='uwnd200':
                    ### CASO NCEP ###
                    minimo=np.floor(np.nanpercentile(np.mean(uwnd200[:,:,mes],2)-np.mean(uwnd200[:,:,mesesresta],2),perinf))
                    maximo=np.floor(np.nanpercentile(np.mean(uwnd200[:,:,mes],2)-np.mean(uwnd200[:,:,mesesresta],2),persup))
                    if 'lista-variables' in changed_id:
                        figura=contourf_resta(lon,lat,np.mean(uwnd200[:,:,mes],2)-np.mean(uwnd200[:,:,mesesresta],2),mes,mesesresta,'Viento zonal en 200 hPa [m/s]',minimo,maximo,'balance','rgba(50, 50, 50, .8)')
                        rangocolor=[minimo,maximo]
                    else:
                        figura=contourf_resta(lon,lat,np.mean(uwnd200[:,:,mes],2)-np.mean(uwnd200[:,:,mesesresta],2),mes,mesesresta,'Viento zonal en 200 hPa [m/s]',rangocolor[0],rangocolor[1],'balance','rgba(50, 50, 50, .8)')

                        
################ Viento meridional 200hPa RESTA ############# 
                elif variable=='vwnd200':
                    ### CASO NCEP ###
                    minimo=np.floor(np.nanpercentile(np.mean(vwnd200[:,:,mes],2)-np.mean(vwnd200[:,:,mesesresta],2),perinf))
                    maximo=np.floor(np.nanpercentile(np.mean(vwnd200[:,:,mes],2)-np.mean(vwnd200[:,:,mesesresta],2),persup))
                    if 'lista-variables' in changed_id:
                        figura=contourf_resta(lon,lat,np.mean(vwnd200[:,:,mes],2)-np.mean(vwnd200[:,:,mesesresta],2),mes,mesesresta,'Viento meridional en 200 hPa [m/s]',minimo,maximo,'balance','rgba(50, 50, 50, .8)')
                        rangocolor=[minimo,maximo]
                    else:
                        figura=contourf_resta(lon,lat,np.mean(vwnd200[:,:,mes],2)-np.mean(vwnd200[:,:,mesesresta],2),mes,mesesresta,'Viento meridional en 200 hPa [m/s]',rangocolor[0],rangocolor[1],'balance','rgba(50, 50, 50, .8)')

################ Temperatura superficial del mar RESTA ############# 
                elif variable=='sst':
                    ### CASO OISSTv2 ###
                    minimo=np.floor(np.nanpercentile(np.nanmean(sstOI[:,:,mes],2)-np.nanmean(sstOI[:,:,mesesresta],2),perinf))
                    maximo=np.floor(np.nanpercentile(np.nanmean(sstOI[:,:,mes],2)-np.nanmean(sstOI[:,:,mesesresta],2),persup))
                    if basedatos=='oisstv2':
                        if 'lista-variables' in changed_id:
                            figura=contourf_resta(lonOI,latOI,np.nanmean(sstOI[:,:,mes],2)-np.nanmean(sstOI[:,:,mesesresta],2),mes,mesesresta,'Temperatura superficial del mar [⁰C]',minimo,maximo,'Jet','rgba(50, 50, 50, .8)')
                            rangocolor=[minimo,maximo]
                        else:
                            figura=contourf_resta(lonOI,latOI,np.nanmean(sstOI[:,:,mes],2)-np.nanmean(sstOI[:,:,mesesresta],2),mes,mesesresta,'Temperatura superficial del mar [⁰C]',rangocolor[0],rangocolor[1],'Jet','rgba(50, 50, 50, .8)')
                    ### CASO ICOADS ###
                    else:
                        figura=contourf_resta(lonCO,latCO,np.nanmean(sstCO[:,:,mes],2)-np.nanmean(sstCO[:,:,mesesresta],2),mes,mesesresta,'Temperatura superficial del mar [⁰C]',rangocolor[0],rangocolor[1],'Jet','rgba(50, 50, 50, .8)')
                else:
                    figura=contourf(lon,lat,tmean[:,:,0]*np.nan,' ',rangocolor[0],rangocolor[1],'Jet','rgba(50, 50, 50, .8)', '')
                return figura,minimo,maximo,[rangocolor[0],rangocolor[1]]    
            
        else: ################ ELSE NO SE SELECCIONA NINGUN MES ############# 
            if variable=='climo':
                if basedatos=='ghcn':
                    minimo=0
                    maximo=1000                  
                    figura=scattermap_climo(lonGHclimo,latGHclimo,name_GHclimo,elev_GHclimo,'Altura estación [m]',0,1000,'Cividis','rgba(50, 50, 50, .8)', 'Seleccione una estación haciendo click sobre ella')                          
                else:
                    minimo=-5000
                    maximo=5000                   
                    figura=contourf(lon,lat,land[:,:,0],'','Elevación del terreno [m]',-5000,5000,'delta','rgba(50, 50, 50, .8)', '')  
                return figura,minimo,maximo,[minimo,maximo]
            else:
                figura=contourf(lon,lat,tmean[:,:,0]*np.nan,'',' ',rangocolor[0],rangocolor[1],'Jet','rgba(50, 50, 50, .8)', '')
                return figura,-10000,10000,[-10000,10000]
            
#############################################################################
####### INTERACCION CON EL GRAFICO CLIMATOLOGIA EN UN PUNTO #################
#############################################################################        

@app.callback([
    Output('salida_prueba', 'children'),
    Output('graficoclim','figure'),
    Output('divgraficoclim','style')],
    [Input('mapaglobal', 'clickData'),
     Input('lista-variables', 'value'),
     Input('lista-basedatos', 'value'),
     Input('operacion', 'value')])
def callback_image(clickData,variable,basedato,operacion):
    if clickData==None or (operacion=='resta' or operacion=='suma') and variable!='climo':
        plotclim = {'data':[go.Scatter(
        x = [],
        y = [],
        mode='lines+markers',
        marker={'color':'red'}
        )],
        'layout':go.Layout(title='',yaxis = {'title':'','fixedrange':True},xaxis = {'title':'','showgrid': False,'fixedrange':True})
        }
        return [],plotclim,{'display':'none'}
    else:
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        plotclim_aux = {'data':[go.Scatter(
        x = [],
        y = [],
        mode='lines+markers',
        marker={'color':'red'}
        )],
        'layout':go.Layout(title='',yaxis = {'title':'','fixedrange':True},xaxis = {'title':'','showgrid': False,'fixedrange':True})
        }
        if variable =='climo':
            if basedato=='ghcn':
                if 'mapaglobal' in changed_id:
                    plotclim=grafico_puntoGHCNclimo(lonGHclimo,latGHclimo,name_GHclimo,elev_GHclimo,tmeanGHclimo,precipGHclimo,clickData,'lineas','red','Climograma')
                else:
                    plotclim=plotclim_aux
                    return [],plotclim,{'display':'none'}
            else:
                plotclim=grafico_climo(lon,lat,tmean,precip,clickData,'lineas','red','Climograma')
            return [],plotclim,{}
        elif variable =='tmean':
            if basedato=='ncep':
                plotclim=grafico_punto(lon,lat,tmean,clickData,'lineas','red','Temperatura media','⁰C')
            else:
                if 'mapaglobal' in changed_id:
                    plotclim=grafico_puntoGHCN(lonGHtmean,latGHtmean,name_GHtmean,elev_GHtmean,tmeanGH,clickData,'lineas','red','Temperatura media','⁰C')
                else:
                    plotclim=plotclim_aux
                    return [],plotclim,{'display':'none'}
        elif variable =='tmax':
            if basedato=='ncep':
                plotclim=grafico_punto(lon,lat,tmax,clickData,'lineas','red','Temperatura máxima','⁰C')
            else:
                if 'mapaglobal' in changed_id:
                    plotclim=grafico_puntoGHCN(lonGHtmax,latGHtmax,name_GHtmax,elev_GHtmax,tmaxGH,clickData,'lineas','red','Temperatura máxima','⁰C')
                else:
                    plotclim=plotclim_aux
                    return [],plotclim,{'display':'none'}
        elif variable =='tmin':
            if basedato=='ncep':
                plotclim=grafico_punto(lon,lat,tmin,clickData,'lineas','red','Temperatura mínima','⁰C')
            else:
                if 'mapaglobal' in changed_id:
                    plotclim=grafico_puntoGHCN(lonGHtmin,latGHtmin,name_GHtmin,elev_GHtmin,tminGH,clickData,'lineas','red','Temperatura mínima','⁰C')
                else:
                    plotclim=plotclim_aux
                    return [],plotclim,{'display':'none'}
        elif variable =='pp':
            if basedato=='cmap':
                plotclim=grafico_punto(lonCM,latCM,precipCM,clickData,'barras','lightblue','Precipitación promedio','mm/mes')
            elif basedato=='ncep':
                plotclim=grafico_punto(lon,lat,precip,clickData,'barras','lightblue','Precipitación promedio','mm/mes')
            else:
                if 'mapaglobal' in changed_id:
                    plotclim=grafico_puntoGHCN(lonGHprecip,latGHprecip,name_GHprecip,elev_GHprecip,precipGH,clickData,'barras','lightblue','Precipitación promedio','mm/mes')
                else:
                    plotclim=plotclim_aux
                    return [],plotclim,{'display':'none'}
        elif variable =='slp':
            if basedato=='ncep':
                plotclim=grafico_punto(lon,lat,slp,clickData,'lineas','brown','Presión a nivel del mar','hPa')
            else:
                plotclim=grafico_punto(lonCO,latCO,slpCO,clickData,'lineas','brown','Presión a nivel del mar','hPa')
        elif variable =='uwnd10':
            plotclim=grafico_punto(lon,lat,uwnd,clickData,'lineas','green','Viento zonal a 10m','m/s')
        elif variable =='vwnd10':
            plotclim=grafico_punto(lon,lat,vwnd,clickData,'lineas','green','Viento meridional a 10m','m/s')
        elif variable =='uwnd200':
            plotclim=grafico_punto(lon,lat,uwnd200,clickData,'lineas','green','Viento zonal a 200 hPa','m/s')
        elif variable =='vwnd200': 
            plotclim=grafico_punto(lon,lat,uwnd200,clickData,'lineas','green','Viento meridional a 200 hPa','m/s')               
        elif variable =='sst':
            if basedato=='oisstv2':
                plotclim=grafico_punto(lonOI,latOI,sstOI,clickData,'lineas','orange','Temperatura superficial del mar','⁰C')
            else:
                plotclim=grafico_punto(lonCO,latCO,sstCO,clickData,'lineas','orange','Temperatura superficial del mar','⁰C')
        else:
            plotclim = {'data':[go.Scatter(
            x = [],
            y = [],
            mode='lines+markers',
            marker={'color':'red'}
            )],
            'layout':go.Layout(title='',yaxis = {'title':'','fixedrange':True},xaxis = {'title':'','showgrid': False,'fixedrange':True})
            }            
        
        return [],plotclim,{}




#boton de descarga a csv
@app.callback(Output("exportarCsv", "data"), [Input("boton-exportarCsv", "n_clicks"),Input('graficoclim','figure')])
def generate_csv(n_clicks,figura):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    data_meses=figura['data'][0]['x']
    if len(figura['data'])==2:
        if None in figura['data'][0]['y']:
            data_y1=[np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan] 
            data_y2=np.around(figura['data'][1]['y'],decimals=2)
            adf1 = pd.DataFrame(data_y1, columns= ['precipitacion'],index=data_meses)
            adf2 = pd.DataFrame(data_y2, columns= ['temperatura'],index=data_meses)
            df = pd.merge(adf1,adf2,left_index=True, right_index=True, how='outer')
        elif None in figura['data'][1]['y']:
            data_y1=np.around(figura['data'][0]['y'],decimals=2)
            data_y2=[np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan] 
            adf1 = pd.DataFrame(data_y1, columns= ['precipitacion'],index=data_meses)
            adf2 = pd.DataFrame(data_y2, columns= ['temperatura'],index=data_meses)
            df = pd.merge(adf1,adf2,left_index=True, right_index=True, how='outer')
        else:
            data_y1=np.around(figura['data'][0]['y'],decimals=2)
            data_y2=np.around(figura['data'][1]['y'],decimals=2)
            adf1 = pd.DataFrame(data_y1, columns= ['precipitacion'],index=data_meses)
            adf2 = pd.DataFrame(data_y2, columns= ['temperatura'],index=data_meses)
            df = pd.merge(adf1,adf2,left_index=True, right_index=True, how='outer')            
            
    else:
        if None in figura['data'][0]['y']:
            data_y=[np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]    
            df = pd.DataFrame(data_y, columns= ['Datos'],index=data_meses) 
        else:
            data_y=np.around(figura['data'][0]['y'],decimals=2)    
            df = pd.DataFrame(data_y, columns= ['Datos'],index=data_meses)             
    if 'n_clicks' in changed_id: 
        return send_data_frame(df.to_csv, filename="serie_datos.csv")

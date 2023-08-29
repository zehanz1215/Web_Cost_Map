from flask import request, Flask, render_template, url_for, flash, redirect, request, jsonify
import folium
import sqlite3, os
import pandas as pd

app = Flask(__name__)
cities=f'static/usstates.json'
usState=pd.read_excel('static/usState.xlsx', header=0)

# make the us state lists:
usStateList=usState['state'].tolist()
usStateMaList=usState['Material'].tolist()
usStateInList=usState['Installation'].tolist()
usStateAveList=usState['Average'].tolist()

# make the us cities lists:
city=pd.read_excel('static/CostIndex.xlsx', header=0)
cityList=city['ab'].tolist()

@app.route('/')
# make the us states map, return the index:
def makeUSMap():
    usMap = folium.Map(location=[40,-95], zoom_start=4)
    folium.GeoJson(cities, name="geojson").add_to(usMap)
    # map for average index:
    folium.Choropleth(
        geo_data=cities,
        data=usState,
        columns=['state',"Average"],
        key_on="feature.properties.NAME",
        fill_color='YlGnBu',
        fill_opacity=1,
        line_opacity=0.2,
        legend_name="Average Index",
        smooth_factor=0,
        Highlight= True,
        line_color = "#0000",
        name = "Average Index",
        show=True,
        overlay=True,
        nan_fill_color = "White",
        bins=list(usState["Average"].quantile([0, 0.25, 0.5, 0.75, 1]))
        ).add_to(usMap)
    # map for material index:
    folium.Choropleth(
        geo_data=cities,
        data=usState,
        columns=['state',"Material"],
        key_on="feature.properties.NAME",
        fill_color='BuPu',
        fill_opacity=1,
        line_opacity=0.2,
        legend_name="Metarial Index",
        smooth_factor=0,
        Highlight= True,
        line_color = "#0000",
        name = "Material Index",
        show=False,
        overlay=True,
        nan_fill_color = "White",
        bins=list(usState["Material"].quantile([0, 0.25, 0.5, 0.75, 1]))
        ).add_to(usMap) 
    # map for installation index:
    folium.Choropleth(
        geo_data=cities,
        data=usState,
        columns=['state',"Installation"],
        key_on="feature.properties.NAME",
        fill_color='RdPu',
        fill_opacity=1,
        line_opacity=0.2,
        legend_name="Installation Index",
        smooth_factor=0,
        Highlight= True,
        line_color = "#0000",
        name = "Installation Index",
        show=False,
        overlay=True,
        nan_fill_color = "White",
        bins=list(usState["Installation"].quantile([0, 0.25, 0.5, 0.75, 1]))
        ).add_to(usMap)     
    # Add hover functionality.
    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}
    NIL = folium.features.GeoJson(
        data = 'static/usstates.json',
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        tooltip=folium.features.GeoJsonTooltip(
            fields=['NAME','Material','Installation','Average'],
            aliases=['State','Material Index','Installation Index','Average Index'],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
        )
    )
    usMap.add_child(NIL)
    usMap.keep_in_front(NIL)
    # add layer control:
    folium.LayerControl(collapsed=False).add_to(usMap)
    usMap.save('templates/usMap.html')
    return render_template('index.html', usStateList=usStateList, len=len(usStateList),
                            usStateMaList=usStateMaList, usStateInList=usStateInList,
                            usStateAveLsit=usStateAveList)

# return the us states map:
@app.route('/usMap')
def usMap():
    return render_template('usMap.html')

# find the index data using the state information that the user selected on html:
@app.route('/_findData', methods=['POST'])
def findData():
    if request.method == "POST":
        i=request.json['i']
        material=usStateMaList[int(i)]
        installation=usStateInList[int(i)]
        average=usStateAveList[int(i)]
    return jsonify({'material':material,'installation':installation,'average':average})

# find the value data from the input and calculate the estimation of cost from average and material & installation:
@app.route('/estimation',methods=['POST'])
def estimate():
    if request.method == "POST":
        materialValue=request.json['valueM']
        installationValue=request.json['valueI']
        averageValue=request.json['valueA']
        indexM=request.json['indexM']
        indexI=request.json['indexI']
        indexA=request.json['indexA']
        result1=(100+float(indexA))*float(averageValue)*150/100
        result2=(100+float(indexI))*float(installationValue)*128/100+(100+float(indexM))*float(materialValue)*166/100
    return jsonify({'aveR':result1,'mandIR':result2})
        
# make different state maps:
@app.route('/<state>')
def makeStateMap():
    usMap = folium.Map(location=[40,-95], zoom_start=6)
    folium.GeoJson(f'static/cities/'+'.json', name="geojson").add_to(usMap)

# statePage (future work):
@app.route('/statePage')
def statePage():
    file=f'static/cities/pa.json'
    stateMap = folium.Map(location=[40,-95], zoom_start=6)
    folium.GeoJson(file, name="geojson").add_to(stateMap)   

    # map for average index:
    folium.Choropleth(
        geo_data=file,
        data=city[city['ab']=='pa'],
        columns=['city',"Average"],
        key_on="feature.properties.NAME",
        fill_color='YlGnBu',
        fill_opacity=1,
        line_opacity=0.2,
        legend_name="Average Index",
        smooth_factor=0,
        Highlight= True,
        line_color = "#0000",
        name = "Average Index",
        show=True,
        overlay=True,
        nan_fill_color = "White"
        ).add_to(stateMap)
    # map for material index:
    folium.Choropleth(
        geo_data=file,
        data=city,
        columns=['city',"Material"],
        key_on="feature.properties.NAME",
        fill_color='BuPu',
        fill_opacity=1,
        line_opacity=0.2,
        legend_name="Metarial Index",
        smooth_factor=0,
        Highlight= True,
        line_color = "#0000",
        name = "Material Index",
        show=False,
        overlay=True,
        nan_fill_color = "White"
        ).add_to(stateMap) 
    # map for installation index:
    folium.Choropleth(
        geo_data=file,
        data=city,
        columns=['city',"Installation"],
        key_on="feature.properties.NAME",
        fill_color='RdPu',
        fill_opacity=1,
        line_opacity=0.2,
        legend_name="Installation Index",
        smooth_factor=0,
        Highlight= True,
        line_color = "#0000",
        name = "Installation Index",
        show=False,
        overlay=True,
        nan_fill_color = "White"
        ).add_to(stateMap)     
    # Add hover functionality.
    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}
    # add layer control:
    folium.LayerControl(collapsed=False).add_to(stateMap)
    stateMap.save('templates/stateMap.html')    
    return render_template('state.html', usStateList=usStateList)


def main():
    return render_template('index.html', usStateList=usStateList, len=len(usStateList),
                            usStateMaList=usStateMaList, usStateInList=usStateInList,
                            usStateAveLsit=usStateAveList)

if __name__ == "__main__":

    app.run(debug=True)
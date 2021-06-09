import requests as r
import pandas as pd
import folium
import plotly.express as px
from folium.plugins import MarkerCluster

def add_lat_long_coordinates(art_no_lat_lon_df, col_name):
    """
    Parameters
    ----------
    art_no_lat_lon_df (dataframe object) contains dataframe with column col_name containing coordinates in a list
    col_name (string) name of column
    
    Returns
    -------
    art_df (dataframe object) dataframe with new columns latitude and longitue
    
    """
    
    art_df = art_no_lat_lon_df.copy()
    
    # After removing empty entries, we can then iterate over them
    clean_list_of_coordinates = art_df[col_name].to_list()

    # not super efficient way of doing things, but they get it done
    latitude = []
    longitude = []
    # Iterate over every pair of coordinates
    for item in clean_list_of_coordinates:
        longitude.append(item[0])
        latitude.append(item[1])
        
    art_df['latitude'] = latitude
    art_df['longitude'] = longitude
    
    return art_df


def create_base_map(lat, long):
    """
    Parameters
    ----------
    lat (float): latitude for a location
    long (float): longitude for a location
    
    Returns
    -------
    map_van (folium.Map object) displays map of given latitude and longitude
    """
    coordinates = [latitude_van, longitude_van]

    map_ = folium.Map(location=coordinates,
                    zoom_start=10,
                    tiles="Stamen Terrain")
    
    return map_


def add_data_points(data_df, marker_cluster):
    
    """
    Parameters
    ----------
    data_df (dataframe object) dataframe with latitude longitue coordinates
    marker_cluster (folium.plugins.MarkerCluster object) base map with marker cluster properties
    
    Returns
    -------
    None
    """
    
    # Iterate over each record in our dataset 
    # try subset first
    max_records = len(data_df)
    # Iterating over each record
    for row in data_df[0:max_records].iterrows():
        # Use folium.Marker function, and use latitude and longitude coordinates
        folium.Marker(location=[ row[1]['latitude'], row[1]['longitude']], 
                     # Add art url
                      popup = folium.Popup(row[1]['fields.url'], sticky=True),
                      # Make changes to icon
                      icon = folium.Icon(color='red', icon='glyphicon glyphicon-eye-open'),
                      # Make sure they cluster well
                      clustered_marker = True).add_to(marker_cluster)



if __name__ == '__main__':
    
    print("Downloading data")
    
    ## Reading the data
    # Access data through link
    art_link = "https://opendata.vancouver.ca/api/records/1.0/search/?dataset=public-art&rows=500&facet=type&facet=status&facet=sitename&facet=siteaddress&facet=primarymaterial&facet=ownership&facet=neighbourhood&facet=artists&facet=photocredits"
    print("Parse data into table")
    # Get the data
    API_response_trees = r.get(art_link)
    # Parse data as JSON object
    data = API_response_trees.json()
    print("Success!")
    # Parse as dataframe
    public_art_df = pd.json_normalize(data, record_path= "records")
    
    # Then we can clean up
    # Removing empty entries from coordinates column
    public_art_df.dropna(subset=["fields.geom.coordinates"], inplace = True)
    # add lat lon coordinates
    public_art_df = add_lat_long_coordinates(public_art_df, "fields.geom.coordinates")
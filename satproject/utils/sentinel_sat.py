# For testing
# from env import TOP_COORD, LEFT_COORD, RIGHT_COORD, BOTTOM_COORD, START_DATE, END_DATE
# from env import SENTINEL_API_USERNAME, SENTINEL_API_PASSWORD

from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt

def query_SentinelAPI(top_coord, left_coord, bottom_coord, right_coord, start_date, end_date, api_username, api_password, platform_name='Sentinel-2', max_cc_percentage=30):
    print("querying")
    
    api = SentinelAPI(api_username, api_password, 'https://apihub.copernicus.eu/apihub')
    footprint = f'POLYGON(({top_coord} {left_coord},{top_coord} {right_coord},{bottom_coord} {right_coord},{bottom_coord} {left_coord}, {top_coord} {left_coord}))'
    products = api.query(footprint, 
        date=(start_date, end_date), 
        platformname = platform_name, )
        #cloudcoverpercentage=(0, max_cc_percentage))
    
    products_df = api.to_dataframe(products)

    print(products_df.size)
    
    #sort by cloud cover and ingestion date
    # products_df_sorted = products_df.sort_values(['cloudcoverpercentage', 'ingestiondate'], ascending=[True, True])
    # products_df_sorted = products_df.sort_values(['ingestiondate'], ascending=[True, True])


    # if products_df_sorted.size == 0:
    if products_df.size == 0:
        raise Exception("No satellite image could be found during the specified times that contains the entire area of interest")

    #print first product's data & download
    # first_product = products_df_sorted.head(1).index
    first_product = products_df.head(1).index
    print(first_product)
    api.download_all(first_product)

    title = api.get_product_odata(first_product)['title']
    return title

# For testing:
# query_SentinelAPI(TOP_COORD, LEFT_COORD, RIGHT_COORD, BOTTOM_COORD, START_DATE, END_DATE)




































# def query_SentinelAPI(top_coord, left_coord, bottom_coord, right_coord):
#     print("querying")
    
#     api = SentinelAPI(SENTINEL_API_USERNAME, SENTINEL_API_PASSWORD, 'https://apihub.copernicus.eu/apihub')

#     # search by polygon, time, and SciHub query keywords
#     #footprint = 'POLYGON ((34.322010 0.401648,36.540989 0.876987,36.884121 -0.747357,34.664474 -1.227940,34.322010 0.401648))' #geojson_to_wkt(read_geojson('map.geojson'))
#     footprint = f'POLYGON(({top_coord} {left_coord},{top_coord} {right_coord},{bottom_coord} {right_coord},{bottom_coord} {left_coord}, {top_coord} {left_coord}))'
#     products = api.query(footprint,
#                         date=('20151219', date(2015, 12, 29)),
#                         platformname='Sentinel-2')

#     # convert to Pandas DataFrame
#     products_df = api.to_dataframe(products)

#     print(products_df.size)

#     # sort and limit to first 5 sorted products
#     products_df_sorted = products_df.sort_values(['cloudcoverpercentage', 'ingestiondate'], ascending=[True, True])
#     products_df_sorted = products_df_sorted.head(5)

#     # download sorted and reduced products
#     #api.download_all(products_df_sorted.index)
    



#     # api = SentinelAPI(SENTINEL_API_USERNAME, SENTINEL_API_PASSWORD, 'https://apihub.copernicus.eu/apihub')
#     # footprint = f'POLYGON(({top_coord} {left_coord},{top_coord} {right_coord},{bottom_coord} {right_coord},{bottom_coord} {left_coord}, {top_coord} {left_coord}))'
#     # products = api.query(footprint, 
#     #     date=(start_date, end_date), 
#     #     platformname = platform_name, )
#     #     #cloudcoverpercentage=(0, max_cc_percentage))
    
#     # products_df = api.to_dataframe(products)

#     # print(products_df.size)
    
#     # #sort by cloud cover and ingestiondate
#     # products_df_sorted = products_df.sort_values(['cloudcoverpercentage', 'ingestiondate'], ascending=[True, True])
#     # first_product = products_df_sorted.head(1).index


#     # #print product data & download
#     # api.download_all(first_product)
# #{"type":"Polygon","coordinates":[[[-84.526543,39.093075],[-84.526543,39.15277],[-84.425262,39.15277],[-84.425262,39.093075],[-84.526543,39.093075]]]}
# query_SentinelAPI(-84.526543, 39.093075, -84.425262, 39.15277)
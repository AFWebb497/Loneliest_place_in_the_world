import rasterio
import matplotlib as plt
import time
import numpy as np
import scipy.ndimage
import random
import pyproj
from rasterio.crs import CRS
from rasterio import warp

for boundary in range(0,10000,500):

    prog_time_start = time.time()

        
    print(boundary)
    final_dictionary = {}
    final_list = []
    no_of_tiles_scanned = 1
    file_path = str(boundary) + ',' + str(boundary) + '.txt'
    print(file_path)


    # Get the path to the large raster dataset
    input_dataset_path = 'GHS_POP_E2030_GLOBE_R2023A_54009_100_V1_0.tif'

    # Open the dataset
    with rasterio.open(input_dataset_path) as src:
        print(f"Dataset size is = {src.shape}")

        target_crs = CRS.from_epsg(4326)

        


        
        # Generate window size (anything over 10000 crashes)
        window_size_x = 10000
        window_size_y = 10000

        # Get original dimensions
        width = src.width
        height = src.height

        #Begin loop
        for x in range(boundary, width, window_size_x):
            for y in range(boundary, height, window_size_y):
                print("New Window")
                print(f"Window shape is ({y}-{y+9999},{x}-{x+9999})")

                window_time_start = time.time()

                # Define the window to read
                window = rasterio.windows.Window(x, y, window_size_x, window_size_y)

                window_time_end = time.time()

                window_time_taken = window_time_end - window_time_start

                print(f'Window Generation, Time Taken : {window_time_taken}')


                # Read the data for the specified window
                data = src.read(1, window=window)
                if np.all(data == -200):
                    print(f"Tiles Scanned: {no_of_tiles_scanned}")
                    no_of_tiles_scanned+=1
                    print("Open Ocean, go to next tile")
                    continue

                binary_mask  = np.where(data != 0,0,1)
                
                distance_time_start = time.time()
                
                distance_transform = scipy.ndimage.distance_transform_edt(binary_mask)
                
                distance_time_end = time.time()
                distance_time_taken = distance_time_end - distance_time_start
                print(f"Distance Transform, Time Taken : {distance_time_end - distance_time_start}")


                
                mollweide_time_start = time.time()
                
                    
                max_distance = np.max(distance_transform)
                max_distance_location = np.argwhere(distance_transform == max_distance)
                
                #print(max_distance_indices)
                isolated_point = random.choice(max_distance_location)

                #print(i)
                distance_transform[isolated_point[0],isolated_point[1]]
                (full_array_x,full_array_y ) = (y+isolated_point[0],x+isolated_point[1])
                print(full_array_x,full_array_y)

                mollweide_x, mollweide_y = src.xy(full_array_x,full_array_y)


                mollweide_time_end = time.time()
                mollweide_time_taken = mollweide_time_end - mollweide_time_start
                print(f"Mollweide Generation, Time Taken : {mollweide_time_taken}")


                
                large_population_time_start = time.time()
                data[data == -200] = 0
                large_population = np.sum(data)

                large_population_time_end = time.time()
                large_population_time_taken = large_population_time_end - large_population_time_start
                print(f"Large Population Calculation, Time Taken : {large_population_time_taken}")


                small_population_time_start = time.time()


                grid_size = data.shape
                


                # Define the size of the smaller window
                small_window_size = 2000

                center_i = isolated_point[0]
                center_j = isolated_point[1]


                # Calculate indices for the surrounding window
                min_row = max(0, center_i - small_window_size // 2)
                max_row = min(grid_size[0], center_i + small_window_size // 2 + 1)
                min_col = max(0, center_j - small_window_size // 2)
                max_col = min(grid_size[1], center_j + small_window_size // 2 + 1)

                # Extract the subarray corresponding to the surrounding window
                smallwindow = data[min_row:max_row, min_col:max_col]
                small_population = np.sum(smallwindow)

                small_population_time_end = time.time()
                small_population_time_taken = small_population_time_end - small_population_time_start
                print(f"Small Population, Time Taken : {small_population_time_taken}")


                longitude_latitude__time_start = time.time()


                target_crs = 'EPSG:4326'

                print("Calculating Long and Lat")

                mollweide_proj = pyproj.CRS.from_wkt('PROJCS["World_Mollweide",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mollweide"],PARAMETER["central_meridian",0],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]')
                # Define the PROJ string for Mollweide projection
                wgs84_proj = pyproj.CRS.from_epsg(4326)  # EPSG code for WGS84
                # Create a pyproj transformer for the coordinate transformation
                transformer = pyproj.Transformer.from_crs(mollweide_proj, wgs84_proj,always_xy=True)
                longitude, latitude = transformer.transform(mollweide_x,mollweide_y)

                longitude_latitude__time_end = time.time()
                longitude_latitude__time_taken = longitude_latitude__time_end - longitude_latitude__time_start
                print(f"Longitude and Latitude Generation, Time Taken : {longitude_latitude__time_taken}")

            
                print(f"Candidate is {latitude,longitude}")
                
                final_list.append([(latitude,longitude),(mollweide_x,mollweide_y),(full_array_x,full_array_y),distance_transform[isolated_point[0],isolated_point[1]],large_population,small_population])
                final_dictionary[(latitude,longitude)] = distance_transform[isolated_point[0],isolated_point[1]]
                with open(file_path, "a") as file:
                    file.write(str([(latitude,longitude),(mollweide_x,mollweide_y),(full_array_x,full_array_y),distance_transform[isolated_point[0],isolated_point[1]],large_population,small_population]) + "\n")


                print("Real world coordinates logged and saved")

                print(f"Tiles Scanned: {no_of_tiles_scanned}")
                no_of_tiles_scanned+=1

                print(f'Window: {window_time_taken}')
                print(f'Distance Transform : {distance_time_taken}')
                print(f'Mollweide Generation : {mollweide_time_taken}')
                print(f'Large Population Generation : {large_population_time_taken}')
                print(f'Small Population Generation : {small_population_time_taken}')
                print(f'Longitude and Latitude Generation : {longitude_latitude__time_taken}')



    


print(final_dictionary)  
for i in final_list:
    print(i)      
        
prog_time_end = time.time()
print(f"Time Taken : {prog_time_end - prog_time_start}")

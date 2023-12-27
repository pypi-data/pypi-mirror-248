from math import radians,sin,cos,asin,sqrt,atan2,degrees
class Grid:
    def __init__(self, lat, long, gridSize) -> None:
        self.lat = float(lat)
        self.long = float(long)
        self.gridSize = gridSize

    def calculate_distance(self, lat1, long1, lat2, long2) -> float:
        """
        Calculate the distance between two coordinates on Earth.

        Args:
            lat1 (float): Latitude of the first coordinate.
            lon1 (float): Longitude of the first coordinate.
            lat2 (float): Latitude of the second coordinate.
            lon2 (float): Longitude of the second coordinate.

        Returns:
            float: The distance between the two coordinates in meters.
        """
        long1 = radians(float(long1))
        long2 = radians(float(long2))
        lat1 = radians(float(lat1))
        lat2 = radians(float(lat2))

        # Haversine formula
        dlong = long2 - long1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlong / 2)**2

        c = 2 * asin(sqrt(a))

        # Radius of earth in meters. Use 3956 for miles
        r = 6371 * 1000

        distance = c*r
        return(distance)

    def getLatLong(self, lat, long, d, bear):
        """
        Calculate latitude and longitude from a starting point, distance, and bearing.

        Args:
            lat (float): Starting latitude in degrees.
            lon (float): Starting longitude in degrees.
            d (float): Distance to travel in meters.
            bear (float): Bearing in degrees.

        Returns:
            Tuple[float, float]: A tuple containing the latitude and longitude of the destination point in degrees.
        """
        long = radians(long)
        lat = radians(lat)
        bear = radians(bear)
        R = 6371 * 1000 #Radius of the Earth in meters

        lat2 = asin( sin(lat)*cos(d/R) +
            cos(lat)*sin(d/R)*cos(bear))

        long2 = long + atan2(sin(bear)*sin(d/R)*cos(lat),
                    cos(d/R)-sin(lat)*sin(lat2))

        lat2 = degrees(lat2)
        long2 = degrees(long2)

        return lat2,long2
    
    def getGrdiId(self) -> str:
        """
        Create a custom grid ID based on the given latitude, longitude, and grid size.

        Returns:
            str: A string representing the grid ID in the format of "<grid_size>_<vertical_axis>_<horizontal_axis>".
        """
        distance_horizontal = self.calculate_distance(0,self.lon,0,94.9527682)
        distance_vertical = self.calculate_distance(self.lat,94.9527682,0,94.9527682)

        step_horizontal = int(distance_horizontal/self.gridSize)
        step_vertical = int(distance_vertical/self.gridSize)

        if self.lat >= 0:
            grid_id = str(self.gridSize) + '_' + str(step_vertical) + '_' + str(step_horizontal)
        else:
            grid_id = str(self.gridSize) + '_-' + str(step_vertical+1) + '_' + str(step_horizontal)

        return grid_id

    def decodeGeohash(self):
        """
        Converts a grid ID to latitude and longitude coordinates for each angle.

        Returns:
            dict: A dictionary containing the latitude and longitude coordinates for each angle, as well as the centroid of the grid.
        """
        interval,step_north,step_east = self.getGrdiId().split('_')
        interval = int(interval)
        direction_north = step_north[0]
        distance_east = int(step_east) * interval

        if direction_north!='-':
            distance_north = int(step_north) * interval
            bear_vertical = 0
        else:
            distance_north = (int(step_north)+1) * interval
            bear_vertical = 180

        distance_north = abs(distance_north)
        res_n1 = self.getLatLong(0,94.9527682,distance_north,bear_vertical)
        res_e1 = self.getLatLong(0,94.9527682,distance_east,90)
        res_ne1 = [res_n1[0],res_e1[1]]

        res_n2 = self.getLatLong(res_ne1[0],res_ne1[1],interval,bear_vertical)
        res_e2 = self.getLatLong(res_ne1[0],res_ne1[1],interval,90)
        res_ne2 = [res_n2[0],res_e2[1]]

        res_n_centroid = self.getLatLong(res_ne1[0],res_ne1[1],interval/2,bear_vertical)[0]
        res_e_centroid = self.getLatLong(res_ne1[0],res_ne1[1],interval/2,90)[1]
        res_ne_centroid = [res_n_centroid,res_e_centroid]

        dict_rect = {
            'point1':res_ne1,
            'point2':[res_ne1[0],res_ne2[1]],
            'point3':[res_ne2[0],res_ne1[1]],
            'point4':res_ne2,
            'centroid':res_ne_centroid
        }
        return dict_rect
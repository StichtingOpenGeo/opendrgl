from osgeo.osr import SpatialReference, CoordinateTransformation

__author__ = 'joelthuis'

def rd_wgs84(x, y):
    '''
    With help from https://publicwiki.deltares.nl/display/OET/Python+convert+coordinates
    :param x: RD-x
    :param y: RD-y
    :return: Lat, lon
    '''
    # Define the Rijksdriehoek projection system (EPSG 28992)
    epsg28992 = SpatialReference()
    epsg28992.ImportFromEPSG(28992)

    # correct the towgs84
    epsg28992.SetTOWGS84(565.237,50.0087,465.658,-0.406857,0.350733,-1.87035,4.0812)

    # Define the wgs84 system (EPSG 4326)
    epsg4326 = SpatialReference()
    epsg4326.ImportFromEPSG(4326)

    rd2latlon = CoordinateTransformation(epsg28992, epsg4326)
    #latlon2rd = CoordinateTransformation(epsg4326, epsg28992)

    # Check the transformation for a point close to the centre of the projected grid
    return rd2latlon.TransformPoint(x, y)
    return latlonz
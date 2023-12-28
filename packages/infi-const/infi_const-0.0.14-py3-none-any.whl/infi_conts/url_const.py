class UrlConsts:
    """
    Centralized location for all service URLs used in the application.
    """
    AZCOPY_API_URL: str = "http://infinity-serivces.westeurope.cloudapp.azure.com:8080/send_to_azcopy"

    TGV_API_URL: str = "http://infinity-serivces.westeurope.cloudapp.azure.com:8080/tgv_process"

    WALL_E_SOLUTION_SKYLINE_SERVICE: str = 'https://pmapi.skylineglobe.com/startproject/Mipui/poda/a247acd3-977c-4a77-b93f-e713a8632d57'

    WAR_E_SOLUTION_SKYLINE_SERVICE: str = 'https://pmapi.skylineglobe.com/startproject/Mipui/podb/a247acd3-977c-4a77-b93f-e713a8632d57'
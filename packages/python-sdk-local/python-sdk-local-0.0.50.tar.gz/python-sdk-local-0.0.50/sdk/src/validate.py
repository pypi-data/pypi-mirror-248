import os

def validate_enviroment_variables():
    if(os.getenv("ENVIRONMENT_NAME") is None):
        raise Exception("logger-local-python-package LoggerLocal.py please add Environment Variable called ENVIRONMENT_NAME=local or play1 (instead of ENVIRONMENT)")
    if(os.getenv("BRAND_NAME") is None):
        raise Exception("logger-local-python-package LoggerLocal.py please add Environment Variable called BRAND_NAME=Circlez")
    # if(os.getenv("PRODUCT_USER_IDENTIFIER") is None):
    #     raise Exception("logger-local-python-package LoggerLocal.py please add Environment Variable called PRODUCT_USER_IDENTIFIER (instead of PRODUCT_USERNAME)")
    #removed by Idan because it dont has to be in every project
    # if(os.getenv("PRODUCT_PASSWORD") is None): 
    #     raise Exception("logger-local-python-package LoggerLocal.py please add Environment Variable called PRODUCT_PASSWORD")
    if(os.getenv("LOGZIO_TOKEN") is None):
        raise Exception("logger-local-python-package LoggerLocal.py please add Environment Variable called LOGZIO_TOKEN=cXNHuVkkffkilnkKzZlWExECRlSKqopE")
    
 

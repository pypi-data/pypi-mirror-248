
import io
import cv2
from starlette.responses import StreamingResponse
from iscte.piops import version as piops
from iscte.piops.analysis import distributions as dist
import numpy as np
from json import loads, dumps
from typing import Union
from fastapi.responses import JSONResponse
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    piops.version()
    return piops.version()
    
@app.get("/fit")
def read_root():
    piops.version()
    x = dist.distfit()
    x.fit()
    y = x.summary(10, plot=False)
    result = y.to_json(orient="index")
    #parsed = loads(result)
    #z = dumps(parsed, indent=4)  
    #im_png = cv2.imencode(".png", np.array(y.plot()))[1]
    
    #data_encode = np.array(im_png) 
    #byte_encode = data_encode.tobytes() 

    #return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")
    #print(parsed)
    return JSONResponse(content = loads( result ))
    #return str(z) #{"Message": }


@app.get("/bestfit")
def get_best():
    x = dist.distfit()
    x.fit()
    return str(x.get_best()) #{"Message": }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}



from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn
import utils

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# templates = Jinja2Templates(directory="templates")

# Loading the Excel data
ephemeris = pd.read_csv("ephemeris.csv").fillna('')
radiotelescopes = pd.read_csv("AllRadiotelescopes.csv").fillna('')
names = [x for x in (radiotelescopes['Name']) if x]

@app.get("/")
async def main():
    # request: Request):
    # return templates.TemplateResponse("index.html",{"request":request})
    pass


@app.get("/observatories")
async def observatories_list():
    return names

@app.get("/observatories_info")
async def print_obs_info(
    # request: Request,
    id1: int, # str = Query(names[0],enum=names),
    id2: int, # str = Query(names[1],enum=names),
    remarks: bool = Query(False,enum=[True,False])):
    columns = ["Name","Location","Longitude","Latitude","Power","Diameter"]
    if remarks:
        columns.append("Remarks")
    obs1 = radiotelescopes.iloc[id1] # radiotelescopes.loc[radiotelescopes['Name'] == id1].iloc[0]
    obs2 = radiotelescopes.iloc[id2] # radiotelescopes.loc[radiotelescopes['Name'] == id2].iloc[0]
    obss = [obs1,obs2]
    jsonNames = [0,1]

    obj = {}
    for i in range(2):
        obj[jsonNames[i]] = {column:obss[i][column] for column in columns}

    return obj
    # return templates.TemplateResponse("observatories_info.html",{"request":request, **obj})

@app.get("/ephemeris_info")
async def ephemeris_info(
    # request: Request,
    id1: int, # str = Query(names[0],enum=names),
    id2: int): # str = Query(names[1],enum=names),):
    obs1 = radiotelescopes.iloc[id1] # radiotelescopes.loc[radiotelescopes['Name'] == id1].iloc[0]
    obs2 = radiotelescopes.iloc[id2]
    obj = utils.table2(obs1,obs2,ephemeris)
    return obj
    # return templates.TemplateResponse("ephemeris_data.html",{"request":request, **obj})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
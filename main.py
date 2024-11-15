from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from info_text import *
from functions import SepTeam

sep = SepTeam()
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/projects")
async def projects(request: Request):
    return templates.TemplateResponse("projects.html", {"request": request})




#### Gráficos ####
@app.get("/septeams", response_class=HTMLResponse)
def get_graph_page(request: Request, graph_type: str = Query(default="last_survey")):
    info = ""
    stats = ""
    graph_html = ""

    # Manejo de las opciones de gráficos
    if graph_type not in ["global", "tw_evolution", "hs_evolution", "last_survey"]:
        graph_type = "last_survey"

    if graph_type == "global":
        global_evaluations = sep.global_mean_each_member()
        graph_html = sep.graph(evaluations=global_evaluations, title="All Time View", means=sep.global_mean())
        info = info_global
        stats = all_time_stats
    elif graph_type == "tw_evolution":
        graph_html = sep.tw_evolution()
        info = info_team_work_evolution
    elif graph_type == "hs_evolution":
        graph_html = sep.hs_evolution()
        info = info_hard_skill_evolution
    elif graph_type == "last_survey":
        last_survey = sep.last_survey()
        graph_html = sep.graph(evaluations=last_survey, title="Last Survey", means=sep.last_mean())
        info = info_last_survey
        stats = last_survey_stats

    return templates.TemplateResponse("septeams.html", {
        "request": request,
        "graph_html": graph_html,
        "info": info,
        "stats": stats
    })
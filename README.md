# basal_mom5

A collaborative project to work on the ACCESS-OM2-01 + "basal melt distributed at depth parameterization" simulations. This is a central repository where we can propose different scenarios that could affect the overall impact of fresh water input at depth. Diagnostics, figures, scripts, and/or changes to the parameterization are also open for discussion.

# How it works (from https://github.com/adele157/easterlies-collaborative-project)

All aspects of the project are tracked through issues. Create an issue to represent each small task. Issues will develop to include discussion of analysis methods and figures associated with each task.

The [Project/analysis Overview](https://github.com/pedrocol/basal_mom5-collaborative-project/projects/1) lists all the analysis tasks (as detailed in the issues) at various stages.

To start contributing to the code, make your own branch directly in this repository, edit away on your branch, and then submit pull requests between your branch and the master branch (or merge directly).

As we figure out the main results and develop the storyline, we can add to the [Results Summary here] and [draft figure list for the paper here].

Overleaf project https://www.overleaf.com/project/62ba65027822b61f00348ec6

# Main experiment and parameterization design

The parameterization can be found [Here](https://github.com/pedrocol/basal_routines/tree/master/MOM_routines). It is based on Mathiot et al., 2017. It distributes the runoff south of 60S uniformly at depth, between the ice shelf front and the grounding line (data coming from Merino et al., 2016).

This parameterization is run in the same model version as the run done by Adele (/g/data/ik11/outputs/access-om2-01/01deg_jra55v13_ryf9091_rerun_for_easterlies/ control /home/157/akm157/access-om2/01deg_jra55v13_ryf9091_rerun_for_easterlies/) , using the restart after 250 years spinup.

So far three runs are available

accessom2_10-GPC001: Tfreezing calculated with salinity equal to insitu value (1 year avail)

accessom2_10-GPC002: Tfreezing calculated with salinity equal to zero (1 year avail)

accessom2_10-GPC003: Tbasal calculated tbasal = min(tfreezing,Tinsitu), with tfreezing as in GPC001. This is done in order to avoid warming the ocean. (3 years)
 
A bug was fixed in the intialization, previous runs are re runned as follows

accessom2_10-GPC004: Tbasal = Tfreezing(s=s_insitu) (2 years)

accessom2_10-GPC005: Tbasal = Tfreezing(s=0) (2 years)

accessom2_10-GPC006: Tbasal = min( Tfreezing(s=s_insitu),T_insitu) (2 years)

accessom2_10-GPC007: Idem as GPC008 but vert dist as in BG03 (2 years)

accessom2_10-GPC008: Tbasal = min( Tfreezing(s=s_0),T_insitu) (5 years)

New simulations:

accessom2_10-GPC013: Tbasal based on heat balance formulation

accessom2_10-GPC015: Tbasal based on Gade line

# Hackathon schedule (in Canberra/Sydney time zone)

Fortnightly on Thursday mornings:



# basal_mom5

A collaborative project to work on the ACCESS-OM2-01 + "basal melt distributed at depth parameterization" simulations. This is a central repository where we can propose different scenarios that could affect the overall impact of fresh water input at depth. Diagnostics, figures, scripts, and/or changes to the parameterization are also open for discussion.

## How it works (from https://github.com/adele157/easterlies-collaborative-project)

All aspects of the project are tracked through issues. Create an issue to represent each small task. Issues will develop to include discussion of analysis methods and figures associated with each task.

The [Project/analysis Overview](https://github.com/pedrocol/basal_mom5-collaborative-project/projects/1) lists all the analysis tasks (as detailed in the issues) at various stages.

To start contributing to the code, make your own branch directly in this repository, edit away on your branch, and then submit pull requests between your branch and the master branch (or merge directly).

As we figure out the main results and develop the storyline, we can add to the [Results Summary here](https://github.com/pedrocol/basal_mom5-collaborative-project/blob/main/Results_summary.md) and [draft figure list for the paper here](https://github.com/pedrocol/basal_mom5-collaborative-project/blob/main/Figure_outline.md).

Overleaf project https://www.overleaf.com/9899553184vvvjhhhcffnf

## Main experiment and parameterization design

The parameterization can be found [Here](https://github.com/pedrocol/basal_routines/tree/master/MOM_routines). It is based on Mathiot et al., 2017. It distributes the runoff south of 60S uniformly at depth, between the ice shelf front and the grounding line (data coming from Merino et al., 2016).

This parameterization is run as a perturbation of `01deg_jra55v13_ryf9091`, starting from WOA. The bathymetry is modified slightly (minimum depth is slightly deeper than normal) from the usual `01deg_jra55v13_ryf9091` simulations, as done by Wilton Aguiar.

## New simulations (use these ones!!):

GPC029 (Basal No Gade)                                01deg_jra55v13_ryf9091_DSW_BasalNoGade_NoIcb     : Tbasal equal Tinsitu, calving flux inserted at the surface as runoff

GPC023 (Basal with Gade)                              01deg_jra55v13_ryf9091_DSW_BasalGade_NoIcb       : Tbasal based on Gade line, calving flux inserted at the surface as runoff

GPC062 (Basal with Gade, brine param)                 01deg_jra55v13_ryf9091_DSW_BasalGade_NoIcb_Brine : Tbasal based on Gade line, calving flux inserted at the surface as runoff, brine param.


session_name = '/g/data/ik11/databases/basal_melt_MOM5.db'

Control simulation can be found here:
```
session_name = '/g/data/v45/wf4500/databases/gdata_01deg_jra55v13_ryf9091_DSW.db'
original control = '01deg_jra55v13_ryf9091_DSW'
```

## Hackathon schedule (in Canberra/Sydney time zone)

Fortnightly on Thursday mornings:



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

GPC029 (Basal)                                01deg_jra55v13_ryf9091_DSW_BasalNoGade_NoIcb     : Tbasal equal Tinsitu, calving flux inserted at the surface as runoff

GPC023 (Basal_LH)                           01deg_jra55v13_ryf9091_DSW_BasalGade_NoIcb       : Tbasal based on Gade line, calving flux inserted at the surface as runoff

GPC062 (Basal_LH_Brine)                     01deg_jra55v13_ryf9091_DSW_BasalGade_NoIcb_Brine : Tbasal based on Gade line, calving flux inserted at the surface as runoff, brine param.


session_name = '/g/data/ik11/databases/basal_melt_MOM5.db'

Control simulation can be found here:
```
session_name = '/g/data/v45/wf4500/databases/gdata_01deg_jra55v13_ryf9091_DSW.db'
original control = '01deg_jra55v13_ryf9091_DSW'
```

## Climatology: use the final 3 years (1907 - 1909 inclusive)

```python
start_time = '1907-01-01'
end_time = '1910-01-01'
time_slice = slice(start_time, end_time)
```

## Plotting formats/dict:

```python
# CONTROL
session_name = '/g/data/v45/wf4500/databases/gdata_01deg_jra55v13_ryf9091_DSW.db'
master_session = cc.database.create_session(session_name)
#experiment
control = '01deg_jra55v13_ryf9091_DSW'

#PERTURBATIONS
session_name = '/g/data/ik11/databases/basal_melt_MOM5.db'
basal_melt_session = cc.database.create_session(session_name)
#experiments
basal_gade_woa_newname = '01deg_jra55v13_ryf9091_DSW_BasalGade_NoIcb'
basal_nogade_woa = '01deg_jra55v13_ryf9091_DSW_BasalNoGade_NoIcb'
basal_gade_brine = '01deg_jra55v13_ryf9091_DSW_BasalGade_NoIcb_Brine'

#dict with plotting colors, linestyles, linewidth, and a shortname which may or may not be useful
exptdict = OrderedDict([
    ('Control',  {'expt':control,'session':master_session,
                  'colors':"#000000",'linestyles':'-','linewidth':3,'shortname':'control'}),
    ('Basal',  {'expt':basal_nogade_woa,'session':basal_melt_session,
                'colors':"#DDAA33",'linestyles':'--','linewidth':2,'shortname':'basal_nogade'}),
    ('Basal_LH',  {'expt':basal_gade_woa_newname,'session':basal_melt_session,
                    'colors':"#BB5566",'linestyles':'--','linewidth':2,'shortname':'basal'}),
    ('Basal_LH_Brine',  {'expt':basal_gade_brine,'session':basal_melt_session,
                         'colors':"steelblue",'linestyles':'-','linewidth':2,'shortname':'basal_gade_brine'}),
])
keys = ['Control','Basal','Basal_LH','Basal_LH_Brine']

#observational data should be color = 'grey', linestyle = '-', linewidth =3

# to plot:
for i in np.arange(4):
    ekey = keys[i]
    color = exptdict[ekey]['colors']
    # etc...

# or (neater)
for ekey, e in exptdict.items():
    color = e['colors']
    # etc...
```
another approach:
```python
styles = { # defines line plot order, legend labels (keys) and keyword args (dicts)
    'Obs':            {'color':'grey',      'linestyle':'-',  'linewidth':3},
    'Control':        {'color':"#000000",   'linestyle':'-',  'linewidth':3},
    'Basal':          {'color':"#DDAA33",   'linestyle':'--', 'linewidth':2},
    'Basal_LH':       {'color':"#BB5566",   'linestyle':'--', 'linewidth':2},
    'Basal_LH_Brine': {'color':"steelblue", 'linestyle':'-',  'linewidth':2},
}

# plot like so, if `data` is a dict of dataarrays with keys that are (possibly a subset of) the keys in `styles`
for k, d in data.items():
    plt.plot(d, label=k, **styles[k])
```

# ================================================================================================================================================================================================

## Hackathon schedule (in Canberra/Sydney time zone)

Fortnightly on Thursday mornings: 9:00-10:00am
- Next meeting on 2nd or 16th February, 2026 (pending confirmation): https://utas.zoom.us/j/86813420539

## Part 2 experiments: Meltwater anomaly experiments follwing SOFIA protocol (SSP1-2.6 and Antwater)

The part 1 runs (control, basal, basal_LH_brine) were extended until year 20, and the +MW runs were restarted in 1st January year 10 (and ran for 10 years). These output are sitting in the following directories:

```
control                           = /g/data/ik11/outputs/access-om2-01/01deg_jra55v13_ryf9091_21mbath
control_LH                        = /scratch/e14/fbd581/access-om2/fbd581/access-om2/archive/01deg_jra55_ryf9091_21mbath_Gade-914fd6e4

control_SOFIA (ssp126)            = /g/data/ik11/outputs/access-om2-01/01deg_jra55v13_ryf9091_21mbath_sofia_ssp126
control_SOFIA_antwater            = /g/data/ik11/outputs/access-om2-01/01deg_jra55v13_ryf9091_21mbath_sofia_antwater
control_SOFIA_antwater_LH         = /scratch/e14/fbd581/access-om2/fbd581/access-om2/archive/01deg_jra55_ryf9091_21mbath_sofia_antwater_Gade-160c9273
control_LH_SOFIA_antwater         = /scratch/e14/fbd581/access-om2/fbd581/access-om2/archive/01deg_jra55_ryf9091_21mbath_Gade_sofia_antwater-383eae28

basal (noGade)                    = /g/data/ik11/outputs/access-om2-01/01deg_jra55v13_ryf9091_DSW_BasalNoGade_NoIcb
basal_SOFIA (ssp126)              = /g/data/ik11/outputs/access-om2-01/01deg_jra55v13_ryf9091_DSW_BasalNoGade_NoIcb_sofia_ssp126

basal_LH_brine           = /g/data/ik11/outputs/access-om2-01/01deg_jra55v13_ryf9091_DSW_BasalGade_NoIcb_Brine_rep
basal_LH_brine_SOFIA (ssp126)     = /g/data/ik11/outputs/access-om2-01/01deg_jra55v13_ryf9091_DSW_BasalGade_NoIcb_Brine_sofia_ssp126
basal_LH_brine_SOFIA_antwater     = /g/data/ik11/outputs/access-om2-01/01deg_jra55v13_ryf9091_DSW_BasalGade_NoIcb_Brine_sofia_antwater
```

I have created a intake datastore for each experiments (both part I and II) here:
`/g/data/e14/fbd581/Basal_Pedro_project/intake_datastore`

And respective names are:

| Experiment                    | Time Period | Description                                      |
|-------------------------------|-------------|--------------------------------------------------|
| DSW_control                   | 0–20 yrs    | Original control, surface MW                     |
| DSW_control_LH                | 0–20 yrs    | Surface MW + LH removal                          |
| Basal_LH_Brine                | 0–20 yrs    | Basal MW + LH removal                            |
| DSW_control_antwater          | 10–20 yrs   | Surface MW + Antwater MW anomaly                 |
| DSW_control_LH_antwater       | 10–20 yrs   | Surface MW + LH removal + Antwater MW anomaly    |
| Basal_LH_Brine_antwater       | 10–20 yrs   | Basal MW + LH removal + Antwater MW anomaly      |
| DSW_control_antwater_LH       | 10–20 yrs   | Surface MW + Antwater MW anomaly w/ LH removal   |
| DSW_control_sofia             | 10–20 yrs   | Surface MW + SSP1.2‑6 MW anomaly                 |
| Basal_LH_Brine_sofia          | 10–20 yrs   | Basal MW + LH removal + SSP1.2‑6 MW anomaly      |

|                                                                                   |                                     Surface MW, no latent heat                                     |                                                                                                                   |                                                                                                                                 |   |
|-----------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------:|---|
|                                                                                   | SFCCON                                                                                             | SFCSSP126                                                                                                         | SFCAntw                                                                                                                         |   |
| Length simulation                                                                 | 20 years                                                                                           | 10 years                                                                                                          | 10 years                                                                                                                        |   |
| MW at SFC                                                                         | Yes                                                                                                | Yes                                                                                                               | Yes                                                                                                                             |   |
| MW at BASAL                                                                       | No                                                                                                 | No                                                                                                                | No                                                                                                                              |   |
| MW perturbation                                                                   | No                                                                                                 | 0.015 Sv                                                                                                          | 0.1 Sv                                                                                                                          |   |
| LH only anomaly?                                                                  | No                                                                                                 | No                                                                                                                | No                                                                                                                              |   |
| LH all runoff?                                                                    | No                                                                                                 | No                                                                                                                | No                                                                                                                              |   |
| Path scratch/gdata                                                                | /g/data/ik11/outputs/access-om2-01/01deg_jra55v13_ryf9091_21mbath                                  | /g/data/ik11/outputs/access-om2-01/01deg_jra55v13_ryf9091_21mbath_sofia_ssp126                                    | /scratch/e14/fbd581/access-om2/fbd581/access-om2/archive/01deg_jra55_ryf9091_21mbath_sofia_antwater-d0ea3a2d                    |   |
| Datastore name; Location: /g/data/e14/fbd581/Basal_Pedro_project/intake_datastore | DSW_control                                                                                        | DSW_control_sofia                                                                                                 | DSW_control_antwater                                                                                                            |   |
|                                                                                   |                                     Surface MW with latent heat                                    |                                                                                                                   |                                                                                                                                 |   |
|                                                                                   | SFC_LHCON                                                                                          | SFC_LHAntw                                                                                                        | SFCAntw_LH                                                                                                                      |   |
| Length simulation                                                                 | 20 years                                                                                           | 10 years                                                                                                          | 10 years                                                                                                                        |   |
| MW at SFC                                                                         | Yes                                                                                                | Yes                                                                                                               | Yes                                                                                                                             |   |
| MW at BASAL                                                                       | No                                                                                                 | No                                                                                                                | No                                                                                                                              |   |
| MW perturbation                                                                   | No                                                                                                 | 0.1 Sv                                                                                                            | 0.1 Sv                                                                                                                          |   |
| LH only anomaly?                                                                  | No                                                                                                 | No                                                                                                                | Yes                                                                                                                             |   |
| LH all runoff?                                                                    | Yes                                                                                                | Yes                                                                                                               | No                                                                                                                              |   |
| Path scratch/gdata                                                                | /scratch/e14/fbd581/access-om2/fbd581/access-om2/archive/01deg_jra55_ryf9091_21mbath_Gade-914fd6e4 | /scratch/e14/fbd581/access-om2/fbd581/access-om2/archive/01deg_jra55_ryf9091_21mbath_Gade_sofia_antwater-383eae28 | /scratch/e14/fbd581/access-om2/fbd581/access-om2/archive/01deg_jra55_ryf9091_21mbath_sofia_antwater_Gade-160c9273               |   |
| Datastore name                                                                    | DSW_control_LH                                                                                     | DSW_control_LH_antwater                                                                                           | DSW_control_antwater_LH                                                                                                         |   |
|                                                                                   |                                   Basal/Deep MW with latent heat                                   |                                                                                                                   |                                                                                                                                 |   |
|                                                                                   | BASAL_LHCON                                                                                        | BASAL_LHSSP126                                                                                                    | BASAL_LHAntw                                                                                                                    |   |
| Length simulation                                                                 | 20 years                                                                                           | 10 years                                                                                                          | 10 years                                                                                                                        |   |
| MW at SFC                                                                         | No                                                                                                 | No                                                                                                                | No                                                                                                                              |   |
| MW at BASAL                                                                       | Yes                                                                                                | Yes                                                                                                               | Yes                                                                                                                             |   |
| MW perturbation                                                                   | No                                                                                                 | 0.015 Sv                                                                                                          | 0.1 Sv                                                                                                                          |   |
| LH only anomaly?                                                                  | No                                                                                                 | No                                                                                                                | No                                                                                                                              |   |
| LH all runoff?                                                                    | Yes                                                                                                | Yes                                                                                                               | Yes                                                                                                                             |   |
| Path scratch/gdata                                                                | /g/data/ik11/outputs/access-om2-01/01deg_jra55v13_ryf9091_DSW_BasalGade_NoIcb_Brine                | /g/data/ik11/outputs/access-om2-01/01deg_jra55v13_ryf9091_DSW_BasalGade_NoIcb_Brine_sofia_ssp126                  | /scratch/e14/fbd581/access-om2/fbd581/access-om2/archive/01deg_jra55_ryf9091_21mbath_basal_sofia_antwater_SSSrestoring-c1fb6bf0 |   |
| Datastore name                                                                    | Basal_LH_Brine                                                                                     | Basal_LH_Brine_sofia                                                                                              | Basal_LH_Brine_antwater                                                                                                         |   |
|                                                                                   |                                                                                                    |                                                                                                                   |                                                                                                                                 |   |
|                                                                                   |                                                                                                    |                                                                                                                   |                                                                                                                                 |   |
|                                                                                   |                                                                                                    |                                                                                                                   |                                                                                                                                 |   |

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

GPC023 (Basal-Gade)                           01deg_jra55v13_ryf9091_DSW_BasalGade_NoIcb       : Tbasal based on Gade line, calving flux inserted at the surface as runoff

GPC062 (Basal-Gade-Brine)                     01deg_jra55v13_ryf9091_DSW_BasalGade_NoIcb_Brine : Tbasal based on Gade line, calving flux inserted at the surface as runoff, brine param.


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
    ('BasalGade',  {'expt':basal_gade_woa_newname,'session':basal_melt_session,
                    'colors':"#BB5566",'linestyles':'--','linewidth':2,'shortname':'basal'}),
    ('BasalGadeBrine',  {'expt':basal_gade_brine,'session':basal_melt_session,
                         'colors':"steelblue",'linestyles':'-','linewidth':2,'shortname':'basal_gade_brine'}),
])
keys = ['Control','Basal','BasalGade','BasalGadeBrine']

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
    'BasalGade':      {'color':"#BB5566",   'linestyle':'--', 'linewidth':2},
    'BasalGadeBrine': {'color':"steelblue", 'linestyle':'-',  'linewidth':2},
}

# plot like so, if `data` is a dict of dataarrays with keys that are (possibly a subset of) the keys in `styles`
for k, d in data.items():
    plt.plot(d, label=k, **styles[k])
```
## Hackathon schedule (in Canberra/Sydney time zone)

Fortnightly on Thursday mornings:



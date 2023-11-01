# The story so far

## Forcing perturbations

Possibly we can come up with better experiment names. Any thoughts?

**BASAL**

Put basal melt component of meltwater at depth instead of at surface. Pedro: Add details of exactly what depths the meltwater goes in at.

Temperature of meltwater is supercold, according to Gade line, which accounts for the latent heat of melting ice. _Pedro: Add details of exactly how this temperature is determined._

Calving component of meltwater is still input at the coast at the surface at normal temperature (min of SST / 0C?).

**BASAL-ICEBERG**

Same as BASAL, but calving (iceberg) component of meltwater is distributed horizontally with the same distribution as Merino et al, and vertically spread evenly over the top X m. _Pedro: add more details of the horizontal distribution - I remember we did some further processing of the Merino data? Also add depth for ice berg melt._

**BASAL-NOGADE** 

Same as BASAL, i.e. the basal melt component of the runoff is distributed vertically, and calving component is still at the surface. Except in this case, the temperature of the basal meltwater is ... _Pedro: Add details on how you set the temperature of the meltwater in this case._

## Simulation responses

* Comparison with observations (No plots or comparison yet on BASAL-NOGADE):
  
  Improvement of biases:
  - [Bottom fresh bias compared to Schmidtko improves in Weddell, Ross, Prydz, Adelie](https://github.com/pedrocol/basal_mom5-collaborative-project/issues/63#issuecomment-1672354811). Some of the improvement comes from BASAL, with further improvement from BASAL-ICEBERG. No improvement in West Antarctica.
  - [Surface fresh bias very close to Antarctic coast improves](https://github.com/pedrocol/basal_mom5-collaborative-project/issues/63#issuecomment-1672376142). Surface biases elsewhere over the shelf / open ocean remain the same.
 
  Deterioration of biases:
  - [No obvious improvement in shelf bottom temperature](https://github.com/pedrocol/basal_mom5-collaborative-project/issues/63#issuecomment-1672352663) compared to Schmidtko obs in BASAL or BASAL-ICEBERG. Amundsen/Bellingshausen gets worse (cold bias becomes MUCH colder).
  - [At mid-depth (300-350m), also no obvious improvement](https://github.com/pedrocol/basal_mom5-collaborative-project/issues/63#issuecomment-1672383875) in BASAL and BASAL-ICEBERG. The biases that degrade are: too cold in West Antarctica, too salty in Amundsen / Ross / Weddell, particularly in BASAL-ICEBERG.

* DSW export increases ~30% in BASAL and ~80% in BASAL-ICEBERG. Large increases in Adelie and Prydz in both simulations. Ross doesn't change much / decreases (check new region plots)? Weddell doesn't change much in BASAL and increases a lot in BASAL-ICEBERG. We also get dense water formation in the Amundsen in BASAL-ICEBERG! _Why do the different regions respond differently to the different perturbations?_

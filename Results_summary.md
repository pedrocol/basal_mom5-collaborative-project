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

Same as BASAL, i.e. the basal melt component of the runoff is distributed vertically, and calving component is still at the surface. Except in this case, the temperature of the basal meltwater is the insitu temperature 

* The impact of the Gade line formulation (i.e. putting basal and iceberg waters in at very cold temperatures) is seen in the change in heat flux over the shelf. In the control we have ~40TW of heat loss from the ocean over the shelf. The [cooling increases](https://github.com/pedrocol/basal_mom5-collaborative-project/issues/66#issuecomment-1681499552) by ~25% in BASAL and by ~40% in BASAL-ICEBERG.

## Simulation responses

* **Comparison with observations** (No plots or comparison yet on BASAL-NOGADE):
  
  Improvement of biases:
  - [Bottom fresh bias compared to Schmidtko improves in Weddell, Ross, Prydz, Adelie](https://github.com/pedrocol/basal_mom5-collaborative-project/issues/63#issuecomment-1672354811). Some of the improvement comes from BASAL, with further improvement from BASAL-ICEBERG. No improvement in West Antarctica.
  - [Surface fresh bias very close to Antarctic coast improves](https://github.com/pedrocol/basal_mom5-collaborative-project/issues/63#issuecomment-1672376142). Surface biases elsewhere over the shelf / open ocean remain the same.
  - We do get [Ice Shelf Water](https://github.com/pedrocol/basal_mom5-collaborative-project/issues/62#issuecomment-1690682954) below the surface freezing point in BASAL.
 
  Deterioration of biases:
  - [No obvious improvement in shelf bottom temperature](https://github.com/pedrocol/basal_mom5-collaborative-project/issues/63#issuecomment-1672352663) compared to Schmidtko obs in BASAL or BASAL-ICEBERG. Amundsen/Bellingshausen gets worse (cold bias becomes MUCH colder).
  - [At mid-depth (300-350m), also no obvious improvement](https://github.com/pedrocol/basal_mom5-collaborative-project/issues/63#issuecomment-1672383875) in BASAL and BASAL-ICEBERG. The biases that degrade are: too cold in West Antarctica, too salty in Amundsen / Ross / Weddell, particularly in BASAL-ICEBERG.
  - We also seem to be getting [unrealistically cold temperatures](https://github.com/pedrocol/basal_mom5-collaborative-project/issues/62#issuecomment-1690682954) (below the in situ freezing point), particularly in the West Antarctic sector. How/why is this occurring?

* **DSW export** [increases](https://github.com/pedrocol/basal_mom5-collaborative-project/issues/65#issuecomment-1789862897) ~30% in BASAL and ~80% in BASAL-ICEBERG, with very little change from the control in the BASAL-NOGADE simulation. Large increases in Adelie, mostly due to the BASAL component. Ross increases in both experiments, but more in BASAL-ICEBERG. Weddell doesn't change at all really in BASAL but increases a lot in BASAL-ICEBERG. Prydz seems to decrease or stay mostly the same. We also get dense water formation in the Amundsen in BASAL-ICEBERG! These dense water changes are also seen in [bottom age](https://github.com/pedrocol/basal_mom5-collaborative-project/issues/29#issuecomment-1672377844), with more ventilation to the abyss in all sectors in BASAL-ICEBERG, and decreased age on the shelf in the Amundsen indicating the increased convection there. _Why do the different regions respond differently to the different perturbations?_
 
  This increase in DSW occurs because less fresh water input at the surface means that denser surface waters can form in the DSW formation regions.

* The [**ASC** changes differently in different regions and depths](https://github.com/pedrocol/basal_mom5-collaborative-project/issues/58#issuecomment-1691024637) in BASAL and BASAL-ICEBERG. 

* What are the **Sea ice** changes?

* What are the **T/S changes** compared to the CONTROL? These are detailed a little above in the obs bias discussion, but would be good to describe smaller differences from CONTROL here.

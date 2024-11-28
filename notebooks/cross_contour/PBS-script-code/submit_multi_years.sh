#!/bin/bash

## loop over months and years, which submits submit_binning_script.sh to gadi for each month

# can give year_count as a single year 'in 2150' or as a list of years: 'in {2009,2011,2012}' or a range: 'in {2009..2018}':
for year_count in {1901..1909}
do
	for month_count in {1..12}
	do
   		echo "submitting year $year_count, month $month_count"
   		qsub -v month=${month_count},year=${year_count} submit_transport_job.sh
	done
done

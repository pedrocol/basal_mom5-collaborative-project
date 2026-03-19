#!/bin/bash
#PBS -N multi_Yr_transports
#PBS -P e14
#PBS -q normalbw
#PBS -l walltime=1:00:00
#PBS -l mem=120GB
#PBS -l ncpus=1
#PBS -l storage=gdata/v45+gdata/hh5+gdata/cj50+gdata/ik11+scratch/x77+gdata/x77+gdata/e14+gdata/g40+gdata/xp65

export dir_path=/g/data/e14/fbd581/Basal_Pedro_project/updated_git_basal_mom5-collaborative/basal_mom5-collaborative-project/notebooks/cross_contour/PBS-script-code

cd $dir_path
## loop over months and years, which submits submit_binning_script.sh to gadi for each month

# can give year_count as a single year 'in 2150' or as a list of years: 'in {2009,2011,2012}' or a range: 'in {2009..2018}':
#for year_count in {1901..1910}
for year_count in {1915..1915}
do
	for month_count in {4..6}
	do
   		echo "submitting year $year_count, month $month_count"
   		qsub -v month=${month_count},year=${year_count} $dir_path/submit_transport_job.sh
	done
done


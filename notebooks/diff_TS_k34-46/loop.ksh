##################################################################################################
#Init values
##################################################################################################
conf="acces-om2-01-GPC002"
year=2150
var='temp'
freq=2 #1 daily, 2 monthly
if [ "$conf" = "acces-om2-01-GAM001" ]; then
   if [ $year = 2150 ]; then
      outini=996
      outfin=999
   elif [ $year = 2151 ]; then
      outini=1000
      outfin=1003
   fi
   root_data=/g/data/ik11/outputs/access-om2-01/01deg_jra55v13_ryf9091_rerun_for_easterlies/
elif [ "$conf" = "acces-om2-01-GPC001" ]; then
   outini=996
   outfin=1001
   root_data=/home/552/pc5520/access-om2/control/01deg_jra55v13_ryf9091_rerun_for_easterlies/archive/accessom2-GPC001
elif [ "$conf" = "acces-om2-01-GPC002" ]; then
   outini=996
   outfin=1006
   root_data=/home/552/pc5520/access-om2/control/01deg_jra55v13_ryf9091_rerun_for_easterlies/archive/accessom2-GPC002
elif [ "$conf" = "acces-om2-01-GPC003" ]; then
   if [ $year = 2150 ]; then
      outini=996
      outfin=1002
   elif [ $year = 2151 ]; then
      outini=1003
      outfin=1008
   fi
   root_data=/home/552/pc5520/access-om2/control/01deg_jra55v13_ryf9091_rerun_for_easterlies/archive/accessom2-GPC003
fi

if [ $freq = 1 ]; then
   filename=rregionocean_daily_3d_"$var".nc
elif [ $freq = 2 ]; then
   filename=ocean.nc
fi

##################################################################################################
#3d values of temp and salt - Daily
##################################################################################################
root_save=/scratch/e14/pc5520/OUTPUT/$conf/extract/y$year/vert_levels/$var
mkdir -p $root_save/2334/
mkdir -p $root_save/3446/
#t0=$(expr 30 + 59 + 91 + 92 + 1)
t0=0
for digit in $(seq $outini $outfin); do
    number=`ncdump -h $root_data/output$digit/ocean/"$filename" | grep UNLIMITED | sed 's/[^0-9]*//g'`
    init_t=0
    end_t=$(expr $number - 1)
    for tim in $(seq $init_t $end_t ); do
        tf=$(expr $t0 + $tim)
        tf=$(seq -f "%03g" $tf $tf)
        echo $tf
        ncks -O -v "$var" -d st_ocean,23,34 -d time,$tim,$tim $root_data/output"$digit"/ocean/$filename $root_save/2334/"$filename"_$tf.nc
        ncks -O -v "$var" -d st_ocean,34,46 -d time,$tim,$tim $root_data/output"$digit"/ocean/$filename $root_save/3446/"$filename"_$tf.nc
    done
    t0=$(expr $t0 + $end_t + 1)
done

#### Averages ####
#2334
for levels in 3446; do
    root_data=/scratch/e14/pc5520/OUTPUT/$conf/extract/y$year/vert_levels/$var/$levels/
    root_save=/scratch/e14/pc5520/OUTPUT/$conf/extract/y$year/vert_levels/$var/$levels/
    cd $root_save
    for f in "$filename"* ; do
        echo "$f"
	ncwa -O -a st_ocean $f avek_"$f"
    done
ncrcat -O avek_"$filename"* cat_avek_k"$levels"_"$var".nc
#rm avek*nc
ncra -O cat_avek_k"$levels"_"$var".nc avet_cat_avek_k"$levels"_"$var".nc
done

#### Simple differences in levels for temp and salt ####
conf1="acces-om2-01-GPC002"
conf2="acces-om2-01-GAM001"
#2334
for levels in 3446; do
    #Perform differences
    root_data1=/scratch/e14/pc5520/OUTPUT/$conf1/extract/y$year/vert_levels/$var/$levels/
    root_data2=/scratch/e14/pc5520/OUTPUT/$conf2/extract/y$year/vert_levels/$var/$levels/
    root_save=/scratch/e14/pc5520/OUTPUT/$conf1/extract/y$year/diffs/$var/$levels/
    mkdir -p $root_save
    f=avet_cat_avek_k"$levels"_"$var".nc
    ncdiff -O $root_data1/$f $root_data2/$f $root_save/ncdiff_$f
done

#### Differences in levels for temp and salt ####
conf1="acces-om2-01-GPC003"
conf2="acces-om2-01-GAM001"
for levels in 2334 3446; do
    #Perform differences
    root_data1=/scratch/e14/pc5520/OUTPUT/$conf1/extract/y$year/vert_levels/$var/$levels/
    root_data2=/scratch/e14/pc5520/OUTPUT/$conf2/extract/y$year/vert_levels/$var/$levels/
    root_save=/scratch/e14/pc5520/OUTPUT/$conf1/extract/y$year/diffs/$var/$levels/
    mkdir -p $root_save
    cd $root_data1
    for f in "$filename"*; do
        echo $f
        ncdiff -O $root_data1/$f $root_data2/$f $root_save/ncdiff_$f
    done
    #Perform vertical average
    root_data=/scratch/e14/pc5520/OUTPUT/$conf1/extract/y$year/diffs/$var/$levels/
    root_save=/scratch/e14/pc5520/OUTPUT/$conf1/extract/y$year/diffs_vertave/$var/$levels/
    mkdir -p $root_save
    cd $root_data
    for f in *; do
        echo $f
        ncwa -O -a st_ocean $f $root_save/vertave_$f
    done
    cd $root_save
    ncrcat -O vertave_* avek_cat_ncdiff_k"$levels"_"$var"_y"$year".nc
    ncea -O  vertave_* avet_avek_ncdiff_k"$levels"_"$var"_y"$year".nc
    rm vertave_ncdiff_*
done
##################################################################################################

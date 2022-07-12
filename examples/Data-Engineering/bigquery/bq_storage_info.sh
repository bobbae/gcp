#!/bin/bash

project=$1
max_results=1000


# Get the datasets

datasets=$(bq ls --datasets=true --project_id=$project | awk '{print $1}' | tail -n +3)

echo $datasets

for dataset in $datasets
do
   # get list of tables
   # The tail -n +3 strips off the header lines
   tables=$(bq ls --max_results $max_results "$project:$dataset" | awk '{print $1}' | tail -n +3)

   echo $tables
   # get LTS bytes for each table
   for table in $tables
   do
       printf '%-35s %-50s\n' "$table" "$(bq show --format prettyjson $project:$dataset.$table | grep numLongTermBytes)"
   done
done

#!/bin/bash
#########################################
##  Submit-Script Generator LC Kassel  ##
#########################################

####### Mail Notify / Job Name / Comment #######
#SBATCH --job-name="pfft"

####### Partition #######
#SBATCH --partition=public4

####### Ressources #######
#SBATCH --time=0-10:00:00

####### Output #######
#SBATCH --output=%j.out
#SBATCH --error=%j.err

python3 polynomial_multiplication.py $@ 
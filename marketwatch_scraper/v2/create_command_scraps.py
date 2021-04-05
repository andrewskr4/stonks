import glob

f = glob.glob("/home/asikora/projects/rrg-vkaspi-ad/CHIME/R5/*.fil")
mjdfile = open("failed_mjds_4.txt","r")
mjdlines = mjdfile.readlines()
num_jobs = int(len(mjdlines)/23) + 1
#print(num_jobs)
for i in range(num_jobs):
    g = open("command_scraps_"+str(i)+".sh", "w")
    g.write("#!/bin/bash\n")
    g.write("#SBATCH --time=96:00:00\n")
    g.write("#SBATCH --account=rrg-vkaspi-ad\n")
    g.write("#SBATCH --mem=8G\n")
    g.write("module load python/3.6\n")
    g.write("virtualenv --no-download $SLURM_TMPDIR/env\n")
    g.write("source $SLURM_TMPDIR/env/bin/activate\n")
    g.write("pip install --no-index --upgrade pip\n")
    g.write("pip install numpy\n")
    g.write("pip install torch\n")
    g.write("pip install torchvision\n")
    g.write("pip install matplotlib\n")
    g.write("pip install glob\n")
    g.write("pip install -r requirements.txt\n")
    g.write("mkdir all\n")
    g.write("cd all\n")
    for j in range(23):
        k=23*i +j
        mjd = mjdlines[k].split("\n")[0]
        for l in range(len(f)):
            filname = f[l].split("/")[-1]
            if(len(filname.split("_"))>3):
                fil_mjd = filname.split("_")[3]
                if (fil_mjd == mjd):
                    break
            


        g.write("mkdir "+str(mjd)+"\n")
        g.write("cd "+str(mjd)+"\n")
        g.write("rm *.png\n")
        g.write("rm *.plt\n")
        g.write("sleep 5\n")
        g.write("/home/asikora/ML_FRB_search/generate_plots_for_ML/analyze_pulsar_data/gen_samples /home/asikora/projects/rrg-vkaspi-ad/CHIME/R5/"+str(filname)+" -d 450.0 -i ~/flags_list.dat\n")
        g.write("sleep 5\n")
        g.write("python /home/asikora/ML_FRB_search/MachineLearning/frb_search/run_model.py . R5 "+str(mjd)+"\n")
        g.write("rm *.plt\n")
        g.write("cd ..\n")
    g.close()

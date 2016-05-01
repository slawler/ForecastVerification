

asc2dss=/home/slawler/asc2dssGrid.exe
xmrgtoasc=/home/slawler/xmrgtoasc

for dir in ~/Desktop/ToLinux_copy/MPE/*//*; 

do
    cd "$dir"
    echo "$dir"
    install -m 755 "$xmrgtoasc" "$dir";
    install -m 755 "$asc2dss" "$dir";

    for j in *.xmrg; 
    
    do 
        ./xmrgtoasc "$j" "${j%.*}" hrap; 
        chmod 775 *.asc
    done

    echo '============RUNNING PYTHON SCRIPT============'

    ipython /home/slawler/Documents/scripts/pyscripts/XMRG2DSS_v_MARFC_MPE.py 

    echo '***********PYTHON PROCESS COMPLETE***********'
 
    chmod 775 batchload.sh
    ./batchload.sh

    tar -cvzf ascii.tar.gz *.asc
    rm *.asc

done


echo 'PROCESSES COMPLETE'
echo 'GOODBYE'


for dir in ~/Desktop/ToLinux_copy/QPF/*; 

do
    cd "$dir"
    echo "$dir"

    echo '============RUNNING PYTHON SCRIPT============'
 
    ipython /home/slawler/Desktop/SREM2D/CreateInput.py

    echo '***********PYTHON PROCESS COMPLETE***********'

done

echo 'PROCESSES COMPLETE'
echo 'GOODBYE'

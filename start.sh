# mamba activate pyqt6
source ~/miniforge3/bin/activate pyqt6
# start executable
while true; do
    cd ~/pyqt6-camera
    python main.py
    echo "return " $?
    echo "restarting..."
    sleep 1
done


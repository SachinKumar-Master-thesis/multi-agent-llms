#!/bin/sh

# screen -dmS Jupyter bash -c 'jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''; exec bash'
# screen -dmS Chainlit bash -c 'chainlit run  /workspace/applications/app.py --host=0.0.0.0 --port=8000 --watch; exec bash'

tmux new -d -s Jupyter bash -c 'jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''; exec bash'
tmux new -d -s Chainlit bash -c 'chainlit run  /workspace/applications/app.py --host=0.0.0.0 --port=8000 --watch --no-cache; exec bash'
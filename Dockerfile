FROM python:3.11

RUN apt-get update
RUN apt-get install -y libgdal-dev
# dependencies for debugging
RUN apt-get install -y vim tree
RUN apt-get install -y screen tmux



RUN pip install --no-cache-dir ipython ipykernel nbdev jupyter
RUN ipython kernel install --name "python3" --user

COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

RUN mkdir workspace
WORKDIR /workspace

COPY start.sh  /workspace/
COPY start_screens.sh  /workspace/
COPY screen_connect.sh  /workspace/
RUN chmod 775 /workspace/*.sh
COPY screens /workspace/screens

# Bundle app source
COPY llm_urbanpulse /workspace/llm_urbanpulse
COPY applications /workspace/applications
COPY configs /workspace/configs
COPY public /workspace/public

#RUN nbdev_clean 
#RUN nbdev_export  
#RUN pip install --no-cache-dir . 

#By Sachin:
CMD ["cd", "/workspace"]
ENTRYPOINT ["/bin/bash","-c" ,"/workspace/start.sh;exec bash"]
# helm uses this command:
# CMD/ENTRYPOINT ["/bin/bash","-c" ,"/workspace/start_screens.sh"]

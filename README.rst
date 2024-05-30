=========
CHATBOOK:
=========
It's is a chatbot app that provides answers to user queries related to a textbook by leveraging RAG techniques.


PROJECT SETUP:
--------------
1. Activate venv: source learn-env/bin/activate
2. Checkout the project then run command: pip3 install -r requirements.txt
3. Run app: streamlit run src/app.py


DOCKER BUILD:
-------------
1. Start DockerDesktop
2. Set temporary path: export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"
3. Docker build: sudo docker build -t chatbook .
4. Check docker image: docker image ls 
5. Run docker image: docker run -p 8501:8501 chatbook


TOOLS AND TECHNOLOGY:
---------------------
1. Python: 3.9.6
2. pip3: 21.2.4
3. Visual Studio Code: 1.89.1


IMPORTANT LINKS:
-----------------
1. UI: https://docs.streamlit.io
2. LLM: https://deepinfra.com
3. Vector DB: https://app.pinecone.io
4. Code play: https://nb.anaconda.cloud
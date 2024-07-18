## Configuraion
To run the project you will need to:
- Download the repo
- Optional: Build a virtual environemnt.
- Install te dependencies: 
	- ```  pip install -r requirements.txt ```
- Create the following file: ```.env```
	- Save your API keys on the file.
	- ```OPENAI_API_KEY=XXXXXX```
	- ```ELEVENLABS_API_KEY=XXXXXX```
	- ```WEATHER_API_KEY=XXXXXX```
	- ```WIKIPEDA API IS FREE so we don't need a KEY```

## Settings
There are a few things we can modify on the project:

- On the LLM class we can modify the behavior of the assistant.
- On the PcCommand class the route is fo windows but it can be modify so it can work with mac o linux as well.

## Execution
- This project uses Flas. You can tun the server in debug mode on the port 5000 by uisng the command:
	- ```flask --app app run --debug```
	- Go to your browser http://localhost:5000
	- Click on the microphne and it will start recording.


## Licences
- Microphone image by Freepik
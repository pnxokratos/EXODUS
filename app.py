import os
import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
from google_calendar import SCOPES, authenticate_google_calendar, get_upcoming_events
import json
from transcriber import Transcriber
from llm import LLM
from weather import Weather
from tts import TTS
from pc_command import PcCommand
from wikipedia import Wikipedia
from google_auth_oauthlib.flow import InstalledAppFlow
import threading
import webbrowser
from time_1 import Time


# It loads the API Keys .env
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    return render_template("recorder.html")

@app.route("/audio", methods=["POST"])
def audio():
    # Obtain the audio and then it transcribes it
    audio = request.files.get("audio")
    text = Transcriber().transcribe(audio)
    
    # LLM to verify if we need to call a function
    llm = LLM()
    function_name, args, message = llm.process_functions(text)
    if function_name is not None:
        # If we need to call one of the declared functions
        if function_name == "get_weather":
            function_response = Weather().get(args["ubicacion"])
            function_response = json.dumps(function_response)
            final_response = llm.process_response(text, message, function_name, function_response)
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}

        elif function_name == "send_email":
             final_response = "Abriendo Gmail en tu navegador."
             tts_file = TTS().process(final_response)
             webbrowser.open("https://mail.google.com")
             return {"result": "ok", "text": final_response, "file": tts_file}

        
        elif function_name == "open_chrome":
             final_response = "Listo, ya abrí chrome en el sitio solicitado "
             tts_file = TTS().process(final_response)
             response = {"result": "ok", "text": final_response, "file": tts_file}
    
             # Executes the command to open Chrome on a separated thread
             threading.Thread(target=PcCommand().open_chrome, args=(args["website"],)).start()
    
             return response

        #This function is just for fun
        elif function_name == "dominate_human_race":
            final_response = "ES UNA BROMA"
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
        elif function_name == "search_wikipedia":
            wiki_response = Wikipedia().search(args["query"])
            wiki_response = json.dumps(wiki_response)
            final_response = llm.process_response(text, message, function_name, wiki_response)
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
        elif function_name == "get_calendar_events":
            service = authenticate_google_calendar()
            events = get_upcoming_events(service, args.get("max_results", 10))
            events_response = json.dumps(events)
            final_response = llm.process_response(text, message, function_name, events_response)
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
        elif function_name == "get_time":
            current_time = Time().get_current_time()
            final_response = f"La hora actual es {current_time}."
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
    
    else:
        final_response = "No tengo idea de lo que estás hablando, prueba de nuevo"
        tts_file = TTS().process(final_response)
        return {"result": "ok", "text": final_response, "file": tts_file}
# This is the authentication in order to access google calendar
@app.route('/authorize')
def authorize():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',
        SCOPES,
        redirect_uri='http://localhost:5000/oauth2callback')
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',
        scopes=SCOPES,
        state=state,
        redirect_uri='http://localhost:5000/oauth2callback')
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

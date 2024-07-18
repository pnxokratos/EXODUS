import openai
import json

class LLM():
    def __init__(self):
        pass
    
    def process_functions(self, text):
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "Eres un asistente muy educado y alegre. Tienes que respondes en el idioma que te hablen"},
                {"role": "user", "content": text},
            ],
            functions=[
                {
                    "name": "get_weather",
                    "description": "Obtener el clima actual",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ubicacion": {
                                "type": "string",
                                "description": "La ubicación, debe ser una ciudad",
                            }
                        },
                        "required": ["ubicacion"],
                    },
                },
                {
                    "name": "send_email",
                    "description": "Enviar un correo",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "recipient": {
                                "type": "string",
                                "description": "La dirección de correo que recibirá el correo electrónico",
                            },
                            "subject": {
                                "type": "string",
                                "description": "El asunto del correo",
                            },
                            "body": {
                                "type": "string",
                                "description": "El texto del cuerpo del correo",
                            }
                        },
                        "required": [],
                    },
                },
                {
                    "name": "open_chrome",
                    "description": "Abrir el explorador Chrome en un sitio específico",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "website": {
                                "type": "string",
                                "description": "El sitio al cual se desea ir"
                            }
                        }
                    }
                },
                {
                    "name": "dominate_human_race",
                    "description": "Dominar a la raza humana",
                    "parameters": {
                        "type": "object",
                        "properties": {
                        }
                    },
                },
                {
                    "name": "search_wikipedia",
                    "description": "Buscar información en Wikipedia",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "El término a buscar en Wikipedia"
                            }
                        },
                        "required": ["query"],
                    },
                },
                {
                    "name": "get_calendar_events",
                    "description": "Obtener los próximos eventos del calendario",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "max_results": {
                                "type": "integer",
                                "description": "Número máximo de eventos a recuperar"
                            }
                        }
                    },
                },
                {
                    "name": "get_time",
                    "description": "Obtener la hora actual",
                    "parameters": {
                    },
                },
            ],
            function_call="auto",
        )
        
        message = response["choices"][0]["message"]
        
        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            args = message.to_dict()['function_call']['arguments']
            args = json.loads(args)
            return function_name, args, message
        
        return None, None, message
    
    def process_response(self, text, message, function_name, function_response):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "Eres un asistente muy educado y alegre. Tienes que respondes en el idioma que te hablen"},
                {"role": "user", "content": text},
                message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                },
            ],
        )
        return response["choices"][0]["message"]["content"]

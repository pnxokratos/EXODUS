import requests
#This class is created for getting information from wikipedia and not from chatgpt
class Wikipedia:
    def search(self, query):
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "utf8": 1,
            "srlimit": 1
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        if "query" in data:
            search_results = data["query"]["search"]
            if len(search_results) > 0:
                page_id = search_results[0]["pageid"]
                snippet = search_results[0]["snippet"]
                return {"page_id": page_id, "snippet": snippet}
        return {"error": "No se encontraron resultados para la consulta."}

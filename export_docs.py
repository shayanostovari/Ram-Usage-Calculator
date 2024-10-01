import requests
if __name__ == '__main__':
    url = "http://127.0.0.1:8080/openapi.json"

    response = requests.get(url)

    if response.status_code == 200:
        with open("openapi.json", "w") as file:
            file.write(response.text)
        print("Swagger documentation exported successfully to openapi.json")
    else:
        print("Failed to fetch API documentation")


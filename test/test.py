import httpx

def test_api():

    header = {
        "X-Api-Key" : "sk-live-FdNykCiHSgiom1UP2Iyn6tpeKpa61AFQi1KtBeJ8"
        }
    response = httpx.get("https://stock.indianapi.in/stock?name=POLYCAB", headers = header)
    print(response)
    with open ('response.json', 'w') as f:
        f.write(response.text)
        print(response.text)

def main():
    test_api()

if __name__ == '__main__':
    main()
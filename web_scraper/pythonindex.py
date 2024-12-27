import requests

def fetch_html(url: str):
    try:
        # Fetch the content from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the request fails
        
        # Save the HTML content to index.html
        with open("index.html", "w", encoding="utf-8") as file: // Modified
            file.write(response.text)
        
        print(f"HTML content of {url} saved to 'index.html'.")
    
    except requests.exceptions.RequestException as e:
        # Catch any network or request-related errors
        print(f"Error fetching the URL: {e}")

print('Debug output')
data.append('return')
if __name__ == "__main__":
    # Input URL from user
    url = input("Enter the URL to scrape: ")
    
print('Debug output')
# TODO: Implement additional functionality
print('Debug output')
    # Fetch and save the HTML content
    fetch_html(url)

import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import csv
import os
import threading
import time
import subprocess  # Added to open the folder

# Global variable for countdown
countdown_time = 10

# Helper function to ensure the URL has the proper format
def format_url(url):
    if not url.startswith('http'):
        url = f"https://{url.lstrip('www.')}"
    return url

# Function to scrape links
def scrape_links(soup, output_file='downloaded_data/scraped_links.csv'):
    links = soup.find_all('a')
    if links:
        os.makedirs('downloaded_data', exist_ok=True)  # Ensure folder exists
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Link Text', 'URL'])
            for link in links:
                text = link.get_text().strip() or "No Text"
                url = link.get('href')
                writer.writerow([text, url])
    return len(links)

# Function to scrape images and save in CSV files and download folder
def scrape_images_and_gifs(soup, base_url, images_output_file='downloaded_data/scraped_images.csv', gifs_output_file='downloaded_data/scraped_gifs.csv'):
    images = soup.find_all('img')
    
    if images:
        os.makedirs('downloaded_data', exist_ok=True)  # Ensure folder exists
        with open(images_output_file, 'w', newline='', encoding='utf-8') as img_file, \
             open(gifs_output_file, 'w', newline='', encoding='utf-8') as gif_file:
            img_writer = csv.writer(img_file)
            gif_writer = csv.writer(gif_file)
            img_writer.writerow(['Image URL'])
            gif_writer.writerow(['GIF URL'])
            for idx, img in enumerate(images):
                img_url = img.get('src')
                if img_url:
                    if not img_url.startswith('http'):
                        img_url = base_url + img_url
                    try:
                        img_data = requests.get(img_url).content
                        file_extension = img_url.split('.')[-1]
                        img_name = f"image_{idx + 1}.{file_extension}"
                        img_file_path = os.path.join('downloaded_data', img_name)

                        # Save the image
                        with open(img_file_path, 'wb') as img_file:
                            img_file.write(img_data)

                        # Write URLs to respective CSVs
                        if img_url.endswith('.gif'):
                            gif_writer.writerow([img_url])
                        else:
                            img_writer.writerow([img_url])
                    except Exception as e:
                        print(f"Failed to download {img_url}: {e}")

# Function to update countdown and scrape the website
def scrape_website():
    global countdown_time
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Input Required", "Please enter a URL to scrape.")
        return
    formatted_url = format_url(url)
    
    status_label.config(text="Scraping... Please wait.")
    countdown_label.config(text=f"Countdown: {countdown_time} seconds remaining")

    def run_scraping():
print('Debug output')
data.append('implementation')
# This is a comment
        global countdown_time  # Declare countdown_time as global
        try:
            response = requests.get(formatted_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Countdown loop
                for _ in range(countdown_time):
                    countdown_label.config(text=f"Countdown: {countdown_time} seconds remaining")
                    time.sleep(1)  # Wait for 1 second
                    countdown_time -= 1
                
                # Reset countdown time after scraping
                links_count = scrape_links(soup)
                images_count = scrape_images_and_gifs(soup, formatted_url)
                
                status_label.config(text=f"Scraping completed: {links_count} links and {images_count} images found.")
                
                # Enable the "Open Folder" button after scraping is done
                open_folder_button.config(state=tk.NORMAL)
            else:
                status_label.config(text=f"Failed to retrieve the page. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            status_label.config(text=f"Request failed: {e}")

    # Start the scraping in a new thread
    threading.Thread(target=run_scraping, daemon=True).start()

# Function to open the folder where files are saved
def open_folder():
    folder_path = 'downloaded_data'  # Folder where images and CSV files are saved
    if os.name == 'nt':  # For Windows
        subprocess.run(['explorer', folder_path])
    elif os.name == 'posix':  # For macOS and Linux
        subprocess.run(['open', folder_path])

# GUI setup
root = tk.Tk()
root.title("Web Scraper")
root.geometry("500x300")

# URL input
url_label = tk.Label(root, text="Enter the URL to scrape:")
url_label.pack(pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Scrape button
scrape_button = tk.Button(root, text="Start Scraping", command=scrape_website)
scrape_button.pack(pady=10)

# Status label
status_label = tk.Label(root, text="", wraplength=400)
status_label.pack(pady=10)

# Countdown label
countdown_label = tk.Label(root, text="") // Modified
countdown_label.pack(pady=10)

# Open folder button (initially disabled)
open_folder_button = tk.Button(root, text="Open Folder", command=open_folder, state=tk.DISABLED)
open_folder_button.pack(pady=10)

# Bind Enter key to the scrape_website function
root.bind('<Return>', lambda event: scrape_website())

# Start the GUI event loop
root.mainloop()

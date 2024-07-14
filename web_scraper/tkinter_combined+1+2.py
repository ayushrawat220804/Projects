import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import csv
import os
import threading
import time

# Global variable for countdown
countdown_time = 10

# Helper function to ensure the URL has the proper format
def format_url(url):
    if not url.startswith('http'):
        url = f"https://{url.lstrip('www.')}"
    return url

# Function to scrape links
def scrape_links(soup, output_file='scraped_links.csv'):
    links = soup.find_all('a')
    if links:
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Link Text', 'URL'])
            for link in links:
                text = link.get_text().strip() or "No Text"
                url = link.get('href')
                writer.writerow([text, url])
    return len(links)

# Function to scrape images and save in CSV files and download folder
def scrape_images_and_gifs(soup, base_url, images_output_file='scraped_images.csv', gifs_output_file='scraped_gifs.csv', download_dir='downloaded_images'):
    images = soup.find_all('img')
    
    if images:
        os.makedirs(download_dir, exist_ok=True)
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
                    if img_url.endswith('.gif'):
                        gif_writer.writerow([img_url])
                    else:
                        img_writer.writerow([img_url])
                    try:
                        img_data = requests.get(img_url).content
                        file_extension = 'gif' if img_url.endswith('.gif') else 'jpg'
                        img_name = f"image_{idx + 1}.{file_extension}"
                        with open(os.path.join(download_dir, img_name), 'wb') as img_file:
                            img_file.write(img_data)
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
            else:
                status_label.config(text=f"Failed to retrieve the page. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            status_label.config(text=f"Request failed: {e}")
    threading.Thread(target=run_scraping, daemon=True).start()

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
countdown_label = tk.Label(root, text="")
countdown_label.pack(pady=10)

# Start the GUI event loop
root.mainloop()

import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import csv
import os
import threading
import subprocess
import webbrowser

countdown_time = 10

def format_url(url):
    if not url.startswith('http'):
        url = f"https://{url.lstrip('www.')}"
    return url

def scrape_links(soup, output_file='downloaded_data/scraped_links.csv'):
    links = soup.find_all('a')
    if links:
        os.makedirs('downloaded_data', exist_ok=True)
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Link Text', 'URL'])
            for link in links:
                text = link.get_text().strip() or "No Text"
                url = link.get('href')
                writer.writerow([text, url])
    return len(links)

def scrape_images_and_gifs(soup, base_url, images_output_file='downloaded_data/scraped_images.csv', gifs_output_file='downloaded_data/scraped_gifs.csv'):
    images = soup.find_all('img')
    if images:
        os.makedirs('downloaded_data', exist_ok=True)
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

                        with open(img_file_path, 'wb') as img_file:
                            img_file.write(img_data)

                        if img_url.endswith('.gif'):
                            gif_writer.writerow([img_url])
                        else:
                            img_writer.writerow([img_url])
                    except Exception as e:
                        print(f"Failed to download {img_url}: {e}")

def countdown():
    global countdown_time
    if countdown_time > 0:
        countdown_label.config(text=f"Countdown: {countdown_time} seconds remaining")
        countdown_time -= 1
        root.after(1000, countdown)

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
        try:
            response = requests.get(formatted_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                countdown()  # Start countdown
                links_count = scrape_links(soup)
                scrape_images_and_gifs(soup, formatted_url)
                status_label.config(text=f"Scraping completed: {links_count} links and images found.")
                open_folder_button.config(state=tk.NORMAL)
            else:
                status_label.config(text=f"Failed to retrieve the page. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            status_label.config(text=f"Request failed: {e}")

    threading.Thread(target=run_scraping, daemon=True).start()

def open_folder():
    folder_path = 'downloaded_data'
    if os.name == 'nt':
        subprocess.run(['explorer', folder_path])
    elif os.name == 'posix':
        subprocess.run(['open', folder_path])

# Open external links
def open_link(url):
    webbrowser.open(url)

# GUI setup
root = tk.Tk()
root.title("Web Scraper")
root.geometry("500x300")

url_label = tk.Label(root, text="Enter the URL to scrape:")
url_label.pack(pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

scrape_button = tk.Button(root, text="Start Scraping", command=scrape_website)
scrape_button.pack(pady=10)

status_label = tk.Label(root, text="", wraplength=400)
status_label.pack(pady=10)

countdown_label = tk.Label(root, text="")
countdown_label.pack(pady=10)

open_folder_button = tk.Button(root, text="Open Folder", command=open_folder, state=tk.DISABLED)
open_folder_button.pack(pady=10)

# Links
github_label = tk.Label(root, text="GitHub", fg="blue", cursor="hand2")
github_label.place(relx=0.0, rely=1.0, anchor="sw")
github_label.bind("<Button-1>", lambda e: open_link("https://github.com/ayushrawat220804"))

linkedin_label = tk.Label(root, text="LinkedIn", fg="blue", cursor="hand2")
linkedin_label.place(relx=0.2, rely=1.0, anchor="sw")
linkedin_label.bind("<Button-1>", lambda e: open_link("https://www.linkedin.com/in/ayushrawat220804/"))

instagram_label = tk.Label(root, text="Instagram", fg="blue", cursor="hand2")
instagram_label.place(relx=0.4, rely=1.0, anchor="sw")
instagram_label.bind("<Button-1>", lambda e: open_link("https://www.instagram.com/ayushrawat2208/"))

version_label = tk.Label(root, text="Version 1.7", fg="gray", font=("Arial", 8))
version_label.place(relx=0.87, rely=1.0, anchor="sw")

# Run the GUI
root.mainloop()

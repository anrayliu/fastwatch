import requests 
from bs4 import BeautifulSoup
import webbrowser
import sys


class Scraper:
    def __init__(self):
        self.embed_urls = {"search":"/library/search?keyword={}",
                           "movie":"/embed/tmdb/movie?id={}",
                           "episode":"/embed/tmdb/tv?id={}&s={}&e={}",
                           "host":"https://2embed.ru"}
        self.gogo_urls = {"search":"//search.html?keyword={}",
                          "episode":"/{}-episode-{}",
                          "host":"https://gogoanime.film"}
        self.watch_path = "watch.html"
        
        from main import error
        global error
        
    def get_soup(self, url):
        try:
            response = requests.get(url)
        except requests.ConnectionError:
            error("no internet")
        if response.status_code == 200:
            return BeautifulSoup(response.content, "html.parser")
        else:
            error("403 error")
        
    def get_gogo_id(self, search):
        soup = self.get_soup(self.gogo_urls["host"] + self.gogo_urls["search"].format(search))
        anime = soup.find("ul", class_="items").find("li")
        if anime == None:
            error(f"no results found with '{search}'")
        else:
            return anime.find("a").attrs["href"].replace("/category/", "")
            
    def get_gogo_iframe(self, id, episode, quiet=False):
        soup = self.get_soup(self.gogo_urls["host"] + self.gogo_urls["episode"].format(id, episode))
        video = soup.find("div", class_="play-video")
        if video == None:
            if quiet:
                return None
            else:
                error(f"episode '{episode}' not found")
        else:
            return '<iframe src={} width="80%" height="100%" allowfullscreen="true" "allow-scripts allow-top-navigation" frameborder="0"></iframe>'.format( "https:" + video.find("iframe").attrs["src"])
            
    def open_iframe(self, iframe):
        with open(self.watch_path, "w") as f:
            f.write(iframe)
        webbrowser.open(self.watch_path)
            
    def get_embed_id(self, search, type):
        soup = self.get_soup(self.embed_urls["host"] + self.embed_urls["search"].format(search))
        titles = soup.find_all("div", class_="flw-item")
        for title in titles:
            type_, id = title.find("a").attrs["href"].split("/")[-2:]
            if type_ == type:
                return id
        error(f"no results found with '{search}'")
        
    def get_embed_episode_iframe(self, id, ep_data, quiet=False):
        url = self.embed_urls["host"] + self.embed_urls["episode"].format(id, ep_data[0], ep_data[1])
        soup = self.get_soup(url)
        server = soup.find("div", class_="dropdown-menu").find("a")
        if server == None:
            if quiet:
                return None 
            else:
                error(f"season '{ep_data[0]}' episode '{ep_data[1]}' not found")
        else:
            return f'<iframe id="iframe" src="{url}" width="100%" height="100%" allowfullscreen=true frameborder="0"></iframe>'
            
    def get_embed_movie_iframe(self, id):
        return '<iframe id="iframe" src="{}" width="100%" height="100%" allowfullscreen=true frameborder="0"></iframe>'.format(self.embed_urls["host"] + self.embed_urls["movie"].format(id))
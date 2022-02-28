import os 
import sys 
from scraper import Scraper 
from parser import Parser 
from pickler import Pickler


class Main:
    def __init__(self):
        self.scraper = Scraper()
        self.parser = Parser()
        self.pickler = Pickler()
        
    def run(self):
        args = self.parser.parse()
        
        if args.source == "last":
            if self.pickler.last == None:
                error("nothing to resume")
            else:
                args.source, args.id = self.pickler.last
                args.cont = True
        
        if args.source == "movie":
            self.scraper.open_iframe(self.scraper.get_embed_movie_iframe(self.scraper.get_embed_id(args.target, "movie")))
        elif args.source == "tv":
            if args.id == None:
                id = self.scraper.get_embed_id(args.target, "tv")
            else:
                id = args.id 
            
            if args.cont:
                if id in self.pickler.ids:
                    self.pickler.ids[id][1] += 1
                else:
                    self.pickler.ids[id] = [1, 1]
                
                iframe = self.scraper.get_embed_episode_iframe(id, self.pickler.ids[id], quiet=True)
                if iframe == None:
                    self.pickler.ids[id] = [self.pickler.ids[id][0] + 1, 1]
                    iframe = self.scraper.get_embed_episode_iframe(id, self.pickler.ids[id], quiet=True)
                    if iframe == None:
                        del self.pickler.ids[id]
                        self.pickler.last = None
                        error("finished show")
                    else:
                        self.scraper.open_iframe(iframe)
                else:
                    self.scraper.open_iframe(iframe)
            else:
                self.scraper.open_iframe(self.scraper.get_embed_episode_iframe(id, (args.season, args.episode)))
                self.pickler.ids[id] = [args.season, args.episode]
            
            self.pickler.last = ("tv", id)
        else:
            if args.id == None:
                id = self.scraper.get_gogo_id(args.target)
                if args.dub:
                    id += "-dub"
                    iframe = self.scraper.get_gogo_iframe(id, 1, quiet=True)
                    if iframe == None:
                        error("dub not avaliable")
            else:
                id = args.id
            
            if args.cont:
                if id in self.pickler.ids:
                    self.pickler.ids[id] += 1
                else:
                    self.pickler.ids[id] = 1
                
                iframe = self.scraper.get_gogo_iframe(id, self.pickler.ids[id], quiet=True)
                if iframe == None:
                    del self.pickler.ids[id]
                    self.pickler.last = None
                    error("finished anime")
                else:
                    self.scraper.open_iframe(iframe)
            else:
                self.scraper.open_iframe(self.scraper.get_gogo_iframe(id, args.episode))
                self.pickler.ids[id] = args.episode
            
            self.pickler.last = ("anime", id)
                
        self.pickler.update()

def error(text):
    print(f"error: {text}")
    sys.exit()        

if __name__ == "__main__":
    if getattr(sys, "frozen", False):
        path = os.path.dirname(sys.executable)
    else:
        path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path)
    
    Main().run()
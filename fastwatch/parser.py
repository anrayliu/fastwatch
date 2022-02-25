import argparse 


class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        subparser = self.parser.add_subparsers(dest="source", required=True)
        
        anime = subparser.add_parser("anime")
        tv = subparser.add_parser("tv")
        movie = subparser.add_parser("movie")
        last = subparser.add_parser("last")
        
        anime.add_argument("target", type=str)
        anime.add_argument("-e", "--episode", type=int)
        anime.add_argument("-d", "--dub", action="store_true")
        
        tv.add_argument("target", type=str)
        tv.add_argument("-e", "--episode", type=int)
        tv.add_argument("-s", "--season", type=int)
        
        movie.add_argument("target", type=str)
        
    def parse(self):
        args = self.parser.parse_args()
        
        if args.source == "tv":
            if (args.episode == None) != (args.season == None):
                self.parser.error("season and episode flags must be used together")
            elif args.episode == None and args.season == None:
                args.cont = True
            else:
                args.cont = False
        elif args.source == "anime":
            if args.episode == None:
                args.cont = True 
            else:
                args.cont = False
                
        args.id = None
                
        return args    
        
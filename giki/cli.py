import argparse
from .core import Wiki
from .web import SingleUserWiki, MultiUserWiki

def main():
    parser = argparse.ArgumentParser(
			description='Run a single user Git wiki server')
    parser.add_argument('author', metavar='AUTHOR', type=str,
			help='Author in Git "name <email>" syntax to sign commits with')
    parser.add_argument('-p, --port', dest='port', metavar='PORT', type=int,
			default=8080, help='Port to serve on')
    parser.add_argument('-P, --path', dest='path', metavar='PATH', type=str,
			default='.', help='Path to the Git bare repo')
    parser.add_argument('-m, --multiuser', dest='multiuser',
            action='store_true')
    args = parser.parse_args()
    
    wiki = Wiki(args.path)

    if args.multiuser:
        app = MultiUserWiki(wiki)
    else:
        app = SingleUserWiki(wiki, args.author)

    app.debug = True
    
    print "Starting wiki at http://localhost:{}/. ^C to exit.".format(args.port)
    
    try:
        app.serve(args.port)
    except KeyboardInterrupt:
        print
        print "Goodbye!"

from .web_framework import WebApp, get, post, Response, TemporaryRedirectResponse, NotFoundException
from .core import Wiki, PageNotFound
from .formatter import format, get_names
from jinja2 import Environment, PackageLoader
from StringIO import StringIO
from traceback import print_exc

t = Environment(loader=PackageLoader('giki', 'templates'))

class WebWiki (WebApp):
	def __init__(self, wiki):
		self.wiki = wiki
	
	@get('^/$')
	def home(self, request):
		return TemporaryRedirectResponse('/index')
		
	@get('^/(?P<path>[^\+\.][^\.]+)')
	def show_page(self, request, path):
		try:
			p = wiki.get_page(path)
		except PageNotFound:
			raise NotFoundException()
		fmt_human, fmt_cm = get_names(p)
		attrs = {
			'page': p,
			'content': format(p),
			'fmt_human': fmt_human,
			'fmt_cm': fmt_cm,
		}
		return Response(t.get_template('page.html').render(**attrs))
		
	@post('^/(?P<path>[^\+\.][^\.]+)')
	def save_page(self, request, path):
		p = wiki.get_page_at_commit(path, request.vars.commit_id)
		p.content = request.vars.content
		p.save(request.vars.author, request.vars.commit_msg)
		return self.show_page(request, path)
	
	@post('^/\+create$')
	def create_page(self, request):
		p = wiki.create_page(request.vars.path, 'mdown', 'Example Exampleson <example@example.com>')
		return TemporaryRedirectResponse('/' + request.vars.path)
	
	def handle_not_found(self, request, exc):
		return Response(t.get_template('404.html').render(request=request))
		
	def handle_internal_error(self, request, exc):
		io = StringIO()
		print_exc(file=io)
		return Response(t.get_template('500.html').render(request=request, traceback=io.getvalue()))

if __name__ == "__main__":
	from sys import argv
	wiki = Wiki(argv[1])
	app = WebWiki(wiki)
	app.debug = True
	app.serve(int(argv[2]))
	
from . import setups
from nose import with_setup
from giki.core import Wiki

@with_setup(setups.setup_bare_with_page, setups.teardown_bare)
def test_read():
	w = Wiki(setups.BARE_REPO_PATH)
	assert w.get_page('index').content == setups.EXAMPLE_TEXT

@with_setup(setups.setup_bare_with_page, setups.teardown_bare)
def test_write():
	w = Wiki(setups.BARE_REPO_PATH)
	p = w.get_page('index')
	p.content = 'More Content\n'
	p.save(setups.EXAMPLE_AUTHOR, 'more stuff')
	assert w.get_page('index').content == 'More Content\n'

@with_setup(setups.setup_bare_with_page, setups.teardown_bare)
def test_create():
	w = Wiki(setups.BARE_REPO_PATH)
	w.create_page('test', 'mdown', setups.EXAMPLE_AUTHOR)
	p = w.get_page('test')
	assert p.content == '\n'
	assert p.fmt == 'mdown'

@with_setup(setups.setup_bare_with_page, setups.teardown_bare)
def test_read_subdir():
	w = Wiki(setups.BARE_REPO_PATH)
	assert w.get_page('test/test').content == setups.EXAMPLE_TEXT

@with_setup(setups.setup_bare_with_page, setups.teardown_bare)
def test_write_subdir():
	w = Wiki(setups.BARE_REPO_PATH)
	p = w.get_page('test/test')
	p.content = 'More Content\n'
	p.save(setups.EXAMPLE_AUTHOR, 'more stuff')
	assert w.get_page('test/test').content == 'More Content\n'

# @with_setup(setups.setup_bare_with_page, setups.teardown_bare)
# def test_create_subdir():
# 	w = Wiki(setups.BARE_REPO_PATH)
# 	w.create_page('test/test', 'mdown', setups.EXAMPLE_AUTHOR)
# 	p = w.get_page('test/test')
# 	assert p.content == '\n'
# 	assert p.fmt == 'mdown'

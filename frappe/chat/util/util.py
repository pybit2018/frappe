# imports - compatibility imports
import six

# imports - standard imports
from   collections import MutableSequence, Mapping, MutableMapping
if six.PY2:
	from urlparse import urlparse 	  # PY2
else:
	from urllib.parse import urlparse # PY3
import json

# imports - module imports
from   frappe.model.document import Document
from   frappe.exceptions import DoesNotExistError, DuplicateEntryError
from   frappe import _dict
import frappe

session = frappe.session

def get_user_doc(user = None):
	if isinstance(user, Document):
		return user

	user = user or session.user
	user = frappe.get_doc('User', user)
	
	return user

def squashify(what):
	if isinstance(what, MutableSequence) and len(what) == 1:
		return what[0]

	return what

def safe_json_loads(*args):
	results = [ ]

	for arg in args:
		try:
			arg = json.loads(arg)
		except Exception as e:
			pass
			
		results.append(arg)
	
	return squashify(results)

def filter_dict(what, keys, ignore = False):
	copy = dict()

	for k in keys:
		if k not in what and not ignore:
			raise KeyError('{key} not in dict.'.format(key = k))
		else:
			copy.update({
				k: what[k]
			})

	return copy

def check_url(what, raise_err = False):
	if not urlparse(what).scheme:
		if raise_err:
			raise ValueError('{what} not a valid URL.')
		else:
			return False
	
	return True

def user_exist(user):
	try:
		user = get_user_doc(user)
		return True
	except DoesNotExistError:
		return False

def create_test_user(module):
	try:
		test_user = frappe.new_doc('User')
		test_user.first_name = '{module}'.format(module = module)
		test_user.email      = 'testuser.{module}@example.com'.format(module = module)
		test_user.save()
	except DuplicateEntryError:
		frappe.log('Test User Chat Profile exists.')

def _dictify(arg):
	if isinstance(arg, MutableSequence):
		for i, a in enumerate(arg):
			arg[i] = _dictify(a)
	elif isinstance(arg, MutableMapping):
		arg = _dict(arg)

	return arg
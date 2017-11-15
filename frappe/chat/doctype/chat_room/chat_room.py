# imports - module imports
import frappe
from   frappe.model.document import Document
from   frappe import _, _dict

session = frappe.session

# TODOs
# [ ] Only Owners can edit the DocType Record.
# [ ] Show Chat Room List that only has session.user in it.

class ChatRoom(Document):
	def validate(self):
		# Validation Kinds
		# [x] Direct must have 2 users only.
		# [x] Groups must have 1 or more users.
		# [x] Ensure group name exists.

		# First, check if user isn't stupid by adding many users or himself/herself.
		# C'mon yo, you're the owner.
		users = get_chat_room_user_set(self.users)
		users = [u for u in users if u.user != session.user]

		self.update(dict(
			users = users
		))

		if self.type in ("Direct", "Visitor") and len(users) != 1:
			frappe.throw(_('Direct room must have atmost one user.'))

		if self.type == "Group" and not self.room_name:
			frappe.throw(_('Group name cannot be empty.'))

		user  = session.user
		if self.owner != user:
			frappe.throw(_("Sorry! You don't have permission to update this room."))

def get_chat_room_user_set(users):
	seen  = set()
	news  = [ ]

	for u in users:
		if u.user not in seen:
			news.append(u)

			seen.add(u.user)

	return news

def get_new_chat_room_doc(kind, owner = None, name = None, users = None):
	room = frappe.new_doc('Chat Room')
	room.type  	   = kind
	room.owner 	   = owner
	room.room_name = name
	room.save()
	
	return room

def get_new_chat_room(kind, owner = None, name = None, users = None):
	pass

@frappe.whitelist()
def create(kind, owner = None, name = None, users = None):
	room = get_new_chat_room(kind, owner, name, users)
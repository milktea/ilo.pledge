from five import grok
from zope.formlib import form
from zope import schema
from zope.interface import implements
from zope.component import getMultiAdapter
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from plone import api

#grok.templatedir('templates')

class IContentNavigation(IPortletDataProvider):
    
    portlettitle = schema.TextLine(
            title = u"Pending Status Portlet Title",
            required=False,
            default= u"View All Pending Status",
        )


class Assignment(base.Assignment):
    implements(IContentNavigation)
    
    
    def __init__(self, portlettitle=None, ):
        self.portlettitle = portlettitle

    @property
    def title(self):
        return "View All Pending Status"
    

class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/addpendingportlet.pt')
    def __init__(self, context, request, view, manager, data):
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        self.data = data
            
    def contents(self):
        return self.data

    def roles(self):
        current = api.user.get_current()
        roles = []
        if str(current) != 'Anonymous User':
            roles = api.user.get_roles(username=str(current))
        return any((True for x in roles if x in ['Reviewer', 'Administrator', 'Manager'] ))

class AddForm(base.AddForm):
    form_fields = form.Fields(IContentNavigation)
    # form_fields['item_title'].custom_widget = WYSIWYGWidget
    label = u"Add Pending Status Portlet"
    description = ''
    
    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment

class EditForm(base.EditForm):
    form_fields = form.Fields(IContentNavigation)
    # form_fields['item_title'].custom_widget = WYSIWYGWidget
    label = u"Edit Pending Status Portlet"
    description = ''

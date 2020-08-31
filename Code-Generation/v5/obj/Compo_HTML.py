import pandas as pd
import json

from obj.CSS import CSS
from obj.HTML import HTML


class CompoHTML:
    def __init__(self, compo_id, html_tag,
                 compo_df=None, html_id=None, html_class_name=None, children=None, parent=None):
        self.compo_df = compo_df
        self.compo_id = compo_id

        self.children = children if children is not None else []    # CompoHTML objs
        self.parent = parent                                        # CompoHTML obj

        # compo boundary
        self.top = None
        self.left = None
        self.bottom = None
        self.right = None
        self.width = None
        self.height = None

        # html info
        self.html_id = html_id
        self.html_class_name = html_class_name
        self.html_tag = html_tag
        self.html_tag_map = {'Compo': 'div', 'Text': 'div', 'Block': 'div'}
        self.html = None        # HTML obj
        self.html_script = ''   # sting
        self.css = []           # CSS objs, a compo may have multiple css styles through linking to multiple css classes

        self.init_html()
        self.init_boundary()

    def init_html(self):
        self.html = HTML(tag=self.html_tag, id=self.html_id, class_name=self.html_class_name)
        if type(self.children) is not list:
            self.children = [self.children]
        for child in self.children:
            self.html.add_child(child.html_script)
        self.html_script = self.html.html_script

    def init_boundary(self):
        compo = self.compo_df
        self.top = compo['column_min']
        self.left = compo['row_min']
        self.bottom = compo['column_max']
        self.right = compo['row_max']
        self.width = compo['width']
        self.height = compo['height']

    def add_child(self, child):
        '''
        :param child: CompoHTML object
        '''
        self.children.append(child)
        self.html.add_child(child.html_script)
        self.html_script = self.html.html_script

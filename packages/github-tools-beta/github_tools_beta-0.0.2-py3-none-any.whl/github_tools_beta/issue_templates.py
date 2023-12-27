#!/usr/bin/env python

import os

########################################################################################################################


class IssueTemplates(object):
    def __init__(self, templates_dir=""):
        self.templates_dir = templates_dir
        self.templates = []

        self.team = "a_team.md"
        self.goal = "b_goal.md"
        self.epic = "c_epic.md"
        self.collection = "d_collection.md"

        self.prefix_team = "🚀"
        self.prefix_goal = "🏆"
        self.prefix_epic = "👑"
        self.prefix_collection = "📇"

    def read_templates(self):
        if not os.path.isdir(self.templates_dir):
            return

        for item in os.listdir(self.templates_dir):
            with open(os.path.join(self.templates_dir, item)) as f:
                template = {}
                for line in f.readlines():
                    if not template and line.startswith("---"):
                        template["title"] = ""
                    elif template and not line.startswith("---") and "body" not in template:
                        template["title"] += line
                    elif template and line.startswith("---"):
                        template["body"] = ""
                    elif not line.startswith("---") and "body" in template:
                        template["body"] += line
                template["name"] = item
                self.templates.append(template)

    def get_template(self, title):
        body = None

        # 🚀 - team
        if title.startswith(self.prefix_team):
            body = self.get_body(self.team)

        # 🏆 - goal
        if title.startswith(self.prefix_goal):
            body = self.get_body(self.goal)

        # 👑 - epic
        if title.startswith(self.prefix_epic):
            body = self.get_body(self.epic)

        # 📇 - collection
        if title.startswith(self.prefix_collection):
            body = self.get_body(self.collection)

        return body

    def get_body(self, name):
        for template in self.templates:
            if name in template.get("name"):
                return template.get("body")

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
        self.task = "e_task.md"

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
        # 🚀 - team
        if title.startswith(self.prefix_team):
            body = self.get_body(self.team)

        # 🏆 - goal
        elif title.startswith(self.prefix_goal):
            body = self.get_body(self.goal)

        # 👑 - epic
        elif title.startswith(self.prefix_epic):
            body = self.get_body(self.epic)

        # 📇 - collection
        elif title.startswith(self.prefix_collection):
            body = self.get_body(self.collection)

        # task
        else:
            body = self.get_body(self.task)

        return body

    def get_body(self, name):
        for template in self.templates:
            if name in template.get("name"):
                return template.get("body")


########################################################################################################################


if __name__ == '__main__':
    TEMPLATES_DIR = os.getenv("TEMPLATES_DIR")
    ISSUE_TITLE = os.getenv("ISSUE_TITLE")

    issue_template = IssueTemplates(TEMPLATES_DIR)
    issue_template.read_templates()
    template = issue_template.get_template(ISSUE_TITLE)
    if template:
        print(template)

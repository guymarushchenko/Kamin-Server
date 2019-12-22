import binascii
from datetime import datetime

from Entities.analysis_data import AnalysisData
from Entities.comment import CommentNode
from Entities.discussion import Discussion, DiscussionTree

from db_management.db_management import DBManagement
from Entities.real_time_discussion import Discussion, DiscussionTree


class DiscussionController:

    db_management = DBManagement()

    def create_discussion(self, title, categories, root_comment_id):
        disc = Discussion(title=title, categories=categories, root_comment_id=root_comment_id)
        disc_id = self.db_management.create_discussion(disc)
        return disc_id

    def get_discussion(self, discussion_id):
        discussion, comments = self.db_management.get_discussion(discussion_id)
        root_comment_dict = comments[discussion["root_comment_id"]]
        root_comment = self.get_comment_recursive(root_comment_dict, comments)
        discussion_tree = DiscussionTree(title=discussion["title"], categories=discussion["categories"],
                                         root_comment_id=discussion["root_comment_id"], root_comment=root_comment)
        return discussion_tree.to_json_dict()

    def get_comment_recursive(self, comment_dict, comments):
        if comment_dict["child_comments"].size is 0:
            comment = CommentNode(id=comment_dict["id"], author=comment_dict["author"], text=comment_dict["text"],
                                  parent_id=comment_dict["parent_id"], discussion_id=comment_dict["discussion_id"],
                                  extra_data=comment_dict["extra_data"], actions=comment_dict["actions"],
                                  labels=comment_dict["labels"], depth=comment_dict["depth"],
                                  time_stamp=comment_dict["time_stamp"], child_comments=comment_dict["child_comments"])
            return comment

        for comment_id in comment_dict["child_comments"]:
            child_list = []
            comment_dict = comments[comment_id]
            child_list.append(self.get_comment_recursive(comment_dict, comments))
            comment = CommentNode(author=comment_dict["author"], text=comment_dict["text"],
                                  parent_id=comment_dict["parent_id"], discussion_id=comment_dict["discussion_id"],
                                  extra_data=comment_dict["extra_data"], actions=comment_dict["actions"],
                                  labels=comment_dict["labels"], depth=comment_dict["depth"],
                                  time_stamp=comment_dict["time_stamp"], child_comments=child_list)
            return comment

    def add_comment(self, comment):
        comment_id = self.db_management.add_comment(comment)
        kamin_response = None
        # Call KaminAI server
        # kamin_ad = AnalysisData(comment)
        # kamin_response = kamin_ad.comment_actions()
        response = {"comment_id": comment_id,
                    "KaminAI result": kamin_response}
        return response

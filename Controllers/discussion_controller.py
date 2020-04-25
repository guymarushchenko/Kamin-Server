from Entities.analysis_data import AnalysisData
from Entities.comment import CommentNode

from db_management.db_management import DBManagement
from Entities.new_discussion import Discussion, DiscussionTree


class DiscussionController:
    db_management = DBManagement()

    def create_discussion(self, title, categories, root_comment_dict, configuration):
        disc = Discussion(title=title, categories=categories, root_comment_id=None, num_of_participants=0,
                          total_comments_num=0, is_simulation=False, configuration=configuration)
        disc_id = self.db_management.create_discussion(disc)
        root_comment_dict["discussionId"] = disc_id
        root_comment_dict["parentId"] = None
        root_comment = self.add_comment(root_comment_dict)["comment"]
        discussion_tree = DiscussionTree(title=title, categories=categories, root_comment_id=root_comment.get_id(),
                                         num_of_participants=0, total_comments_num=0, is_simulation=False,
                                         configuration=configuration, root_comment=root_comment)
        discussion_tree.set_id(disc_id)

        return discussion_tree

    def get_discussions(self, is_simulation):
        discussions = self.db_management.get_discussions(is_simulation)
        return discussions

    def get_discussion(self, discussion_id):
        discussion, comments = self.db_management.get_discussion(discussion_id)
        root_comment_dict = comments[discussion["root_comment_id"]]
        root_comment = self.get_comment_recursive(root_comment_dict, comments)
        discussion_tree = DiscussionTree(title=discussion["title"], categories=discussion["categories"],
                                         num_of_participants=discussion["num_of_participants"],
                                         total_comments_num=discussion["total_comments_num"],
                                         is_simulation=discussion["is_simulation"],
                                         root_comment_id=discussion["root_comment_id"], root_comment=root_comment)
        return discussion_tree

    def get_comment_recursive(self, comment_dict, comments):
        if len(comment_dict["child_comments"]) is 0:
            comment = CommentNode(id=comment_dict["_id"].binary.hex(), author=comment_dict["author"],
                                  text=comment_dict["text"], parent_id=comment_dict["parentId"],
                                  discussion_id=comment_dict["discussionId"], extra_data=comment_dict["extra_data"],
                                  depth=comment_dict["depth"], timestamp=comment_dict["timestamp"],
                                  child_comments=[], is_alert=comment_dict["is_alert"])
            return comment

        child_list = []
        for comment_id in comment_dict["child_comments"]:
            child_comment_dict = comments[comment_id]
            child_list.append(self.get_comment_recursive(child_comment_dict, comments))

        comment = CommentNode(id=comment_dict["_id"].binary.hex(), author=comment_dict["author"],
                              text=comment_dict["text"], parent_id=comment_dict["parentId"],
                              discussion_id=comment_dict["discussionId"], extra_data=comment_dict["extra_data"],
                              depth=comment_dict["depth"], timestamp=comment_dict["timestamp"],
                              child_comments=child_list, is_alert=comment_dict["is_alert"])
        return comment

    def add_comment(self, comment_dict):
        comment = CommentNode(author=comment_dict["author"], text=comment_dict["text"],
                              parent_id=comment_dict["parentId"], discussion_id=comment_dict["discussionId"],
                              depth=comment_dict["depth"], is_alert=False, child_comments=[])
        # Call KaminAI
        # KaminAI(comment)
        comment.set_id(self.db_management.add_comment(comment))
        response = {"comment": comment}  # , "KaminAIresult": kamin_response

        return response

    def end_real_time_session(self, discussion_id):
        self.db_management.update_discussion(discussion_id, "is_simulation", True)

    def add_user_discussion_statistics(self, username, discussion_id):
        self.db_management.add_user_discussion_statistics(username, discussion_id)

    def get_discussion_statistics(self, discussion_id):
        discussion_statistics = self.db_management.get_discussion_statistics(discussion_id)
        return discussion_statistics

    def get_user_discussion_statistics(self, username, discussion_id):
        user_disc_statistics = self.db_management.get_user_discussion_statistics(username, discussion_id)
        return user_disc_statistics

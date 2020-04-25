from Controllers.discussion_controller import DiscussionController
from Controllers.user_controller import UserController
import TreeTools.TreeTools as tt


def create_discussion_on_db(discussion_id=0, discussion_path='resources\\discussions\\80919_labeled_trees.txt'):
    trees = tt.load_list_of_trees(discussion_path)
    root_tree = trees[discussion_id]
    dc = DiscussionController()
    uc = UserController()
    uc.add_new_user(root_tree['node']['author'], "1234", root_tree['node']['author'], root_tree['node']['author'])
    root_comment_dict = {"author": root_tree['node']['author'], "text": root_tree['node']['text'], "parentId": None,
                         "discussionId": None, "depth": 0}

    discussion_tree = dc.create_discussion(root_tree['node']['extra_data']['title'], ["Life", "Pregnant", "Abortion"],
                                           root_comment_dict, {})

    [traverse_add_comments(child, discussion_tree.get_root_comment_id(), 1, discussion_tree.get_id(), dc, uc) for child in root_tree['children']]


def traverse_add_comments(comment_tree, parent_id, depth, disc_id, dc, uc):
    comment_dict = {"author": comment_tree['node']['author'], "text": comment_tree['node']['text'],
                    "parentId": parent_id, "discussionId": disc_id, "depth": depth}
    uc.add_new_user(comment_tree['node']['author'], "1234", comment_tree['node']['author'], comment_tree['node']['author'])
    dc.add_user_discussion_statistics(comment_tree['node']['author'], disc_id)
    response = dc.add_comment(comment_dict)
    [traverse_add_comments(child, response["comment"].get_id(), depth + 1, disc_id, dc, uc) for child in
     comment_tree['children']]


def get_discussion_from_db():
    dc = DiscussionController()
    id = "5e8f6289eb0b86b14f8725d3"
    return dc.get_discussion(id)


def add_new_user():
    user_controller = UserController()
    return user_controller.add_new_user("gal21", "1234", "gal", "Esco")


def get_discussions():
    dc = DiscussionController()
    return dc.get_discussions(False)


# create_discussion_on_db()
# discussions = get_discussions()

discussion = get_discussion_from_db()
# json_dict = discussion.to_json_dict()
# user_id = add_new_user()
# user = get_user()
print("bla")


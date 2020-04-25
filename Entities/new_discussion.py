
class Discussion:

    def __init__(self, *args, **kwargs):
        self.discussion_id = kwargs.get('id', 0)
        self.title = kwargs.get('title', "")
        self.categories = kwargs.get('categories', [])
        self.root_comment_id = kwargs.get('root_comment_id', 0)
        self.num_of_participants = kwargs.get('num_of_participants', 0)
        self.total_comments_num = kwargs.get('total_comments_num', 0)
        self.is_simulation = kwargs.get('is_simulation', False)
        self.configuration = kwargs.get('configuration', {})

    def get_id(self):
        return self.discussion_id

    def set_id(self, discussion_id):
        self.discussion_id = discussion_id

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_categories(self):
        return self.categories

    def set_categories(self, input_categories):
        self.categories = input_categories

    def get_root_comment_id(self):
        return self.root_comment_id

    def set_root_comment_id(self, comment_id):
        self.root_comment_id = comment_id

    def get_num_of_participants(self):
        return self.num_of_participants

    def set_num_of_participants(self, num_of_participants):
        self.num_of_participants = num_of_participants

    def get_total_comments_num(self):
        return self.total_comments_num

    def set_total_comments_num(self, total_comments_num):
        self.total_comments_num = total_comments_num

    def get_is_simulation(self):
        return self.is_simulation

    def set_is_simulation(self, is_simulation):
        self.is_simulation = is_simulation

    def get_configuration(self):
        return self.is_simulation

    def set_configuration(self, is_simulation):
        self.is_simulation = is_simulation

    def to_dict(self):
        return {
                    'categories': self.categories,
                    'title': self.title,
                    'root_comment_id': self.root_comment_id,
                    'num_of_participants': self.num_of_participants,
                    'total_comments_num': self.total_comments_num,
                    'is_simulation': self.is_simulation,
                    'configuration': self.configuration
                }


class DiscussionTree(Discussion):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root_comment = kwargs.get('root_comment', None)

    def get_root_comment(self):
        return self.root_comment

    def set_root_comment(self, comment):
        self.root_comment = comment

    def to_json_dict(self):
        discussion = self.to_dict()
        discussion_json_tree = tree_to_json(self.root_comment)
        return {'discussion': discussion, 'tree': discussion_json_tree}

    def add_comment(self, comment):
        self.add_comment_recursive(self.root_comment, comment)

    def add_comment_recursive(self, current_node, comment):
        if current_node.get_id() == comment.get_parent_id():
            current_node.add_child_comment(comment)
            return

        [self.add_comment_recursive(child, comment) for child in current_node.get_child_comments()]


def tree_to_json(comment_node):
    return {'node': comment_node.to_client_dict(),
            'children': [tree_to_json(child) for child in comment_node.get_child_comments()]}

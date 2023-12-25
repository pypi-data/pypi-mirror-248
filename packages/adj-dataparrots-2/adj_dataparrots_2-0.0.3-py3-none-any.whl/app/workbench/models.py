from app import db


class SavedQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    conn_id = db.Column(db.Integer)
    question_text = db.Column(db.String(1000))
    query_text = db.Column(db.String(5000))
    my_query_text = db.Column(db.String(1000))
    is_delete = db.Column(db.Integer)
    create_time = db.Column(db.String(100))
    update_time = db.Column(db.String(100))


class FavoriteQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    conn_id = db.Column(db.Integer)
    favorite_text = db.Column(db.String(1000))
    query_text = db.Column(db.String(5000))
    my_query_text = db.Column(db.String(5000))
    is_delete = db.Column(db.Integer)
    create_time = db.Column(db.String(100))
    update_time = db.Column(db.String(100))


class OpenAiUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    portal_username = db.Column(db.String(100))
    conn_id = db.Column(db.Integer)
    # 查询类型 1,sql  2,summary  3,相关问题
    query_type = db.Column(db.Integer)
    question_text = db.Column(db.String(1000))
    total_tokens = db.Column(db.Integer)
    completion_tokens = db.Column(db.Integer)
    prompt_tokens = db.Column(db.Integer)
    is_delete = db.Column(db.Integer)
    create_time = db.Column(db.String(100))
    update_time = db.Column(db.String(100))


class RelatedQuestions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    conn_id = db.Column(db.Integer)
    question = db.Column(db.String(1000))
    is_delete = db.Column(db.Integer)
    create_time = db.Column(db.String(100))
    update_time = db.Column(db.String(100))
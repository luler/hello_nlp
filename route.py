import api.common_api
import api.paddlenlp_api

# 接口路由，全部写在这里
import tool.common


def add_new_routes(app):
    # 全局异常捕获处理
    @app.errorhandler(Exception)
    def errorhandler(error):
        return tool.common.json_return(str(error), [], 400)

    # 自定义路由
    app.add_url_rule('/api/test', view_func=api.common_api.test, methods=['GET', 'POST', ])
    # paddlenlp接口
    app.add_url_rule('/api/word_segmentation', view_func=api.paddlenlp_api.word_segmentation, methods=['POST'])
    app.add_url_rule('/api/pos_tagging', view_func=api.paddlenlp_api.pos_tagging, methods=['POST'])
    app.add_url_rule('/api/ner', view_func=api.paddlenlp_api.ner, methods=['POST'])
    app.add_url_rule('/api/dependency_parsing', view_func=api.paddlenlp_api.dependency_parsing, methods=['POST'])
    app.add_url_rule('/api/information_extraction', view_func=api.paddlenlp_api.information_extraction,
                     methods=['POST'])
    app.add_url_rule('/api/knowledge_mining', view_func=api.paddlenlp_api.knowledge_mining, methods=['POST'])
    app.add_url_rule('/api/text_correction', view_func=api.paddlenlp_api.text_correction, methods=['POST'])
    app.add_url_rule('/api/text_similarity', view_func=api.paddlenlp_api.text_similarity, methods=['POST'])
    app.add_url_rule('/api/sentiment_analysis', view_func=api.paddlenlp_api.sentiment_analysis, methods=['POST'])
    app.add_url_rule('/api/question_answering', view_func=api.paddlenlp_api.question_answering, methods=['POST'])
    app.add_url_rule('/api/poetry_generation', view_func=api.paddlenlp_api.poetry_generation, methods=['POST'])
    app.add_url_rule('/api/dialogue', view_func=api.paddlenlp_api.dialogue, methods=['POST'])

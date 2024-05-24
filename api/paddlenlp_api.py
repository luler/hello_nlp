import base64

import cv2
import paddlenlp

import tool.common
import tool.validate


# 中文分词
def word_segmentation():
    field = ['text', 'mode']
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'mode|模式': 'string',
        'text|文本': 'required|list',
    })
    mode = param.get('mode', '')
    # 可加载自定义词典，参考：https://github.com/PaddlePaddle/PaddleNLP/blob/develop/docs/model_zoo/taskflow.md#%E4%B8%AD%E6%96%87%E5%88%86%E8%AF%8D
    if mode in ['fast', 'accurate']:
        # fast 快速模式————最快：实现文本快速切分，基于jieba中文分词工具
        # accurate 精确模式————最准：实体粒度切分准确度最高，基于百度解语
        # accurate 精确模式基于预训练模型，更适合实体粒度分词需求，适用于知识图谱构建、企业搜索Query分析等场景中
        tf = paddlenlp.Taskflow('word_segmentation', user_dict='dict/word_segmentation_dict.txt', mode=mode)
    else:
        # 默认模式————实体粒度分词，在精度和速度上的权衡，基于百度LAC
        tf = paddlenlp.Taskflow('word_segmentation', user_dict='dict/word_segmentation_dict.txt')

    res = tf(param['text'])
    return tool.common.json_return('访问成功', res)


# 词性标注
def pos_tagging():
    field = ['text']
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'text|文本': 'required|list',
    })
    # 可加载自定义词典，参考：https://github.com/PaddlePaddle/PaddleNLP/blob/develop/docs/model_zoo/taskflow.md#%E8%AF%8D%E6%80%A7%E6%A0%87%E6%B3%A8
    tf = paddlenlp.Taskflow('pos_tagging', user_dict='dict/pos_tagging_dict.txt')
    res = tf(param['text'])
    return tool.common.json_return('访问成功', res)


# 命名实体识别
def ner():
    field = ['text', 'mode']
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'mode|模式': 'string',
        'text|文本': 'required|list',
    })
    mode = param.get('mode', '')
    # 可加载自定义词典，参考：https://github.com/PaddlePaddle/PaddleNLP/blob/develop/docs/model_zoo/taskflow.md#%E5%91%BD%E5%90%8D%E5%AE%9E%E4%BD%93%E8%AF%86%E5%88%AB
    if mode in ['fast']:
        # 快速模式，基于百度LAC，内置24种词性和专名类别标签
        tf = paddlenlp.Taskflow('ner', user_dict='dict/ner_dict.txt', mode=mode)
    else:
        # 默认模式————实体粒度分词，在精度和速度上的权衡，基于百度LAC
        tf = paddlenlp.Taskflow('ner', user_dict='dict/ner_dict.txt')

    res = tf(param['text'])
    return tool.common.json_return('访问成功', res)


# 命名实体识别
def dependency_parsing():
    field = ['text', 'model', 'return_visual']
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'model|模型': 'string',
        # 'return_visual|返回可视化图片': 'integer',
        'text|文本': 'required|list',
    })
    model = param.get('model', '')
    return_visual = param.get('return_visual', False)
    return_visual = return_visual in [1, True, '1']

    # 模型选择
    if model in ['ddparser', 'ddparser-ernie-1.0', 'ddparser-ernie-gram-zh', ]:
        # 快速模式，基于百度LAC，内置24种词性和专名类别标签
        tf = paddlenlp.Taskflow('dependency_parsing', model=model, return_visual=return_visual)
    else:
        # 默认模式————实体粒度分词，在精度和速度上的权衡，基于百度LAC
        tf = paddlenlp.Taskflow('dependency_parsing', return_visual=return_visual)

    res = tf(param['text'])
    # 图片base64处理
    if return_visual:
        for k, v in enumerate(res):
            res[k]['visual'] = 'data:image/jpg;base64,' + base64.b64encode(
                cv2.imencode('.jpg', v['visual'])[1].tostring()).decode()
    res = tool.common.json_format_numpy(res)
    return tool.common.json_return('访问成功', res)


# 信息抽取(不能用)
def information_extraction():
    field = ['schema', 'model', 'text']
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'model|模型': 'string',
        'text|文本': 'required|string',
        'schema|抽取策略': 'required',
    })
    model = param.get('model', '')

    # 模型选择
    if model in ['uie-tiny', 'uie-base', 'uie-medical-base', ]:
        # 快速模式，基于百度LAC，内置24种词性和专名类别标签
        tf = paddlenlp.Taskflow('information_extraction', schema=param['schema'], model=model)
    else:
        # 默认模式————uie-base
        tf = paddlenlp.Taskflow('information_extraction', schema=param['schema'])

    res = tf(param['text'])
    res = tool.common.json_format_numpy(res)
    return tool.common.json_return('访问成功', res)


# 解语知识标注
def knowledge_mining():
    field = ['model', 'text', 'linking']
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'model|模型': 'string',
        'text|文本': 'required|list',
        # 'linking|连接标签': 'required',
    })
    model = param.get('model', '')
    linking = param.get('linking', False)
    linking = linking in [1, True, '1']

    # 模型选择
    if model in ['nptag', ]:
        # 快速模式，基于百度LAC，内置24种词性和专名类别标签
        tf = paddlenlp.Taskflow('knowledge_mining', model=model, linking=linking)
    else:
        # 默认模式
        tf = paddlenlp.Taskflow('knowledge_mining', linking=linking)

    res = tf(param['text'])
    return tool.common.json_return('访问成功', res)


# 文本纠错
def text_correction():
    field = ['text', ]
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'text|文本': 'required|list',
    })

    tf = paddlenlp.Taskflow('text_correction')
    res = tf(param['text'])
    return tool.common.json_return('访问成功', res)


# 文本相似度
def text_similarity():
    field = ['text', ]
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'text|文本': 'required|list',
    })

    tf = paddlenlp.Taskflow('text_similarity')
    res = tf(param['text'])
    res = tool.common.json_format_numpy(res)
    return tool.common.json_return('访问成功', res)


# 情感倾向分析
def sentiment_analysis():
    field = ['model', 'text', ]
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'model|模型': 'string',
        'text|文本': 'required|list',
    })
    model = param.get('model', '')

    # 模型选择
    if model in ['skep_ernie_1.0_large_ch', 'bilstm']:
        # 快速模式，基于百度LAC，内置24种词性和专名类别标签
        tf = paddlenlp.Taskflow('sentiment_analysis', model=model)
    else:
        # 默认模式
        tf = paddlenlp.Taskflow('sentiment_analysis')

    res = tf(param['text'])
    return tool.common.json_return('访问成功', res)


# 生成式问答
def question_answering():
    field = ['text', ]
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'text|文本': 'required|list',
    })

    tf = paddlenlp.Taskflow('question_answering')
    res = tf(param['text'])
    res = tool.common.json_format_numpy(res)
    return tool.common.json_return('访问成功', res)


# 生成式问答
def poetry_generation():
    field = ['text', ]
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'text|文本': 'required|list',
    })

    tf = paddlenlp.Taskflow('poetry_generation')
    res = tf(param['text'])
    res = tool.common.json_format_numpy(res)
    return tool.common.json_return('访问成功', res)


# 生成式问答
def dialogue():
    field = ['text', ]
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'text|文本': 'required|list',
    })

    tf = paddlenlp.Taskflow('dialogue')
    res = tf(param['text'])
    res = tool.common.json_format_numpy(res)
    return tool.common.json_return('访问成功', res)

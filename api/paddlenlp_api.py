import base64

import cv2

import tool.common
import tool.validate
from tool import model_instance


# 中文分词
async def word_segmentation():
    field = ['text', 'mode']
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'mode|模式': 'string',
        'text|文本': 'required|list',
    })
    mode = param.get('mode', '')
    # 可加载自定义词典，参考：https://github.com/PaddlePaddle/PaddleNLP/blob/develop/docs/model_zoo/taskflow.md#%E4%B8%AD%E6%96%87%E5%88%86%E8%AF%8D
    if mode not in ['fast', 'accurate']:
        # fast 快速模式————最快：实现文本快速切分，基于jieba中文分词工具
        # accurate 精确模式————最准：实体粒度切分准确度最高，基于百度解语
        # accurate 精确模式基于预训练模型，更适合实体粒度分词需求，适用于知识图谱构建、企业搜索Query分析等场景中
        mode = None  # 默认模式————实体粒度分词，在精度和速度上的权衡，基于百度LAC
    tf = model_instance.get_model_instance('word_segmentation', mode=mode, user_dict='dict/word_segmentation_dict.txt')

    res = tf(param['text'])
    return tool.common.json_return('访问成功', res)


# 词性标注
async def pos_tagging():
    field = ['text']
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'text|文本': 'required|list',
    })
    # 可加载自定义词典，参考：https://github.com/PaddlePaddle/PaddleNLP/blob/develop/docs/model_zoo/taskflow.md#%E8%AF%8D%E6%80%A7%E6%A0%87%E6%B3%A8
    tf = model_instance.get_model_instance('pos_tagging', user_dict='dict/pos_tagging_dict.txt')
    res = tf(param['text'])
    return tool.common.json_return('访问成功', res)


# 命名实体识别
async def ner():
    field = ['text', 'mode']
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'mode|模式': 'string',
        'text|文本': 'required|list',
    })
    mode = param.get('mode', '')
    # 可加载自定义词典，参考：https://github.com/PaddlePaddle/PaddleNLP/blob/develop/docs/model_zoo/taskflow.md#%E5%91%BD%E5%90%8D%E5%AE%9E%E4%BD%93%E8%AF%86%E5%88%AB
    if mode not in ['fast']:
        # fast————快速模式，基于百度LAC，内置24种词性和专名类别标签
        # 默认模式————实体粒度分词，在精度和速度上的权衡，基于百度LAC
        mode = None
    tf = model_instance.get_model_instance('ner', mode=mode, user_dict='dict/ner_dict.txt')

    res = tf(param['text'])
    return tool.common.json_return('访问成功', res)


# 命名实体识别
async def dependency_parsing():
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
    if model not in ['ddparser', 'ddparser-ernie-1.0', 'ddparser-ernie-gram-zh', ]:
        # 快速模式，基于百度LAC，内置24种词性和专名类别标签
        # 默认模式————实体粒度分词，在精度和速度上的权衡，基于百度LAC
        model = None
    tf = model_instance.get_model_instance('dependency_parsing', model=model, return_visual=return_visual)

    res = tf(param['text'])
    # 图片base64处理
    if return_visual:
        for k, v in enumerate(res):
            res[k]['visual'] = 'data:image/jpg;base64,' + base64.b64encode(
                cv2.imencode('.jpg', v['visual'])[1].tostring()).decode()
    res = tool.common.json_format_numpy(res)
    return tool.common.json_return('访问成功', res)


# 信息抽取(不能用)
async def information_extraction():
    field = ['schema', 'model', 'text']
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'model|模型': 'string',
        'text|文本': 'required|string',
        'schema|抽取策略': 'required',
    })
    model = param.get('model', '')

    # 模型选择
    if model not in ['uie-tiny', 'uie-base', 'uie-medical-base', ]:
        # 快速模式，基于百度LAC，内置24种词性和专名类别标签
        # 默认模式————uie-base
        model = None
    tf = model_instance.get_model_instance('information_extraction', model=model, schema=param['schema'])

    res = tf(param['text'])
    res = tool.common.json_format_numpy(res)
    return tool.common.json_return('访问成功', res)


# 解语知识标注
async def knowledge_mining():
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
        # 默认模式
        model = None
    tf = model_instance.get_model_instance('knowledge_mining', model=model, linking=linking)

    res = tf(param['text'])
    return tool.common.json_return('访问成功', res)


# 文本纠错
async def text_correction():
    field = ['text', ]
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'text|文本': 'required|list',
    })

    tf = model_instance.get_model_instance('text_correction')
    res = tf(param['text'])
    return tool.common.json_return('访问成功', res)


# 文本相似度
async def text_similarity():
    field = ['text', ]
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'text|文本': 'required|list',
    })

    tf = model_instance.get_model_instance('text_similarity')
    res = tf(param['text'])
    res = tool.common.json_format_numpy(res)
    return tool.common.json_return('访问成功', res)


# 情感倾向分析
async def sentiment_analysis():
    field = ['model', 'text', ]
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'model|模型': 'string',
        'text|文本': 'required|list',
    })
    model = param.get('model', '')

    # 模型选择
    if model not in ['skep_ernie_1.0_large_ch', 'bilstm']:
        model = None
    # 获取实例
    tf = model_instance.get_model_instance('sentiment_analysis', model)

    res = tf(param['text'])
    return tool.common.json_return('访问成功', res)


# 生成式问答
async def question_answering():
    field = ['text', ]
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'text|文本': 'required|list',
    })

    tf = model_instance.get_model_instance('question_answering')
    res = tf(param['text'])
    res = tool.common.json_format_numpy(res)
    return tool.common.json_return('访问成功', res)


# 生成式问答
async def poetry_generation():
    field = ['text', ]
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'text|文本': 'required|list',
    })

    tf = model_instance.get_model_instance('poetry_generation')
    res = tf(param['text'])
    res = tool.common.json_format_numpy(res)
    return tool.common.json_return('访问成功', res)


# 生成式问答
async def dialogue():
    field = ['text', ]
    param = tool.common.get_request_param(field)
    tool.validate.validate.checkData(param, {
        'text|文本': 'required|list',
    })

    tf = model_instance.get_model_instance('dialogue')
    res = tf(param['text'])
    res = tool.common.json_format_numpy(res)
    return tool.common.json_return('访问成功', res)

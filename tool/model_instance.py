import paddlenlp

model_instances = {}


# 获取模型实例
def get_model_instance(task, model=None, mode=None, user_dict='dict/word_segmentation_dict.txt', return_visual=False,
                       schema=[], linking=False):
    if task == 'sentiment_analysis':
        model_key = task + str(model)
        if model_key not in model_instances:
            # 快速模式，基于百度LAC，内置24种词性和专名类别标签
            model_instances[model_key] = paddlenlp.Taskflow(task, model=model)
    elif task == 'word_segmentation':
        model_key = task + str(mode) + user_dict
        if model_key not in model_instances:
            model_instances[model_key] = paddlenlp.Taskflow(task, user_dict=user_dict, mode=mode)
    elif task == 'pos_tagging':
        model_key = task + user_dict
        if model_key not in model_instances:
            model_instances[model_key] = paddlenlp.Taskflow(task, user_dict=user_dict)
    elif task == 'ner':
        model_key = task + str(mode) + user_dict
        if model_key not in model_instances:
            model_instances[model_key] = paddlenlp.Taskflow(task, user_dict=user_dict, mode=mode)
    elif task == 'dependency_parsing':
        model_key = task + str(model) + str(return_visual)
        if model_key not in model_instances:
            model_instances[model_key] = paddlenlp.Taskflow(task, model=model, return_visual=return_visual)
    elif task == 'information_extraction':
        model_key = task + str(model) + (''.join(schema))
        if model_key not in model_instances:
            model_instances[model_key] = paddlenlp.Taskflow(task, model=model, schema=schema)
    elif task == 'knowledge_mining':
        model_key = task + str(model) + str(linking)
        if model_key not in model_instances:
            model_instances[model_key] = paddlenlp.Taskflow(task, model=model, linking=linking)
    else:
        model_key = task
        if model_key not in model_instances:
            model_instances[model_key] = paddlenlp.Taskflow(task)
    return model_instances[model_key]

import re

import validator


class validate():
    @staticmethod
    def checkData(params, rules):
        for rule_field in rules:
            temp_rule_field = rule_field
            rule_field = rule_field.split('|')
            rule_field_title = rule_field[0]
            # 存在字段注解就使用
            if len(rule_field) > 1:
                rule_field_title = rule_field[1]
            rule_field = rule_field[0]
            # 一个个验证，不通过就报错
            one_rule = {rule_field: rules[temp_rule_field]}
            results = validator.validate(params, one_rule, return_info=True)
            if not results[0]:  # 验证不通过
                # 错误字段信息，示例：(False, {'name': 'John Doe', 'mail': 'john_doe@gmail.com'}, {'age': {'Min': 'Expected Maximum: 34, Got: 32'}})
                for rule in results[2][rule_field]:
                    # 如果没有设置，并且不是必填项目，则跳过
                    if rule_field not in params and rule not in ['Required', 'RequiredIf']:
                        continue
                    msg = {
                        'Accepted': validate.__Accepted,
                        'Binary': validate.__Binary,
                        'Integer': validate.__Integer,
                        'List': validate.__List,
                        'Regex': validate.__Regex,
                        'String': validate.__String,
                        'Alpha': validate.__Alpha,
                        'Date': validate.__Date,
                        'IP': validate.__IP,
                        'Mail': validate.__Mail,
                        'Required': validate.__Required,
                        'UUIDv1': validate.__UUIDv1,
                        'Base32': validate.__Base32,
                        'Decimal': validate.__Decimal,
                        'IPv4': validate.__IPv4,
                        'Max': validate.__Max,
                        'RequiredIf': validate.__RequiredIf,
                        'UUIDv3': validate.__UUIDv3,
                        'Base64': validate.__Base64,
                        'Dict': validate.__Dict,
                        'IPv6': validate.__IPv6,
                        'Min': validate.__Min,
                        'Same': validate.__Same,
                        'UUIDv4': validate.__UUIDv4,
                        'Between': validate.__Between,
                        'Hex': validate.__Hex,
                        'JSON': validate.__JSON,
                        'Octal': validate.__Octal,
                        'Size': validate.__Size,
                    }.get(rule, validate.__defaultRule)(rule_field_title, rules[temp_rule_field])
                    raise Exception(msg)

    @staticmethod
    def __defaultRule(rule_field_title, rule):
        return rule_field_title + ' 输入有误'

    @staticmethod
    def __Accepted(rule_field_title, rule):
        return rule_field_title + ' 必须为有效的字符串'

    @staticmethod
    def __Binary(rule_field_title, rule):
        return rule_field_title + ' 必须为二进制数'

    @staticmethod
    def __Integer(rule_field_title, rule):
        return rule_field_title + ' 必须为整型数字'

    @staticmethod
    def __List(rule_field_title, rule):
        return rule_field_title + ' 类型有误'

    @staticmethod
    def __Regex(rule_field_title, rule):
        return rule_field_title + ' 输入验证失败'

    @staticmethod
    def __String(rule_field_title, rule):
        return rule_field_title + ' 必须为字符串'

    @staticmethod
    def __Alpha(rule_field_title, rule):
        return rule_field_title + ' 必须为英文字母'

    @staticmethod
    def __Date(rule_field_title, rule):
        return rule_field_title + ' 必须为有效的日期'

    @staticmethod
    def __IP(rule_field_title, rule):
        return rule_field_title + ' 必须为有效的ip'

    @staticmethod
    def __Mail(rule_field_title, rule):
        return rule_field_title + ' 必须为有效的邮箱'

    @staticmethod
    def __Required(rule_field_title, rule):
        return rule_field_title + ' 不能为空'

    @staticmethod
    def __UUIDv1(rule_field_title, rule):
        return rule_field_title + ' 必须为有效的uuidv1格式'

    @staticmethod
    def __Base32(rule_field_title, rule):
        return rule_field_title + ' 必须为有效的base32格式'

    @staticmethod
    def __Decimal(rule_field_title, rule):
        return rule_field_title + ' 必须为有效的十进制数'

    @staticmethod
    def __IPv4(rule_field_title, rule):
        return rule_field_title + ' 必须为有效的ipv4'

    @staticmethod
    def __Max(rule_field_title, rule):
        regex = re.search("max:(\d+)", rule, re.IGNORECASE)
        return rule_field_title + ' 不能大于 ' + regex.group(1)

    @staticmethod
    def __RequiredIf(rule_field_title, rule):
        return rule_field_title + ' 不能为空'

    @staticmethod
    def __UUIDv3(rule_field_title, rule):
        return rule_field_title + ' 必须为有效的uuidv3格式'

    @staticmethod
    def __Base64(rule_field_title, rule):
        return rule_field_title + ' 必须为有效的base64格式'

    @staticmethod
    def __Dict(rule_field_title, rule):
        return rule_field_title + ' 类型有误'

    @staticmethod
    def __IPv6(rule_field_title, rule):
        return rule_field_title + ' 必须为有效的ipv6'

    @staticmethod
    def __Min(rule_field_title, rule):
        regex = re.search("min:(\d+)", rule, re.IGNORECASE)
        return rule_field_title + ' 不能小于 ' + regex.group(1)

    @staticmethod
    def __Same(rule_field_title, rule):
        return rule_field_title + ' 输入有误'

    @staticmethod
    def __UUIDv4(rule_field_title, rule):
        return rule_field_title + ' 必须为有效的uuidv4格式'

    @staticmethod
    def __Between(rule_field_title, rule):
        regex = re.search("between:(\d+),(\d+)", rule, re.IGNORECASE)
        return rule_field_title + ' 必须在 ' + regex.group(1) + ' 到 ' + regex.group(2) + ' 之间'

    @staticmethod
    def __Hex(rule_field_title, rule):
        return rule_field_title + ' 必须为有效的十六进制数'

    @staticmethod
    def __JSON(rule_field_title, rule):
        return rule_field_title + ' 必须输入有效的json格式'

    @staticmethod
    def __Octal(rule_field_title, rule):
        return rule_field_title + ' 必须为有效的八进制数'

    @staticmethod
    def __Size(rule_field_title, rule):
        regex = re.search("size:(\d+)", rule, re.IGNORECASE)
        return rule_field_title + ' 大小尺寸必须为 ' + regex.group(1)

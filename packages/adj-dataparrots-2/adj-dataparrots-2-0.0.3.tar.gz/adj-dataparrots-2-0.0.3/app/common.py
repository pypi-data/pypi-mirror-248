from flask import jsonify


class Result:
    code: int = None
    msg: str = None
    data = None

    @staticmethod
    def common(code, msg, data=None):
        result = {
            'code': code,
            'msg': msg,
            'data': data
        }
        return jsonify(result)

    @staticmethod
    def success(data=None):
        result = {
            'code': 200,
            'msg': 'success',
            'data': data
        }
        return jsonify(result)

    # 分页列表数据响应
    @staticmethod
    def successWithPage(dataList, totalPages: int, currentPage: int, totalElements: int):
        result = {
            'code': 200,
            'msg': 'success',
            'data': {
                'list': dataList,
                'totalPages': totalPages,
                'currentPage': currentPage,
                'totalElements': totalElements
            }
        }
        return jsonify(result)

    @staticmethod
    def internalError():
        result = {
            'code': 500,
            'msg': 'Internal Server Error!',
            'data': None
        }
        return jsonify(result)

    @staticmethod
    def unauthorized():
        result = {
            'code': 401,
            'msg': 'unauthorized!',
            'data': None
        }
        return jsonify(result)

# 分页查询工具类
def pageUtils(query, page: int, size: int):
    # 计算offset
    offset = size * (int(page) - 1)
    # 查询总数、页数
    totalElements = query.count()
    totalPages = totalElements // size
    if totalElements % size > 0:
        totalPages += 1
    dataList = query.offset(offset).limit(size).all()
    return dataList, totalElements, totalPages

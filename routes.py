from flask import Flask, request, jsonify
from service import create_task, create, show_task, list_task, update_task, update_tasks, find_task, delete_task, \
    delete_tasks

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


def todolist():
    create()

    # 添加一条新的待办事项
    @app.route("/task", methods=['POST'])
    def cre():
        try:
            title = request.form.get('title')
            content = request.form.get('content')
            status = request.form.get('status')
            end_time = request.form.get('end_time')
            code = create_task(title, content, status, end_time)
            if code == 200:
                return jsonify(code=200, msg="success")
            elif code == 404:
                return jsonify(code=404, msg="该活动不存在")
        except Exception as e:
            print(e)
            return jsonify(code=404, msg="该活动不存在")

    # 查看所有事项(可选择状态)
    @app.route("/tasks/<int:page>", methods=['GET'])
    def show_all(page):
        status = request.args.get('status')
        res = list_task(page, status)
        if res['code'] == 200:
            return jsonify(code=200, msg="success", data=res['data'], total=res['total'])
        elif res['code'] == 404:
            return jsonify(code=404, msg="该活动不存在")

    # 输入关键字查询事项
    @app.route("/tasks/find-keyword/<int:page>", methods=['GET'])
    def find_keyword(page):
        keyword = request.args.get('keyword')
        res = find_task(page, keyword)
        if res['code'] == 200:
            return jsonify(code=200, msg="success", data=res['data'], total=res['total'])
        elif res['code'] == 404:
            return jsonify(code=404, msg="该活动不存在")

    # 通过id查询事项
    @app.route("/task/find-id/<int:tid>", methods=['GET'])
    def find_id(tid):
        res = show_task(tid)
        if res['code'] == 200:
            return jsonify(code=200, msg="success", data=res['data'])
        elif res['code'] == 404:
            return jsonify(code=404, msg="该活动不存在")

    # 设置一条待办事项的状态
    @app.route("/task/<int:tid>", methods=['PUT'])
    def update_one(tid):
        status = request.args.get('status')
        code = update_task(tid, status)
        if code == 200:
            return jsonify(code=200, msg="success", )
        elif code == 404:
            return jsonify(code=404, msg="该活动不存在")

    # 设置所有待办事项的状态
    @app.route("/tasks", methods=['PUT'])
    def update_all():
        status = request.args.get('status')
        code = update_tasks(status)
        if code == 200:
            return jsonify(code=200, msg="success", )
        elif code == 404:
            return jsonify(code=404, msg="该活动不存在")

    # 删除一条事项
    @app.route("/task/<int:tid>", methods=['DELETE'])
    def delete_one(tid):
        code = delete_task(tid)
        if code == 200:
            return jsonify(code=200, msg="success", )
        elif code == 404:
            return jsonify(code=404, msg="该活动不存在")

    # 删除 所有已完成/所有待办/所有事项
    @app.route("/tasks", methods=['DELETE'])
    def delete_all():
        status = request.args.get('status')
        code = delete_tasks(status)
        if code == 200:
            return jsonify(code=200, msg="success", )
        elif code == 404:
            return jsonify(code=404, msg="该活动不存在")

    app.run()

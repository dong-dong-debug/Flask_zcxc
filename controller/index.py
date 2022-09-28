from flask import Blueprint, request, render_template, flash, redirect, url_for
from common.decorators import login_required
from linux.linux_commands import Python_Linux
import os
from module.billcarry import Billcarry

index = Blueprint("index", __name__)

plinux = Python_Linux()


@index.route('/', methods=['GET', 'POST'])
@login_required
def idx():
    return render_template('index.html')


# 文件上传解到指定目录
@index.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        file = request.files['zipfile']
        destpath = request.form.get("destpath")
        file_name = file.filename
        print("获取上传文件的名称为:", file_name)
        local_file = os.path.abspath(__file__) + '../../../static/upload/' + file_name
        remoute_file = destpath + file_name
        print(remoute_file)
        file.save(local_file)  # 保存文件
        plinux.upload_file(local_file, remoute_file)
        flash("上传成功")
        return redirect(url_for("index.upload_file"))


# 监控进程
@index.route('/findprocess', methods=['GET', 'POST'])
@login_required
def find_process():
    if request.method == 'GET':
        return render_template("findprocess.html")
    else:
        status = plinux.process_find_python_status()
        if status == 1:
            new_port = plinux.get_process_port()
            old_port, times = plinux.get_file_last_port_time()
            if new_port == old_port:
                message = "normal"
                times = 0
            else:
                plinux.insert_status_and_time_to_txt()
                old_port, times = plinux.get_file_last_port_time()
                message = "un-normal"
        else:
            status = 0
            times = 0
            message = ""
        dict = {"status": status, "times": times, "message": message}
        return dict


# 话单搬运
@login_required
@index.route('/billcarry', methods=['GET', 'POST'])
def bill_carry():
    if request.method == "GET":
        bill_id = Billcarry().find_billcarry_by_status()
        ids = [x[0] for x in bill_id]
        if len(bill_id) == 0:
            return render_template('billcarry.html')
        else:
            result = Billcarry().find_billcarry_by_id(ids[0])
            plinux.active_carry(result[0][0], result[0][1])
            return render_template('billcarry.html', list=result)


@login_required
@index.route('/open', methods=['POST'])
def open_bill_carry():
    source = request.form.get("source")
    dest = request.form.get("dest")
    count = Billcarry().find_bill_islive()
    if count >= 1:
        status = "live"
        dict = {"status": status}
        return dict
    else:
        result = Billcarry().find_bill_by_source_and_dest(source, dest)
        print(result)
        if result is None or result.status == 0:
            Billcarry().insert_billcarry(source, dest)
        else:
            status = "exists"
            dict = {"status": status}
            return dict
        plinux.active_carry(source, dest)
        status = "normal"
        dict = {"status": status, "source": source, "dest": dest}
        return dict


@login_required
@index.route('/close', methods=['POST'])
def close_bill_carry():
    source = request.form.get("source")
    dest = request.form.get("dest")
    result = Billcarry().find_bill_by_source_and_dest(source, dest)
    if result is None:
        return "no-find"
    elif result.status == 0:
        return "no-find"
    else:
        Billcarry().update_billcarry(0, source, dest)
        plinux.close_carry()
        return "normal"

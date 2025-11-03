from flask import Flask, render_template, request, redirect, url_for, flash
import json, requests

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # untuk flash message

global appType
appType = 'Web Service'

# -----------------------------
# 🏠 HALAMAN UTAMA
# -----------------------------
@app.route('/')
def index():
    return render_template('index.html', appType=appType)

# -----------------------------
# 🚗 CREATE
# -----------------------------
@app.route('/createcar')
def createcar():
    return render_template('createcar.html', appType=appType)


@app.route('/createcarsave', methods=['POST'])
def createcarsave():
    try:
        fName = request.form['carName']
        fBrand = request.form['carBrand']
        fModel = request.form['carModel']
        fPrice = request.form['carPrice']

        datacar = {
            "carname": fName,
            "carbrand": fBrand,
            "carmodel": fModel,
            "carprice": fPrice
        }

        alamatserver = "http://localhost:5012/cars/"
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

        kirimdata = requests.post(alamatserver, data=json.dumps(datacar), headers=headers)

        if kirimdata.status_code == 200:
            flash(f"✅ Car '{fName}' successfully added!", "success")
        else:
            flash("⚠️ Failed to add car.", "danger")

    except Exception as e:
        flash(f"❌ Error: {e}", "danger")

    return redirect(url_for('readcar'))

# -----------------------------
# 📋 READ
# -----------------------------
@app.route('/readcar')
def readcar():
    try:
        alamatserver = "http://localhost:5012/cars/"
        datas = requests.get(alamatserver)
        rows = json.loads(datas.text)
    except Exception:
        rows = []
        flash("⚠️ Could not load car data.", "warning")

    return render_template('readcar.html', rows=rows, appType=appType)

# -----------------------------
# ✏️ UPDATE
# -----------------------------
@app.route('/updatecar')
def updatecar():
    return render_template('updatecar.html', appType=appType)


@app.route('/updatecarsave', methods=['POST'])
def updatecarsave():
    try:
        fName = request.form['carName']
        fNewBrand = request.form['carBrand']
        fNewModel = request.form['carModel']
        fNewPrice = request.form['carPrice']

        alamatserver = "http://localhost:5012/cars/"
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

        # Ambil semua data dulu
        allcars = json.loads(requests.get(alamatserver).text)
        found = None

        for car in allcars:
            if car['carname'].lower() == fName.lower():
                found = car
                break

        if found:
            # Hapus yang lama lalu simpan baru (karena API belum punya PUT)
            requests.delete(alamatserver, data=json.dumps({"carname": fName}), headers=headers)
            requests.post(alamatserver, data=json.dumps({
                "carname": fName,
                "carbrand": fNewBrand,
                "carmodel": fNewModel,
                "carprice": fNewPrice
            }), headers=headers)

            flash(f"✅ Car '{fName}' successfully updated!", "success")
        else:
            flash(f"❌ Car '{fName}' not found.", "warning")

    except Exception as e:
        flash(f"❌ Error: {e}", "danger")

    return redirect(url_for('readcar'))

# -----------------------------
# 🗑️ DELETE
# -----------------------------
@app.route('/deletecar')
def deletecar():
    return render_template('deletecar.html', appType=appType)


@app.route('/deletecarsave', methods=['POST'])
def deletecarsave():
    try:
        fName = request.form['carName']
        datacar = {"carname": fName}

        alamatserver = "http://localhost:5012/cars/"
        headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
        kirimdata = requests.delete(alamatserver, data=json.dumps(datacar), headers=headers)

        if kirimdata.status_code == 200:
            flash(f"🗑️ Car '{fName}' deleted successfully!", "success")
        else:
            flash("⚠️ Failed to delete car.", "danger")
    except Exception as e:
        flash(f"❌ Error: {e}", "danger")

    return redirect(url_for('readcar'))

# -----------------------------
# 🔍 SEARCH
# -----------------------------
@app.route('/searchcar')
def searchcar():
    return render_template('searchcar.html', appType=appType, searched=False)

@app.route('/searchcarsave', methods=['POST'])
def searchcarsave():


    try:
        fName = request.form['carName']
        alamatserver = "http://localhost:5012/cars/"

        response = requests.get(alamatserver)
        if response.status_code != 200:
            flash("⚠️ Failed to connect to data server.", "danger")
            return render_template('searchcar.html', appType=appType, searched=False)

        allcars = json.loads(response.text)
        result = None

        for car in allcars:
            if car["carname"].lower() == fName.lower():
                result = car
                break

        if result:
            flash(f"✅ Found car '{fName}'!", "success")
            return render_template('searchcar.html', appType=appType, result=result, searched=True)
        else:
            flash(f"❌ Car '{fName}' not found.", "warning")
            return render_template('searchcar.html', appType=appType, searched=True)

    except Exception as e:
        flash(f"❌ Error: {e}", "danger")
        return render_template('searchcar.html', appType=appType, searched=False)

# -----------------------------
# 🚀 RUN
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5011)

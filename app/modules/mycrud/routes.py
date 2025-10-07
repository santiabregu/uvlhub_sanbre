from flask import render_template
from app.modules.mycrud import mycrud_bp


@mycrud_bp.route('/mycrud', methods=['GET'])
def index():
    return render_template('mycrud/index.html')

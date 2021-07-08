from flask import Blueprint, render_template, request, flash

views = Blueprint('views', __name__)

@views.route('/', methods = ['GET','POST'])
def home():
    #search function
    data = request.form
    print(data)
    
    """
    if name in channels_list:
        image_fetcher(name)
    else:
        flash("Channel is not currently tracked.", category='error')
    """
    return render_template("home.html")


#TODO: figure out how to pass DB context into channel page
"""
@views.route('/<string:name>', methods = ['GET','POST'])
def channel_view():
    show page with graph from grapher api call
"""
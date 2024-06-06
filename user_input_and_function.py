from flask import * #Flask, render_template, send_file, make_response, url_for, Response, redirect, request 
import requests
import json

app = Flask(__name__)

# Getting the data-base of the json files, produced with the "get_data_prdc_dict.py" file

good_neighbours = json.load(open("good_neighbours.json"))
bad_neighbours = json.load(open("bad_neighbours.json"))

# Gathering file from form

@app.route("/", methods=["GET", "POST"])

# 


def finding_neighbours_function():
    
    # getting user input of the html page

    if request.method =="POST":
        
        veg1 = request.form.get("txt_file1", False)
        veg2 = request.form.get("txt_file2", False)
        veg3 = request.form.get("txt_file3", False)

        veg1 = veg1.capitalize()
        veg2 = veg2.capitalize()
        veg3 = veg3.capitalize()
      
        messages = []

    # Check if the vegetables are in the dictionary and fitting together 

        def is_match(x, y):
            if (x in good_neighbours.keys()) and (y in good_neighbours[x]):
                return True
            elif (x in bad_neighbours.keys()) and (y in bad_neighbours[x]):
                msg = (f"{x} and {y} are bad neighbours!")
                messages.append(msg)
                return False
            elif (x not in (good_neighbours.keys() or bad_neighbours.keys()) and 
                y not in (good_neighbours.keys() or bad_neighbours.keys())):
                msg = (f"{x} and {y} are not in the dictionary!")
                messages.append(msg)
                return False
            elif (y not in (good_neighbours.keys() or bad_neighbours.keys())):
                msg = (f"{y} is not in the dictionary!")
                messages.append(msg)
                return False
            elif (x not in (good_neighbours.keys() or bad_neighbours.keys())):
                msg = f"{x} is not in the dictionary!"
                messages.append(msg)
                return False, msg
            else:
                return False, ""

    # Check if all three vegetables are fitting together

        def fitting_together():

            match_veg1_veg2 = is_match(veg1, veg2)
            match_veg1_veg3 = is_match(veg1, veg3)
            match_veg2_veg3 = is_match(veg2, veg3)

            if match_veg1_veg2 and match_veg1_veg3 and match_veg2_veg3: 
                return f"You chose {veg1}, {veg2} and {veg3}: All options are possible for arranging the vegetables :-)"
            
            elif match_veg1_veg2 and match_veg1_veg3 and not match_veg2_veg3:
                return f"You chose {veg1}, {veg2} and {veg3}: The arrangement should be with {veg1} in the middle"
            
            elif match_veg1_veg2 and not match_veg1_veg3 and match_veg2_veg3:
                return f"You chose {veg1}, {veg2} and {veg3}: The arrangement should be with {veg2} in the middle"
            
            elif not match_veg1_veg2 and match_veg1_veg3 and match_veg2_veg3:
                return f"You chose {veg1}, {veg2} and {veg3}: The arrangement should be with {veg3} in the middle"
            
            elif match_veg1_veg2 and not match_veg1_veg3 and not match_veg2_veg3:
                return f"You chose {veg1}, {veg2} and {veg3}: Only {veg1} and {veg2} can be brought together; {veg3} doesn't like the others :-("
            
            elif not match_veg1_veg2 and match_veg1_veg3 and not match_veg2_veg3:
                return f"You chose {veg1}, {veg2} and {veg3}: Only {veg1} and {veg3} can be brought together; {veg2} doesn't like the others :-("
            elif not match_veg1_veg2 and not match_veg1_veg3 and match_veg2_veg3:
                return f"You chose {veg1}, {veg2} and {veg3}: Only {veg2} and {veg3} can be brought together; {veg1} doesn't like the others :-("

            elif not match_veg1_veg2 and not match_veg1_veg3 and not match_veg2_veg3:
                return f"You chose {veg1}, {veg2} and {veg3}: Nothing works - they don't like each other at all. Try something else!"
            
            else: 
                return "Unexpacted case! Try again!"


        result = fitting_together() 

    # Give the result back for rendering at the result page

        return render_template("results_page.html", result=result, messages=messages)
    else:
        return render_template("home.html")


if __name__ == "__main__":
    app.run(debug = True)



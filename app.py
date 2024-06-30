from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
import pandas as pd
import numpy as np

app = Flask(__name__)

model = load_model('./Models/my_model.h5')
df = pd.read_csv("./food_calories.csv")

model.make_predict_function()

def predict_label(img_path):
	i = image.load_img(img_path, target_size=(256,256))
	i = image.img_to_array(i)
	i = i.reshape(1, 256,256,3)
	p = np.argmax(model.predict(i))
	return df[df["Class"]==p]["Name"].values[0], df[df["Class"]==p]["Calories per 100g"].values[0]

# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")


@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/" + img.filename	
		img.save(img_path)

		p, c = predict_label(img_path)

	return render_template("index.html", prediction = p, img_path = img_path, cal=c,)


if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)
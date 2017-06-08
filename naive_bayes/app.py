from flask import jsonify, request, Flask
from sklearn.externals import joblib

print "Loading Pickled Pipeline"
fitted_pipeline = joblib.load('classifier.pkl')

app = Flask(__name__)

@app.route('/', methods=['POST'])
def predict():
  text = request.form.get('text')
  guess = fitted_pipeline.predict([text])[0] #pipeline returns array
  results = {"class": guess}
  return jsonify(results)

if __name__ == '__main__':
  app.run()


from flask import Flask, request, jsonify
import sympy as sp

app = Flask(__name__)

@app.route('/calculator', methods=['POST'])
def calculate():
    try:
        # Get the expression from the incoming request
        expression = request.json.get('expression')
        # Use sympy to evaluate the expression safely
        result = sp.sympify(expression)
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Return error if something goes wrong

if __name__ == "__main__":
    app.run(debug=True)

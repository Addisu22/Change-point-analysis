from flask import Blueprint, jsonify, request
import pandas as pd
from utils.load_data import get_data
from utils.indicators import compute_volatility, event_impacts

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/api/prices', methods=['GET'])
def get_prices():
    df = get_data()
    return jsonify(df.to_dict(orient='records'))

@api_blueprint.route('/api/volatility', methods=['GET'])
def get_volatility():
    df = get_data()
    vol = compute_volatility(df)
    return jsonify(vol.to_dict(orient='records'))

@api_blueprint.route('/api/events', methods=['GET'])
def get_events():
    df = get_data()
    impact_df = event_impacts(df)
    return jsonify(impact_df.to_dict(orient='records'))

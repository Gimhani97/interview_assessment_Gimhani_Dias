import datetime
from flask import Flask, request, jsonify

from db import get_data_to_average_power, insert_reading, create_table

app = Flask(__name__)


# data validation
def is_valid_data(data):
    # validate data format : separated by space
    split_data = data.strip().split()
    return len(split_data) == 3 and split_data[0].isdigit() and split_data[2].replace('.', '', 1).isdigit()


def get_average_power_by_day(from_date, to_date):
    average_power_by_day = []
    data_to_avg_power = get_data_to_average_power(from_date, to_date)

    for data in data_to_avg_power:
        if data[1] == 'Current':
            average_current = data[2]
        elif data[1] == 'Power':
            average_power = data[2]
            average_power_by_day.append({
                'time': data[0],
                'name': 'Power',
                'value': average_power * average_current
            })

    return average_power_by_day


@app.post("/data", method=['POST'])
def post_data():
    data = request.data.decode('utf-8')
    readings = data.strip().split('\n')

    for reading in readings:
        if is_valid_data(reading):
            timestamp, name, value = reading.split()
            insert_reading(int(timestamp), name, float(value))
        else:
            return jsonify({'success': False}), 400
    return jsonify({'success': True})


@app.route('/data', methods=['GET'])
def get_data():
    from_date = request.args.get('from')
    to_date = request.args.get('to')

    if not from_date or not to_date:
        return jsonify({'error': 'Invalid query parameters. Both "from" and "to" are required.'}), 400

    try:
        datetime.datetime.strptime(from_date, '%Y-%m-%d')
        datetime.datetime.strptime(to_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Please use ISO standard date format (YYYY-MM-DD).'}), 400

    average_power_by_day = get_average_power_by_day(from_date, to_date)

    return jsonify(average_power_by_day)


if __name__ == '__main__':
    create_table()
    app.run(debug=True)

from flask import Flask, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)

valid_timeframes = [
    "now 7-d",
    "today 1-m",
    "today 3-m",
    "today 12-m",
    "today 5-y"
]


@app.route('/sva', methods=["GET"])
def interest_over_time():
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        product_name = global_title
        print(f"\nproduct name {product_name}\n")
        kw_list = [product_name]
        geo_global = "IN"
        # geo_regional = "IN-IN"  # Regional level for India
        
        sva_data = {}
        regional_data = {}

        for timeframe in valid_timeframes:
            # Global Interest Over Time
            pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo=geo_global)
            interest_over_time_df = pytrends.interest_over_time().reset_index()
            interest_over_time_df['date'] = interest_over_time_df['date'].astype(str)
            sva_data[timeframe] = interest_over_time_df.rename(columns={product_name: 'score'})[['date', 'score']].to_dict(orient='records')

            # Regional Interest
            pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo=geo_global)
            regional_interest_df = pytrends.interest_by_region(resolution='CITY', inc_low_vol=True)
            regional_data[timeframe] = regional_interest_df.to_dict()

        result = {'sva': sva_data, 'regional': regional_data, 'product_name': global_title}
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)

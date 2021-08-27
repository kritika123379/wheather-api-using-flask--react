from flask import Flask,render_template,request,abort
# import json to load json data to python dictionary
import json
# urllib.request to make a request to api
import urllib.request


app = Flask(__name__)
def tocelcius(temp):
    return str(round(float(temp) - 273.16,2))

@app.route('/',methods=['POST','GET'])
def weather():
    api_key = '48a90ac42caa09f90dcaeee4096b9e53'
    if request.method == 'POST':
        city = request.form['city']
    else:
        #for default name mathura
        city = 'mathura'

    # source contain json data from api
    try:
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid='+api_key).read()
    except:
        return abort(404)
    # converting json data to dictionary

    list_of_data = json.loads(source)

    # data for variable list_of_data
    data = {
        "country_code": str(list_of_data['sys']['country']),
        "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
        "temp": str(list_of_data['main']['temp']) + 'k',
        "temp_cel": tocelcius(list_of_data['main']['temp']) + 'C',
        "pressure": str(list_of_data['main']['pressure']),
        "humidity": str(list_of_data['main']['humidity']),
        "cityname":str(city),
    }
    return render_template('index.html',data=data)


    @app.route('/city')
    def search_city():
        API_KEY = '48a90ac42caa09f90dcaeee4096b9e53'  # initialize your key here
        city = request.args.get('q')  # city name passed as argument
        
        # call API and convert response into Python dictionary
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
        response = requests.get(url).json()
        
        # error like unknown city name, inavalid api key
        if response.get('cod') != 200:
            message = response.get('message', '')
            return f'Error getting temperature for {city.title()}. Error message = {message}'
        
        # get current temperature and convert it into Celsius
        current_temperature = response.get('main', {}).get('temp')
        if current_temperature:
            current_temperature_celsius = round(current_temperature - 273.15, 2)
            return f'Current temperature of {city.title()} is {current_temperature_celsius} &#8451;'
        else:
            return f'Error getting temperature for {city.title()}'



if __name__ == '__main__':
    app.run(debug=True)

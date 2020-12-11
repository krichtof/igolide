require 'sinatra'

get '/' do
  "Welcome to Notif Light"
end

post '/events' do
  `python3 ble_guirlande_client.py`
end

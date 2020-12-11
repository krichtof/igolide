require 'sinatra'

get '/' do
  "Notif Light crée une animation visuelle quand un événement survient"
end

post '/events' do
  `python3 ble_guirlande_client.py`
end

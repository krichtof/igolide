require 'sinatra'

get '/' do
  "Welcome to Notif Light"
end

post '/events' do
  puts "params: #{params}"
end

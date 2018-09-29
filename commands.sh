# api calls

curl -X POST -H "Content-Type: application/json" -d  '{"name": "Channel1"}' http://0.0.0.0:5000/add_channel

curl -X POST -H "Content-Type: application/json" -d  '{"name": "Channel2"}' http://0.0.0.0:5000/add_channel

curl -X POST -H "Content-Type: application/json" -d  '{"name": "Perfomer1"}' http://0.0.0.0:5000/add_performer

curl -X POST -H "Content-Type: application/json" -d  '{"performer": "Perfomer2","title":"Music 4"}' http://0.0.0.0:5000/add_song

curl -X POST -H "Content-Type: application/json" -d  '{"performer": "Perfomer1","title": "Music 2", "channel": "Channel3", "start": "2013-01-01T00:00:00", "end": "2013-01-01T10:00:00"}' http://0.0.0.0:5000/add_play

curl -X POST -H "Content-Type: application/json" -d  '{"performer": "Perfomer2","title": "Music 3", "channel": "Channel4", "start": "2013-01-02T00:00:00", "end": "2013-01-02T10:00:00"}' http://0.0.0.0:5000/add_play

curl -X POST -H "Content-Type: application/json" -d  '{"performer": "Perfomer5","title": "Music 4", "channel": "Channel4", "start": "2013-01-03T00:00:00", "end": "2013-01-03T10:00:00"}' http://0.0.0.0:5000/add_play

curl -X POST -H "Content-Type: application/json" -d  '{"performer": "Perfomer3","title": "Music 5", "channel": "Channel5", "start": "2013-01-03T00:00:00", "end": "2013-01-03T08:00:00"}' http://0.0.0.0:5000/add_play

curl -X POST -H "Content-Type: application/json" -d  '{"performer": "Perfomer4","title": "Music 6", "channel": "Channel1", "start": "2013-01-04T12:00:00", "end": "2013-01-04T14:00:00"}' http://0.0.0.0:5000/add_play

curl -X POST -H "Content-Type: application/json" -d  '{"performer": "Perfomer3","title": "Music 5", "channel": "Channel5", "start": "2013-01-04T10:00:00", "end": "2013-01-04T12:00:00"}' http://0.0.0.0:5000/add_play

curl -X POST -H "Content-Type: application/json" -d  '{"performer": "Perfomer3","title": "Music 5", "channel": "Channel5", "start": "2013-01-08T10:00:00", "end": "2013-01-08T12:00:00"}' http://0.0.0.0:5000/add_play

curl -X POST -H "Content-Type: application/json" -d  '{"performer": "Perfomer3","title": "Music 5", "channel": "Channel5", "start": "2013-01-09T10:00:00", "end": "2013-01-09T12:00:00"}' http://0.0.0.0:5000/add_play

curl -X POST -H "Content-Type: application/json" -d  '{"performer": "Perfomer3","title": "Music 5", "channel": "Channel5", "start": "2013-01-10T10:00:00", "end": "2013-01-10T12:00:00"}' http://0.0.0.0:5000/add_play

curl -X POST -H "Content-Type: application/json" -d  '{"performer": "Perfomer3","title": "Music 4", "channel": "Channel2", "start": "2013-01-08T09:00:00", "end": "2013-01-08T09:30:00"}' http://0.0.0.0:5000/add_play

curl -X POST -H "Content-Type: application/json" -d  '{"performer": "Perfomer3","title": "Music 3", "channel": "Channel2", "start": "2013-01-09T08:00:00", "end": "2013-01-09T08:30:00"}' http://0.0.0.0:5000/add_play

curl -X POST -H "Content-Type: application/json" -d  '{"performer": "Perfomer3","title": "Music 2", "channel": "Channel2", "start": "2013-01-10T13:30:00", "end": "2013-01-10T14:00:00"}' http://0.0.0.0:5000/add_play

curl -X POST -H "Content-Type: application/json" -d  '{"channel": "Channel2","start": "2012-01-01T00:00:00","end": "2014-01-01T10:00:00"}' http://0.0.0.0:5000/get_channel_plays

curl -X POST -H "Content-Type: application/json" -d '{"performer": "Perfomer1","title": "Music 2", "start": "2012-01-01T00:00:00","end": "2014-01-01T10:00:00"}' http://0.0.0.0:5000/get_song_plays

curl -X POST -H "Content-Type: application/json" -d '{"channels":["Channel1","Channel2"],"start": "2013-01-01T00:00:00","limit": 10} http://0.0.0.0:5000/get_top


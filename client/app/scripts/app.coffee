define (require) ->
	my_user_status = 'aehmm'

	ws = new WebSocket("ws://localhost:8888/")
	ws.onopen = ->
		ws.onmessage = (msg) ->
			#console.log msg.data
			data = msg.data

			if data is "Click"
				$(document).trigger('click_gesture', 'clicked')

			else if data is "personal"
				$(document).trigger('phase', 'personal')

			else if data is "subtle"
				$(document).trigger('phase', 'subtle')

			else if data is "implicit"
				$(document).trigger('phase', 'implicit')

			else if data is "ambient"
				$(document).trigger('phase', 'ambient')

			else if data is "user_detected"
				$(document).trigger('user_tracking', 'user_detected')

			else if data is "user_lost"
				$(document).trigger('user_tracking', 'user_lost')
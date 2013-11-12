define (require) ->
	Ractive = require('ractive');

	ractive = new Ractive(
		el: 'user_status'
		template: '#user_status_template'
		data:
			user_status: "user_lost"
	)

	$(document).on "user_tracking", (e, eventInfo) ->
		#console.log eventInfo
		ractive.set('user_status', eventInfo)


	### other events ###

	$(document).on "phase", (e, eventInfo) ->
		console.log eventInfo
		#$('#notify').html(eventInfo)

	$(document).on "click_gesture", (e, eventInfo) ->
		console.log eventInfo
		#$('#gesture').html(eventInfo)
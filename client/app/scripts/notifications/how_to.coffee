define (require) ->
	Ractive = require('ractive');

	ractive = new Ractive(
		el: 'how_to_wrapper'
		template: '#how_to_template'
		data:
			text: "hide"
			how_to: "move?"

	)	

	@phase = ''

	#wurde der hinweis schon mal angezeigt?
	@ambient = false
	@implicit = false
	@subtle = false
	@personal = false

	

	
	#activate how-to dialog every X sec
	activate = ->
		@timing = setTimeout (=>

			if @phase is 'ambient' and not @ambient
				how_to = 'Gehe näher heran um mehr zu erfahren'
				@ambient = true
				ractive.set('how_to', how_to)
				ractive.set('text', 'active')
			else if @phase is 'implicit' and not @implicit
				how_to = 'Gehe näher heran um mehr zu erfahren'
				@implicit = true
				ractive.set('how_to', how_to)
				ractive.set('text', 'active')
			else if @phase is 'subtle' and not @subtle
				how_to = 'Versuche es doch mal mit einer Push-Geste'
				@subtle = true
				ractive.set('how_to', how_to)
				ractive.set('text', 'active')
			else if @phase is 'personal' and not @personal
				how_to = 'Touch this'
				@personal = true
				ractive.set('how_to', how_to)
				ractive.set('text', 'active')
			
			deactivate()

		), 4000 #interval

	deactivate = ->
		setTimeout (->
				ractive.set('text', 'hide')
		), 4000 #display time
	

	$(document).on "phase", (e, eventInfo) =>
		if eventInfo isnt @phase
			activate()

		@phase = eventInfo


	

	


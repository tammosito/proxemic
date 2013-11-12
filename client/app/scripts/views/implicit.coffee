define (require) ->
	Ractive = require('ractive');


	@phrases = [
		'Get together and create games in one weekend in over 300 locations worldwide.',
		'Think of it as a hackathon focused on game development.',
		'be creative, share experiences and express yourself',
		'make a new game in the time span of 48 hours',
		'People are invited to explore new technologies and tools'
	]

	ractive = new Ractive(
		el: 'animate'
		template: '#animate_template'
		data:
			text: @phrases[0]
			class: 'active'
	)

	counter = 0
	activate = ->
		setInterval (=>
			counter++
			if counter >= @phrases.length
				counter = 0
			ractive.set('class', '')

			setTimeout (->
				ractive.set('text', @phrases[counter])
				ractive.set('class', 'active')
			), 1000

		), 6000 #interval

	activate()


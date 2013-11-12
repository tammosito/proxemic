define (require) ->
	Ractive = require('ractive');


	@images = [
		'<img src="../images/event/2.jpg">',
		'<img src="../images/event/3.jpg">',
		'<img src="../images/event/4.jpg">',
		'<img src="../images/event/5.jpg">',
		'<img src="../images/event/6.jpg">',
		'<img src="../images/event/1.jpg">',
	]

	ractive = new Ractive(
		el: 'images'
		template: '#images_template'
		data:
			image: @images[0]
			animation_class: ''
	)

	counter = 0

	activate = ->
		ractive.set('animation_class', 'fadeout')

		setTimeout (->
			counter++
			if counter >= @images.length
				counter = 0
		
			ractive.set('image', @images[counter])

			ractive.set('animation_class', '')
		), 1000

	
	setInterval (->
		activate()
	), 15000

	$(document).on "click_gesture", (e, eventInfo) ->
		console.log eventInfo
		activate()


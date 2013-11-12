define (require) ->
	setTimeout (->
		#offset to body
		scroller = $('.scroller').offset()

		#height of page
		page_height = $('body').height()
		diff = (3*page_height) - page_height

		console.log page_height
		console.log scroller.top
		

		offset = ((page_height - scroller.top) + diff) * -1

		scroller_height = page_height - offset

		console.log scroller_height	

		$('.scroller').height(scroller_height)
	), 1000 #display time
		


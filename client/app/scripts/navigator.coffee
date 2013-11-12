define (require) ->
	class Navigator

		onepage_scroll = require('onepage_scroll')

		pages: null
		current_page: null

		constructor: ->
			$(".main").onepage_scroll
				sectionContainer: "section"
				easing: "ease"
				animationTime: 500
				pagination: true
				updateURL: false

			@current_page = 1
			pages = $('.main > section').length

			$(document).on "phase", (e, eventInfo) =>
				console.log eventInfo

				if eventInfo is 'ambient'
					page = 1
				else if eventInfo is 'implicit'
					page = 2

				else if eventInfo is 'subtle'
					page = 3

				else if eventInfo is 'personal'
					page = 4

				else
					page = 1

				@scroll_to_page(page)


		get_current_page: ->
			console.log @current_page

		scroll_to_page: (target_page) ->
			while @current_page isnt parseInt(target_page)
				if target_page > @current_page
					$(".main").moveDown()
					@current_page++
				else 
					$(".main").moveUp()
					@current_page--
			



	navi = new Navigator
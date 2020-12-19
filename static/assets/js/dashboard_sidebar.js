$(document).ready(function () {
	//listens to the click event of the question tabs then close and open the tabs 
	$(document).on("click", ".sidebar__section__header h5", function(){
		$(".sidebar__section__header").toggleClass("sidebar__section__header--notactive");
		$(".sidebar__section__header  i").toggleClass("notactive");
	});
	$(document).on("click", ".sidebar__section__content__sub h5", function(){
		$(this).parent().toggleClass("sidebar__section__content__sub--notactive");
		$(this).children().toggleClass("notactive");
	});
	$(document).on("click", "#dashboard .content header .menu i", function(){
		$("#dashboard .sidebar").toggleClass("sidebar--mobile");
	});
});
$(document).ready(function () {
	//listens to the click event of the question tabs then close and open the tabs 
	$(document).on("click", ".block__question", function(){
		
		if($(this).hasClass("block__question--active")){
			$(".block__question--active .block__question__header .block__question__header__btn").toggleClass("block__question__header__btn--active");
			$(this).toggleClass("block__question--active");
		}else{
			$(".block__question--active .block__question__header .block__question__header__btn").toggleClass("block__question__header__btn--active");
			$(".block__question--active").toggleClass("block__question--active");
			$(this).toggleClass("block__question--active");
			$(".block__question--active .block__question__header .block__question__header__btn").toggleClass("block__question__header__btn--active");
		}
		
	});
});
let allTabs = ['#get-started', '#reference', '#endpoint', '#tutorial', '#hire_consultant']

let buttons = document.querySelectorAll('.tab__menu__link');


buttons.forEach((btn, index) => {

  btn.addEventListener('click', (e) => {


    for (let i = 0; i < allTabs.length; i++) {
      buttons[i].classList.remove('active')
    }
    buttons[index].classList.add('active')
  

    // add invisible class to all tabs
    for (let i = 0; i < allTabs.length; i++) {
    
      document.querySelector(allTabs[i]).classList.add('invisible');
      
    }

    // remove invisible class from the tab that was clicked
    document.querySelector(allTabs[index]).classList.remove('invisible');

  })

});
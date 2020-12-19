/*jshint esversion: 6 */

// nav menu open

document.querySelector('.hamburger').addEventListener('click', () => {
  document.querySelector('.mobile__menu').classList.toggle('mobile__menu--open')
})

//nav menu close 

document.querySelector('.mobile__menu').addEventListener('click', (e) => {
  let nav = document.querySelector('.mobile__menu nav');
  let greyArea = document.querySelector('.mobile__menu');

  if (e.target == greyArea) {
    nav.classList.add('nav--close');
    document.querySelector('.mobile__menu').classList.add('mobile__menu--close');

    setTimeout(() => {
      nav.classList.remove('nav--close')
      document.querySelector('.mobile__menu').classList.toggle('mobile__menu--open');
      document.querySelector('.mobile__menu').classList.remove('mobile__menu--close');
    }, 1000);
  }
});

// Style links based on the page URL

links = document.querySelectorAll('a.nav_link');

links.forEach(link => {

  if (link.href == window.location.href) {

    link.classList.add('active_link');
  }
});

// Style Sign In/ Sign Up Buttons based on page URL
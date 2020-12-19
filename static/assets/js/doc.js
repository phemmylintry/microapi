/*jshint esversion: 6 */

var x = document.querySelectorAll(".tab__content");
var tabs = document.querySelectorAll(".tab");

const currentTab = n => {
    showTab(slideIndex = n);
};

const showTab = n => {
    var i;
    var x = document.querySelectorAll(".tab__content");
    var tabs = document.querySelectorAll(".tab");

    console.log(tabs);

    if (n > x.length) {
        slideIndex = 1;
    }
    if (n < 1) {
        slideIndex = x.length;
    }
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    for (i = 0; i < tabs.length; i++) {
        tabs[i].className = tabs[i].className.replace("active", "");
    }
    x[slideIndex - 1].style.display = "block";
    tabs[slideIndex - 1].className += " active ";
};



// Copy Text

const copyText = caller => {
    parent = caller.parentElement;

    textarea = parent.previousElementSibling;

    textarea.select();

    textarea.setSelectionRange(0, 99999);

    document.execCommand("copy");

};


// Display platform API request based on Language



platform = document.querySelectorAll(".req-platform");
platform.forEach(item => {

    item.onchange = () => {
        codeEl = item.nextElementSibling;
        console.log(codeEl.innerText);
        if (item.value == "node") {
            console.log(item.value);
            codeEl.innerText = "node request goes here";

        }

        if (item.value == "php") {
            console.log(item.value);

            codeEl.innerText = "php request goes here";
        }

        if (item.value == "python") {
            console.log(item.value);
            codeEl.innerText = "python request goes here";
        }
    };
});
// console.log(platform);

// output = document.querySelector(".req__code code");


// platform.onchange = () => {


//     if (platform.value == "node") {
//         output.innerHTML = "node request goes here";

//     }

//     if (platform.value == "php") {
//         output.innerHTML = "php request goes here";
//     }

//     if (platform.value == "python") {
//         output.innerHTML = "python request goes here";
//     }
// };


//Togle between api responses

const showOk = caller => {

    console.log(caller);

    caller.classList.toggle('active_tab');
    caller.nextElementSibling.classList.toggle('active_tab');

    parent = caller.parentNode;
    parentSibling = parent.nextElementSibling;
    target = parentSibling.children;
    ok = target[0];
    bad = target[1];


    if (ok.style.display == "none") {
        ok.style.display = "block";
        bad.style.display = "none";
    }

};



const showBad = (caller) => {

    caller.classList.toggle('active_tab');
    caller.previousElementSibling.classList.toggle('active_tab');


    parent = caller.parentNode;
    parentSibling = parent.nextElementSibling;
    target = parentSibling.children;
    ok = target[0];
    bad = target[1];

    if (bad.style.display == "none") {
        bad.style.display = "block";
        ok.style.display = "none";
    }

};






// Toggle API Reference Nested Nav

more = document.querySelector('.more');

more.addEventListener('click', () => {
    parent = more.parentNode;
    console.log(parent);

    content = parent.nextElementSibling;
    if (content.style.display == "none") {
        content.style.display = "block";
    } else {
        content.style.display = "none";
    }
    console.log(content);

})
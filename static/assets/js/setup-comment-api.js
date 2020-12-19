



function showMoreLinks(e,id,no){

    // console.log(id);

    e.stopImmediatePropagation();
    e.stopPropagation();
    
    let more = document.getElementById(id);
    more.className == 'hide'? more.classList.remove('hide') : more.classList.add('hide');

    // let dontSHow = document.getElementById(no);
    // dontSHow.classList.add('hide')

    // $('#' + id).show();
    // $('#' + no).hide();
    // console.log(more.className);
    
}




$('body')

.on('click', (e)=>{
    e.stopImmediatePropagation()
    e.stopPropagation();
    // let more = document.getElementById('more__links_div');
    let moreB = document.getElementById('other__links_div');
    // more.classList.add('hide')
    moreB.classList.add('hide')

    
})

// .on('click', '#more__links_div', (e)=>{
//      e.stopImmediatePropagation()
//      e.stopPropagation();
// })

.on('click', '#other__links_div', (e) => {
    e.stopImmediatePropagation()
    e.stopPropagation();
})


//get search form and page
let searchform = document.getElementById('searchForm')
let pagelinks= document.getElementsByClassName('page-link')

//ensuree search form exist

if(searchform){
    for(let i = 0; pagelinks.length >i; i++){
        pagelinks[i].addEventListener('click',function(e){
            e.preventDefault()

            
            //get the data attribut.
            let page = this.dataset.page
            

            //add hiden searchinput to form
            searchform.innerHTML +=`<input value=${page} name="page" hidden/>`
            
            //submit form
            searchform.submit()
            console.log(page)
        })
        
    }
}
// To fix issue where if go to different page after searching, the search will be overwritten by page query.
// This will end up sending 2 values to the backend to search values without overwritting.

// Get search form and page links.
let searchForm = document.getElementById('searchForm')
let pageLinks = document.getElementsByClassName('page-link')

// Ensure search form exists. If no search form, does not need to run.
if(searchForm){
    // Loops through page links. 
    for (let i = 0; pageLinks.length > i; i++) {
        // Everytime button is clicked for pageLinks, listen for click. 
        pageLinks[i].addEventListener('click', function (e) {
            // Default action of going to page being prevented. 
            e.preventDefault()
            
            // Get data attribute in above elements. "this" being the button clicked on.
            // 1. Get current page we clicked on. 
            let page = this.dataset.page
            
            // Add hidden search input to form. innerHTML allows to add html content. 
            // 2. Add in the page value. 
            searchForm.innerHTML += `<input value=${page} name="page" hidden/>`
            
            // 3. Then submit form.
            searchForm.submit()
        })
    }
}

let tags = document.getElementsByClassName('project-tag')

for (let i = 0; tags.length > i; i++) {
    tags[i].addEventListener('click', (e) => {
        let tagId = e.target.dataset.tag
        let projectId = e.target.dataset.project

        // console.log('TAG ID:', tagId)
        // console.log('PROJECT ID:', projectId)

        fetch('http://127.0.0.1:8000/api/remove-tag/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'project': projectId, 'tag': tagId })
        })
            .then(response => response.json())
            .then(data => {
                e.target.remove()
            })

    })
}

for (let i = 0; i < tags.length; i++){
    tags[i].addEventListener('click', (e)=>{
        let tagId = e.target.dataset.tag
        let projectId = e.target.dataset.project

        fetch('http://127.0.0.1:8000/api/remove-tag/', {
            method:'DELETE',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify({'project':projectId, 'tag':tagId})
        })
        .then(response => response.json())
        .then(data => {
            e.target.remove()
        })

    })
}

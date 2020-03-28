///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////       uSer book search results table display
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

d3.select('#bookList').html('');

//create bookresults table--- display results when user is searching for the books

var url = "/api/findbook";
d3.json(url, function(response) {
    console.log(response);
    const bookList= book=> `<div class='row'>
                            <div class="card col-mb-3" style="max-width: 25rem;">
                            <div class="row no-gutters">
                                <div class="col-md-3">
                                <img src="${book.image_url}" class="card-img" alt="${book.title}">
                                </div>
                                <div class="col-md-8">
                                <div class="card-body">
                                    <h3 class="card-title">${book.title}</h3>
                                    <h4 class="card-title">${book.author}</h4>
                                    <h5 class="card-title">${book.average_rating}</h5>
                                    <h5 class="card-title">${book.id}</h5
                                    <p></p>
                                    <hr class="my-4">           
                                    <a href="/" id='btn' class="card-link btn btn-primary">Find Book</a>
                                    <a href="/getuserinputs" id='share_btn' class="card-link btn btn-primary">Share Book</a>
                                </div>
                                </div>
                        </div>
                        </div>
                        </div>`


    document.querySelector("#bookList")
    .innerHTML = response.map(book => bookList(book)).join('');

    var find= d3.select("#btn");
    
});








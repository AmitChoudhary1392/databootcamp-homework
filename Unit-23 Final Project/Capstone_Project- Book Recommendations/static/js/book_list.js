d3.select("#bookList").html('');

var url_list="/api/bookList";
d3.json(url_list, function(response){

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
                                        
                                        <p></p>
                                        <hr class="my-4">           
                                        <a href="/" class="btn btn-primary">Find Book</a>
                                        <a href="/getuserinputs" class="btn btn-primary">Share Book</a>
                                    </div>
                                    </div>
                            </div>
                            </div>
                            </div>`


    document.querySelector("#bookList")
    .innerHTML = response.map(book => bookList(book)).join('');
});
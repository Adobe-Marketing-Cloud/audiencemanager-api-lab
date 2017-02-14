$(document).ready(function(e){
    $('.search-bar .dropdown-menu').find('a').click(function(e) {
        e.preventDefault();
        var param = $(this).attr("href").replace("#","");
        var concept = $(this).text();
        $('.search-bar #search_category_label').text(concept);
        $('.search-bar #search_category').val(param);
        console.log(param);
        console.log(concept);
    });
});

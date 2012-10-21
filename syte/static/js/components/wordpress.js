
function fetchWordpressPosts(offset, tag){
  var blog_fetch_url = '/wordpress.json/?o=' + offset;

  // TODO tag
  $.getJSON(blog_fetch_url, function(response){
    require(["text!templates/wordpress-post.html"],
      function(text_post_template){
        var text_template = Handlebars.compile(text_post_template);
        $('.loading').remove();
        $.each(response.posts, function(i, p){
            p.formated_date = moment(p.date).format('MMMM DD, YYYY');
            console.log(p);
            $("#blog-posts").append(text_template(p));
        });

        setupLinks();
        adjustBlogHeaders();
        prettyPrint();
        setTimeout(setupBlogHeaderScroll, 1000);
        adjustSelection('home');

        $('body').trigger("blog-post-loaded");
      }
    )
  });


}

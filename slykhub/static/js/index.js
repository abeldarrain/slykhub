$.fn.isInViewport = function() {
    var elementTop = $(this).offset().top;
    var elementBottom = elementTop + $(this).outerHeight();

    var viewportTop = $(window).scrollTop();
    var viewportBottom = viewportTop + $(window).height();

    return elementBottom > viewportTop && elementTop < viewportBottom;
};

$(window).on('scroll', function() {
    $('.col-md-3').each(function() {
      if ($(this).isInViewport()) {
        $(this).addClass('animated');
      }
    //   else{
    //     $(this).removeClass('animated');
    //   }
    });
    $('.col-md-6').each(function() {
        if ($(this).isInViewport()) {
          $(this).addClass('animated');
        }
        // else{
        //   $(this).removeClass('animated');
        // }
      });
  });
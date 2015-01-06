/* jQuery Ajax Mail Send Script */

(function ($) {
    $(function() {

        var contactForm = $( '#contact-form' );

        var $alert = $('.site-alert');

        contactForm.submit(function()
        {
            if (contactForm.valid())
            {

                $.ajax({
                    url: '/contact/',
                    data: $('#contact-form').serialize(),
                    type: 'post',
                    cache: false,
                    beforeSend: function(){
                        NProgress.start();
                        var formValues = $(this).serialize();
                    },
                    complete: function() {
                    },
                    success: function(data) {
                      if(data == 'success') {
                        NProgress.done();
                        $alert.removeClass('slideOutRight').show().addClass('slideInLeft');
                        setTimeout(function() { $alert.removeClass('slideInLeft').addClass('slideOutRight'); },4000)
                        contactForm.clearForm();
                    }
                }
            });
            }
            return false
        });

    });
$.fn.clearForm = function() {
      return this.each(function() {
            var type = this.type, tag = this.tagName.toLowerCase();
            if (tag == 'form')
                  return $(':input',this).clearForm();
            if (type == 'text' || type == 'email' || tag == 'textarea')
                  this.value = '';
            else if (type == 'checkbox' || type == 'radio')
                  this.checked = false;
            else if (tag == 'select')
                  this.selectedIndex = -1;
      });
};

})(jQuery);
(function ($) {
    $.fn.roll = function(delegated, options) {
        var onsuccess = function($object, $delegated, json) {
            if ($delegated.hasClass('action-enroll')) {
                $delegated.text('Desencribirse');
                $delegated.removeClass('action-enroll');
                $delegated.addClass('action-unroll');
                new_href = $delegated.attr('href').replace('/inscribirse', '/desinscribirse')
                $delegated.attr('href', new_href)
            } else if ($delegated.hasClass('action-unroll')) {
                $delegated.text('Inscribirse');
                $delegated.removeClass('action-unroll');
                $delegated.addClass('action-enroll')
                new_href = $delegated.attr('href').replace('/desinscribirse', '/inscribirse')
                $delegated.attr('href', new_href)
            }
        }
        this.action(delegated, { onsuccess: onsuccess, check_confirm: true })
    }
})(jQuery);

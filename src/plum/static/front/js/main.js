$(function () {
    $('[data-toggle="tooltip"]').tooltip();
    $("[data-formset]").formset(
        {
            animateForms: true,
            reorderMode: 'animate'
        }
    );
    $(document).on('click', '[data-toggle="lightbox"]', function (event) {
        event.preventDefault();
        $(this).ekkoLightbox();
    });
});